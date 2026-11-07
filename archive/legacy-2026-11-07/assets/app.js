/* Shared UI: navigation, data loading, table rendering, counters. */
const NAV = [
  ["index.html", "Dashboard", "▦"],
  ["market.html", "Market & Demographics", "◔"],
  ["economy.html", "Economy & Prices", "◍"],
  ["schools.html", "Schools & Community", "✎"],
  ["tenant.html", "Tenant & Lease", "▣"],
  ["risk.html", "Risk Register", "⚠"],
  ["model.html", "Projection Model", "∑"],
  ["decision.html", "Decision & Recommendation", "★"],
  ["flagged.html", "Flagged for Review", "⚑"],
  ["sources.html", "Sources & Method", "≡"],
];

const STATUS_PILL = {
  verified: ['ok', 'Verified · official source'],
  derived: ['der', 'Derived · arithmetic on verified values'],
  unverified: ['unv', 'Unverified · value left blank'],
  placeholder: ['plc', 'Placeholder · private data withheld'],
};

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') n.className = v;
    else if (k === 'html') n.innerHTML = v;
    else n.setAttribute(k, v);
  }
  for (const k of kids) if (k != null) n.append(k.nodeType ? k : document.createTextNode(k));
  return n;
}

function shortUrl(u) {
  try {
    const x = new URL(u);
    return (x.hostname.replace(/^www\./, '') + x.pathname).replace(/\/$/, '');
  } catch { return u; }
}

function pill(status) {
  const [cls, label] = STATUS_PILL[status] || ['', status];
  const span = el('span', { class: 'pill ' + cls, title: label }, status);
  return span;
}

function buildNav() {
  const page = document.body.dataset.page || 'index.html';
  const list = el('ul'.replace('ul', 'ul'), { class: 'nav' });
  NAV.forEach(([href, label, ico]) => {
    const a = el('a', { href, class: href === page ? 'active' : '' },
      el('span', { class: 'ico', 'aria-hidden': 'true' }, ico), el('span', {}, label));
    list.append(el('li', {}, a));
  });
  const side = document.getElementById('sidebar');
  if (side) {
    side.innerHTML = `
      <div class="brand"><span class="dot"></span><b>Jack in the Box · NNN</b></div>
      <div class="brand-sub">Central Los Angeles</div>`;
    side.append(list);
    const foot = el('div', { class: 'side-foot' });
    foot.innerHTML = `<b>Decision window</b><br>Lease expiry 2030&ndash;2035<br>
      <b>Data cut</b><br>2026-11-06 (UTC)<br>
      <b>Property data</b><br>withheld / placeholder<br><br>
      <a href="sources.html">Methodology &amp; verification log →</a>`;
    side.append(foot);
  }
  const mnav = document.getElementById('mnav');
  if (mnav) {
    const clone = list.cloneNode(true);
    clone.className = 'nav';
    mnav.append(clone);
    const btn = document.getElementById('navbtn');
    if (btn) btn.addEventListener('click', () => mnav.classList.toggle('open'));
  }
}

let RECORDS = null, RISKS = null;

async function loadData() {
  if (RECORDS) return;
  const [a, b] = await Promise.all([
    fetch('data/records.json').then(r => r.json()),
    fetch('data/risks.json').then(r => r.json()),
  ]);
  RECORDS = a; RISKS = b;
}

function tableShell(title, count, note) {
  const wrap = el('div', { class: 'tablewrap' });
  const cap = el('div', { class: 'tablecap' });
  cap.append(el('div', { class: 't' }, title));
  const right = el('div', { class: 'c' });
  right.textContent = count + ' rows' + (note ? ' · ' + note : '');
  cap.append(right);
  wrap.append(cap);
  const scroll = el('div', { class: 'tscroll' });
  const table = el('table');
  table.innerHTML = `<thead><tr>
      <th>ID</th><th>Metric</th><th>Value</th><th>Unit</th><th>Period</th>
      <th>Geography</th><th>Status</th><th>Source (official)</th><th>Note</th>
    </tr></thead>`;
  const tb = el('tbody');
  table.append(tb);
  scroll.append(table);
  wrap.append(scroll);
  return { wrap, tb };
}

function rowHtml(r) {
  const tr = el('tr');
  tr.dataset.status = r.status;
  const val = (r.value === '' || r.value == null) ? '—' : r.value;
  const noteBits = [];
  if (r.note) noteBits.push(r.note);
  tr.innerHTML = `
    <td class="id">${r.id}</td>
    <td class="metric">${r.metric}</td>
    <td class="val">${val}</td>
    <td class="small">${r.unit || ''}</td>
    <td class="small">${r.period || ''}</td>
    <td class="small">${r.geography || ''}</td>
    <td></td>
    <td class="src"><a href="${r.url}" target="_blank" rel="noopener noreferrer"
        title="${(r.source || '').replace(/"/g, '&quot;')}">${shortUrl(r.url)} ↗</a>
        <div class="small" style="font-size:11px;margin-top:3px">${r.source || ''}</div></td>
    <td class="note">${noteBits.join(' ')}</td>`;
  tr.children[6].append(pill(r.status));
  return tr;
}

function renderTable(target, rows, title, note) {
  const { wrap, tb } = tableShell(title, rows.length, note);
  rows.forEach(r => tb.append(rowHtml(r)));
  target.append(wrap);
}

async function tableFor(selector, category) {
  const nodes = document.querySelectorAll(`[data-table="${selector}"]`);
  if (!nodes.length) return;
  await loadData();
  const rows = RECORDS.records.filter(r => r.category === category);
  nodes.forEach(n => renderTable(n, rows, category, n.dataset.note || ''));
}

async function stats() {
  await loadData();
  const c = { verified: 0, derived: 0, unverified: 0, placeholder: 0 };
  RECORDS.records.forEach(r => c[r.status]++);
  document.querySelectorAll('[data-stat]').forEach(n => {
    const k = n.dataset.stat;
    if (k in c) n.textContent = c[k];
    if (k === 'total') n.textContent = RECORDS.records.length;
    if (k === 'sources') n.textContent = new Set(RECORDS.records.map(r => r.source)).size;
    if (k === 'risks') n.textContent = RISKS.risks.length;
  });
}

async function flaggedTable() {
  const target = document.getElementById('flagged-table');
  if (!target) return;
  await loadData();
  const rows = RECORDS.records.filter(r => r.status === 'unverified' || r.status === 'placeholder');
  const tip = el('div', { class: 'small', style: 'margin:6px 0 0' },
    'These rows are published open, not filled. Every one requires a document or a lookup that was not available to this session.');
  target.before(tip);
  renderTable(target, rows, 'Open items — values deliberately left blank', 'sorted by status');
}

async function riskTable() {
  const target = document.getElementById('risk-table');
  if (!target) return;
  await loadData();
  const wrap = el('div', { class: 'tablewrap' });
  const cap = el('div', { class: 'tablecap' });
  cap.innerHTML = `<div class="t">Risk register — 16 events</div>
    <div class="c">${RISKS.risks.length} rows · probability &amp; impact are analyst assessments</div>`;
  wrap.append(cap);
  const scroll = el('div', { class: 'tscroll' });
  const t = el('table');
  t.innerHTML = `<thead><tr><th>ID</th><th>Category</th><th>Event</th><th>Type</th>
    <th>Probability</th><th>Impact</th><th>Exposure</th><th>Mitigation</th><th>Early-warning indicator</th><th>Factual basis</th></tr></thead>`;
  const tb = el('tbody');
  RISKS.risks.forEach(r => {
    const tr = el('tr');
    tr.innerHTML = `<td class="id">${r.id}</td>
      <td class="small" style="color:#fff">${r.category}</td>
      <td class="metric">${r.event}</td>
      <td><span class="pill ${r.type === 'black swan' ? 'sev' : ''}">${r.type}</span></td>
      <td class="small">${r.probability}<div class="small" style="font-size:10.5px">assessment</div></td>
      <td class="small">${r.impact}</td>
      <td class="note">${r.exposure}</td>
      <td class="note">${r.mitigation}</td>
      <td class="note">${r.indicator}</td>
      <td class="src"><a href="${r.basis_url}" target="_blank" rel="noopener noreferrer">${shortUrl(r.basis_url)} ↗</a>
        <div class="small" style="font-size:11px;margin-top:3px">${r.basis}</div></td>`;
    tb.append(tr);
  });
  t.append(tb); scroll.append(t); wrap.append(scroll);
  target.append(wrap);
}

async function sourceRegistry() {
  const target = document.getElementById('source-registry');
  if (!target) return;
  await loadData();
  const bySource = new Map();
  RECORDS.records.forEach(r => {
    if (!bySource.has(r.source)) bySource.set(r.source, { url: r.url, n: 0, ids: [] });
    const e = bySource.get(r.source); e.n++; e.ids.push(r.id);
  });
  const wrap = el('div', { class: 'tablewrap' });
  wrap.innerHTML = `<div class="tablecap"><div class="t">Source registry</div>
    <div class="c">${bySource.size} distinct official publications</div></div>`;
  const scroll = el('div', { class: 'tscroll' });
  const t = el('table');
  t.innerHTML = `<thead><tr><th>Publisher / publication</th><th>Link</th><th>Rows cited</th><th>Row IDs</th></tr></thead>`;
  const tb = el('tbody');
  [...bySource.entries()].sort((a, b) => b[1].n - a[1].n).forEach(([name, v]) => {
    const tr = el('tr');
    tr.innerHTML = `<td class="metric">${name}</td>
      <td class="src"><a href="${v.url}" target="_blank" rel="noopener noreferrer">${shortUrl(v.url)} ↗</a></td>
      <td class="val">${v.n}</td>
      <td class="small">${v.ids.join(', ')}</td>`;
    tb.append(tr);
  });
  t.append(tb); scroll.append(t); wrap.append(scroll);
  target.append(wrap);
}

function wireSearch() {
  const input = document.getElementById('tsearch');
  if (!input) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();
    document.querySelectorAll('tbody tr').forEach(tr => {
      tr.style.display = !q || tr.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  buildNav();
  try {
    await Promise.all([
      tableFor('demographics', 'Demographics'),
      tableFor('income', 'Income & Poverty'),
      tableFor('housing', 'Housing'),
      tableFor('economy', 'Economy & Jobs'),
      tableFor('prices', 'Prices'),
      tableFor('population', 'Population Outlook'),
      tableFor('schools', 'Schools'),
      tableFor('tenant', 'Tenant'),
      tableFor('property', 'Property & Lease'),
      tableFor('taxreg', 'Tax & Regulation'),
      tableFor('catastrophe', 'Catastrophe'),
      tableFor('capital', 'Capital Markets'),
      stats(), flaggedTable(), riskTable(), sourceRegistry(),
    ]);
  } catch (e) {
    console.error(e);
    document.querySelectorAll('[data-table]').forEach(n => {
      n.innerHTML = '<div class="callout bad"><div class="h">Data file not reachable</div><p>Open the site through GitHub Pages or a local web server; <code>fetch()</code> of <code>data/records.json</code> does not work from <code>file://</code>.</p></div>';
    });
  }
  wireSearch();
});
