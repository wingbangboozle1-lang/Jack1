(function () {
  "use strict";

  /* ---- Mobile navigation ---- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (evt) {
      if (window.innerWidth > 900) return;
      if (!nav.contains(evt.target) && !toggle.contains(evt.target) && nav.classList.contains("open")) {
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---- Per-table row filter with visible match feedback ----
     Each table gets its own search box. Filtering hides rows only; it never
     hides a row silently, because the counter states how many rows matched. */
  document.querySelectorAll("[data-table-search]").forEach(function (input) {
    var table = document.getElementById(input.getAttribute("data-table-search"));
    if (!table) return;
    var body = table.tBodies[0];
    if (!body) return;
    var rows = Array.prototype.slice.call(body.rows);

    var counter = document.createElement("span");
    counter.className = "filter-count micro muted";
    counter.setAttribute("aria-live", "polite");
    input.parentNode.appendChild(counter);

    function apply() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (row) {
        var hit = q === "" || row.textContent.toLowerCase().indexOf(q) !== -1;
        row.hidden = !hit;
        if (hit) shown += 1;
      });
      counter.textContent = q === ""
        ? rows.length + " rows"
        : shown + " of " + rows.length + " rows match";
      table.classList.toggle("is-filtered", q !== "");
    }

    input.addEventListener("input", apply);
    input.addEventListener("keydown", function (evt) {
      if (evt.key === "Escape") {
        input.value = "";
        apply();
      }
    });
    apply();
  });

  /* ---- Keyboard shortcut: "/" focuses the first filter on the page ---- */
  document.addEventListener("keydown", function (evt) {
    var tag = (evt.target.tagName || "").toLowerCase();
    if (evt.key !== "/" || tag === "input" || tag === "textarea") return;
    var first = document.querySelector("[data-table-search]");
    if (!first) return;
    evt.preventDefault();
    first.focus();
  });
})();
