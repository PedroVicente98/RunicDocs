// src/util/lang.ts
function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

// src/i18n/locales/en-US.ts
var en_US_default = {
  components: {
    graph: {
      title: "Graph View"
    }
  }
};

// src/i18n/index.ts
var locales = {
  "en-US": en_US_default
};
function i18n(locale) {
  return locales[locale] || en_US_default;
}

// src/components/styles/graph.css
var graph_default = `/* Quartz's graph styles (quartz-community/graph), then the RunicDocs settings panel. */

.graph > h3 {
  font-size: 1rem;
  margin: 0;
}

.graph > .graph-outer {
  border-radius: 5px;
  border: 1px solid var(--lightgray);
  box-sizing: border-box;
  height: 250px;
  margin: 0.5em 0;
  position: relative;
  overflow: hidden;
}

.graph > .graph-outer > .global-graph-icon {
  cursor: pointer;
  background: none;
  border: none;
  color: var(--dark);
  opacity: 0.5;
  width: 24px;
  height: 24px;
  position: absolute;
  padding: 0.2rem;
  margin: 0.3rem;
  top: 0;
  right: 0;
  border-radius: 4px;
  background-color: transparent;
  transition: background-color 0.5s ease;
}

.graph > .graph-outer > .global-graph-icon:hover {
  background-color: var(--lightgray);
}

.graph > .global-graph-outer {
  position: fixed;
  z-index: 9999;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100%;
  backdrop-filter: blur(4px);
  display: none;
  overflow: hidden;
}

.graph > .global-graph-outer.active {
  display: inline-block;
}

.graph > .global-graph-outer > .global-graph-container {
  border: 1px solid var(--lightgray);
  background-color: var(--light);
  border-radius: 5px;
  box-sizing: border-box;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  height: 80vh;
  width: 80vw;
}

@media all and (max-width: 800px) {
  .graph > .global-graph-outer > .global-graph-container {
    width: 90%;
  }
}

.graph-container {
  width: 100%;
  height: 100%;
}

/* ---- settings panel ---- */

.runic-graph-gear {
  cursor: pointer;
  border: none;
  background-color: transparent;
  color: var(--dark);
  opacity: 0.55;
  width: 24px;
  height: 24px;
  padding: 0.2rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease, opacity 0.3s ease;
}

.runic-graph-gear:hover {
  opacity: 1;
  background-color: var(--lightgray);
}

.runic-graph-gear-local {
  position: absolute;
  top: 0;
  right: 28px;
  margin: 0.3rem;
}

.runic-graph-gear-global {
  position: fixed;
  top: calc(10vh + 8px);
  right: calc(10vw + 8px);
  z-index: 2;
}

.runic-graph-panel {
  box-sizing: border-box;
  background-color: var(--light);
  color: var(--darkgray);
  border: 1px solid var(--lightgray);
  border-radius: 6px;
  font-size: 0.85rem;
  overflow-y: auto;
  overscroll-behavior: contain;
  z-index: 3;
}

.runic-graph-panel[hidden] {
  display: none;
}

.runic-graph-panel-local {
  position: absolute;
  inset: 0;
  border-radius: 5px;
  border: none;
}

.runic-graph-panel-global {
  position: fixed;
  top: calc(10vh + 40px);
  right: calc(10vw + 8px);
  width: min(290px, calc(80vw - 16px));
  max-height: calc(80vh - 48px);
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.18);
}

@media all and (max-width: 800px) {
  .runic-graph-gear-global {
    right: calc(5% + 8px);
  }

  .runic-graph-panel-global {
    right: calc(5% + 8px);
    width: calc(90% - 16px);
  }
}

.runic-graph-panel .rgp-head {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.6rem;
  border-bottom: 1px solid var(--lightgray);
  position: sticky;
  top: 0;
  background-color: var(--light);
  z-index: 1;
}

.runic-graph-panel .rgp-head > span {
  flex: 1;
  font-weight: 600;
  color: var(--dark);
}

.runic-graph-panel button {
  font: inherit;
  cursor: pointer;
  color: var(--dark);
  background-color: var(--highlight, rgba(143, 159, 169, 0.15));
  border: 1px solid var(--lightgray);
  border-radius: 5px;
  padding: 0.2rem 0.55rem;
}

.runic-graph-panel button:hover {
  border-color: var(--secondary);
}

.runic-graph-panel .rgp-head button[data-act="close"] {
  border: none;
  background: none;
  font-size: 1.1rem;
  line-height: 1;
  padding: 0 0.2rem;
}

.runic-graph-panel details {
  border-bottom: 1px solid var(--lightgray);
  padding: 0.35rem 0.6rem 0.55rem;
}

.runic-graph-panel details:last-child {
  border-bottom: none;
}

.runic-graph-panel summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--dark);
  padding: 0.2rem 0;
  user-select: none;
}

.runic-graph-panel input[type="search"],
.runic-graph-panel input[type="text"] {
  box-sizing: border-box;
  width: 100%;
  font: inherit;
  color: var(--dark);
  background-color: var(--light);
  border: 1px solid var(--lightgray);
  border-radius: 5px;
  padding: 0.3rem 0.45rem;
  margin: 0.3rem 0 0.1rem;
}

.runic-graph-panel input[type="search"]:focus,
.runic-graph-panel input[type="text"]:focus {
  outline: none;
  border-color: var(--secondary);
}

.runic-graph-panel .rgp-hint {
  font-size: 0.75rem;
  color: var(--gray);
  margin-bottom: 0.25rem;
}

.runic-graph-panel .rgp-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.25rem 0;
  cursor: pointer;
}

.runic-graph-panel .rgp-toggle input {
  appearance: none;
  -webkit-appearance: none;
  position: relative;
  width: 34px;
  height: 18px;
  margin: 0;
  border-radius: 9px;
  background-color: var(--lightgray);
  cursor: pointer;
  transition: background-color 0.2s ease;
  flex: none;
}

.runic-graph-panel .rgp-toggle input::after {
  content: "";
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background-color: var(--light);
  transition: transform 0.2s ease;
}

.runic-graph-panel .rgp-toggle input:checked {
  background-color: var(--secondary);
}

.runic-graph-panel .rgp-toggle input:checked::after {
  transform: translateX(16px);
}

.runic-graph-panel .rgp-range {
  display: block;
  padding: 0.25rem 0;
}

.runic-graph-panel .rgp-range-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.runic-graph-panel .rgp-range input {
  flex: 1;
  min-width: 0;
  accent-color: var(--secondary);
}

.runic-graph-panel .rgp-range output {
  order: -1;
  min-width: 2.6rem;
  font-variant-numeric: tabular-nums;
  color: var(--gray);
}

.runic-graph-panel .rgp-wide {
  width: 100%;
  margin-top: 0.35rem;
}

.runic-graph-panel .rgp-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin: 0.25rem 0;
}

.runic-graph-panel .rgp-group input[type="text"] {
  margin: 0;
  flex: 1;
  min-width: 0;
}

.runic-graph-panel .rgp-group input[type="color"] {
  width: 26px;
  height: 26px;
  padding: 0;
  border: 1px solid var(--lightgray);
  border-radius: 50%;
  background: none;
  cursor: pointer;
  flex: none;
}

.runic-graph-panel .rgp-group input[type="color"]::-webkit-color-swatch-wrapper {
  padding: 0;
}

.runic-graph-panel .rgp-group input[type="color"]::-webkit-color-swatch {
  border: none;
  border-radius: 50%;
}

.runic-graph-panel .rgp-group button {
  border: none;
  background: none;
  font-size: 1rem;
  padding: 0 0.2rem;
}
`;

// src/components/scripts/graph.inline.ts
var graph_inline_default = `(function(){function tr(){return document.body&&document.body.dataset&&document.body.dataset.basepath||""}function ar(t){return tr()+(t.startsWith("/")?t:"/"+t)}function $(t){var s=String(t);return s==="index"?s="":s.endsWith("/index")&&(s=s.slice(0,-5)),s.startsWith("/")&&(s=s.slice(1)),s.length===0?"/":s}function U(){var t=decodeURI(window.location.pathname);t.endsWith("/")&&(t=t.slice(0,-1)),t.startsWith("/")&&(t=t.slice(1));var s=tr().replace(/^\\//,"");return s&&(t===s||t.startsWith(s+"/"))&&(t=t.slice(s.length),t.startsWith("/")&&(t=t.slice(1))),t}function nr(t){for(;t.firstChild;)t.removeChild(t.firstChild)}var or="runicdocs-graph-settings",fe={local:{search:"",onlyMatches:!1},global:{search:"",onlyMatches:!1}},Wr={search:!0,onlyMatches:!0},Nr={search:"style",groups:"style",arrows:"style",textFade:"style",linkWidth:"style",nodeSize:"forces",center:"forces",repel:"forces",linkForce:"forces",linkDistance:"forces",onlyMatches:"structure",showTags:"structure",showOrphans:"structure",depth:"structure"};function Vr(){try{var t=JSON.parse(localStorage.getItem(or)||"{}");return t&&typeof t=="object"?t:{}}catch{return{}}}function ir(t){try{localStorage.setItem(or,JSON.stringify(t))}catch{}}function Z(t,s){return typeof t=="number"&&isFinite(t)?t:s}function kr(t){return{showTags:!!t.showTags,showOrphans:t.showOrphans!==!1,depth:Z(t.depth,1),groups:Array.isArray(t.groups)?t.groups:[],arrows:!!t.arrows,textFade:Math.round(Math.log2(Z(t.opacityScale,1))*10)/10,nodeSize:1,linkWidth:1,center:Z(t.centerForce,.3),repel:Z(t.repelForce,.5)*10,linkForce:1,linkDistance:Z(t.linkDistance,30)}}var k=Vr(),lr={};function sr(t,s){s&&(lr[t]=s);var b=kr(lr[t]||{}),x=k[t]||{};for(var E in x)b[E]=x[E];for(var O in fe[t])b[O]=fe[t][O];return b}function he(t,s,b){if(Wr[s]){fe[t][s]=b;return}k[t]=k[t]||{},k[t][s]=b,ir(k)}function zr(t){delete k[t],ir(k),fe[t]={search:"",onlyMatches:!1}}function de(t){var s=String(t||"").trim();if(!s)return null;var b=s.match(/^(path|tag|file):\\s*(.*)$/i),x=b?b[1].toLowerCase():"text",E=(b?b[2]:s).trim().replace(/^"(.*)"$/,"$1").trim().toLowerCase();return E?function(O){var z=O.id.toLowerCase();if(x==="path"){var ve=E.replace(/\\s+/g,"-").replace(/^\\/+/,"").replace(/\\/+$/,"");return z===ve||z.startsWith(ve+"/")}if(x==="tag"){var P=E.replace(/^#/,"");if(z==="tags/"+P)return!0;for(var G=0;G<O.tags.length;G++){var I=String(O.tags[G]).toLowerCase();if(I===P||I.startsWith(P+"/"))return!0}return!1}var ge=String(O.text||"").toLowerCase();return x==="file"?ge.indexOf(E)!==-1:ge.indexOf(E)!==-1||z.indexOf(E.replace(/\\s+/g,"-"))!==-1}:null}function cr(t){return new Promise(function(s,b){var x=document.createElement("script");x.src=t,x.onload=s,x.onerror=b,document.head.appendChild(x)})}Promise.all([cr("https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"),cr("https://cdn.jsdelivr.net/npm/pixi.js@8/dist/pixi.js")]).then(function(){Ir()}).catch(function(t){console.error("[Graph] Failed to load libraries:",t)});function Ir(){var t=window.d3,s=window.PIXI;if(!t||!s){console.error("[Graph] Libraries not loaded");return}var b="graph-visited";function x(){try{return new Set(JSON.parse(localStorage.getItem(b)||"[]"))}catch{return new Set}}function E(r){var a=x();a.add(r);try{localStorage.setItem(b,JSON.stringify(Array.from(a)))}catch{}}function O(r){return r.classList.contains("global-graph-container")?"global":"local"}async function z(r,a,o){var n=$(a),c=x();if(nr(r),r.__runicGraph=null,o!==void 0&&o!==qe)return function(){};var l=JSON.parse(r.dataset.cfg||"{}"),h=O(r),d=sr(h,l),_=l.drag,Ve=l.zoom,re=h==="local"?d.depth:l.depth,F=l.scale||1,Jr=l.fontSize||.6,$r=l.removeTags||[],Br=d.showTags,Xr=l.focusOnHover,Yr=l.enableRadial,te=de(d.search),q;try{var wr=await fetchData;q=new Map;for(var Sr in wr)q.set($(Sr),wr[Sr])}catch(e){return console.error("[Graph] Error loading data:",e),function(){}}var C=r.offsetWidth,L=Math.max(r.offsetHeight,250),X=[],Ce=[],xr=new Set(q.keys());q.forEach(function(e,i){for(var u=e.links||[],f=0;f<u.length;f++){var v=$(u[f]);xr.has(v)&&X.push({source:i,target:v})}if(Br)for(var g=e.tags||[],f=0;f<g.length;f++){var T=g[f];if($r.indexOf(T)===-1){var N=$("tags/"+T);Ce.indexOf(N)===-1&&Ce.push(N),X.push({source:i,target:N})}}});var Le=new Set;if(re>=0)for(var Me=[n],Ee=new Set([n]),Cr=0;Cr<=re&&Me.length>0;Cr++){for(var ke=[],ze=0;ze<Me.length;ze++){var Ie=Me[ze];Le.add(Ie);for(var He=0;He<X.length;He++){var S=X[He];S.source===Ie&&!Ee.has(S.target)&&(Ee.add(S.target),ke.push(S.target)),S.target===Ie&&!Ee.has(S.source)&&(Ee.add(S.source),ke.push(S.source))}}Me=ke}else{xr.forEach(function(e){Le.add(e)});for(var p=0;p<Ce.length;p++)Le.add(Ce[p])}var y=[],Ke=new Map;Le.forEach(function(e){var i=e.startsWith("tags/"),u=i?"#"+e.substring(5):q.get(e)&&q.get(e).title||e,f=i?[]:q.get(e)&&q.get(e).tags||[],v={id:e,text:u,tags:f,x:Math.random()*C-C/2,y:Math.random()*L-L/2,vx:0,vy:0};d.onlyMatches&&te&&!te(v)&&e!==n||(y.push(v),Ke.set(e,v))});for(var Ge=[],R={},p=0;p<X.length;p++){var S=X[p],Je=Ke.get(S.source),$e=Ke.get(S.target);Je&&$e&&Je!==$e&&(Ge.push({source:Je,target:$e}),R[S.source]=(R[S.source]||0)+1,R[S.target]=(R[S.target]||0)+1)}d.showOrphans||(y=y.filter(function(e){return R[e.id]||e.id===n}));var H=getComputedStyle(document.documentElement),Dr=H.getPropertyValue("--secondary").trim()||"#c792ea",Be=H.getPropertyValue("--tertiary").trim()||"#82aaff",Ae=H.getPropertyValue("--gray").trim()||"#6c6c6c",Xe=H.getPropertyValue("--lightgray").trim()||"#d4d4d4",Ur=H.getPropertyValue("--dark").trim()||"#1a1a1a",Zr=H.getPropertyValue("--light").trim()||"#f5f5f5",Qr=H.getPropertyValue("--bodyFont").trim()||"inherit",K=new s.Application;await K.init({width:C,height:L,antialias:!0,backgroundAlpha:0,resolution:window.devicePixelRatio||1,autoDensity:!0,eventMode:"static"}),r.appendChild(K.canvas);var Y=new s.Container;K.stage.addChild(Y);function et(e){return 2+Math.sqrt(R[e.id]||0)}function Te(e){return et(e)*d.nodeSize}var A=t.forceSimulation(y).force("charge",t.forceManyBody()).force("center",t.forceCenter()).force("x",t.forceX()).force("y",t.forceY()).force("link",t.forceLink(Ge)).force("collide",t.forceCollide().iterations(3));if(Yr){var rt=Math.min(C,L)/2*.8;A.force("radial",t.forceRadial(rt).strength(.2))}function Lr(){A.force("charge").strength(-10*d.repel),A.force("x").strength(d.center*.1),A.force("y").strength(d.center*.1),A.force("link").distance(d.linkDistance).strength(function(e){return d.linkForce/Math.max(1,Math.min(R[e.source.id]||1,R[e.target.id]||1))}),A.force("collide").radius(Te)}Lr();var Mr=new s.Container,Er=new s.Container,Gr=new s.Container;Y.addChild(Mr),Y.addChild(Er),Y.addChild(Gr);var M=[],W=[],D=null,ae=new Set,Ar=0,_e=!1,m=t.zoomIdentity,ne=[],w=null;function Tr(){ne=[];for(var e=Array.isArray(d.groups)?d.groups:[],i=0;i<e.length;i++){var u=e[i]||{},f=de(u.query);f&&u.color&&ne.push({match:f,color:u.color})}}function tt(e){if(e.id===n)return Dr;for(var i=0;i<ne.length;i++)if(ne[i].match(e))return ne[i].color;return c.has(e.id)||e.id.startsWith("tags/")?Be:Ae}function _r(e){var i=e.simulationData,u=i.id.startsWith("tags/"),f=Te(i)*(w&&w.has(i.id)?1.3:1),v=tt(i);e.color=v,e.gfx.clear(),e.gfx.circle(0,0,f),e.gfx.fill({color:u?Zr:v}),u&&e.gfx.stroke({width:2,color:v===Be?Be:v})}function at(){var e=m.k*Math.pow(2,d.textFade);return Math.max(Math.min((e-1)/3.75,1),0)}function Ye(e){D=e,ae=new Set;for(var i=0;i<W.length;i++){var u=W[i].simulationData,f=e!==null&&(u.source.id===e||u.target.id===e);W[i].active=f,f&&(ae.add(u.source.id),ae.add(u.target.id))}e!==null&&ae.add(e);for(var i=0;i<M.length;i++)M[i].active=ae.has(M[i].simulationData.id)}function nt(){for(var e=0;e<W.length;e++){var i=W[e],u=i.simulationData,f=1;D!==null?f=i.active?1:.2:w&&(f=w.has(u.source.id)&&w.has(u.target.id)?1:.08),i.alpha=f,i.color=i.active?Ae:Xe}}function Or(){for(var e=1/F,i=e*1.1,u=at(),f=0;f<M.length;f++){var v=M[f],g=v.simulationData.id;D===g?(v.label.alpha=1,v.label.scale.set(i)):(v.label.scale.set(e),w?v.label.alpha=w.has(g)?1:0:D!==null&&v.active?v.label.alpha=Math.max(u,.8):v.label.alpha=u)}}function ot(){for(var e=0;e<M.length;e++){var i=M[e],u=1;D!==null&&Xr?u=i.active?1:.2:w&&(u=w.has(i.simulationData.id)?1:.15),i.gfx.alpha=u}}function oe(){ot(),nt(),Or()}function Fr(){if(!te)return w=null,0;w=new Set;for(var e=0;e<y.length;e++)te(y[e])&&w.add(y[e].id);return w.size}Tr(),Fr();for(var p=0;p<y.length;p++){var Oe=y[p],ie=new s.Text({text:Oe.text,style:{fontSize:Jr*15,fill:Ur,fontFamily:Qr},resolution:window.devicePixelRatio*4});ie.anchor.set(.5,1.2),ie.alpha=0,ie.scale.set(1/F),Gr.addChild(ie);var J=new s.Graphics;J.eventMode="static",J.cursor="pointer",J.label=Oe.id;var Pr={simulationData:Oe,gfx:J,label:ie,color:Ae,alpha:1,active:!1};_r(Pr),(function(i){J.on("pointerover",function(){Ye(i.id),_e||oe()}),J.on("pointerleave",function(){Ye(null),_e||oe()})})(Oe),Er.addChild(J),M.push(Pr)}for(var p=0;p<Ge.length;p++){var De=new s.Graphics;De.eventMode="none",Mr.addChild(De),W.push({simulationData:Ge[p],gfx:De,color:Xe,alpha:1,active:!1})}if(_){var it=function(e){for(var i=(e.x-m.x)/m.k,u=(e.y-m.y)/m.k,f=0;f<y.length;f++){var v=y[f],g=i-v.x-C/2,T=u-v.y-L/2;if(Math.sqrt(g*g+T*T)<Te(v)+5)return v}return null},lt=function(e){e.active||A.alphaTarget(1).restart(),e.subject.fx=e.subject.x,e.subject.fy=e.subject.y;var i=(e.x-m.x)/m.k-C/2,u=(e.y-m.y)/m.k-L/2;e.subject.__dragOffset={x:i-e.subject.x,y:u-e.subject.y},Ar=Date.now(),_e=!0,D=e.subject.id},st=function(e){var i=(e.x-m.x)/m.k-C/2,u=(e.y-m.y)/m.k-L/2;e.subject.fx=i-e.subject.__dragOffset.x,e.subject.fy=u-e.subject.__dragOffset.y},ct=function(e){e.active||A.alphaTarget(0),e.subject.fx=null,e.subject.fy=null,_e=!1,Ye(null),oe(),Date.now()-Ar<500&&(window.location.href=ar(e.subject.id))};t.select(K.canvas).call(t.drag().container(K.canvas).subject(it).on("start",lt).on("drag",st).on("end",ct))}else for(var p=0;p<M.length;p++)(function(i){i.gfx.on("click",function(){window.location.href=ar(i.simulationData.id)})})(M[p]);Ve&&t.select(K.canvas).call(t.zoom().extent([[0,0],[C,L]]).scaleExtent([.1,6]).on("zoom",function(e){m=e.transform,Y.scale.set(m.k,m.k),Y.position.set(m.x,m.y),Or()}));var jr=!1;function qr(){if(!jr){for(var e=0;e<M.length;e++){var i=M[e],u=i.simulationData.x,f=i.simulationData.y;u!=null&&f!=null&&(i.gfx.position.set(u+C/2,f+L/2),i.label.position.set(u+C/2,f+L/2))}for(var v=d.linkWidth,e=0;e<W.length;e++){var g=W[e],T=g.simulationData,N=T.source.x,Fe=T.source.y,le=T.target.x,se=T.target.y;if(!(N==null||Fe==null||le==null||se==null)&&(N+=C/2,Fe+=L/2,le+=C/2,se+=L/2,g.gfx.clear(),g.gfx.moveTo(N,Fe),g.gfx.lineTo(le,se),g.gfx.stroke({alpha:g.alpha,width:v,color:g.color}),d.arrows)){var Ue=le-N,Ze=se-Fe,Qe=Math.sqrt(Ue*Ue+Ze*Ze);if(Qe>.001){var ce=Ue/Qe,ue=Ze/Qe,Rr=Te(T.target),er=le-ce*Rr,rr=se-ue*Rr,V=2.5+v*1.5;g.gfx.poly([er,rr,er-ce*V*1.6-ue*V,rr-ue*V*1.6+ce*V,er-ce*V*1.6+ue*V,rr-ue*V*1.6-ce*V]),g.gfx.fill({alpha:g.alpha,color:g.active?Ae:Xe})}}}requestAnimationFrame(qr)}}return A.restart(),oe(),qr(),r.__runicGraph={kind:h,matches:w?w.size:null,nodeCount:y.length,apply:function(e,i){d=e,te=de(d.search),Tr();var u=Fr();this.matches=w?u:null,i==="forces"&&(Lr(),A.alpha(.6).restart());for(var f=0;f<M.length;f++)_r(M[f]);return oe(),this.matches},animate:function(){for(var e=0;e<y.length;e++)y[e].x=Math.random()*C-C/2,y[e].y=Math.random()*L-L/2,y[e].vx=0,y[e].vy=0;A.alpha(1).restart()}},pr(h),function(){jr=!0,A.stop(),r.__runicGraph=null;try{K.destroy(!0)}catch{}}}var ve='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>',P=["#e0a526","#3498db","#e67e22","#7f8c8d","#9b59b6","#1abc9c","#2ecc71","#e74c3c"];function G(r,a,o,n,c){return'<label class="rgp-range"><span>'+r+'</span><span class="rgp-range-row"><input type="range" data-key="'+a+'" min="'+o+'" max="'+n+'" step="'+c+'"><output data-out="'+a+'"></output></span></label>'}function I(r,a){return'<label class="rgp-toggle"><span>'+r+'</span><input type="checkbox" role="switch" data-key="'+a+'"></label>'}function ge(r){return'<div class="rgp-head"><span>'+(r==="global"?"Graph settings":"Local graph settings")+'</span><button type="button" data-act="reset" title="Reset to the site defaults">Reset</button><button type="button" data-act="close" title="Close" aria-label="Close">\\xD7</button></div><details open><summary>Filters</summary><input type="search" data-key="search" placeholder="Search notes\\u2026" title="Text, or path:Vision, tag:status/open, file:combat"><div class="rgp-hint" data-out="matches">path:Vision \\xB7 tag:status/open \\xB7 file:combat</div>'+I("Only matches","onlyMatches")+I("Tags","showTags")+I("Orphans","showOrphans")+(r==="local"?G("Depth","depth",1,5,1):"")+'</details><details open><summary>Groups</summary><div class="rgp-groups"></div><button type="button" class="rgp-wide" data-act="add-group">New group</button></details><details><summary>Display</summary>'+I("Arrows","arrows")+G("Text fade threshold","textFade",-3,3,.1)+G("Node size","nodeSize",.1,5,.1)+G("Link thickness","linkWidth",.1,5,.1)+'<button type="button" class="rgp-wide" data-act="animate">Animate</button></details><details><summary>Forces</summary>'+G("Center force","center",0,1,.01)+G("Repel force","repel",0,20,.1)+G("Link force","linkForce",0,1,.01)+G("Link distance","linkDistance",10,300,1)+"</details>"}function pe(r){var a=r==="global"?".global-graph-container":".graph-container";return Array.from(document.querySelectorAll(a))}function B(r){var a=pe(r)[0],o=a?JSON.parse(a.dataset.cfg||"{}"):void 0;return sr(r,o)}var ur={};function fr(r){clearTimeout(ur[r]),ur[r]=setTimeout(function(){r==="global"?ee()&&Ne():br()},250)}function Pe(r,a){var o=B(r),n=Nr[a]||"style";if(a==="search"&&o.onlyMatches&&(n="structure"),n==="structure"){fr(r);return}for(var c=pe(r),l=0;l<c.length;l++)c[l].__runicGraph&&c[l].__runicGraph.apply(o,n);pr(r)}function hr(r,a){return r==="depth"||r==="linkDistance"?String(Math.round(a)):Number(a).toFixed(2)}function dr(r,a){for(var o=B(a),n=r.querySelectorAll("[data-key]"),c=0;c<n.length;c++){var l=n[c],h=l.dataset.key;l.type==="checkbox"?l.checked=!!o[h]:l.type==="range"?l.value=String(o[h]):document.activeElement!==l&&(l.value=o[h]||"");var d=r.querySelector('[data-out="'+h+'"]');d&&(d.textContent=hr(h,o[h]))}je(r,a,o.groups||[]),vr(r,a)}function vr(r,a){var o=r.querySelector('[data-out="matches"]');if(o){var n=B(a),c=pe(a).filter(function(h){return h.__runicGraph})[0];if(!n.search||!de(n.search))o.textContent="path:Vision \\xB7 tag:status/open \\xB7 file:combat";else if(c){var l=n.onlyMatches?c.__runicGraph.nodeCount:c.__runicGraph.matches;o.textContent=l+(l===1?" matching note":" matching notes")}}}function je(r,a,o){var n=r.querySelector(".rgp-groups");!n||n.contains(document.activeElement)||(nr(n),o.forEach(function(c,l){var h=document.createElement("div");h.className="rgp-group",h.innerHTML='<input type="color" aria-label="Group color"><input type="text" placeholder="path:Vision" aria-label="Group query"><button type="button" title="Remove group" aria-label="Remove group">\\xD7</button>';var d=h.children[0],_=h.children[1],Ve=h.children[2];d.value=/^#[0-9a-f]{6}$/i.test(c.color||"")?c.color:P[l%P.length],_.value=c.query||"";function re(){var F=(B(a).groups||[]).slice();F[l]={query:_.value,color:d.value},he(a,"groups",F),Pe(a,"groups")}d.addEventListener("input",re),_.addEventListener("input",re),Ve.addEventListener("click",function(){var F=(B(a).groups||[]).slice();F.splice(l,1),he(a,"groups",F),je(r,a,F),Pe(a,"groups")}),n.appendChild(h)}))}function Hr(r,a){r.addEventListener("input",function(o){var n=o.target,c=n.dataset&&n.dataset.key;if(c){var l=n.type==="checkbox"?n.checked:n.type==="range"?Number(n.value):n.value;he(a,c,l);var h=r.querySelector('[data-out="'+c+'"]');h&&n.type==="range"&&(h.textContent=hr(c,l)),Pe(a,c)}}),r.addEventListener("click",function(o){var n=o.target.closest("[data-act]");if(n){var c=n.dataset.act;if(c==="close")r.hidden=!0;else if(c==="reset")zr(a),dr(r,a),fr(a);else if(c==="add-group"){var l=(B(a).groups||[]).slice();l.push({query:"",color:P[l.length%P.length]}),he(a,"groups",l),je(r,a,l);var h=r.querySelectorAll(".rgp-group input[type=text]");h.length&&h[h.length-1].focus()}else if(c==="animate")for(var d=pe(a),_=0;_<d.length;_++)d[_].__runicGraph&&d[_].__runicGraph.animate()}}),["keydown","wheel","pointerdown","mousedown","touchstart"].forEach(function(o){r.addEventListener(o,function(n){o==="keydown"&&n.key==="Escape"||n.stopPropagation()},{passive:!0})})}function gr(r,a){if(!(!r||r.querySelector(":scope > .runic-graph-panel"))){var o=document.createElement("button");o.type="button",o.className="runic-graph-gear runic-graph-gear-"+a,o.title="Graph settings",o.setAttribute("aria-label","Graph settings"),o.innerHTML=ve;var n=document.createElement("div");n.className="runic-graph-panel runic-graph-panel-"+a,n.hidden=!0,n.innerHTML=ge(a),o.addEventListener("click",function(c){c.stopPropagation(),n.hidden=!n.hidden,n.hidden||dr(n,a)}),Hr(n,a),r.appendChild(o),r.appendChild(n)}}function Kr(){for(var r=document.querySelectorAll(".graph-outer"),a=0;a<r.length;a++)gr(r[a],"local");for(var o=document.querySelectorAll(".global-graph-outer"),a=0;a<o.length;a++)gr(o[a],"global")}function pr(r){for(var a=document.querySelectorAll(".runic-graph-panel-"+r),o=0;o<a.length;o++)a[o].hidden||vr(a[o],r)}var me=[],ye=[],qe=0;function mr(){for(var r=0;r<me.length;r++)me[r]();me=[]}function Re(){for(var r=0;r<ye.length;r++)ye[r]();ye=[]}var j=[],Q=[],be=null,we=null,Se=null;function We(){Re();for(var r=0;r<j.length;r++){j[r].classList.remove("active");var a=j[r].closest(".sidebar");a&&(a.style.zIndex="")}}function ee(){for(var r=0;r<j.length;r++)if(j[r].classList.contains("active"))return!0;return!1}function Ne(){Re();for(var r=U(),a=0;a<j.length;a++){var o=j[a];o.classList.add("active");var n=o.closest(".sidebar");n&&(n.style.zIndex="1");var c=o.querySelector(".global-graph-container");c&&(function(l){z(l,r,void 0).then(function(h){ye.push(h)}).catch(function(h){console.error("[Graph] Global render error:",h)})})(c)}}function yr(){ee()?We():Ne()}function br(){mr();var r=++qe,a=U();E($(a));for(var o=document.querySelectorAll(".graph-container"),n=0;n<o.length;n++)(function(c){z(c,a,r).then(function(l){r===qe?me.push(l):l()}).catch(function(l){console.error("[Graph] Local render error:",l)})})(o[n])}function xe(r){var a=r.detail?r.detail.url:U();if(E($(a)),Kr(),br(),j=Array.from(document.querySelectorAll(".global-graph-outer")),Se)for(var o=0;o<Q.length;o++)Q[o].removeEventListener("click",Se);Q=Array.from(document.querySelectorAll(".global-graph-icon")),Se=function(){yr()};for(var o=0;o<Q.length;o++)Q[o].addEventListener("click",Se);be&&document.removeEventListener("click",be),be=function(n){if(ee()){var c=n.target.closest(".global-graph-container, .global-graph-icon, .runic-graph-panel, .runic-graph-gear");c||We()}},document.addEventListener("click",be),we&&document.removeEventListener("keydown",we),we=function(n){if(n.key==="Escape"){var c=document.querySelector(".runic-graph-panel:not([hidden])");if(c){c.hidden=!0;return}ee()&&We();return}n.key==="g"&&(n.ctrlKey||n.metaKey)&&!n.shiftKey&&(n.preventDefault(),yr())},document.addEventListener("keydown",we),ee()&&Ne()}document.readyState==="loading"?document.addEventListener("DOMContentLoaded",function(){xe({detail:{url:U()}})}):xe({detail:{url:U()}}),document.addEventListener("prenav",function(){mr(),Re()}),document.addEventListener("nav",xe),document.addEventListener("render",xe)}})();
`;

// src/components/Graph.tsx
import { jsx, jsxs } from "preact/jsx-runtime";
var defaultOptions = {
  localGraph: {
    drag: true,
    zoom: true,
    depth: 1,
    scale: 1.1,
    repelForce: 0.5,
    centerForce: 0.3,
    linkDistance: 30,
    fontSize: 0.6,
    opacityScale: 1,
    showTags: true,
    removeTags: [],
    focusOnHover: false,
    enableRadial: false
  },
  globalGraph: {
    drag: true,
    zoom: true,
    depth: -1,
    scale: 0.9,
    repelForce: 0.5,
    centerForce: 0.2,
    linkDistance: 30,
    fontSize: 0.6,
    opacityScale: 1,
    showTags: true,
    removeTags: [],
    focusOnHover: true,
    enableRadial: true
  }
};
var Graph_default = ((userOpts) => {
  const Graph = ({ displayClass, cfg }) => {
    const localGraph = { ...defaultOptions.localGraph, ...userOpts?.localGraph };
    const globalGraph = { ...defaultOptions.globalGraph, ...userOpts?.globalGraph };
    return /* @__PURE__ */ jsxs("div", { class: classNames(displayClass, "graph"), children: [
      /* @__PURE__ */ jsx("h3", { children: i18n(cfg.locale ?? "en-US").components.graph.title }),
      /* @__PURE__ */ jsxs("div", { class: "graph-outer", children: [
        /* @__PURE__ */ jsx("div", { class: "graph-container", "data-cfg": JSON.stringify(localGraph) }),
        /* @__PURE__ */ jsx("button", { class: "global-graph-icon", "aria-label": "Global Graph", children: /* @__PURE__ */ jsx(
          "svg",
          {
            version: "1.1",
            xmlns: "http://www.w3.org/2000/svg",
            xmlnsXlink: "http://www.w3.org/1999/xlink",
            x: "0px",
            y: "0px",
            viewBox: "0 0 55 55",
            fill: "currentColor",
            xmlSpace: "preserve",
            children: /* @__PURE__ */ jsx(
              "path",
              {
                d: "M49,0c-3.309,0-6,2.691-6,6c0,1.035,0.263,2.009,0.726,2.86l-9.829,9.829C32.542,17.634,30.846,17,29,17\n                s-3.542,0.634-4.898,1.688l-7.669-7.669C16.785,10.424,17,9.74,17,9c0-2.206-1.794-4-4-4S9,6.794,9,9s1.794,4,4,4\n                c0.74,0,1.424-0.215,2.019-0.567l7.669,7.669C21.634,21.458,21,23.154,21,25s0.634,3.542,1.688,4.897L10.024,42.562\n                C8.958,41.595,7.549,41,6,41c-3.309,0-6,2.691-6,6s2.691,6,6,6s6-2.691,6-6c0-1.035-0.263-2.009-0.726-2.86l12.829-12.829\n                c1.106,0.86,2.44,1.436,3.898,1.619v10.16c-2.833,0.478-5,2.942-5,5.91c0,3.309,2.691,6,6,6s6-2.691,6-6c0-2.967-2.167-5.431-5-5.91\n                v-10.16c1.458-0.183,2.792-0.759,3.898-1.619l7.669,7.669C41.215,39.576,41,40.26,41,41c0,2.206,1.794,4,4,4s4-1.794,4-4\n                s-1.794-4-4-4c-0.74,0-1.424,0.215-2.019,0.567l-7.669-7.669C36.366,28.542,37,26.846,37,25s-0.634-3.542-1.688-4.897l9.665-9.665\n                C46.042,11.405,47.451,12,49,12c3.309,0,6-2.691,6-6S52.309,0,49,0z M11,9c0-1.103,0.897-2,2-2s2,0.897,2,2s-0.897,2-2,2\n                S11,10.103,11,9z M6,51c-2.206,0-4-1.794-4-4s1.794-4,4-4s4,1.794,4,4S8.206,51,6,51z M33,49c0,2.206-1.794,4-4,4s-4-1.794-4-4\n                s1.794-4,4-4S33,46.794,33,49z M29,31c-3.309,0-6-2.691-6-6s2.691-6,6-6s6,2.691,6,6S32.309,31,29,31z M47,41c0,1.103-0.897,2-2,2\n                s-2-0.897-2-2s0.897-2,2-2S47,39.897,47,41z M49,10c-2.206,0-4-1.794-4-4s1.794-4,4-4s4,1.794,4,4S51.206,10,49,10z"
              }
            )
          }
        ) })
      ] }),
      /* @__PURE__ */ jsx("div", { class: "global-graph-outer", children: /* @__PURE__ */ jsx("div", { class: "global-graph-container", "data-cfg": JSON.stringify(globalGraph) }) })
    ] });
  };
  Graph.css = graph_default;
  Graph.afterDOMLoaded = graph_inline_default;
  return Graph;
});
export {
  Graph_default as Graph
};
