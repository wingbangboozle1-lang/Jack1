/* After-tax sale module (session 4c386ad4, 2026-11-15).
 *
 * Runs entirely in the reader's browser. No fetch, no XHR, no storage, no cookies, no
 * network calls. Inputs live only in the page's memory and are cleared on reload.
 * Rule constants are read from the inline JSON block generated from
 * data/k-4c386ad4-supplement.json; nothing is hard-coded here except the arithmetic.
 *
 * compute(inputs, rules) is pure and is also exported for the Node-based unit test.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.AfterTax = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var STATUSES = ["single", "mfj", "hoh", "mfs"];
  var JURISDICTIONS = ["la_city", "county_only"];
  var NUMERIC_FIELDS = [
    ["price", "Sale price (consideration)"],
    ["sellingCosts", "Selling costs excluding transfer tax"],
    ["debt", "Debt payoff and prepayment charges"],
    ["adjustedBasis", "Federal adjusted basis at sale"],
    ["unrecapturedGain", "Unrecaptured section 1250 gain (from CPA)"],
    ["fedTaxableIncomeBefore", "Federal taxable income before the sale"],
    ["magiBefore", "Federal modified AGI before the sale"],
    ["otherNii", "Other net investment income (included in MAGI)"],
    ["caTaxableIncomeBefore", "California taxable income before the sale"]
  ];

  function isNum(v) {
    return typeof v === "number" && isFinite(v);
  }

  function cents(x) {
    return Math.round(x * 100) / 100;
  }

  // Schedule lookup. Each row is [lower, upper|null, base, rate]; tax = base + rate * (TI - lower).
  function caTax(schedule, ti) {
    if (ti <= 0) return 0;
    for (var i = 0; i < schedule.length; i++) {
      var row = schedule[i];
      var lower = row[0], upper = row[1], base = row[2], rate = row[3];
      if (ti > lower && (upper === null || ti <= upper)) {
        return base + rate * (ti - lower);
      }
    }
    return 0;
  }

  function bhst(rules, ti) {
    var over = ti - rules.ca_bhst.threshold;
    return over > 0 ? rules.ca_bhst.rate * over : 0;
  }

  function transferTax(price, jurisdiction, sellerPays, rules) {
    var out = { county: 0, city: 0, ula: 0, total: 0 };
    if (!sellerPays || !(price > rules.dtt.min_taxable_value)) return out;
    if (jurisdiction === "la_city") {
      out.county = price * rules.dtt.la_city_county_full_rate;
      out.city = Math.ceil(price / 500) * rules.dtt.city_base_per_500;
      if (price >= rules.dtt.ula_upper_threshold) {
        out.ula = price * rules.dtt.ula_top_rate;
      } else if (price > rules.dtt.ula_lower_threshold) {
        out.ula = price * rules.dtt.ula_mid_rate;
      }
    } else {
      out.county = Math.ceil(price / 500) * rules.dtt.county_per_500;
    }
    out.county = cents(out.county);
    out.city = cents(out.city);
    out.ula = cents(out.ula);
    out.total = cents(out.county + out.city + out.ula);
    return out;
  }

  // Returns { missing: [labels], errors: [strings], result: {...} | null }.
  function compute(inp, rules) {
    var missing = [];
    var errors = [];

    NUMERIC_FIELDS.forEach(function (f) {
      var v = inp[f[0]];
      if (v === null || v === undefined || v === "") {
        missing.push(f[1]);
      } else if (!isNum(v) || v < 0) {
        errors.push(f[1] + " must be a number of zero or more.");
      }
    });
    if (STATUSES.indexOf(inp.status) === -1) missing.push("Filing status");
    if (JURISDICTIONS.indexOf(inp.jurisdiction) === -1) missing.push("Jurisdiction");
    if (inp.sellerPaysTransfer !== "yes" && inp.sellerPaysTransfer !== "no") missing.push("Who pays the transfer tax");
    if (inp.heldMoreThanOneYear === "no") {
      errors.push("Short-term holding is not modeled here: short-term gain is taxed at ordinary rates, which need the full bracket table.");
    } else if (inp.heldMoreThanOneYear !== "yes") {
      missing.push("Held more than one year?");
    }
    if (inp.caGain !== null && inp.caGain !== undefined && inp.caGain !== "" && (!isNum(inp.caGain) || inp.caGain < 0)) {
      errors.push("California gain, if entered, must be a number of zero or more.");
    }
    if (missing.length || errors.length) {
      return { missing: missing, errors: errors, result: null };
    }

    var s = inp.status;
    var price = inp.price;
    var fed = rules.federal_ltcg_2026;
    var niitRules = rules.niit;

    var tt = transferTax(price, inp.jurisdiction, inp.sellerPaysTransfer === "yes", rules);
    var sellingCosts = inp.sellingCosts;
    var amountRealized = price - sellingCosts - tt.total;
    var gain = amountRealized - inp.adjustedBasis;
    var gainPos = gain > 0 ? gain : 0;
    var unrec = Math.min(inp.unrecapturedGain, gainPos);
    var ltcg = gainPos - unrec;

    // Federal: unrecaptured section 1250 at the 25% statutory maximum (upper bound), placed below the
    // long-term gain in the stacking; long-term gain is layered over taxable income plus that amount.
    var base0 = inp.fedTaxableIncomeBefore + unrec;
    var zeroMax = fed.zero_rate_max[s];
    var fifteenMax = fed.fifteen_rate_max[s];
    var inZero = Math.min(ltcg, Math.max(0, zeroMax - base0));
    var capMid = Math.max(0, fifteenMax - Math.max(base0, zeroMax));
    var inMid = Math.min(ltcg - inZero, capMid);
    var inTop = ltcg - inZero - inMid;
    var fedUnrecTax = fed.unrecaptured_1250_max_rate * unrec;
    var fedLtcgTax = fed.mid_ltcg_rate * inMid + fed.top_ltcg_rate * inTop;
    var fedTax = cents(fedUnrecTax + fedLtcgTax);

    // NIIT, incremental to the sale: tax with the gain minus tax without it.
    var thr = niitRules.threshold[s];
    var niitWith = Math.min(inp.otherNii + gainPos, Math.max(0, inp.magiBefore + gainPos - thr));
    var niitWithout = Math.min(inp.otherNii, Math.max(0, inp.magiBefore - thr));
    var niit = cents(niitRules.rate * (niitWith - niitWithout));

    // California: gain taxed as ordinary income on the CA schedule for the status, incremental.
    var caG = (inp.caGain !== null && inp.caGain !== undefined && inp.caGain !== "") ? inp.caGain : gainPos;
    var sched = rules.ca_schedules_2025[rules.ca_schedules_2025.schedule_for_status[s]];
    var caBefore = inp.caTaxableIncomeBefore;
    var caIncr = caTax(sched, caBefore + caG) - caTax(sched, caBefore) +
                 bhst(rules, caBefore + caG) - bhst(rules, caBefore);
    var caGainTax = cents(caIncr);

    var totalIncomeTax = cents(fedTax + niit + caGainTax);
    var preTaxNet = price - sellingCosts - tt.total - inp.debt;
    var afterTaxNet = cents(preTaxNet - totalIncomeTax);

    var result = {
      transferTax: tt,
      sellerPaysTransfer: inp.sellerPaysTransfer === "yes",
      amountRealized: cents(amountRealized),
      adjustedBasis: cents(inp.adjustedBasis),
      gain: cents(gainPos),
      unrecaptured: cents(unrec),
      longTermGain: cents(ltcg),
      fedUnrecaptured25Tax: cents(fedUnrecTax),
      fedLongTermTax: cents(fedLtcgTax),
      fedLongTermBandSplit: { zero: cents(inZero), fifteen: cents(inMid), twenty: cents(inTop) },
      fedTax: fedTax,
      niit: niit,
      caGainTax: caGainTax,
      totalIncomeTax: totalIncomeTax,
      effectiveTaxOnGain: gainPos > 0 ? totalIncomeTax / gainPos : 0,
      preTaxNetEquity: cents(preTaxNet),
      afterTaxNetProceeds: afterTaxNet,
      negativeNet: afterTaxNet < 0
    };
    return { missing: [], errors: [], result: result };
  }

  return { compute: compute, transferTax: transferTax, caTax: caTax, bhst: bhst };
});
