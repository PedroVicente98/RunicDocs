// Quartz's graph plugin (commit c54226d) works out the current page from location.pathname without decoding it.
// For a page whose name has a non-ASCII character, such as the "—" in "RunicGame — Ideias", the address holds
// "%E2%80%94", the graph doesn't find the page and draws one unknown dot. @quartz-community/utils fixed this later
// (d16d8d9, "decode URI in getFullSlugFromUrl for non-ASCII slugs"), but no graph commit that works with
// Quartz 5.0.0 includes it, so this applies the same one-word fix to the built plugin. Safe to run again.
//
//   node quartz-patches/decode-graph-slug.mjs .quartz/.quartz/plugins/graph/dist
import fs from "node:fs";
import path from "node:path";

const dir = path.resolve(process.argv[2] ?? ".quartz/plugins/graph/dist");
// the minified getFullSlugFromUrl(): function X(){let y=window.location.pathname;return y.endsWith("/")...
const undecoded = /(function [\w$]+\(\)\{let ([\w$]+)=)window\.location\.pathname;(return \2\.endsWith\()/g;
const decoded = /function [\w$]+\(\)\{let ([\w$]+)=decodeURI\(window\.location\.pathname\);return \1\.endsWith\(/;

let changed = 0;
let fixed = 0;
for (const name of fs.readdirSync(dir, { recursive: true })) {
  const file = path.join(dir, String(name));
  if (!file.endsWith(".js")) continue;
  const src = fs.readFileSync(file, "utf8");
  const out = src.replace(undecoded, "$1decodeURI(window.location.pathname);$3");
  if (out !== src) {
    fs.writeFileSync(file, out);
    changed++;
  }
  if (decoded.test(out)) fixed++;
  if (undecoded.test(out)) {
    console.error(`decode-graph-slug: ${file} still reads location.pathname undecoded`);
    process.exit(1);
  }
}
if (fixed === 0) {
  console.error(`decode-graph-slug: found no getFullSlugFromUrl in ${dir}; the graph plugin changed, check this patch`);
  process.exit(1);
}
console.log(`decode-graph-slug: ${fixed} file(s) decode the page address (${changed} changed now)`);
