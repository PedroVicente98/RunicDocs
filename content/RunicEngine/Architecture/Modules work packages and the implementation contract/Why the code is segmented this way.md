---
title: "Why the code is segmented this way"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Why the code is segmented this way"
created: "2026-10-14"
modified: "2026-10-30"
---

* **A session builds well what it can hold in mind at once.** One package needs the module’s ARCHITECTURE.md, the public headers of the modules it depends on and its own code. When a session must also design an interface, change neighboring modules or juggle several subsystems, shortcuts and inconsistencies appear.

* **The design decision stays with you.** The public interface and the acceptance tests are written and approved before the implementation. The implementing session then solves a closed problem: make these tests pass inside this folder.

* **One package writes inside one module.** When it needs something elsewhere, it reports the interface change instead of making it, so changes never ripple silently across the codebase.

* **Reviewable size.** As a rule of thumb a package changes at most about 1,500 to 2,500 lines, which fits a careful review of about 30 minutes. Bigger changes get skimmed, and skimmed code is where defects hide.

* **Modules stay coarse on purpose.** Many tiny libraries add build, link and dependency overhead without making the code better. Big modules are split into packages, not into more libraries; a subsystem becomes its own module only when build isolation or reuse proves it necessary.

* **Progress is visible and testable.** Every roadmap slice lists the packages it needs, so done means specific packages merged with green tests.

* **Independent packages run in parallel.** Packages whose prerequisites are merged can be built at the same time in separate sessions.

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Sizes of work|Sizes of work]] · [[Module contract|Module contract]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Why the code is segmented this way · exported 2026-11-03
