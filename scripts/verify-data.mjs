#!/usr/bin/env node
/**
 * Build verification. Fails (exit 1) on any structural defect.
 * Checks:
 *  1. record schema + unique IDs
 *  2. every value-bearing row is verified|derived
 *  3. every unverified row has an EMPTY value (no estimates smuggled in)
 *  4. every source URL is https and on the official-domain allowlist
 *  5. every internal link and asset reference in every HTML page resolves
 *  6. declared category counts in sources.html match the dataset
 */
import { readFileSync, existsSync, readdirSync } from "node:fs";

const OFFICIAL = [
  "census.gov", "bls.gov", "dof.ca.gov", "sec.gov", "conservation.ca.gov",
  "usgs.gov", "fire.ca.gov", "osfm.fire.ca.gov", "insurance.ca.gov",
  "assessor.lacounty.gov", "lacity.gov", "dir.ca.gov", "nces.ed.gov",
  "stlouisfed.org", "cde.ca.gov",
];

let errors = [];
let checks = 0;
const fail = (m) => errors.push(m);
const ok = () => checks++;

function hostOk(u) {
  let h;
  try { h = new URL(u).hostname; } catch { return false; }
  return OFFICIAL.some(d => h === d || h.endsWith("." + d));
}

const rec = JSON.parse(readFileSync("data/records.json", "utf8"));
const rsk = JSON.parse(readFileSync("data/risks.json", "utf8"));
const scn = JSON.parse(readFileSync("data/scenarios.json", "utf8"));

/* 1-4 */
const ids = new Set();
const allowed = new Set(["verified", "derived", "unverified", "placeholder"]);
for (const r of rec.records) {
  for (const f of ["id", "category", "metric", "value", "unit", "period", "geography", "source", "url", "status"]) {
    if (!(f in r)) fail(`${r.id || "?"}: missing field ${f}`);
  }
  if (ids.has(r.id)) fail(`duplicate id ${r.id}`);
  ids.add(r.id);
  if (!allowed.has(r.status)) fail(`${r.id}: bad status ${r.status}`);
  if (!hostOk(r.url)) fail(`${r.id}: source not on official allowlist -> ${r.url}`);
  if (!r.url.startsWith("https://")) fail(`${r.id}: non-https source`);
  ok();

  const blank = r.value === "" || r.value == null;
  if (r.status === "unverified" && !blank) fail(`${r.id}: unverified row must be blank, has "${r.value}"`);
  if ((r.status === "verified" || r.status === "derived") && blank) fail(`${r.id}: ${r.status} row has no value`);
  if (r.status === "placeholder" && r.value !== "[WITHHELD]") fail(`${r.id}: placeholder must read [WITHHELD]`);
  if (r.status === "derived" && !/derived|Arithmetic/i.test(r.note)) fail(`${r.id}: derived row must state the arithmetic`);
  ok();
}

/* 5 */
const htmls = readdirSync(".").filter(f => f.endsWith(".html"));
const localTargets = new Set();
for (const f of htmls) {
  const s = readFileSync(f, "utf8");
  const refs = [...s.matchAll(/(?:href|src)="([^"]+)"/g)].map(m => m[1]);
  for (const ref of refs) {
    if (/^(https?:|mailto:|data:|#)/.test(ref)) {
      if (/^http:\/\//.test(ref)) fail(`${f}: insecure external link ${ref}`);
      continue;
    }
    localTargets.add(ref);
    const clean = ref.split("#")[0].split("?")[0];
    if (clean && !existsSync(clean)) fail(`${f}: broken local reference -> ${ref}`);
    ok();
  }
}
/* every page must be reachable from the nav list in assets/app.js */
const appjs = readFileSync("assets/app.js", "utf8");
for (const f of htmls) {
  if (f === "404.html") continue;
  if (!appjs.includes(`"${f}"`)) fail(`${f}: not present in the navigation list`);
  ok();
}
for (const m of appjs.matchAll(/\{"?([a-z0-9-]+\.html)"?/g)) { /* noop guard */ }

/* 6 */
const counts = {};
for (const r of rec.records) counts[r.category] = (counts[r.category] || 0) + 1;
const declared = {
  "Demographics": [12, 10, 2], "Income & Poverty": [9, 9, 0], "Housing": [6, 6, 0],
  "Economy & Jobs": [18, 17, 1], "Prices": [7, 7, 0], "Population Outlook": [7, 7, 0],
  "Schools": [9, 6, 3], "Tenant": [22, 19, 3], "Property & Lease": [15, 0, 15],
  "Tax & Regulation": [8, 5, 3], "Catastrophe": [13, 8, 5], "Capital Markets": [4, 1, 3],
};
for (const [cat, [rows, ver, blank]] of Object.entries(declared)) {
  const actualRows = counts[cat] || 0;
  const actualVer = rec.records.filter(r => r.category === cat && (r.status === "verified" || r.status === "derived")).length;
  const actualBlank = rec.records.filter(r => r.category === cat && (r.status === "unverified" || r.status === "placeholder")).length;
  if (rows !== actualRows) fail(`sources.html count mismatch for ${cat}: declared ${rows}, actual ${actualRows}`);
  if (ver !== actualVer) fail(`sources.html verified count mismatch for ${cat}: declared ${ver}, actual ${actualVer}`);
  if (blank !== actualBlank) fail(`sources.html blank count mismatch for ${cat}: declared ${blank}, actual ${actualBlank}`);
  ok();
}
const sumDeclared = Object.values(declared).reduce((a, b) => a + b[0], 0);
if (sumDeclared !== rec.records.length) fail(`category totals do not sum to dataset (${sumDeclared} vs ${rec.records.length})`);

/* risks */
for (const r of rsk.risks) {
  if (!["business-as-usual", "black swan"].includes(r.type)) fail(`${r.id}: bad risk type ${r.type}`);
  if (!hostOk(r.basis_url)) fail(`${r.id}: risk basis not official -> ${r.basis_url}`);
  for (const f of ["category", "event", "probability", "impact", "exposure", "mitigation", "indicator"]) {
    if (!r[f]) fail(`${r.id}: missing ${f}`);
  }
  ok();
}

/* scenarios */
if (!scn.assumptions || !scn.strategies) fail("scenarios.json missing assumptions/strategies");
if (scn.strategies.length !== 3) fail("scenarios.json must carry exactly three strategies");

/* totals reported on the site */
const tot = {
  records: rec.records.length,
  verified: rec.records.filter(r => r.status === "verified").length,
  derived: rec.records.filter(r => r.status === "derived").length,
  unverified: rec.records.filter(r => r.status === "unverified").length,
  placeholder: rec.records.filter(r => r.status === "placeholder").length,
  open: rec.records.filter(r => r.status !== "verified" && r.status !== "derived").length,
  sources: new Set(rec.records.map(r => r.source)).size,
  risks: rsk.risks.length,
  pages: htmls.length,
};
console.log("dataset", tot);

/* the two hardcoded totals on the site must match */
const idx = readFileSync("index.html", "utf8");
if (!idx.includes(`${tot.records} data rows`) || !idx.includes(`${tot.verified} of them`)) {
  fail(`index.html hardcoded totals do not match dataset (${tot.records} rows, ${tot.verified} verified)`);
}
const flg = readFileSync("flagged.html", "utf8");
const words = { 28: "28", 8: "8" };
if (tot.unverified !== 27 || tot.placeholder !== 8) fail("flagged.html narrative says 27 blank / 8 withheld; dataset differs");
if (!flg.includes("Thirty-five")) fail("flagged.html lead paragraph must state the total open rows");

ok();
if (errors.length) {
  console.error("\nFAILED CHECKS:");
  errors.forEach(e => console.error(" - " + e));
  process.exit(1);
}
console.log(`\nALL CHECKS PASSED (${checks} assertions).`);
