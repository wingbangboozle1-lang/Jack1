/* Consolidated decision brief — client-side navigation and table filtering only.
   No analytics, no cookies, no network requests, no personal data. */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var body = document.body;
    var menuBtn = document.getElementById("menu-btn");
    var closeFn = function () { body.classList.remove("nav-open"); if (menuBtn) menuBtn.setAttribute("aria-expanded", "false"); };

    if (menuBtn) {
      menuBtn.addEventListener("click", function () {
        var open = body.classList.toggle("nav-open");
        menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }
    document.querySelectorAll(".sidebar a").forEach(function (a) { a.addEventListener("click", closeFn); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeFn(); } });

    var search = document.getElementById("global-search");
    var status = document.getElementById("status-filter");
    var clear = document.getElementById("clear-filters");
    var countEl = document.getElementById("result-count");
    var tables = Array.prototype.slice.call(document.querySelectorAll("table[data-table]"));
    var rows = [];
    tables.forEach(function (t) {
      Array.prototype.slice.call(t.querySelectorAll("tbody tr")).forEach(function (r) { rows.push(r); });
    });

    function apply() {
      var q = (search && search.value ? search.value : "").trim().toLowerCase();
      var s = status && status.value ? status.value : "all";
      var shown = 0;
      rows.forEach(function (r) {
        var text = (r.getAttribute("data-search") || r.textContent || "").toLowerCase();
        var st = r.getAttribute("data-status") || "verified";
        var ok = (!q || text.indexOf(q) !== -1) && (s === "all" || s === st);
        r.hidden = !ok;
        if (ok) shown++;
      });
      if (countEl) {
        countEl.textContent = shown === rows.length
          ? rows.length + " rows"
          : shown + " of " + rows.length + " rows";
      }
      tables.forEach(function (t) {
        var visible = Array.prototype.slice.call(t.querySelectorAll("tbody tr")).some(function (r) { return !r.hidden; });
        var empty = t.parentNode.querySelector(".no-results");
        if (!empty) {
          empty = document.createElement("p");
          empty.className = "no-results hint";
          empty.style.padding = "12px";
          empty.style.margin = "0";
          empty.textContent = "No rows match the current filter.";
          t.parentNode.appendChild(empty);
        }
        empty.hidden = visible;
      });
    }

    if (search) search.addEventListener("input", apply);
    if (status) status.addEventListener("change", apply);
    if (clear) clear.addEventListener("click", function () {
      if (search) search.value = "";
      if (status) status.value = "all";
      apply();
      if (search) search.focus();
    });
    apply();
  });
})();
