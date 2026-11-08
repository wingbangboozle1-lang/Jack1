#!/usr/bin/env node
/**
 * RETIRED legacy gate — superseded 2026-11-08 (T11, session arena/14c28bc9-jack1).
 *
 * History: this script asserted the pre-PR-#12 data-driven architecture
 * (130-row `data/records.json` dataset rendered into the old root pages).
 * The canonical public dashboard is now the eight-page site validated by
 * `scripts/validate_site.py` (see README.md, "GitHub Pages deployment"), and
 * the old assertions fail against that site by design drift — not because of
 * a data defect. Example failures this stub replaces: hard-coded totals on
 * the old index.html, old-nav expectations for risks.html/property.html, and
 * the old 130-row / 92-verified hard-coded totals.
 *
 * This wrapper keeps `node scripts/verify-data.mjs` green by delegating to
 * the canonical validator. It performs no independent assertions of its own.
 * For the retired dataset checks see git history (file as of commit 6d8c78a).
 */
import { spawnSync } from "node:child_process";

console.log("scripts/verify-data.mjs is retired and superseded by scripts/validate_site.py.");
console.log("Delegating to the canonical validator now...\n");

const result = spawnSync("python3", ["scripts/validate_site.py"], { stdio: "inherit" });
if (result.error) {
  console.error("Failed to launch python3:", result.error.message);
  process.exit(1);
}
process.exit(result.status ?? 1);
