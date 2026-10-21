#!/usr/bin/env python3
"""Assemble the ISMS website source for MkDocs.

Reads the ISMS documents (docs/, policies/), registers (registers/*.csv) and
README.md, and writes:
  build/site_src/   Markdown pages: dashboard, documents, rendered registers
  build/mkdocs.yml  site/mkdocs.yml plus docs_dir and a generated nav

Documents are enriched with a metadata block, links between document IDs,
links to registers and highlighted {{PLACEHOLDERS}}.

Usage: python tools/build_site.py && mkdocs build -f build/mkdocs.yml
"""
import csv
import datetime as dt
import html
import os
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

import yaml

import validate_isms as v

ROOT = v.ROOT
BUILD = ROOT / "build"
SRC = BUILD / "site_src"
SITE = ROOT / "site"

CLAUSE_SECTIONS = {
    "01-context": "4 Context",
    "02-leadership": "5 Leadership",
    "03-planning": "6 Planning",
    "04-support": "7 Support",
    "05-operation": "8 Operation",
    "06-performance": "9 Performance evaluation",
    "07-improvement": "10 Improvement",
}

# csv file stem -> (title, description, row-id column, row-id prefix)
REGISTERS = {
    "statement-of-applicability": ("Statement of Applicability", "Clause 6.1.3 d: the necessary controls, why they are included or excluded, and whether they are implemented.", "control_id", "ctrl-"),
    "risk-register": ("Risk Register", "Clauses 8.2 and 8.3: results of risk assessment and risk treatment. Score = likelihood × impact (see ISMS-PRC-001).", "risk_id", ""),
    "asset-inventory": ("Asset Inventory", "Control 5.9: information and other associated assets, with owners and classification.", "asset_id", ""),
    "interested-parties": ("Interested Parties", "Clause 4.2: interested parties, their requirements, and which of them the ISMS addresses.", "party_id", ""),
    "legal-regulatory-register": ("Legal & Regulatory Register", "Control 5.31: legal, statutory, regulatory and contractual requirements.", "req_id", ""),
    "internal-audit-programme": ("Internal Audit Programme", "Clause 9.2: the audit programme.", "audit_id", ""),
    "nonconformity-log": ("Nonconformity Log", "Clause 10.2: nonconformities, corrective actions and their results.", "nc_id", ""),
    "reference-annex-a-2022": ("Annex A Reference (2022)", "Reference catalogue of the 93 ISO/IEC 27001:2022 Annex A controls. The validator checks the SoA against it.", "control_id", "ref-"),
}
BADGE_COLUMNS = {"applicable", "implementation_status", "status", "acceptance_status", "compliance_status", "addressed_by_isms", "independence_confirmed"}
DOC_ID = re.compile(r"(?<![\w/\-\[])(ISMS-(?:POL|PRC|DOC|REC)-\d{3})(?![\w\-])")
INLINE_CODE = re.compile(r"(`[^`]+`)")


# ---------------------------------------------------------------- helpers

def page_url(page):
    """URL path (relative to site root) of a Markdown page with directory URLs."""
    page = Path(page)
    if page.name == "index.md":
        return page.parent.as_posix() + "/" if page.parent != Path(".") else ""
    return page.with_suffix("").as_posix() + "/"


def rel_url(from_page, to_page, anchor=""):
    """Relative URL for raw HTML links (MkDocs does not rewrite those)."""
    base = page_url(from_page) or "."
    target = page_url(to_page) or "."
    url = os.path.relpath(target, base).replace(os.sep, "/")
    url = "./" if url == "." else url + "/"
    return url + (f"#{anchor}" if anchor else "")


def rel_md(from_page, to_page):
    """Relative link between Markdown sources (MkDocs rewrites these)."""
    return os.path.relpath(to_page, Path(from_page).parent).replace(os.sep, "/")


def esc(value):
    return html.escape(str(value), quote=True)


def badge(value):
    if not value:
        return ""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return f'<span class="badge badge--{slug}">{esc(value)}</span>'


def score_level(score):
    if score >= 17:
        return "critical"
    if score >= 10:
        return "high"
    if score >= 5:
        return "medium"
    return "low"


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


# ---------------------------------------------------------------- model

class Site:
    def __init__(self):
        self.docs = []           # dicts: id, title, meta, source, page, section
        self.id_to_page = {}
        self.path_to_page = {}   # repo-relative source path -> site page
        self.nav = []

    def collect_documents(self):
        for source in sorted((ROOT / "docs").rglob("*.md")):
            section = source.parent.name
            self._add_doc(source, Path("isms") / section / source.name, CLAUSE_SECTIONS.get(section, section))
        for source in sorted((ROOT / "policies").glob("*.md")):
            self._add_doc(source, Path("policies") / source.name, "Policies")
        for stem in REGISTERS:
            self.path_to_page[f"registers/{stem}.csv"] = Path("registers") / f"{stem}.md"
        self.path_to_page["README.md"] = Path("about.md")

    def _add_doc(self, source, page, section):
        meta = v.parse_front_matter(source.read_text(encoding="utf-8")) or {}
        doc = {"id": meta.get("id", source.stem), "title": meta.get("title", source.stem),
               "meta": meta, "source": source, "page": page, "section": section}
        self.docs.append(doc)
        self.id_to_page[doc["id"]] = page
        self.path_to_page[source.relative_to(ROOT).as_posix()] = page

    # ------------------------------------------------------------ linking

    def enrich_line(self, line, page, own_id=None):
        """Link document IDs and repo paths, highlight placeholders (outside code)."""
        parts = INLINE_CODE.split(line)
        for i, part in enumerate(parts):
            if part.startswith("`") and part.endswith("`"):
                target = self.path_to_page.get(part.strip("`"))
                if target:
                    parts[i] = f"[{part}]({rel_md(page, target)})"
                continue

            def link_id(match):
                doc_id = match.group(1)
                target = self.id_to_page.get(doc_id)
                if not target or doc_id == own_id:
                    return doc_id
                return f"[{doc_id}]({rel_md(page, target)})"

            part = DOC_ID.sub(link_id, part)
            part = v.PLACEHOLDER.sub(lambda m: f'<span class="placeholder">{esc(m.group(0))}</span>', part)
            parts[i] = part
        return "".join(parts)

    def enrich_markdown(self, text, page, own_id=None):
        out, in_fence, in_front = [], False, text.startswith("---\n")
        for n, line in enumerate(text.splitlines()):
            if in_front:
                out.append(line)
                if n > 0 and line.strip() == "---":
                    in_front = False
                continue
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
                out.append(line)
                continue
            out.append(line if in_fence else self.enrich_line(line, page, own_id))
        return "\n".join(out) + "\n"

    def html_refs(self, value, page):
        """Render a ;-separated list of doc IDs / paths as HTML links."""
        links = []
        for ref in v.split_list(value):
            target = self.id_to_page.get(ref) or self.path_to_page.get(ref)
            links.append(f'<a href="{rel_url(page, target)}">{esc(ref)}</a>' if target else esc(ref))
        return ", ".join(links)

    # ------------------------------------------------------------ pages

    def write(self, page, content):
        path = SRC / page
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def doc_meta_block(self, doc):
        m = doc["meta"]
        clauses = ", ".join(m.get("iso_clauses") or []) or "—"
        soa = Path("registers/statement-of-applicability.md")
        controls = ", ".join(
            f'<a href="{rel_url(doc["page"], soa, "ctrl-" + c)}">{esc(c)}</a>' for c in (m.get("annex_a") or [])
        ) or "—"
        rows = [
            ("Document ID", esc(doc["id"])),
            ("Version", esc(m.get("version", ""))),
            ("Status", badge(m.get("status", ""))),
            ("Classification", esc(m.get("classification", ""))),
            ("Owner", esc(m.get("owner", ""))),
            ("Approver", esc(m.get("approver", ""))),
            ("ISO/IEC 27001 clauses", esc(clauses)),
            ("Annex A controls", controls),
            ("Last reviewed", esc(m.get("last_reviewed") or "—")),
            ("Next review", esc(m.get("next_review") or "—")),
        ]
        cells = "".join(f"<tr><th>{k}</th><td>{v_}</td></tr>" for k, v_ in rows)
        cells = v.PLACEHOLDER.sub(lambda mt: f'<span class="placeholder">{mt.group(0)}</span>', cells)
        return f'<div class="doc-meta"><table>{cells}</table></div>\n'

    def build_documents(self):
        for doc in self.docs:
            text = self.enrich_markdown(doc["source"].read_text(encoding="utf-8"), doc["page"], doc["id"])
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    lines.insert(i + 1, "\n" + self.doc_meta_block(doc))
                    break
            self.write(doc["page"], "\n".join(lines) + "\n")

    def build_registers(self):
        for stem, (title, description, id_col, id_prefix) in REGISTERS.items():
            page = Path("registers") / f"{stem}.md"
            fields, rows = read_csv(ROOT / "registers" / f"{stem}.csv")
            shutil.copy(ROOT / "registers" / f"{stem}.csv", SRC / "registers" / f"{stem}.csv")
            table_id = f"reg-{stem}"
            head = "".join(f"<th>{esc(f.replace('_', ' '))}</th>" for f in fields)
            body = []
            for row in rows:
                cells = [self.register_cell(f, row.get(f, "") or "", page) for f in fields]
                row_id = f' id="{esc(id_prefix + row[id_col])}"' if row.get(id_col) else ""
                body.append(f"<tr{row_id}>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
            empty = f'<tr><td colspan="{len(fields)}"><em>No entries yet.</em></td></tr>' if not rows else ""
            content = (
                f"---\ntitle: {title}\nhide:\n  - toc\n---\n\n"
                f"# {title}\n\n{self.enrich_line(description, page)}\n\n"
                f'<div class="register-tools">'
                f'<input type="search" data-filter="{table_id}" placeholder="Filter rows (all words must match)" aria-label="Filter {esc(title)}">'
                f'<span class="register-count" data-count="{table_id}"></span>'
                f'<a class="md-button" href="../{stem}.csv" download>Download CSV</a></div>\n\n'
                f'<div class="md-typeset__scrollwrap"><div class="md-typeset__table">'
                f'<table class="register" id="{table_id}"><thead><tr>{head}</tr></thead>'
                f'<tbody>{"".join(body)}{empty}</tbody></table></div></div>\n\n'
                f"Source: `registers/{stem}.csv`. Edit the CSV through a pull request; this page is generated.\n"
            )
            self.write(page, content)

    def register_cell(self, field, value, page):
        soa = Path("registers/statement-of-applicability.md")
        if field in BADGE_COLUMNS:
            return badge(value)
        if field == "implementation_reference":
            return self.html_refs(value, page)
        if field in ("risk_ids",):
            return ", ".join(f'<a href="{rel_url(page, Path("registers/risk-register.md"), r)}">{esc(r)}</a>' for r in v.split_list(value))
        if field in ("asset_ids", "dependencies"):
            return ", ".join(f'<a href="{rel_url(page, Path("registers/asset-inventory.md"), a)}">{esc(a)}</a>' for a in v.split_list(value))
        if field in ("annex_a_controls", "isms_controls"):
            return ", ".join(f'<a href="{rel_url(page, soa, "ctrl-" + c)}">{esc(c)}</a>' for c in v.split_list(value))
        if field in ("inherent_score", "residual_score") and to_int(value) is not None:
            return f'<span class="badge heat--{score_level(int(value))}" style="color:inherit">{esc(value)}</span>'
        text = esc(value)
        return v.PLACEHOLDER.sub(lambda m: f'<span class="placeholder">{m.group(0)}</span>', text)

    def build_about(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.write(Path("about.md"), self.enrich_markdown(readme, Path("about.md")))

    def build_dashboard(self):
        page = Path("index.md")
        report = v.Report()
        catalogue = {r["control_id"]: r["control_name"] for r in v.read_csv(v.REFERENCE_CATALOGUE, report)}
        assets = {r["asset_id"] for r in v.read_csv(v.REGISTERS / "asset-inventory.csv", report)}
        doc_ids = v.check_documents(report, set(catalogue))
        risk_ids = v.check_risks(report, set(catalogue), assets)
        v.check_soa(report, catalogue, doc_ids, risk_ids)

        _, soa = read_csv(ROOT / "registers/statement-of-applicability.csv")
        _, risks = read_csv(ROOT / "registers/risk-register.csv")
        _, ncs = read_csv(ROOT / "registers/nonconformity-log.csv")
        today = dt.date.today()

        doc_status = Counter(d["meta"].get("status", "") for d in self.docs)
        decided = sum(1 for r in soa if r["applicable"] in ("Yes", "No"))
        applicable = [r for r in soa if r["applicable"] == "Yes"]
        implemented = sum(1 for r in applicable if r["implementation_status"] == "Implemented")
        open_ncs = sum(1 for r in ncs if r.get("status", "").lower() != "closed")

        def current_score(r):
            return to_int(r.get("residual_score")) or to_int(r.get("inherent_score")) or 0

        high_risks = sum(1 for r in risks if current_score(r) >= 10 and r.get("acceptance_status") != "Accepted")
        overdue = [d for d in self.docs if (n := v.parse_date(d["meta"].get("next_review", ""))) and n < today]
        placeholders = sum(len(set(v.PLACEHOLDER.findall(d["source"].read_text(encoding="utf-8")))) for d in self.docs)

        def tile(value, label, href=None):
            inner = f'<div class="tile__value">{value}</div><div class="tile__label">{label}</div>'
            return f'<a class="tile" href="{href}">{inner}</a>' if href else f'<div class="tile">{inner}</div>'

        reg = lambda stem, anchor="": rel_url(page, Path(f"registers/{stem}.md"), anchor)
        tiles = "".join([
            tile(f"{doc_status.get('Approved', 0)}/{len(self.docs)}", "Documents approved"),
            tile(f"{decided}/{len(soa)}", "SoA applicability decided", reg("statement-of-applicability")),
            tile(f"{implemented}/{len(applicable)}", "Applicable controls implemented", reg("statement-of-applicability")),
            tile(len(risks), "Risks identified", reg("risk-register")),
            tile(high_risks, "High/critical risks not yet accepted", reg("risk-register")),
            tile(open_ncs, "Open nonconformities", reg("nonconformity-log")),
            tile(len(overdue), "Documents overdue for review"),
            tile(placeholders, "Unfilled placeholders"),
        ])

        validation = (
            '!!! success "Validation passed"\n    No consistency errors.'
            if not report.errors else
            f'!!! failure "Validation: {len(report.errors)} error(s)"\n' + "\n".join(f"    - {esc(e)}" for e in report.errors[:20])
        )
        validation += f"\n\n    {len(report.warnings)} warning(s): drafts, undecided controls, placeholders or overdue reviews. Run `python tools/validate_isms.py` for details.\n"

        # SoA progress per theme
        theme_rows = []
        for theme in ("Organizational", "People", "Physical", "Technological"):
            rows = [r for r in soa if r["theme"] == theme]
            counts = Counter(r["implementation_status"] for r in rows)
            total = len(rows) or 1
            segs = "".join(
                f'<span style="width:{100 * counts.get(s, 0) / total:.1f}%;background:var({c})" title="{s}: {counts.get(s, 0)}"></span>'
                for s, c in (("Implemented", "--isms-low"), ("Partially implemented", "--isms-medium"), ("Not implemented", "--isms-critical"))
            )
            theme_rows.append(
                f"<tr><td>{theme}</td><td>{len(rows)}</td><td>{sum(1 for r in rows if r['applicable'] == 'Yes')}</td>"
                f"<td>{counts.get('Implemented', 0)}</td><td style='min-width:10rem'><div class='bar'>{segs}</div></td></tr>"
            )
        soa_table = (
            '<div class="md-typeset__scrollwrap"><div class="md-typeset__table"><table><thead>'
            "<tr><th>Theme</th><th>Controls</th><th>Applicable</th><th>Implemented</th><th>Progress</th></tr></thead>"
            f"<tbody>{''.join(theme_rows)}</tbody></table></div></div>"
        )

        def heatmap(prefix):
            grid = Counter()
            for r in risks:
                lk, im = to_int(r.get(f"{prefix}likelihood")), to_int(r.get(f"{prefix}impact"))
                if lk and im:
                    grid[(lk, im)] += 1
            head = "".join(f"<th>{i}</th>" for i in range(1, 6))
            body = ""
            for lk in range(5, 0, -1):
                cells = "".join(
                    f'<td class="heat--{score_level(lk * im)}">{grid[(lk, im)] or ""}</td>' for im in range(1, 6)
                )
                body += f"<tr><th>{lk}</th>{cells}</tr>"
            return f'<table class="heatmap"><thead><tr><th>L \\ I</th>{head}</tr></thead><tbody>{body}</tbody></table>'

        doc_rows = "".join(
            f'<tr><td><a href="{rel_url(page, d["page"])}">{esc(d["id"])}</a></td><td>{esc(d["title"])}</td>'
            f'<td>{badge(d["meta"].get("status", ""))}</td><td>{esc(d["meta"].get("version", ""))}</td>'
            f'<td>{esc(d["meta"].get("next_review") or "—")}</td></tr>'
            for d in sorted(self.docs, key=lambda d: d["id"])
        )

        content = f"""---
title: Dashboard
hide:
  - navigation
  - toc
---

# ISMS Dashboard

Information Security Management System based on **ISO/IEC 27001:2022 including Amendment 1:2024**. See [About]({rel_md(page, Path("about.md"))}) for structure and roadmap. Generated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC.

<div class="tiles">{tiles}</div>

{validation}

## Statement of Applicability progress

{soa_table}

## Risk heat map

Likelihood (rows) × impact (columns). Number of risks in each cell. See the [risk methodology]({rel_md(page, self.id_to_page.get("ISMS-PRC-001", page))}).

<div class="grid cards" markdown>

-   **Inherent risk**

    {heatmap("")}

-   **Residual risk**

    {heatmap("residual_")}

</div>

## Documents

<div class="md-typeset__scrollwrap"><div class="md-typeset__table"><table><thead><tr><th>ID</th><th>Title</th><th>Status</th><th>Version</th><th>Next review</th></tr></thead><tbody>{doc_rows}</tbody></table></div></div>
"""
        self.write(page, content)

    # ------------------------------------------------------------ nav

    def build_nav(self):
        isms = []
        for folder, label in CLAUSE_SECTIONS.items():
            entries = [{d["title"]: d["page"].as_posix()} for d in self.docs if d["page"].parts[:2] == ("isms", folder)]
            if entries:
                isms.append({label: entries})
        policies = [{d["title"]: d["page"].as_posix()} for d in self.docs if d["page"].parts[0] == "policies"]
        registers = [{title: f"registers/{stem}.md"} for stem, (title, *_rest) in REGISTERS.items()]
        return [
            {"Dashboard": "index.md"},
            {"ISMS": isms},
            {"Policies": policies},
            {"Registers": registers},
            {"About": "about.md"},
        ]


def main():
    if SRC.exists():
        shutil.rmtree(SRC)
    (SRC / "registers").mkdir(parents=True)
    shutil.copytree(SITE / "assets", SRC / "assets")

    site = Site()
    site.collect_documents()
    site.build_documents()
    site.build_registers()
    site.build_about()
    site.build_dashboard()

    config = yaml.safe_load((SITE / "mkdocs.yml").read_text(encoding="utf-8"))
    config["docs_dir"] = "site_src"
    config["nav"] = site.build_nav()
    org = os.environ.get("ISMS_SITE_NAME")
    if org:
        config["site_name"] = org
    (BUILD / "mkdocs.yml").write_text(
        "# Generated by tools/build_site.py - do not edit.\n" + yaml.safe_dump(config, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Site source written to {SRC.relative_to(ROOT)} ({len(site.docs)} documents, {len(REGISTERS)} registers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
