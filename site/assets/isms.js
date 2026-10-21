// Filtering and sorting for register tables (no external dependencies).
(function () {
  function cellValue(row, index) {
    const cell = row.cells[index];
    return cell ? cell.textContent.trim() : "";
  }

  function compare(a, b) {
    const na = Number(a), nb = Number(b);
    if (a !== "" && b !== "" && !isNaN(na) && !isNaN(nb)) return na - nb;
    // Natural sort handles control IDs such as 5.2 vs 5.10
    return a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });
  }

  function initRegister(table) {
    if (table.dataset.ready) return;
    table.dataset.ready = "1";
    const tbody = table.tBodies[0];
    const input = document.querySelector('input[data-filter="' + table.id + '"]');
    const counter = document.querySelector('[data-count="' + table.id + '"]');
    const total = tbody.rows.length;

    function updateCount(visible) {
      if (counter) counter.textContent = visible + " of " + total + " rows";
    }

    if (input) {
      input.addEventListener("input", function () {
        const terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
        let visible = 0;
        for (const row of tbody.rows) {
          const text = row.textContent.toLowerCase();
          const show = terms.every(function (t) { return text.includes(t); });
          row.hidden = !show;
          if (show) visible++;
        }
        updateCount(visible);
      });
    }
    updateCount(total);

    Array.from(table.tHead.rows[0].cells).forEach(function (th, index) {
      th.setAttribute("title", "Click to sort");
      th.addEventListener("click", function () {
        const ascending = th.getAttribute("aria-sort") !== "ascending";
        for (const other of th.parentNode.cells) other.removeAttribute("aria-sort");
        th.setAttribute("aria-sort", ascending ? "ascending" : "descending");
        const rows = Array.from(tbody.rows);
        rows.sort(function (r1, r2) {
          const result = compare(cellValue(r1, index), cellValue(r2, index));
          return ascending ? result : -result;
        });
        rows.forEach(function (r) { tbody.appendChild(r); });
      });
    });
  }

  function init() {
    document.querySelectorAll("table.register").forEach(initRegister);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
