/* Projection model — illustrative scenario engine for the NNN lease decision.
   Defaults are clearly-marked EXAMPLES, not this property's actual figures
   (never provided to this analysis). Formulas documented on projections.html. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };

  function fmt(n) { return '$' + Math.round(n).toLocaleString(); }
  function fmtM(n) { return (n < 0 ? '-$' : '$') + (Math.abs(n) / 1e6).toFixed(2) + 'M'; }
  function pct(n) { return (n * 100).toFixed(2) + '%'; }

  // Illustrative WALT penalty (basis points added to base cap rate as term decays).
  function waltPenaltyBps(yearsLeft) {
    if (yearsLeft > 7) return 0;
    if (yearsLeft > 5) return 25;
    if (yearsLeft > 3) return 50;
    if (yearsLeft > 2) return 75;
    if (yearsLeft > 1) return 100;
    return 150;
  }

  function model() {
    var NOI0 = Math.max(0, parseFloat($('rent').value) || 0);
    var esc = (parseFloat($('escalation').value) || 0) / 100;
    var expiryYear = parseInt($('expiryYear').value, 10);
    var capBase = (parseFloat($('capRate').value) || 6.55) / 100;
    var disc = (parseFloat($('discountRate').value) || 8) / 100;
    var rentReset = (parseFloat($('rentReset').value) || 0) / 100;
    var renewProb = (parseFloat($('renewProb').value) || 60) / 100;
    var vacMonths = Math.max(0, parseFloat($('vacMonths').value) || 0);
    var reTenantCost = Math.max(0, parseFloat($('reTenantCost').value) || 0);
    var sellCost = (parseFloat($('sellCost').value) || 2) / 100;
    var now = 2026;
    var yearsToExpiry = Math.max(1, expiryYear - now);

    // --- Value now ---
    var valueNow = capBase > 0 ? NOI0 / capBase : 0;

    // --- Value path (WALT-adjusted cap rate) ---
    var rows = [];
    for (var y = now; y <= expiryYear; y++) {
      var t = y - now;
      var noi = NOI0 * Math.pow(1 + esc, t);
      var yearsLeft = Math.max(0, expiryYear - y);
      var cap = capBase + waltPenaltyBps(yearsLeft) / 10000;
      rows.push({ year: y, noi: noi, yearsLeft: yearsLeft, cap: cap, value: cap > 0 ? noi / cap : 0 });
    }
    var noiAtExpiry = NOI0 * Math.pow(1 + esc, yearsToExpiry);
    var valueAtExpiryPath = rows.length ? rows[rows.length - 1].value : 0;
    var valueAtExpiryClean = capBase > 0 ? noiAtExpiry / capBase : 0;

    // --- PV of rent stream to expiry ---
    var pvRents = 0;
    for (var y2 = now; y2 < expiryYear; y2++) {
      pvRents += (NOI0 * Math.pow(1 + esc, y2 - now)) / Math.pow(1 + disc, y2 - now + 1);
    }
    var pvFactor = Math.pow(1 + disc, yearsToExpiry);

    // Renewal branch: reset rent (rentReset), 10 more years, base cap unchanged.
    var noiRenew = noiAtExpiry * (1 + rentReset);
    var valueRenew = capBase > 0 ? noiRenew / capBase : 0;

    // Vacate/re-lease branch: flat re-tenanting at current escalated rent, less vacancy + TI/LC costs.
    var noiReLease = noiAtExpiry;
    var valueReLease = capBase > 0 ? noiReLease / capBase : 0;
    var vacLoss = noiAtExpiry * (vacMonths / 12);
    var netReLease = valueReLease - vacLoss - reTenantCost;

    // Scenarios (NPV today)
    var A_sellNow = valueNow * (1 - sellCost);
    var B_renewOnly = pvRents + valueRenew / pvFactor;
    var C_vacateOnly = pvRents + netReLease / pvFactor;
    var HOLD_weighted = pvRents + (renewProb * valueRenew + (1 - renewProb) * netReLease) / pvFactor;

    // --- Render ---
    $('outValueNow').textContent = fmtM(valueNow);
    $('outValueAtExpiry').textContent = fmtM(valueAtExpiryClean);
    $('outPathValueAtExpiry').textContent = fmtM(valueAtExpiryPath);
    $('outNoiAtExpiry').textContent = fmt(noiAtExpiry);
    $('outSellNow').textContent = fmtM(A_sellNow);
    $('outHoldRenew').textContent = fmtM(B_renewOnly);
    $('outHoldVacate').textContent = fmtM(C_vacateOnly);
    $('outHoldWeighted').textContent = fmtM(HOLD_weighted);

    var contenders = [A_sellNow, HOLD_weighted];
    var labels = ['Sell now', 'Hold (probability-weighted)'];
    var bestIdx = contenders[0] >= contenders[1] ? 0 : 1;
    $('outBest').textContent = labels[bestIdx];

    // Break-even renewal probability where HOLD NPV == SELL NPV (analytic).
    var denom = valueRenew - netReLease;
    var pStar = Math.abs(denom) > 1e-9 ? (A_sellNow * pvFactor - pvRents * pvFactor - netReLease) / denom : NaN;
    var elBE = $('outBreakEven');
    if (elBE) {
      if (isFinite(pStar)) {
        pStar = Math.max(0, Math.min(1, pStar));
        elBE.textContent = (pStar * 100).toFixed(1) + '%';
      } else {
        elBE.textContent = 'n/a';
      }
    }

    var tbody = '';
    rows.forEach(function (r, i) {
      tbody += '<tr><td>' + r.year + '</td><td>' + fmt(r.noi) + '</td><td>' + r.yearsLeft + ' yrs</td><td>' + pct(r.cap) + ' (+' + waltPenaltyBps(r.yearsLeft) + ' bps)</td><td>' + fmtM(r.value) + '</td></tr>';
    });
    $('pathRows').innerHTML = tbody;

    var noiRange = [0.75, 0.9, 1.0, 1.1, 1.25].map(function (m) { return NOI0 * m; });
    var capRange = [5.75, 6.25, 6.55, 7.00, 7.50].map(function (c) { return c / 100; });
    $('matrixHead').innerHTML = '<tr><th>NOI ↓ / Cap →</th>' + capRange.map(function (c) { return '<th>' + pct(c) + '</th>'; }).join('') + '</tr>';
    $('matrixRows').innerHTML = noiRange.map(function (n) {
      return '<tr><td>' + fmt(n) + '</td>' + capRange.map(function (c) { return '<td>' + fmtM(n / c) + '</td>'; }).join('') + '</tr>';
    }).join('');
  }

  ['rent', 'escalation', 'expiryYear', 'capRate', 'discountRate', 'rentReset', 'renewProb', 'vacMonths', 'reTenantCost', 'sellCost'].forEach(function (id) {
    var el = $(id); if (el) { el.addEventListener('input', model); el.addEventListener('change', model); }
  });
  if (document.getElementById('projector')) model();
})();
