# runic-graph

The graph of the RunicDocs site: Quartz's graph component ([quartz-community/graph](https://github.com/quartz-community/graph)
at commit c54226d, MIT, see `LICENSE`) with a settings panel like Obsidian's graph view.

The gear on the local graph and on the full graph opens the panel:

- **Filters:** search (text, `path:Vision`, `tag:status/open`, `file:combat`) highlights the matching notes; only
  matches, tags, orphans; the depth of the local graph.
- **Groups:** colour the notes that match a query. The defaults come from `groups` in `quartz.config.yaml`.
- **Display:** arrows, text fade threshold, node size, link thickness, animate.
- **Forces:** center, repel, link force, link distance.

Changes apply at once and are kept in the browser's localStorage (`runicdocs-graph-settings`); the search is kept only
until the page is reloaded. **Reset** goes back to the site's defaults.

Changes from upstream: the panel and its options; the page address is decoded (pages with non-ASCII names, such as
"RunicGame — Ideias", find themselves); the small path helpers are inlined, so the plugin imports only preact.

## Build

`dist/` is committed, so the site build needs no npm step. After changing `src/`:

```
npm install --no-save esbuild
node build.mjs
```
