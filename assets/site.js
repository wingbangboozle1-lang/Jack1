(function () {
  "use strict";
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
  document.querySelectorAll("[data-print-page]").forEach(function (button) {
    button.addEventListener("click", function () { window.print(); });
  });
  document.querySelectorAll("[data-table-search]").forEach(function (input) {
    var table = document.getElementById(input.getAttribute("data-table-search"));
    if (!table) return;
    var rows = Array.prototype.slice.call(table.tBodies[0] ? table.tBodies[0].rows : []);
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      rows.forEach(function (row) {
        row.hidden = q !== "" && row.textContent.toLowerCase().indexOf(q) === -1;
      });
    });
  });

  document.querySelectorAll("[data-print]").forEach(function (btn) {
    btn.addEventListener("click", function () { window.print(); });
  });

  var ws = document.getElementById("owner-worksheet");
  if (!ws) return;

  function num(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    var raw = String(el.value || "").trim().replace(/[$,%\s]/g, "");
    if (raw === "") return null;
    var val = Number(raw);
    return Number.isFinite(val) ? val : null;
  }

  function fmtUsd(v) {
    if (v === null || !Number.isFinite(v)) return "—";
    return (v < 0 ? "-$" : "$") + Math.round(Math.abs(v)).toLocaleString("en-US");
  }

  function setOut(id, text, note) {
    var el = document.getElementById(id);
    if (el) el.textContent = text;
    var nEl = document.getElementById(id + "-note");
    if (nEl && note !== undefined) nEl.textContent = note;
  }

  function laTransferRate(price, jurisdiction) {
    if (price === null || price <= 0) return null;
    if (jurisdiction === "county_only") return 0.0011;
    // Verified City of LA effective July 1, 2026: County 0.11% + City Base 0.45% + ULA 4% (>5.4M–<10.9M) or 5.5% (>=10.9M)
    if (price >= 10900000) return 0.0606;
    if (price > 5400000) return 0.0456;
    return 0.0056;
  }

  // Both paths are after tax and use the same owner-entered rates, so the spread is like for like.
  // Hold path: after-tax rent less interest, plus exit value net of exit costs, horizon debt and tax on
  // exit gain, minus after-tax re-leasing downtime. Every hold input must be present or the output stays blank.
  function updateWorksheet() {
    var price = num("ws-sale-price");
    var debt = num("ws-debt");
    var debtExit = num("ws-debt-exit");
    var brokerPct = num("ws-broker-pct");
    var basis = num("ws-tax-basis");
    var taxPct = num("ws-tax-rate");
    var rent = num("ws-rent");
    var rentTaxPct = num("ws-rent-tax");
    var interest = num("ws-interest");
    var years = num("ws-years");
    var escPct = num("ws-esc");
    var discPct = num("ws-discount");
    var exitVal = num("ws-exit-val");
    var downMonths = num("ws-downtime");
    var carry = num("ws-carry");
    var jurEl = document.getElementById("ws-jurisdiction");
    var exchEl = document.getElementById("ws-exchange");
    var jur = jurEl ? jurEl.value : "la_city";
    var is1031 = exchEl ? exchEl.value === "1031" : false;

    var dttRate = laTransferRate(price, jur);
    var dttAmt = (price !== null && dttRate !== null) ? price * dttRate : null;
    if (dttAmt !== null) {
      setOut("ws-out-dtt", fmtUsd(dttAmt), (dttRate * 100).toFixed(2) + "% combined effective transfer rate (" + (jur === "la_city" ? "LA County + City Base + ULA tier" : "LA County 0.11% only") + ").");
    } else {
      setOut("ws-out-dtt", "—", "Enter a sale price to evaluate the 0.56% / 4.56% / 6.06% LA transfer-tax tier.");
    }

    var netProceeds = null;
    var estTax = null;
    if (price !== null && debt !== null && brokerPct !== null && dttAmt !== null) {
      var closingCost = dttAmt + price * (brokerPct / 100);
      if (is1031) {
        estTax = 0;
        netProceeds = price - debt - closingCost;
        setOut("ws-out-sale", fmtUsd(netProceeds), "1031 deferred tax assumed $0 (subject to 45/180-day Form 8824 & zero boot); after debt & " + fmtUsd(closingCost) + " closing/DTT. Not like-for-like with the hold case, which pays tax on exit.");
      } else if (basis !== null && taxPct !== null) {
        var taxableGain = Math.max(0, (price - closingCost) - basis);
        estTax = taxableGain * (taxPct / 100);
        netProceeds = price - debt - closingCost - estTax;
        setOut("ws-out-sale", fmtUsd(netProceeds), "After debt, " + fmtUsd(closingCost) + " DTT/closing, and " + fmtUsd(estTax) + " estimated tax on gain.");
      } else {
        setOut("ws-out-sale", "—", "Enter adjusted tax basis & effective tax rate (or select 1031 deferral) for after-tax proceeds.");
      }
    } else {
      setOut("ws-out-sale", "—", "Requires sale price, debt payoff, and brokerage/other cost % locally.");
    }

    var holdPv = null;
    var holdReady = rent !== null && rentTaxPct !== null && interest !== null && years !== null && years > 0 &&
      escPct !== null && discPct !== null && exitVal !== null && debtExit !== null && basis !== null &&
      taxPct !== null && brokerPct !== null && downMonths !== null && carry !== null &&
      downMonths >= 0 && carry >= 0 && rentTaxPct >= 0 && rentTaxPct <= 100 && taxPct >= 0 && taxPct <= 100 && discPct > -100;
    if (holdReady) {
      var r = discPct / 100;
      var g = escPct / 100;
      var tr = rentTaxPct / 100;
      var tg = taxPct / 100;
      var afterTaxRent = function (t) { return (rent * Math.pow(1 + g, t - 1) - interest) * (1 - tr); };
      var pvOps = 0;
      var fullYears = Math.floor(years);
      for (var t = 1; t <= fullYears; t++) {
        pvOps += afterTaxRent(t) / Math.pow(1 + r, t);
      }
      var rem = years - fullYears;
      if (rem > 0) {
        pvOps += (rem * afterTaxRent(years)) / Math.pow(1 + r, years);
      }
      var exitRate = laTransferRate(exitVal, jur) || 0;
      var exitCost = exitVal * (exitRate + brokerPct / 100);
      var exitGain = Math.max(0, exitVal - exitCost - basis);
      var exitTax = exitGain * tg;
      var netExitAT = exitVal - exitCost - debtExit - exitTax;
      var pvExit = netExitAT / Math.pow(1 + r, years);
      var downLoss = (rent * Math.pow(1 + g, years) * downMonths / 12 + carry * downMonths / 12) * (1 - tr);
      var pvDown = downLoss / Math.pow(1 + r, years);
      holdPv = pvOps + pvExit - pvDown;
      setOut("ws-out-hold", fmtUsd(holdPv), "After-tax PV of rent less interest (" + fmtUsd(pvOps) + ") + PV of exit net of costs, horizon debt and exit-gain tax (" + fmtUsd(pvExit) + ") − PV of after-tax re-leasing downtime (" + fmtUsd(pvDown) + ").");
    } else {
      setOut("ws-out-hold", "—", "Requires every hold input: rent, rent tax rate, interest, years, escalation, discount rate, exit value, horizon debt balance, gain rate, tax basis, closing cost % and downtime (enter 0 where none).");
    }

    if (netProceeds !== null && holdPv !== null) {
      var spread = holdPv - netProceeds;
      var verdict = spread >= 0 ? "Hold / Extend ahead by " + fmtUsd(spread) : "After-tax Sale ahead by " + fmtUsd(-spread);
      setOut("ws-out-spread", verdict, "Arithmetic on owner-entered assumptions only, not a recommendation. Verify lease options, credit, valuation and tax with your advisers.");
    } else {
      setOut("ws-out-spread", "—", "Complete both Sale and Hold inputs above to compare paths locally.");
    }
  }

  ws.querySelectorAll("input, select").forEach(function (field) {
    field.addEventListener("input", updateWorksheet);
    field.addEventListener("change", updateWorksheet);
  });
  var resetBtn = ws.querySelector("[data-ws-reset]");
  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      ws.querySelectorAll("input").forEach(function (inp) { inp.value = ""; });
      updateWorksheet();
    });
  }
  updateWorksheet();
})();
