// Builds dist/ for the RunicDocs graph plugin. dist/ is committed, so the site build needs no npm step.
//
//   npm install --no-save esbuild && node build.mjs
//
// The inline script (src/components/scripts/graph.inline.ts) is bundled and minified into a string, the CSS is read
// as text, and the component is bundled with preact left external (Quartz provides it).
import * as esbuild from "esbuild";
import fs from "node:fs";
import path from "node:path";

const root = path.dirname(new URL(import.meta.url).pathname);

const inline = await esbuild.build({
  entryPoints: [path.join(root, "src/components/scripts/graph.inline.ts")],
  bundle: true,
  minify: true,
  write: false,
  platform: "browser",
  format: "esm",
  target: "es2020",
  external: ["http://*", "https://*"],
});
const script = inline.outputFiles[0].text;

const inlinePlugin = {
  name: "inline-and-css",
  setup(build) {
    build.onLoad({ filter: /\.inline\.ts$/ }, () => ({ contents: script, loader: "text" }));
    build.onLoad({ filter: /\.css$/ }, (args) => ({ contents: fs.readFileSync(args.path, "utf8"), loader: "text" }));
  },
};

for (const [entry, out] of [
  ["src/index.ts", "dist/index.js"],
  ["src/components/index.ts", "dist/components/index.js"],
]) {
  await esbuild.build({
    entryPoints: [path.join(root, entry)],
    outfile: path.join(root, out),
    bundle: true,
    platform: "node",
    format: "esm",
    target: "es2022",
    jsx: "automatic",
    jsxImportSource: "preact",
    external: ["preact", "preact/*"],
    plugins: [inlinePlugin],
    legalComments: "none",
  });
}
console.log(`built dist/ (inline script ${(script.length / 1024).toFixed(1)} KB)`);
