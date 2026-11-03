---
title: "mail — Mail service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › mail — Mail service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Mail headers and claim state. Mail carries items; postage is charged per unit and grows with the item's tier or value, and claimed items go to the inventory or the global chest.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| mails | mail\_id bigint PK; sender\_id bigint ⇢ character.characters null; recipient\_id bigint ⇢ character.characters; subject text; body text; attachment\_container\_id bigint ⇢ ledger.containers null; postage bigint; cod\_amount bigint null; sent\_at timestamptz; opened\_at timestamptz null; claimed\_at timestamptz null; expires\_at timestamptz | Attachments travel in a ledger container owned by the mail. — sender\_id: null \= system mail; postage: per unit, weighted by tier or value |

---

↑ [[Schemas|Schemas]] · ← [[territory Territory service new|territory — Territory service (new)]] · [[guild Guild service|guild — Guild service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › mail — Mail service · exported 2026-11-03
