/* Jack1 — shared UI logic: sidebar/footer injection + sourced tables */
(function () {
  "use strict";

  const NAV = [
    { section: "Overview" },
    { id: "index",        href: "index.html",        label: "Executive Summary" },
    { id: "asset",        href: "asset.html",        label: "Asset Profile (Anonymized)" },
    { section: "Research" },
    { id: "demographics", href: "demographics.html", label: "Demographics & Income" },
    { id: "economy",      href: "economy.html",      label: "Economy & Jobs" },
    { id: "schools",      href: "schools.html",      label: "School Systems" },
    { id: "market",       href: "market.html",       label: "NNN / QSR Market & Taxes" },
    { id: "tenant",       href: "tenant.html",       label: "Tenant: Jack in the Box (SEC)" },
    { section: "Analysis" },
    { id: "risk",         href: "risk.html",         label: "Risk Matrix (incl. Black Swans)" },
    { id: "decision",     href: "decision.html",     label: "Decision: Sell vs. Renew" },
    { id: "projection",   href: "projection.html",   label: "Projection Model" },
    { section: "Governance" },
    { id: "flagged",      href: "flagged.html",      label: "Flagged for Review" },
    { id: "sources",      href: "sources.html",      label: "Sources & Verification" }
  ];

  const page = document.body.getAttribute("data-page") || "index";
  const pageTitle = document.body.getAttribute("data-title") || "Executive Summary";

  /* ---------- Sidebar ---------- */
  const navHtml = NAV.map(item => {
    if (item.section) return `<div class="nav-section">${item.section}</div>`;
    const active = item.id === page ? " active" : "";
    return `<a class="nav-link${active}" href="${item.href}"><span class="dot"></span>${item.label}</a>`;
  }).join("");

  const sidebar = document.getElementById("site-sidebar");
  if (sidebar) {
    sidebar.innerHTML = `
      <aside class="sidebar" id="sidebar">
        <div class="brand">
          <svg class="logo" viewBox="0 0 48 48" role="img" aria-label="Jack in the Box NNN logo — abstract jack-in-the-box" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="18" width="40" height="26" rx="4" fill="#ffd166" stroke="#16324a" stroke-width="2.4"/>
            <path d="M14 18v-4a10 10 0 0 1 20 0v4" fill="none" stroke="#16324a" stroke-width="2.4"/>
            <circle cx="24" cy="31" r="5.6" fill="#16324a"/>
            <path d="M24 25.4v-8M19.5 27.2l-6-5.4M28.5 27.2l6-5.4" stroke="#16324a" stroke-width="2.2" stroke-linecap="round"/>
          </svg>
          <div>
            <div class="brand-name">Jack in the Box<br>Central LA — NNN</div>
            <div class="brand-sub">Sell vs. Renew · 2030–2035</div>
          </div>
        </div>
        <nav class="nav" id="nav">${navHtml}</nav>
        <div class="sidebar-foot">
          Prepared 2026-11-06 · Data public &amp; aggregate only<br>
          No personal information is displayed on this site.<br>
          <a href="sources.html">Verification protocol →</a>
        </div>
      </aside>`;
  }

  /* ---------- Topbar ---------- */
  const topbar = document.getElementById("site-topbar");
  if (topbar) {
    topbar.innerHTML = `
      <header class="topbar">
        <button class="hamburger" id="hamburger" aria-label="Toggle navigation">☰</button>
        <div class="crumbs">Jack1 / <b>${pageTitle}</b></div>
        <span class="privacy-pill">PII-Free Public Data</span>
      </header>`;
  }

  /* ---------- Footer ---------- */
  const footer = document.getElementById("site-footer");
  if (footer) {
    footer.innerHTML = `
      <footer class="footer">
        <div>Jack1 · Decision support for one anonymized NNN asset in central Los Angeles.<br>
        All figures carry an attached source or an explicit “unverified / illustrative” flag. Nothing here is investment, tax or legal advice.</div>
        <div>Data as of Nov 2026 · <a href="sources.html">Sources &amp; verification</a> · <a href="flagged.html">Flagged for review</a></div>
      </footer>`;
  }

  const burger = document.getElementById("hamburger");
  if (burger) burger.addEventListener("click", () => document.getElementById("sidebar").classList.toggle("open"));

  /* ---------- Sourced tables ---------- */
  const STATUS = {
    official:     { cls: "b-official",     label: "Official source" },
    secondary:    { cls: "b-secondary",    label: "Secondary source" },
    market:       { cls: "b-market",       label: "Market / broker data" },
    unverified:   { cls: "b-unverified",   label: "Unverified — flagged" },
    illustrative: { cls: "b-illustrative", label: "Illustrative" }
  };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c]));
  }

  function sourceLinks(ids) {
    if (!ids || !ids.length) return '<span class="small">— none —</span>';
    return ids.map(id => {
      const src = (window.JACK1_SOURCES || {})[id];
      if (!src) return `<span class="small">[missing source id: ${esc(id)}]</span>`;
      return `<a href="${esc(src.url)}" target="_blank" rel="noopener noreferrer" title="${esc(src.label)}">${esc(src.label.split("—")[0].trim())} ↗</a>`;
    }).join("<br>");
  }

  function renderTable(mountId, dataset, opts) {
    const mount = document.getElementById(mountId);
    if (!mount) return;
    const rows = (window.JACK1_DATA && window.JACK1_DATA[dataset]) || [];
    const filters = ["all","official","secondary","market","unverified","illustrative"];
    mount.innerHTML = `
      <div class="table-tools" role="group" aria-label="Table filters">
        <input class="search" type="search" placeholder="Filter rows… (e.g. cap rate, income, fire)" aria-label="Filter table rows">
        ${filters.map(f => `<button class="filter-btn${f==="all"?" active":""}" data-f="${f}">${f==="all" ? "All" : STATUS[f].label}</button>`).join("")}
        <span class="row-count"></span>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Metric</th><th>Value</th><th>Geography</th><th>Period</th><th>Source(s)</th><th>Status</th><th>Notes</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>`;
    const tbody = mount.querySelector("tbody");
    const search = mount.querySelector(".search");
    const countEl = mount.querySelector(".row-count");
    let activeFilter = "all";

    function draw() {
      const q = (search.value || "").trim().toLowerCase();
      let shown = 0;
      tbody.innerHTML = rows.map(r => {
        const st = STATUS[r.st] || STATUS.unverified;
        const hay = [r.m, r.v, r.g, r.p, r.n, (r.s||[]).map(id => (window.JACK1_SOURCES[id]||{}).label || "").join(" ")].join(" ").toLowerCase();
        const okFilter = activeFilter === "all" || r.st === activeFilter;
        const okSearch = !q || hay.includes(q);
        if (!okFilter || !okSearch) return "";
        shown++;
        return `<tr data-st="${esc(r.st)}">
          <td>${esc(r.m)}</td>
          <td><strong>${esc(r.v)}</strong></td>
          <td>${esc(r.g)}</td>
          <td>${esc(r.p)}</td>
          <td>${sourceLinks(r.s)}</td>
          <td><span class="badge ${st.cls}">${esc(st.label)}</span></td>
          <td class="small" style="color:var(--ink-soft)">${esc(r.n || "")}</td>
        </tr>`;
      }).join("");
      countEl.textContent = `${shown} of ${rows.length} rows shown`;
    }
    search.addEventListener("input", draw);
    mount.querySelectorAll(".filter-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        activeFilter = btn.getAttribute("data-f");
        mount.querySelectorAll(".filter-btn").forEach(b => b.classList.toggle("active", b === btn));
        draw();
      });
    });
    draw();
  }

  document.querySelectorAll("[data-table]").forEach(el => renderTable(el.id, el.getAttribute("data-table")));
})();
