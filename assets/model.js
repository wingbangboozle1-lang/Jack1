/* Projection engine.
   UNIT OF ACCOUNT: one year of current base rent (R0 = 1.00).
   No property-specific dollar amount is invented anywhere in this model. */

const DEFAULTS = {
  r: 7.90,          // discount rate = 4.90% verified 10y UST + 3.00% assumption
  g: 2.00,          // contractual rent escalation
  n: 6.0,           // years to expiry (midpoint of the 2030-2035 window from 2026)
  capNow: 7.00,     // exit cap if sold today with ~6 years of term (assumption)
  capRenewed: 6.00, // exit cap with a fresh long lease (assumption)
  saleCost: 6.00,   // ULA 4.0% verified + ~2.0% assumption for title/advisory
  prob: 0.55,       // probability the tenant renews at expiry (assumption)
  dark: 8.0,        // vacant / alternative-use value in multiples of annual rent (assumption)
  capImprove: 0.50, // bp improvement from early renewal -> long remaining term
  probBoost: 0.20,  // added renewal certainty from early renewal
  concession: 0.00, // rent concession given at early renewal, % of rent
};

function compute(p) {
  const r = p.r / 100, g = p.g / 100, s = p.saleCost / 100;
  const capNow = p.capNow / 100, capRen = p.capRenewed / 100;
  const n = p.n;

  // A — sell now, lease in place, ~6 years of term left
  const A = (1 / capNow) * (1 - s);

  // PV of contractual rent to expiry
  let pvRent = 0;
  for (let t = 1; t <= Math.floor(n); t++) pvRent += Math.pow(1 + g, t - 1) / Math.pow(1 + r, t);
  const frac = n - Math.floor(n);
  if (frac > 0) pvRent += frac * Math.pow(1 + g, n - 1) / Math.pow(1 + r, n);

  const Rn = Math.pow(1 + g, n);
  const dfN = 1 / Math.pow(1 + r, n);

  // B — hold to expiry, then renew-or-vacate, then sell
  const termB = ((1 - p.prob) * p.dark + p.prob * (Rn / capRen)) * (1 - s);
  const B = pvRent + termB * dfN;

  // C — renew early (long term locked in), then sell in year n
  const capC = Math.max(0.02, capRen - p.capImprove / 100);
  const pC = Math.min(0.95, p.prob + p.probBoost);
  const rentAdj = (1 - p.concession / 100);
  let pvRentC = 0;
  for (let t = 1; t <= Math.floor(n); t++) {
    const rr = t <= 2 ? 1 : rentAdj;
    pvRentC += rr * Math.pow(1 + g, t - 1) / Math.pow(1 + r, t);
  }
  const termC = ((1 - pC) * p.dark + pC * (Rn * rentAdj / capC)) * (1 - s);
  const C = pvRentC + termC * dfN;

  // break-even renewal probability at which B == A
  const K = ((A - pvRent) / (1 - s)) / dfN;
  const denom = (Rn / capRen - p.dark);
  const pStar = denom !== 0 ? (K - p.dark) / denom : NaN;

  return { A, B, C, pvRent, pStar, capC, pC, Rn };
}

function fmt(x) { return x.toFixed(2); }

function renderModel() {
  const host = document.getElementById('model-app');
  if (!host) return;
  const p = { ...DEFAULTS };

  const ctrls = [
    ['capNow', 'Exit cap if sold now', '%', 4.0, 10.0, 0.25, 'Short remaining term → wider cap (assumption)'],
    ['capRenewed', 'Exit cap with fresh long lease', '%', 3.5, 9.0, 0.25, 'Credit-tenant QSR pricing (assumption, U-06)'],
    ['prob', 'P(tenant renews at expiry)', '', 0.0, 1.0, 0.05, 'Offered by tenant trajectory (assessment)'],
    ['dark', 'Vacant / alternative-use value', '× rent', 2, 16, 0.5, 'Land + building value if the unit goes dark'],
    ['saleCost', 'Sale cost', '% of price', 2, 10, 0.25, 'ULA 4.0% verified + ~2% assumption'],
    ['g', 'Rent escalation', '%/yr', 0, 5, 0.25, 'Contractual bumps'],
    ['r', 'Discount rate', '%', 5, 12, 0.25, '4.90% UST (verified) + 3.00% (assumption)'],
    ['concession', 'Concession given at early renewal', '% of rent', 0, 15, 0.5, 'Cost of buying the term'],
  ];

  host.innerHTML = `
    <div class="ctrls" id="ctrls"></div>
    <div class="out" id="out"></div>
    <p class="small" style="margin-top:10px">All figures are <b>multiples of one year of current base rent</b>.
    Multiply by the actual annual base rent to get dollars. Assumptions are adjustable and are never presented as measured facts.</p>
    <div id="sensitivity" style="margin-top:18px"></div>`;

  const clamp = document.getElementById('ctrls');
  ctrls.forEach(([key, label, unit, min, max, step, hint]) => {
    const d = document.createElement('div');
    d.className = 'ctrl';
    d.innerHTML = `<label><span>${label}</span><b id="v-${key}"></b></label>
      <input type="range" id="i-${key}" min="${min}" max="${max}" step="${step}" value="${p[key]}">
      <div class="hint">${hint}</div>`;
    clamp.append(d);
  });

  function refresh() {
    ctrls.forEach(([key]) => {
      document.getElementById('v-' + key).textContent =
        (key === 'prob' ? (p[key] * 100).toFixed(0) + '%' : p[key].toFixed(key === 'dark' ? 1 : 2));
    });
    const o = compute(p);
    const best = Math.max(o.A, o.B, o.C);
    document.getElementById('out').innerHTML = `
      <div class="outcard ${o.A === best ? 'win' : ''}">
        <div class="lbl">A · Sell now (2027)</div>
        <div class="big">${fmt(o.A)}×</div>
        <div class="sub">Net proceeds per $1 of annual rent, after ${p.saleCost}% exit cost.</div>
      </div>
      <div class="outcard ${o.B === best ? 'win' : ''}">
        <div class="lbl">B · Hold to expiry, then renew or re-lease</div>
        <div class="big">${fmt(o.B)}×</div>
        <div class="sub">PV of rent to expiry (${fmt(o.pvRent)}×) + PV of the expected exit.</div>
      </div>
      <div class="outcard ${o.C === best ? 'win' : ''}">
        <div class="lbl">C · Renew early (2028), sell in ${(2026 + p.n).toFixed(0)}</div>
        <div class="big">${fmt(o.C)}×</div>
        <div class="sub">Locks ${(o.pC * 100).toFixed(0)}% renewal certainty and a ${(o.capC * 100).toFixed(2)}% exit cap.</div>
      </div>`;

    const star = o.pStar;
    document.getElementById('sensitivity').innerHTML = `
      <div class="callout ${isFinite(star) && star > p.prob ? 'warn' : 'ok'}">
        <div class="h">Break-even (holds the decision together)</div>
        <p>Holding to expiry beats selling now only if the tenant renews with probability above
        <b>${isFinite(star) ? (star * 100).toFixed(1) + '%' : 'n/a'}</b>.
        The model currently assumes <b>${(p.prob * 100).toFixed(0)}%</b>.
        ${isFinite(star) && star > p.prob
          ? '→ Under these assumptions, holding is <b>not</b> justified by the expected value: sell or lock the renewal.'
          : '→ Under these assumptions, holding clears the bar, but by a margin you should insist on verifying.'}</p>
      </div>
      ${grid(o, p)}`;
  }

  function grid(o, p) {
    const caps = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0];
    const probs = [0.2, 0.4, 0.55, 0.7, 0.85, 1.0];
    let html = `<div class="tablewrap"><div class="tablecap"><div class="t">Hold-to-expiry minus sell-now (B − A)</div>
      <div class="c">green = holding wins · red = selling wins</div></div><div class="tscroll"><table>
      <thead><tr><th>Exit cap with new lease ↓ / P(renewal) →</th>${probs.map(x => `<th>${(x * 100).toFixed(0)}%</th>`).join('')}</tr></thead><tbody>`;
    caps.forEach(c => {
      html += `<tr><td class="metric">${c.toFixed(2)}%</td>`;
      probs.forEach(pr => {
        const t = compute({ ...p, capRenewed: c, prob: pr });
        const d = t.B - t.A;
        const col = d >= 0 ? '#3ddc97' : '#ff7676';
        html += `<td class="val" style="color:${col}">${d >= 0 ? '+' : ''}${d.toFixed(2)}×</td>`;
      });
      html += `</tr>`;
    });
    html += `</tbody></table></div></div>`;
    return html;
  }

  ctrls.forEach(([key]) => {
    document.getElementById('i-' + key).addEventListener('input', e => {
      p[key] = parseFloat(e.target.value);
      refresh();
    });
  });
  refresh();
}

document.addEventListener('DOMContentLoaded', renderModel);
