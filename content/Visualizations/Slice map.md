---
title: "Slice map"
tags:
  - "visualization"
  - "development"
created: "2026-11-04"
modified: "2026-11-04"
---

The [[Vertical-slice roadmap]] as a dependency graph. Each slice shows what must be done before it and what it unlocks, worked out from the packages' needs in [[Modules, work packages and the implementation contract (Engine, Platform, Game)|Modules and work packages]]. Any slice whose dependencies are done can come next, so the roadmap's numbering is one possible order among several.

Done packages come from the GitHub issues, through [[RunicGame — Development]]. The boxes you tick on the page are a plan kept in your browser only. `tools/build_slice_map.py` rebuilds the page on every deploy.

<iframe class="runic-viz" src="slice-map.htm" title="RunicGame Slice Map" loading="lazy"></iframe>

<a href="slice-map.htm" target="_blank" rel="noopener" data-router-ignore data-no-popover="true">Open the slice map on its own page</a>
