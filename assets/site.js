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

  function updateWorksheet() {
    var price = num("ws-sale-price");
    var debt = num("ws-debt");
    var brokerPct = num("ws-broker-pct");
    var basis = num("ws-tax-basis");
    var taxPct = num("ws-tax-rate");
    var rent = num("ws-rent");
    var years = num("ws-years");
    var escPct = num("ws-esc");
    var discPct = num("ws-discount");
    var exitVal = num("ws-exit-val");
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
        setOut("ws-out-sale", fmtUsd(netProceeds), "1031 deferred tax assumed $0 (subject to 45/180-day Form 8824 & zero boot); after debt & " + fmtUsd(closingCost) + " closing/DTT.");
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
    if (rent !== null && years !== null && years > 0 && escPct !== null && discPct !== null && exitVal !== null && debt !== null) {
      var r = discPct / 100;
      var g = escPct / 100;
      var pvRent = 0;
      var fullYears = Math.floor(years);
      for (var t = 1; t <= fullYears; t++) {
        pvRent += (rent * Math.pow(1 + g, t - 1)) / Math.pow(1 + r, t);
      }
      var rem = years - fullYears;
      if (rem > 0) {
        pvRent += (rem * rent * Math.pow(1 + g, years - 1)) / Math.pow(1 + r, years);
      }
      var exitRate = laTransferRate(exitVal, jur);
      var exitCost = exitVal * ((exitRate || 0) + ((brokerPct || 0) / 100));
      var netExit = exitVal - exitCost - debt;
      var pvExit = netExit / Math.pow(1 + r, years);
      holdPv = pvRent + pvExit;
      setOut("ws-out-hold", fmtUsd(holdPv), "PV of rent (" + fmtUsd(pvRent) + ") + PV of net exit after debt & exit transfer/closing (" + fmtUsd(pvExit) + ").");
    } else {
      setOut("ws-out-hold", "—", "Requires annual NNN rent, remaining years, escalation %, discount rate %, exit value, and debt.");
    }

    if (netProceeds !== null && holdPv !== null) {
      var spread = holdPv - netProceeds;
      var verdict = spread >= 0 ? "Hold / Extend ahead by " + fmtUsd(spread) : "After-tax Sale ahead by " + fmtUsd(-spread);
      setOut("ws-out-spread", verdict, "Sensitivity check on owner-entered assumptions only; verify lease options, credit, and tax advice.");
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
