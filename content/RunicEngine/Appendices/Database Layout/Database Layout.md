---
title: "RunicEngine — Appendix: Database Layout"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
created: "2026-10-26"
modified: "2026-10-30"
---

Design appendix from the conversation of 26 October 2026, to be merged later into the technical architecture. It lays out every [[Physical layout Proposal|PostgreSQL]] schema, table and column, which service owns each, and where C++ and Go reach the database. Items built on existing decisions are marked as such; everything new is a Proposal until reviewed. Numbers are estimates for planning.  
Interactive map with relationship diagrams per schema: [Runic Database Map](https://claude.ai/artifact/GnVBh8fVBYPhck9onfEjRR)  
Size: 32 schemas, 167 tables, 1,042 columns.

## Contents

- [[Decisions this layout builds on|Decisions this layout builds on]]
- [[Physical layout Proposal|Physical layout (Proposal)]]
- [[Conventions Proposal|Conventions (Proposal)]]
- [[Where each thing lives|Where each thing lives]]
- [[Connections|Connections]]
  - [[Connections#C++ no database connection|C++: no database connection]]
  - [[Connections#What the simulation sends and receives|What the simulation sends and receives]]
  - [[Connections#Go one pool per service, one schema per service|Go: one pool per service, one schema per service]]
  - [[Connections#Numbers|Numbers]]
- [[Schemas|Schemas]]
- [[Differences from the Architecture v4 and the Vision|Differences from the Architecture v4 and the Vision]]
- [[Open (Database Layout)|Open]]

---

↑ [[index|RunicDocs]]  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) · exported 2026-11-03
