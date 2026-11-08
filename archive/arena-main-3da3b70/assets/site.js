(() => {
  const menuButton = document.querySelector("[data-nav-toggle]");
  const sidebar = document.querySelector(".sidebar");

  if (menuButton && sidebar) {
    const closeMenu = () => {
      sidebar.classList.remove("is-open");
      menuButton.setAttribute("aria-expanded", "false");
    };

    menuButton.addEventListener("click", () => {
      const open = sidebar.classList.toggle("is-open");
      menuButton.setAttribute("aria-expanded", String(open));
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });

    sidebar.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });
  }

  document.querySelectorAll("[data-table-search]").forEach((input) => {
    const target = document.getElementById(input.dataset.tableSearch);
    if (!target) return;
    const rows = Array.from(target.querySelectorAll("tbody tr"));
    input.addEventListener("input", () => {
      const query = input.value.trim().toLocaleLowerCase();
      rows.forEach((row) => {
        row.hidden = query !== "" && !row.textContent.toLocaleLowerCase().includes(query);
      });
    });
  });

  // Private break-even worksheet for projections.html.
  // Runs entirely in the browser: no network request, no storage, no logging.
  const calc = document.getElementById("calc");
  const calcOut = document.getElementById("c-out");
  const fmt = (n) => n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
  const num = (id) => {
    const el = document.getElementById(id);
    if (!el) return NaN;
    const v = parseFloat(el.value);
    return Number.isFinite(v) ? v : NaN;
  };

  if (calc && calcOut) {
    const run = () => {
      const rent = num("c-rent"), cap = num("c-cap"), years = num("c-years");
      const growth = num("c-growth"), costs = num("c-costs"), debt = num("c-debt");
      const disc = num("c-disc"), exitCap = num("c-resid");
      const missing = [
        ["rent", rent], ["cap rate", cap], ["remaining term", years], ["rent growth", growth],
        ["sale costs", costs], ["debt payoff", debt], ["required return", disc], ["exit cap rate", exitCap],
      ].filter(([, v]) => !Number.isFinite(v)).map(([k]) => k);

      if (missing.length) {
        calcOut.innerHTML =
          '<p class="small">Still needed: <strong>' + missing.join(", ") +
          '</strong>. Results appear only when every input is supplied, so no partial answer is implied.</p>';
        return;
      }
      if ([cap, exitCap, disc, costs].some((v) => v < 0) || [rent, years, debt].some((v) => v < 0)) {
        calcOut.innerHTML = '<p class="small">Negative values are not meaningful for these inputs.</p>';
        return;
      }
      if (cap === 0 || exitCap === 0) {
        calcOut.innerHTML = '<p class="small">A cap rate of zero gives an undefined value. Enter a positive cap rate.</p>';
        return;
      }

      const value = rent / (cap / 100);
      const netProceeds = value * (1 - costs / 100) - debt;
      // Present value of the remaining rent stream, grown annually and discounted at the required return.
      let pv = 0;
      const whole = Math.floor(years);
      for (let t = 1; t <= whole; t += 1) {
        pv += (rent * Math.pow(1 + growth / 100, t - 1)) / Math.pow(1 + disc / 100, t);
      }
      const exitRent = rent * Math.pow(1 + growth / 100, years);
      const residual = exitRent / (exitCap / 100);
      pv += residual / Math.pow(1 + disc / 100, Math.max(years, 0.0001));
      const gap = netProceeds - pv;

      const cell = (label, val, note) =>
        '<div class="calc-result"><div class="calc-label">' + label + '</div><div class="calc-value">' +
        val + '</div><div class="calc-note">' + note + '</div></div>';

      calcOut.innerHTML =
        '<p class="small">Illustrative arithmetic on the figures you entered. Not a valuation, not an appraisal, and not an official statistic. Nothing was transmitted or saved.</p>' +
        '<div class="calc-results">' +
        cell("Implied value today", fmt(value), "Annual rent divided by the cap rate you entered.") +
        cell("Net sale proceeds", fmt(netProceeds), "Value less sale costs and debt payoff. Excludes income tax on gain.") +
        cell("Hold value", fmt(pv), "Present value of the rent stream plus reversion at the exit cap rate.") +
        cell("Sale advantage", fmt(gap), gap >= 0 ? "Net proceeds exceed the hold value on these inputs." : "The hold value exceeds net proceeds on these inputs.") +
        cell("Break-even sale price", fmt(pv / Math.max(1 - costs / 100, 0.0001) + debt), "Price at which net proceeds equal the hold value.") +
        cell("Total rent to expiry", fmt(rent * ((Math.pow(1 + growth / 100, years) - 1) / Math.max(growth / 100, 0.0001))), "Undiscounted contractual rent over the remaining term.") +
        '</div>';
    };

    const runButton = document.getElementById("c-run");
    if (runButton) runButton.addEventListener("click", run);
    calc.addEventListener("submit", (event) => { event.preventDefault(); run(); });
    calc.addEventListener("reset", () => {
      window.setTimeout(() => {
        calcOut.innerHTML = '<p class="small">Cleared. Enter your own figures and choose “Compute”.</p>';
      }, 0);
    });
  }

})();
