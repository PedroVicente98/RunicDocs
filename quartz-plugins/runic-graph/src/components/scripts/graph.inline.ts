// @ts-nocheck
// RunicDocs graph: Quartz's graph (quartz-community/graph c54226d, MIT) with a settings panel like
// Obsidian's graph view. Settings change the graph live and are kept in this browser's localStorage.

(function () {
  // ---------------------------------------------------------------------------------------------
  // Paths (the @quartz-community/utils helpers, with the page address decoded so that pages with
  // non-ASCII names, such as "RunicGame — Ideias", find themselves)

  function getBasePath() {
    return (document.body && document.body.dataset && document.body.dataset.basepath) || "";
  }

  function resolveBasePath(to) {
    return getBasePath() + (to.startsWith("/") ? to : "/" + to);
  }

  function simplifySlug(fp) {
    var s = String(fp);
    if (s === "index") s = "";
    else if (s.endsWith("/index")) s = s.slice(0, -"index".length);
    if (s.startsWith("/")) s = s.slice(1);
    return s.length === 0 ? "/" : s;
  }

  function getSlugFromUrl() {
    var slug = decodeURI(window.location.pathname);
    if (slug.endsWith("/")) slug = slug.slice(0, -1);
    if (slug.startsWith("/")) slug = slug.slice(1);
    var base = getBasePath().replace(/^\//, "");
    if (base && (slug === base || slug.startsWith(base + "/"))) {
      slug = slug.slice(base.length);
      if (slug.startsWith("/")) slug = slug.slice(1);
    }
    return slug;
  }

  function removeAllChildren(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  // ---------------------------------------------------------------------------------------------
  // Settings: defaults from the site config (data-cfg), the viewer's changes from localStorage.
  // The search lives only in memory, so a reload starts without one.

  var SETTINGS_KEY = "runicdocs-graph-settings";
  var session = { local: { search: "", onlyMatches: false }, global: { search: "", onlyMatches: false } };
  var SESSION_KEYS = { search: true, onlyMatches: true };
  // what a change needs: "style" redraws, "forces" moves the layout, "structure" rebuilds the graph
  var EFFECT = {
    search: "style",
    groups: "style",
    arrows: "style",
    textFade: "style",
    linkWidth: "style",
    nodeSize: "forces",
    center: "forces",
    repel: "forces",
    linkForce: "forces",
    linkDistance: "forces",
    onlyMatches: "structure",
    showTags: "structure",
    showOrphans: "structure",
    depth: "structure",
  };

  function loadStored() {
    try {
      var v = JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}");
      return v && typeof v === "object" ? v : {};
    } catch (e) {
      return {};
    }
  }

  function saveStored(all) {
    try {
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(all));
    } catch (e) {
      // storage blocked: the change still applies until the page is closed
    }
  }

  function num(v, d) {
    return typeof v === "number" && isFinite(v) ? v : d;
  }

  function defaultsFrom(cfg) {
    return {
      showTags: !!cfg.showTags,
      showOrphans: cfg.showOrphans !== false,
      depth: num(cfg.depth, 1),
      groups: Array.isArray(cfg.groups) ? cfg.groups : [],
      arrows: !!cfg.arrows,
      textFade: Math.round(Math.log2(num(cfg.opacityScale, 1)) * 10) / 10,
      nodeSize: 1,
      linkWidth: 1,
      center: num(cfg.centerForce, 0.3),
      repel: num(cfg.repelForce, 0.5) * 10,
      linkForce: 1,
      linkDistance: num(cfg.linkDistance, 30),
    };
  }

  var stored = loadStored();
  var memo = {};
  function getSettings(kind, cfg) {
    if (cfg) memo[kind] = cfg;
    var s = defaultsFrom(memo[kind] || {});
    var own = stored[kind] || {};
    for (var k in own) s[k] = own[k];
    for (var k2 in session[kind]) s[k2] = session[kind][k2];
    return s;
  }

  function setSetting(kind, key, value) {
    if (SESSION_KEYS[key]) {
      session[kind][key] = value;
      return;
    }
    stored[kind] = stored[kind] || {};
    stored[kind][key] = value;
    saveStored(stored);
  }

  function resetSettings(kind) {
    delete stored[kind];
    saveStored(stored);
    session[kind] = { search: "", onlyMatches: false };
  }

  // ---------------------------------------------------------------------------------------------
  // Queries, shared by the search and the groups:
  //   path:Vision   notes in the Vision folder      tag:status/open   notes with the tag (or below it)
  //   file:combat   title contains "combat"         combat            title or path contains "combat"

  function makeMatcher(query) {
    var q = String(query || "").trim();
    if (!q) return null;
    var m = q.match(/^(path|tag|file):\s*(.*)$/i);
    var kind = m ? m[1].toLowerCase() : "text";
    var value = (m ? m[2] : q).trim().replace(/^"(.*)"$/, "$1").trim().toLowerCase();
    if (!value) return null;
    return function (node) {
      var id = node.id.toLowerCase();
      if (kind === "path") {
        var p = value.replace(/\s+/g, "-").replace(/^\/+/, "").replace(/\/+$/, "");
        return id === p || id.startsWith(p + "/");
      }
      if (kind === "tag") {
        var t = value.replace(/^#/, "");
        if (id === "tags/" + t) return true;
        for (var i = 0; i < node.tags.length; i++) {
          var x = String(node.tags[i]).toLowerCase();
          if (x === t || x.startsWith(t + "/")) return true;
        }
        return false;
      }
      var text = String(node.text || "").toLowerCase();
      if (kind === "file") return text.indexOf(value) !== -1;
      return text.indexOf(value) !== -1 || id.indexOf(value.replace(/\s+/g, "-")) !== -1;
    };
  }

  // ---------------------------------------------------------------------------------------------

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var script = document.createElement("script");
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  Promise.all([
    loadScript("https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"),
    loadScript("https://cdn.jsdelivr.net/npm/pixi.js@8/dist/pixi.js"),
  ])
    .then(function () {
      initGraph();
    })
    .catch(function (err) {
      console.error("[Graph] Failed to load libraries:", err);
    });

  function initGraph() {
    var d3 = window.d3;
    var PIXI = window.PIXI;

    if (!d3 || !PIXI) {
      console.error("[Graph] Libraries not loaded");
      return;
    }

    var localStorageKey = "graph-visited";

    function getVisited() {
      try {
        return new Set(JSON.parse(localStorage.getItem(localStorageKey) || "[]"));
      } catch (e) {
        return new Set();
      }
    }

    function addToVisited(slug) {
      var visited = getVisited();
      visited.add(slug);
      try {
        localStorage.setItem(localStorageKey, JSON.stringify(Array.from(visited)));
      } catch (e) {}
    }

    function kindOf(graph) {
      return graph.classList.contains("global-graph-container") ? "global" : "local";
    }

    async function renderGraph(graph, fullSlug, renderGeneration) {
      var slug = simplifySlug(fullSlug);
      var visited = getVisited();
      removeAllChildren(graph);
      graph.__runicGraph = null;

      if (renderGeneration !== undefined && renderGeneration !== currentRenderGeneration) {
        return function () {};
      }

      var config = JSON.parse(graph.dataset["cfg"] || "{}");
      var kind = kindOf(graph);
      var S = getSettings(kind, config);
      var enableDrag = config.drag;
      var enableZoom = config.zoom;
      var depth = kind === "local" ? S.depth : config.depth;
      var scale = config.scale || 1;
      var fontSize = config.fontSize || 0.6;
      var removeTags = config.removeTags || [];
      var showTags = S.showTags;
      var focusOnHover = config.focusOnHover;
      var enableRadial = config.enableRadial;
      var searchMatcher = makeMatcher(S.search);

      var data;
      try {
        var dataRaw = await fetchData;
        data = new Map();
        for (var key in dataRaw) {
          data.set(simplifySlug(key), dataRaw[key]);
        }
      } catch (err) {
        console.error("[Graph] Error loading data:", err);
        return function () {};
      }

      var width = graph.offsetWidth;
      var height = Math.max(graph.offsetHeight, 250);

      var links = [];
      var allTags = [];
      var validLinks = new Set(data.keys());

      data.forEach(function (details, source) {
        var outgoing = details.links || [];
        for (var i = 0; i < outgoing.length; i++) {
          var dest = simplifySlug(outgoing[i]);
          if (validLinks.has(dest)) {
            links.push({ source: source, target: dest });
          }
        }

        if (showTags) {
          var tags = details.tags || [];
          for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];
            if (removeTags.indexOf(tag) === -1) {
              var tagSlug = simplifySlug("tags/" + tag);
              if (allTags.indexOf(tagSlug) === -1) {
                allTags.push(tagSlug);
              }
              links.push({ source: source, target: tagSlug });
            }
          }
        }
      });

      var neighbourhood = new Set();
      if (depth >= 0) {
        var queue = [slug];
        var seen = new Set([slug]);
        for (var d = 0; d <= depth && queue.length > 0; d++) {
          var nextQueue = [];
          for (var qi = 0; qi < queue.length; qi++) {
            var cur = queue[qi];
            neighbourhood.add(cur);
            for (var li = 0; li < links.length; li++) {
              var link = links[li];
              if (link.source === cur && !seen.has(link.target)) {
                seen.add(link.target);
                nextQueue.push(link.target);
              }
              if (link.target === cur && !seen.has(link.source)) {
                seen.add(link.source);
                nextQueue.push(link.source);
              }
            }
          }
          queue = nextQueue;
        }
      } else {
        validLinks.forEach(function (id) {
          neighbourhood.add(id);
        });
        for (var i = 0; i < allTags.length; i++) {
          neighbourhood.add(allTags[i]);
        }
      }

      var nodes = [];
      var nodeMap = new Map();
      neighbourhood.forEach(function (url) {
        var isTag = url.startsWith("tags/");
        var text = isTag ? "#" + url.substring(5) : (data.get(url) && data.get(url).title) || url;
        var nodeTags = isTag ? [] : (data.get(url) && data.get(url).tags) || [];
        var node = {
          id: url,
          text: text,
          tags: nodeTags,
          x: Math.random() * width - width / 2,
          y: Math.random() * height - height / 2,
          vx: 0,
          vy: 0,
        };
        if (S.onlyMatches && searchMatcher && !searchMatcher(node) && url !== slug) return;
        nodes.push(node);
        nodeMap.set(url, node);
      });

      var graphLinks = [];
      var degree = {};
      for (var i = 0; i < links.length; i++) {
        var link = links[i];
        var sourceNode = nodeMap.get(link.source);
        var targetNode = nodeMap.get(link.target);
        if (sourceNode && targetNode && sourceNode !== targetNode) {
          graphLinks.push({ source: sourceNode, target: targetNode });
          degree[link.source] = (degree[link.source] || 0) + 1;
          degree[link.target] = (degree[link.target] || 0) + 1;
        }
      }

      if (!S.showOrphans) {
        nodes = nodes.filter(function (n) {
          return degree[n.id] || n.id === slug;
        });
      }

      var styles = getComputedStyle(document.documentElement);
      var secondary = styles.getPropertyValue("--secondary").trim() || "#c792ea";
      var tertiary = styles.getPropertyValue("--tertiary").trim() || "#82aaff";
      var gray = styles.getPropertyValue("--gray").trim() || "#6c6c6c";
      var lightgray = styles.getPropertyValue("--lightgray").trim() || "#d4d4d4";
      var dark = styles.getPropertyValue("--dark").trim() || "#1a1a1a";
      var light = styles.getPropertyValue("--light").trim() || "#f5f5f5";
      var bodyFont = styles.getPropertyValue("--bodyFont").trim() || "inherit";

      var app = new PIXI.Application();
      await app.init({
        width: width,
        height: height,
        antialias: true,
        backgroundAlpha: 0,
        resolution: window.devicePixelRatio || 1,
        autoDensity: true,
        eventMode: "static",
      });

      graph.appendChild(app.canvas);

      var stage = new PIXI.Container();
      app.stage.addChild(stage);

      // the layout, with live-adjustable forces
      function baseRadius(d) {
        return 2 + Math.sqrt(degree[d.id] || 0);
      }
      function nodeRadius(d) {
        return baseRadius(d) * S.nodeSize;
      }

      var simulation = d3
        .forceSimulation(nodes)
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter())
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("link", d3.forceLink(graphLinks))
        .force("collide", d3.forceCollide().iterations(3));

      if (enableRadial) {
        var ring = (Math.min(width, height) / 2) * 0.8;
        simulation.force("radial", d3.forceRadial(ring).strength(0.2));
      }

      function setForces() {
        simulation.force("charge").strength(-10 * S.repel);
        simulation.force("x").strength(S.center * 0.1);
        simulation.force("y").strength(S.center * 0.1);
        simulation
          .force("link")
          .distance(S.linkDistance)
          .strength(function (l) {
            return S.linkForce / Math.max(1, Math.min(degree[l.source.id] || 1, degree[l.target.id] || 1));
          });
        simulation.force("collide").radius(nodeRadius);
      }
      setForces();

      var linkContainer = new PIXI.Container();
      var nodesContainer = new PIXI.Container();
      var labelsContainer = new PIXI.Container();
      stage.addChild(linkContainer);
      stage.addChild(nodesContainer);
      stage.addChild(labelsContainer);

      var nodeRenderData = [];
      var linkRenderData = [];
      var hoveredNodeId = null;
      var hoveredNeighbours = new Set();
      var dragStartTime = 0;
      var dragging = false;
      var currentTransform = d3.zoomIdentity;
      var groupMatchers = [];
      var matched = null; // Set of matching node ids, or null without a search

      function compileGroups() {
        groupMatchers = [];
        var groups = Array.isArray(S.groups) ? S.groups : [];
        for (var i = 0; i < groups.length; i++) {
          var g = groups[i] || {};
          var m = makeMatcher(g.query);
          if (m && g.color) groupMatchers.push({ match: m, color: g.color });
        }
      }

      function nodeColor(d) {
        if (d.id === slug) return secondary;
        for (var i = 0; i < groupMatchers.length; i++) {
          if (groupMatchers[i].match(d)) return groupMatchers[i].color;
        }
        if (visited.has(d.id) || d.id.startsWith("tags/")) return tertiary;
        return gray;
      }

      function drawNode(nodeData) {
        var n = nodeData.simulationData;
        var isTag = n.id.startsWith("tags/");
        var r = nodeRadius(n) * (matched && matched.has(n.id) ? 1.3 : 1);
        var color = nodeColor(n);
        nodeData.color = color;
        nodeData.gfx.clear();
        nodeData.gfx.circle(0, 0, r);
        nodeData.gfx.fill({ color: isTag ? light : color });
        if (isTag) {
          nodeData.gfx.stroke({ width: 2, color: color === tertiary ? tertiary : color });
        }
      }

      function zoomLabelAlpha() {
        var k = currentTransform.k * Math.pow(2, S.textFade);
        return Math.max(Math.min((k - 1) / 3.75, 1), 0);
      }

      function updateHoverInfo(newHoveredId) {
        hoveredNodeId = newHoveredId;
        hoveredNeighbours = new Set();
        for (var i = 0; i < linkRenderData.length; i++) {
          var linkData = linkRenderData[i].simulationData;
          var on =
            newHoveredId !== null &&
            (linkData.source.id === newHoveredId || linkData.target.id === newHoveredId);
          linkRenderData[i].active = on;
          if (on) {
            hoveredNeighbours.add(linkData.source.id);
            hoveredNeighbours.add(linkData.target.id);
          }
        }
        if (newHoveredId !== null) hoveredNeighbours.add(newHoveredId);
        for (var i = 0; i < nodeRenderData.length; i++) {
          nodeRenderData[i].active = hoveredNeighbours.has(nodeRenderData[i].simulationData.id);
        }
      }

      function renderLinks() {
        for (var i = 0; i < linkRenderData.length; i++) {
          var linkData = linkRenderData[i];
          var l = linkData.simulationData;
          var alpha = 1;
          if (hoveredNodeId !== null) {
            alpha = linkData.active ? 1 : 0.2;
          } else if (matched) {
            alpha = matched.has(l.source.id) && matched.has(l.target.id) ? 1 : 0.08;
          }
          linkData.alpha = alpha;
          linkData.color = linkData.active ? gray : lightgray;
        }
      }

      function renderLabels() {
        var defaultScale = 1 / scale;
        var activeScale = defaultScale * 1.1;
        var zoomAlpha = zoomLabelAlpha();
        for (var i = 0; i < nodeRenderData.length; i++) {
          var nodeData = nodeRenderData[i];
          var id = nodeData.simulationData.id;
          if (hoveredNodeId === id) {
            nodeData.label.alpha = 1;
            nodeData.label.scale.set(activeScale);
          } else {
            nodeData.label.scale.set(defaultScale);
            if (matched) {
              nodeData.label.alpha = matched.has(id) ? 1 : 0;
            } else if (hoveredNodeId !== null && nodeData.active) {
              nodeData.label.alpha = Math.max(zoomAlpha, 0.8);
            } else {
              nodeData.label.alpha = zoomAlpha;
            }
          }
        }
      }

      function renderNodes() {
        for (var i = 0; i < nodeRenderData.length; i++) {
          var nodeData = nodeRenderData[i];
          var alpha = 1;
          if (hoveredNodeId !== null && focusOnHover) {
            alpha = nodeData.active ? 1 : 0.2;
          } else if (matched) {
            alpha = matched.has(nodeData.simulationData.id) ? 1 : 0.15;
          }
          nodeData.gfx.alpha = alpha;
        }
      }

      function renderPixiFromD3() {
        renderNodes();
        renderLinks();
        renderLabels();
      }

      function applySearch() {
        if (!searchMatcher) {
          matched = null;
          return 0;
        }
        matched = new Set();
        for (var i = 0; i < nodes.length; i++) {
          if (searchMatcher(nodes[i])) matched.add(nodes[i].id);
        }
        return matched.size;
      }

      compileGroups();
      applySearch();

      for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];

        var label = new PIXI.Text({
          text: node.text,
          style: {
            fontSize: fontSize * 15,
            fill: dark,
            fontFamily: bodyFont,
          },
          resolution: window.devicePixelRatio * 4,
        });
        label.anchor.set(0.5, 1.2);
        label.alpha = 0;
        label.scale.set(1 / scale);
        labelsContainer.addChild(label);

        var gfx = new PIXI.Graphics();
        gfx.eventMode = "static";
        gfx.cursor = "pointer";
        gfx.label = node.id;

        var nodeData = {
          simulationData: node,
          gfx: gfx,
          label: label,
          color: gray,
          alpha: 1,
          active: false,
        };
        drawNode(nodeData);

        (function (n) {
          gfx.on("pointerover", function () {
            updateHoverInfo(n.id);
            if (!dragging) renderPixiFromD3();
          });
          gfx.on("pointerleave", function () {
            updateHoverInfo(null);
            if (!dragging) renderPixiFromD3();
          });
        })(node);

        nodesContainer.addChild(gfx);
        nodeRenderData.push(nodeData);
      }

      for (var i = 0; i < graphLinks.length; i++) {
        var lgfx = new PIXI.Graphics();
        lgfx.eventMode = "none";
        linkContainer.addChild(lgfx);
        linkRenderData.push({
          simulationData: graphLinks[i],
          gfx: lgfx,
          color: lightgray,
          alpha: 1,
          active: false,
        });
      }

      if (enableDrag) {
        var dragSubject = function (event) {
          var mouseX = (event.x - currentTransform.x) / currentTransform.k;
          var mouseY = (event.y - currentTransform.y) / currentTransform.k;
          for (var i = 0; i < nodes.length; i++) {
            var n = nodes[i];
            var dx = mouseX - n.x - width / 2;
            var dy = mouseY - n.y - height / 2;
            if (Math.sqrt(dx * dx + dy * dy) < nodeRadius(n) + 5) return n;
          }
          return null;
        };

        var dragStarted = function (event) {
          if (!event.active) simulation.alphaTarget(1).restart();
          event.subject.fx = event.subject.x;
          event.subject.fy = event.subject.y;
          var mouseSimX = (event.x - currentTransform.x) / currentTransform.k - width / 2;
          var mouseSimY = (event.y - currentTransform.y) / currentTransform.k - height / 2;
          event.subject.__dragOffset = {
            x: mouseSimX - event.subject.x,
            y: mouseSimY - event.subject.y,
          };
          dragStartTime = Date.now();
          dragging = true;
          hoveredNodeId = event.subject.id;
        };

        var dragDragged = function (event) {
          var mouseSimX = (event.x - currentTransform.x) / currentTransform.k - width / 2;
          var mouseSimY = (event.y - currentTransform.y) / currentTransform.k - height / 2;
          event.subject.fx = mouseSimX - event.subject.__dragOffset.x;
          event.subject.fy = mouseSimY - event.subject.__dragOffset.y;
        };

        var dragEnded = function (event) {
          if (!event.active) simulation.alphaTarget(0);
          event.subject.fx = null;
          event.subject.fy = null;
          dragging = false;
          updateHoverInfo(null);
          renderPixiFromD3();
          if (Date.now() - dragStartTime < 500) {
            window.location.href = resolveBasePath(event.subject.id);
          }
        };

        d3.select(app.canvas).call(
          d3
            .drag()
            .container(app.canvas)
            .subject(dragSubject)
            .on("start", dragStarted)
            .on("drag", dragDragged)
            .on("end", dragEnded),
        );
      } else {
        for (var i = 0; i < nodeRenderData.length; i++) {
          (function (nodeData) {
            nodeData.gfx.on("click", function () {
              window.location.href = resolveBasePath(nodeData.simulationData.id);
            });
          })(nodeRenderData[i]);
        }
      }

      if (enableZoom) {
        d3.select(app.canvas).call(
          d3
            .zoom()
            .extent([
              [0, 0],
              [width, height],
            ])
            .scaleExtent([0.1, 6])
            .on("zoom", function (event) {
              currentTransform = event.transform;
              stage.scale.set(currentTransform.k, currentTransform.k);
              stage.position.set(currentTransform.x, currentTransform.y);
              renderLabels();
            }),
        );
      }

      var stopAnimation = false;
      function animate() {
        if (stopAnimation) return;

        for (var i = 0; i < nodeRenderData.length; i++) {
          var n = nodeRenderData[i];
          var x = n.simulationData.x;
          var y = n.simulationData.y;
          if (x != null && y != null) {
            n.gfx.position.set(x + width / 2, y + height / 2);
            n.label.position.set(x + width / 2, y + height / 2);
          }
        }

        var lineWidth = S.linkWidth;
        for (var i = 0; i < linkRenderData.length; i++) {
          var l = linkRenderData[i];
          var linkData = l.simulationData;
          var sx = linkData.source.x;
          var sy = linkData.source.y;
          var tx = linkData.target.x;
          var ty = linkData.target.y;
          if (sx == null || sy == null || tx == null || ty == null) continue;
          sx += width / 2;
          sy += height / 2;
          tx += width / 2;
          ty += height / 2;
          l.gfx.clear();
          l.gfx.moveTo(sx, sy);
          l.gfx.lineTo(tx, ty);
          l.gfx.stroke({ alpha: l.alpha, width: lineWidth, color: l.color });
          if (S.arrows) {
            var dx = tx - sx;
            var dy = ty - sy;
            var len = Math.sqrt(dx * dx + dy * dy);
            if (len > 0.001) {
              var ux = dx / len;
              var uy = dy / len;
              var r = nodeRadius(linkData.target);
              var tipX = tx - ux * r;
              var tipY = ty - uy * r;
              var size = 2.5 + lineWidth * 1.5;
              l.gfx.poly([
                tipX,
                tipY,
                tipX - ux * size * 1.6 - uy * size,
                tipY - uy * size * 1.6 + ux * size,
                tipX - ux * size * 1.6 + uy * size,
                tipY - uy * size * 1.6 - ux * size,
              ]);
              l.gfx.fill({ alpha: l.alpha, color: l.active ? gray : lightgray });
            }
          }
        }

        requestAnimationFrame(animate);
      }

      simulation.restart();
      renderPixiFromD3();
      animate();

      // the settings panel talks to the graph through this controller
      graph.__runicGraph = {
        kind: kind,
        matches: matched ? matched.size : null,
        nodeCount: nodes.length,
        apply: function (newSettings, effect) {
          S = newSettings;
          searchMatcher = makeMatcher(S.search);
          compileGroups();
          var count = applySearch();
          this.matches = matched ? count : null;
          if (effect === "forces") {
            setForces();
            simulation.alpha(0.6).restart();
          }
          for (var i = 0; i < nodeRenderData.length; i++) drawNode(nodeRenderData[i]);
          renderPixiFromD3();
          return this.matches;
        },
        animate: function () {
          for (var i = 0; i < nodes.length; i++) {
            nodes[i].x = Math.random() * width - width / 2;
            nodes[i].y = Math.random() * height - height / 2;
            nodes[i].vx = 0;
            nodes[i].vy = 0;
          }
          simulation.alpha(1).restart();
        },
      };
      updatePanels(kind);

      return function () {
        stopAnimation = true;
        simulation.stop();
        graph.__runicGraph = null;
        try {
          app.destroy(true);
        } catch (_) {
          // PixiJS may throw if the WebGL context was already lost.
        }
      };
    }

    // -------------------------------------------------------------------------------------------
    // The settings panel

    var GEAR =
      '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"></circle>' +
      '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 ' +
      "1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 " +
      "1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 " +
      "4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 " +
      "1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 " +
      '2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>';

    var PALETTE = ["#e0a526", "#3498db", "#e67e22", "#7f8c8d", "#9b59b6", "#1abc9c", "#2ecc71", "#e74c3c"];

    function rangeRow(label, key, min, max, step) {
      return (
        '<label class="rgp-range"><span>' +
        label +
        '</span><span class="rgp-range-row"><input type="range" data-key="' +
        key +
        '" min="' +
        min +
        '" max="' +
        max +
        '" step="' +
        step +
        '"><output data-out="' +
        key +
        '"></output></span></label>'
      );
    }

    function toggleRow(label, key) {
      return (
        '<label class="rgp-toggle"><span>' +
        label +
        '</span><input type="checkbox" role="switch" data-key="' +
        key +
        '"></label>'
      );
    }

    function panelHtml(kind) {
      return (
        '<div class="rgp-head"><span>' +
        (kind === "global" ? "Graph settings" : "Local graph settings") +
        '</span><button type="button" data-act="reset" title="Reset to the site defaults">Reset</button>' +
        '<button type="button" data-act="close" title="Close" aria-label="Close">×</button></div>' +
        '<details open><summary>Filters</summary>' +
        '<input type="search" data-key="search" placeholder="Search notes…" ' +
        'title="Text, or path:Vision, tag:status/open, file:combat">' +
        '<div class="rgp-hint" data-out="matches">path:Vision · tag:status/open · file:combat</div>' +
        toggleRow("Only matches", "onlyMatches") +
        toggleRow("Tags", "showTags") +
        toggleRow("Orphans", "showOrphans") +
        (kind === "local" ? rangeRow("Depth", "depth", 1, 5, 1) : "") +
        "</details>" +
        '<details open><summary>Groups</summary><div class="rgp-groups"></div>' +
        '<button type="button" class="rgp-wide" data-act="add-group">New group</button></details>' +
        "<details><summary>Display</summary>" +
        toggleRow("Arrows", "arrows") +
        rangeRow("Text fade threshold", "textFade", -3, 3, 0.1) +
        rangeRow("Node size", "nodeSize", 0.1, 5, 0.1) +
        rangeRow("Link thickness", "linkWidth", 0.1, 5, 0.1) +
        '<button type="button" class="rgp-wide" data-act="animate">Animate</button></details>' +
        "<details><summary>Forces</summary>" +
        rangeRow("Center force", "center", 0, 1, 0.01) +
        rangeRow("Repel force", "repel", 0, 20, 0.1) +
        rangeRow("Link force", "linkForce", 0, 1, 0.01) +
        rangeRow("Link distance", "linkDistance", 10, 300, 1) +
        "</details>"
      );
    }

    function graphsOf(kind) {
      var sel = kind === "global" ? ".global-graph-container" : ".graph-container";
      return Array.from(document.querySelectorAll(sel));
    }

    function currentSettings(kind) {
      var g = graphsOf(kind)[0];
      var cfg = g ? JSON.parse(g.dataset["cfg"] || "{}") : undefined;
      return getSettings(kind, cfg);
    }

    var rebuildTimers = {};
    function rebuild(kind) {
      clearTimeout(rebuildTimers[kind]);
      rebuildTimers[kind] = setTimeout(function () {
        if (kind === "global") {
          if (anyGlobalGraphActive()) showGlobalGraph();
        } else {
          renderLocal();
        }
      }, 250);
    }

    function applyChange(kind, key) {
      var s = currentSettings(kind);
      var effect = EFFECT[key] || "style";
      if (key === "search" && s.onlyMatches) effect = "structure";
      if (effect === "structure") {
        rebuild(kind);
        return;
      }
      var graphs = graphsOf(kind);
      for (var i = 0; i < graphs.length; i++) {
        if (graphs[i].__runicGraph) graphs[i].__runicGraph.apply(s, effect);
      }
      updatePanels(kind);
    }

    function formatValue(key, v) {
      if (key === "depth" || key === "linkDistance") return String(Math.round(v));
      return Number(v).toFixed(2);
    }

    function fillPanel(panel, kind) {
      var s = currentSettings(kind);
      var inputs = panel.querySelectorAll("[data-key]");
      for (var i = 0; i < inputs.length; i++) {
        var el = inputs[i];
        var key = el.dataset.key;
        if (el.type === "checkbox") el.checked = !!s[key];
        else if (el.type === "range") el.value = String(s[key]);
        else if (document.activeElement !== el) el.value = s[key] || "";
        var out = panel.querySelector('[data-out="' + key + '"]');
        if (out) out.textContent = formatValue(key, s[key]);
      }
      renderGroups(panel, kind, s.groups || []);
      updateMatchCount(panel, kind);
    }

    function updateMatchCount(panel, kind) {
      var out = panel.querySelector('[data-out="matches"]');
      if (!out) return;
      var s = currentSettings(kind);
      var g = graphsOf(kind).filter(function (x) {
        return x.__runicGraph;
      })[0];
      if (!s.search || !makeMatcher(s.search)) {
        out.textContent = "path:Vision · tag:status/open · file:combat";
      } else if (g) {
        var c = s.onlyMatches ? g.__runicGraph.nodeCount : g.__runicGraph.matches;
        out.textContent = c + (c === 1 ? " matching note" : " matching notes");
      }
    }

    function renderGroups(panel, kind, groups) {
      var box = panel.querySelector(".rgp-groups");
      if (!box || box.contains(document.activeElement)) return;
      removeAllChildren(box);
      groups.forEach(function (g, idx) {
        var row = document.createElement("div");
        row.className = "rgp-group";
        row.innerHTML =
          '<input type="color" aria-label="Group color"><input type="text" placeholder="path:Vision" ' +
          'aria-label="Group query"><button type="button" title="Remove group" aria-label="Remove group">×</button>';
        var color = row.children[0];
        var query = row.children[1];
        var del = row.children[2];
        color.value = /^#[0-9a-f]{6}$/i.test(g.color || "") ? g.color : PALETTE[idx % PALETTE.length];
        query.value = g.query || "";
        function save() {
          var list = (currentSettings(kind).groups || []).slice();
          list[idx] = { query: query.value, color: color.value };
          setSetting(kind, "groups", list);
          applyChange(kind, "groups");
        }
        color.addEventListener("input", save);
        query.addEventListener("input", save);
        del.addEventListener("click", function () {
          var list = (currentSettings(kind).groups || []).slice();
          list.splice(idx, 1);
          setSetting(kind, "groups", list);
          renderGroups(panel, kind, list);
          applyChange(kind, "groups");
        });
        box.appendChild(row);
      });
    }

    function wirePanel(panel, kind) {
      panel.addEventListener("input", function (e) {
        var el = e.target;
        var key = el.dataset && el.dataset.key;
        if (!key) return;
        var value = el.type === "checkbox" ? el.checked : el.type === "range" ? Number(el.value) : el.value;
        setSetting(kind, key, value);
        var out = panel.querySelector('[data-out="' + key + '"]');
        if (out && el.type === "range") out.textContent = formatValue(key, value);
        applyChange(kind, key);
      });
      panel.addEventListener("click", function (e) {
        var btn = e.target.closest("[data-act]");
        if (!btn) return;
        var act = btn.dataset.act;
        if (act === "close") {
          panel.hidden = true;
        } else if (act === "reset") {
          resetSettings(kind);
          fillPanel(panel, kind);
          rebuild(kind);
        } else if (act === "add-group") {
          var list = (currentSettings(kind).groups || []).slice();
          list.push({ query: "", color: PALETTE[list.length % PALETTE.length] });
          setSetting(kind, "groups", list);
          renderGroups(panel, kind, list);
          var inputs = panel.querySelectorAll(".rgp-group input[type=text]");
          if (inputs.length) inputs[inputs.length - 1].focus();
        } else if (act === "animate") {
          var graphs = graphsOf(kind);
          for (var i = 0; i < graphs.length; i++) {
            if (graphs[i].__runicGraph) graphs[i].__runicGraph.animate();
          }
        }
      });
      // keep typing, scrolling and dragging inside the panel away from the page and the graph
      ["keydown", "wheel", "pointerdown", "mousedown", "touchstart"].forEach(function (type) {
        panel.addEventListener(
          type,
          function (e) {
            if (type === "keydown" && e.key === "Escape") return;
            e.stopPropagation();
          },
          { passive: true },
        );
      });
    }

    function ensurePanel(host, kind) {
      if (!host || host.querySelector(":scope > .runic-graph-panel")) return;
      var gear = document.createElement("button");
      gear.type = "button";
      gear.className = "runic-graph-gear runic-graph-gear-" + kind;
      gear.title = "Graph settings";
      gear.setAttribute("aria-label", "Graph settings");
      gear.innerHTML = GEAR;
      var panel = document.createElement("div");
      panel.className = "runic-graph-panel runic-graph-panel-" + kind;
      panel.hidden = true;
      panel.innerHTML = panelHtml(kind);
      gear.addEventListener("click", function (e) {
        e.stopPropagation();
        panel.hidden = !panel.hidden;
        if (!panel.hidden) fillPanel(panel, kind);
      });
      wirePanel(panel, kind);
      host.appendChild(gear);
      host.appendChild(panel);
    }

    function ensurePanels() {
      var outers = document.querySelectorAll(".graph-outer");
      for (var i = 0; i < outers.length; i++) ensurePanel(outers[i], "local");
      var globals = document.querySelectorAll(".global-graph-outer");
      for (var i = 0; i < globals.length; i++) ensurePanel(globals[i], "global");
    }

    function updatePanels(kind) {
      var panels = document.querySelectorAll(".runic-graph-panel-" + kind);
      for (var i = 0; i < panels.length; i++) {
        if (!panels[i].hidden) updateMatchCount(panels[i], kind);
      }
    }

    // -------------------------------------------------------------------------------------------

    var localCleanups = [];
    var globalCleanups = [];
    var currentRenderGeneration = 0;

    function cleanupLocal() {
      for (var i = 0; i < localCleanups.length; i++) localCleanups[i]();
      localCleanups = [];
    }

    function cleanupGlobal() {
      for (var i = 0; i < globalCleanups.length; i++) globalCleanups[i]();
      globalCleanups = [];
    }

    var globalContainers = [];
    var globalIcons = [];
    var documentClickHandler = null;
    var documentKeydownHandler = null;
    var iconClickHandler = null;

    function hideGlobalGraph() {
      cleanupGlobal();
      for (var i = 0; i < globalContainers.length; i++) {
        globalContainers[i].classList.remove("active");
        var sidebar = globalContainers[i].closest(".sidebar");
        if (sidebar) sidebar.style.zIndex = "";
      }
    }

    function anyGlobalGraphActive() {
      for (var i = 0; i < globalContainers.length; i++) {
        if (globalContainers[i].classList.contains("active")) return true;
      }
      return false;
    }

    function showGlobalGraph() {
      cleanupGlobal();
      var currentSlug = getSlugFromUrl();
      for (var i = 0; i < globalContainers.length; i++) {
        var container = globalContainers[i];
        container.classList.add("active");
        var sidebar = container.closest(".sidebar");
        if (sidebar) sidebar.style.zIndex = "1";
        var graphContainer = container.querySelector(".global-graph-container");
        if (graphContainer) {
          (function (gc) {
            renderGraph(gc, currentSlug, undefined)
              .then(function (cleanup) {
                globalCleanups.push(cleanup);
              })
              .catch(function (err) {
                console.error("[Graph] Global render error:", err);
              });
          })(graphContainer);
        }
      }
    }

    function toggleGlobalGraph() {
      if (anyGlobalGraphActive()) hideGlobalGraph();
      else showGlobalGraph();
    }

    function renderLocal() {
      cleanupLocal();
      var thisGeneration = ++currentRenderGeneration;
      var slug = getSlugFromUrl();
      addToVisited(simplifySlug(slug));
      var localContainers = document.querySelectorAll(".graph-container");
      for (var i = 0; i < localContainers.length; i++) {
        (function (container) {
          renderGraph(container, slug, thisGeneration)
            .then(function (cleanup) {
              if (thisGeneration === currentRenderGeneration) localCleanups.push(cleanup);
              else cleanup();
            })
            .catch(function (err) {
              console.error("[Graph] Local render error:", err);
            });
        })(localContainers[i]);
      }
    }

    function handleNav(e) {
      var slug = e.detail ? e.detail.url : getSlugFromUrl();
      addToVisited(simplifySlug(slug));
      ensurePanels();
      renderLocal();

      globalContainers = Array.from(document.querySelectorAll(".global-graph-outer"));

      if (iconClickHandler) {
        for (var i = 0; i < globalIcons.length; i++) {
          globalIcons[i].removeEventListener("click", iconClickHandler);
        }
      }
      globalIcons = Array.from(document.querySelectorAll(".global-graph-icon"));
      iconClickHandler = function () {
        toggleGlobalGraph();
      };
      for (var i = 0; i < globalIcons.length; i++) {
        globalIcons[i].addEventListener("click", iconClickHandler);
      }

      if (documentClickHandler) document.removeEventListener("click", documentClickHandler);
      documentClickHandler = function (ev) {
        if (anyGlobalGraphActive()) {
          var inside = ev.target.closest(
            ".global-graph-container, .global-graph-icon, .runic-graph-panel, .runic-graph-gear",
          );
          if (!inside) hideGlobalGraph();
        }
      };
      document.addEventListener("click", documentClickHandler);

      if (documentKeydownHandler) document.removeEventListener("keydown", documentKeydownHandler);
      documentKeydownHandler = function (ev) {
        if (ev.key === "Escape") {
          var open = document.querySelector(".runic-graph-panel:not([hidden])");
          if (open) {
            open.hidden = true;
            return;
          }
          if (anyGlobalGraphActive()) hideGlobalGraph();
          return;
        }
        if (ev.key === "g" && (ev.ctrlKey || ev.metaKey) && !ev.shiftKey) {
          ev.preventDefault();
          toggleGlobalGraph();
        }
      };
      document.addEventListener("keydown", documentKeydownHandler);

      if (anyGlobalGraphActive()) showGlobalGraph();
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        handleNav({ detail: { url: getSlugFromUrl() } });
      });
    } else {
      handleNav({ detail: { url: getSlugFromUrl() } });
    }
    document.addEventListener("prenav", function () {
      cleanupLocal();
      cleanupGlobal();
    });
    document.addEventListener("nav", handleNav);
    document.addEventListener("render", handleNav);
  }
})();
