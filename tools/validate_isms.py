#!/usr/bin/env python3
"""Validate the ISMS repository for structural consistency.

Checks:
  * Document front matter (required fields, ID/filename match, unique IDs,
    valid Annex A references, overdue reviews).
  * Statement of Applicability covers exactly the reference Annex A catalogue,
    with valid values and resolvable references.
  * Risk register scoring (score = likelihood x impact), valid controls,
    assets and treatment options.
  * Unfilled {{PLACEHOLDERS}} (reported as warnings).

Errors always fail. Warnings fail only with --strict (use once the ISMS is
filled in and ready for audit).

Usage: python tools/validate_isms.py [--strict] [--quiet]
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTERS = ROOT / "registers"
DOC_DIRS = [ROOT / "docs", ROOT / "policies"]
REFERENCE_CATALOGUE = REGISTERS / "reference-annex-a-2022.csv"

REQUIRED_FRONT_MATTER = [
    "id", "title", "version", "status", "owner", "approver",
    "classification", "iso_clauses", "annex_a", "last_reviewed", "next_review",
]
DOC_STATUSES = {"Draft", "Approved", "Retired"}
CLASSIFICATIONS = {"Public", "Internal", "Confidential", "Restricted"}
SOA_APPLICABLE = {"Yes", "No", "TBD"}
SOA_STATUSES = {"Not assessed", "Not implemented", "Partially implemented", "Implemented", "Not applicable"}
TREATMENT_OPTIONS = {"Modify", "Avoid", "Share", "Retain"}
ACCEPTANCE_STATUSES = {"Pending", "Accepted", "Rejected"}
PLACEHOLDER = re.compile(r"\{\{[A-Za-z0-9_ .]+\}\}")


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def read_csv(path, report):
    if not path.exists():
        report.error(rel(path), "file missing")
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_front_matter(text):
    """Parse the simple YAML subset used in front matter (scalars and inline lists)."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    data = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        value = value.strip()
        if value.startswith("["):
            try:
                data[key.strip()] = json.loads(value)
            except json.JSONDecodeError:
                data[key.strip()] = value
        else:
            data[key.strip()] = value.strip('"').strip("'")
    return data


def parse_date(value):
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def split_list(value):
    return [v.strip() for v in value.split(";") if v.strip()]


def check_documents(report, control_ids):
    doc_ids = {}
    for base in DOC_DIRS:
        for path in sorted(base.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            where = rel(path)
            fm = parse_front_matter(text)
            if fm is None:
                report.error(where, "missing or malformed front matter")
                continue
            for key in REQUIRED_FRONT_MATTER:
                if key not in fm:
                    report.error(where, f"front matter missing '{key}'")
            doc_id = fm.get("id", "")
            if doc_id:
                if not path.name.startswith(doc_id + "-"):
                    report.error(where, f"filename does not start with id '{doc_id}'")
                if doc_id in doc_ids:
                    report.error(where, f"duplicate id '{doc_id}' (also in {doc_ids[doc_id]})")
                doc_ids[doc_id] = where
            if fm.get("status") and fm["status"] not in DOC_STATUSES:
                report.error(where, f"invalid status '{fm['status']}'")
            if fm.get("classification") and fm["classification"] not in CLASSIFICATIONS:
                report.error(where, f"invalid classification '{fm['classification']}'")
            for control in fm.get("annex_a") or []:
                if control not in control_ids:
                    report.error(where, f"unknown Annex A control '{control}'")
            if fm.get("status") == "Approved" and not fm.get("last_reviewed"):
                report.error(where, "approved document has no last_reviewed date")
            next_review = parse_date(fm.get("next_review", ""))
            if next_review and next_review < dt.date.today():
                report.warn(where, f"review overdue (next_review {next_review})")
            if fm.get("status") == "Draft":
                report.warn(where, "status is Draft")
            placeholders = set(PLACEHOLDER.findall(text))
            if placeholders:
                report.warn(where, f"{len(placeholders)} unfilled placeholder(s), e.g. {sorted(placeholders)[0]}")
    return doc_ids


def check_soa(report, catalogue, doc_ids, risk_ids):
    path = REGISTERS / "statement-of-applicability.csv"
    rows = read_csv(path, report)
    where = rel(path)
    seen = set()
    for i, row in enumerate(rows, start=2):
        cid = row.get("control_id", "")
        loc = f"{where}:{i} ({cid})"
        if cid in seen:
            report.error(loc, "duplicate control")
        seen.add(cid)
        if cid not in catalogue:
            report.error(loc, "control not in reference catalogue")
            continue
        if row.get("control_name") != catalogue[cid]:
            report.error(loc, f"control name differs from catalogue ('{catalogue[cid]}')")
        applicable = row.get("applicable", "")
        status = row.get("implementation_status", "")
        if applicable not in SOA_APPLICABLE:
            report.error(loc, f"applicable must be one of {sorted(SOA_APPLICABLE)}")
        elif applicable == "TBD":
            report.warn(loc, "applicability not yet decided")
        elif not row.get("justification"):
            report.warn(loc, "justification for inclusion/exclusion is required")
        if status not in SOA_STATUSES:
            report.error(loc, f"implementation_status must be one of {sorted(SOA_STATUSES)}")
        if applicable == "No" and status not in ("Not applicable", "Not assessed"):
            report.error(loc, "excluded control must have status 'Not applicable'")
        if applicable == "Yes" and status == "Not applicable":
            report.error(loc, "applicable control cannot have status 'Not applicable'")
        if applicable == "Yes" and not row.get("owner"):
            report.warn(loc, "applicable control has no owner")
        for ref in split_list(row.get("implementation_reference", "")):
            if ref.startswith("ISMS-"):
                if ref not in doc_ids:
                    report.error(loc, f"implementation_reference '{ref}' is not a known document id")
            elif "/" in ref and not (ROOT / ref).exists():
                report.error(loc, f"implementation_reference '{ref}' does not exist")
        for rid in split_list(row.get("risk_ids", "")):
            if rid not in risk_ids:
                report.error(loc, f"risk '{rid}' not in risk register")
    missing = sorted(set(catalogue) - seen, key=control_sort_key)
    if missing:
        report.error(where, f"missing controls: {', '.join(missing)}")


def check_risks(report, control_ids, asset_ids):
    path = REGISTERS / "risk-register.csv"
    rows = read_csv(path, report)
    where = rel(path)
    ids = set()
    for i, row in enumerate(rows, start=2):
        rid = row.get("risk_id", "")
        loc = f"{where}:{i} ({rid})"
        if rid in ids:
            report.error(loc, "duplicate risk_id")
        ids.add(rid)
        if not row.get("risk_owner"):
            report.error(loc, "risk_owner is required (clause 6.1.2 c)")
        for prefix in ("", "residual_"):
            try:
                likelihood = int(row[f"{prefix}likelihood"])
                impact = int(row[f"{prefix}impact"])
                score = int(row[f"{prefix}score" if prefix else "inherent_score"])
            except (KeyError, ValueError):
                if prefix and not any(row.get(f"residual_{k}") for k in ("likelihood", "impact", "score")):
                    continue  # residual not yet assessed
                report.error(loc, f"{prefix or 'inherent '}likelihood/impact/score must be integers")
                continue
            if not (1 <= likelihood <= 5 and 1 <= impact <= 5):
                report.error(loc, f"{prefix}likelihood and impact must be 1-5")
            if score != likelihood * impact:
                report.error(loc, f"{prefix or 'inherent_'}score {score} != {likelihood} x {impact}")
            if prefix and score >= 17 and row.get("acceptance_status") == "Accepted":
                report.warn(loc, "critical residual risk accepted; requires documented CEO decision")
        if row.get("treatment_option") not in TREATMENT_OPTIONS:
            report.error(loc, f"treatment_option must be one of {sorted(TREATMENT_OPTIONS)}")
        if row.get("acceptance_status") not in ACCEPTANCE_STATUSES:
            report.error(loc, f"acceptance_status must be one of {sorted(ACCEPTANCE_STATUSES)}")
        for control in split_list(row.get("annex_a_controls", "")):
            if control not in control_ids:
                report.error(loc, f"unknown Annex A control '{control}'")
        for aid in split_list(row.get("asset_ids", "")):
            if aid not in asset_ids:
                report.error(loc, f"asset '{aid}' not in asset inventory")
    return ids


def control_sort_key(cid):
    return tuple(int(p) for p in cid.split("."))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="only print the summary and errors")
    args = parser.parse_args()

    report = Report()
    catalogue = {r["control_id"]: r["control_name"] for r in read_csv(REFERENCE_CATALOGUE, report)}
    control_ids = set(catalogue)
    asset_ids = {r["asset_id"] for r in read_csv(REGISTERS / "asset-inventory.csv", report)}

    doc_ids = check_documents(report, control_ids)
    risk_ids = check_risks(report, control_ids, asset_ids)
    check_soa(report, catalogue, doc_ids, risk_ids)

    for e in report.errors:
        print(f"ERROR   {e}")
    if not args.quiet:
        for w in report.warnings:
            print(f"WARNING {w}")
    print(f"\n{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    failed = report.errors or (args.strict and report.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
