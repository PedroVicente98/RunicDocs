---
title: "Supply chain and releases"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "Supply chain and releases"
created: "2026-10-22"
modified: "2026-10-22"
---

**Recent incidents.**

* **Shai-Hulud (npm, September and November 2025).** It started by phishing maintainers. Each infected package stole npm, GitHub, cloud and SSH credentials and published infected versions of the maintainer's other packages. The second wave ran before install and registered infected machines as GitHub Actions runners.
* **BoltDB typosquat (Go).** boltdb-go/bolt stayed in the Go module mirror for over three years. The attacker re-pointed the Git tag to clean code, so a manual review looked fine while the mirror kept serving the backdoor.
* **tj-actions/changed-files (March 2025).** A popular GitHub Action's tags were re-pointed to code that printed CI secrets into the logs.

**Defenses.**

* **CI ([[BUILD-1|BUILD-1]]):** Actions pinned to commit SHAs; read-only tokens by default; no secrets for pull requests from forks; SHA-256 pins for third-party sources (already the rule); go.sum with the checksum database, plus a check of the exact module path of every new dependency, since a typosquat passes the checksum; govulncheck; an update bot without auto-merge.
* **Owner settings:** branch protection on main, 2FA with a hardware key or passkey, no long-lived cloud keys on the development machine.
* **AI agents (Decision):** issues, pull requests and comments on the public repositories are untrusted text. An agent with push access never follows instructions written in them.
* **Releases ([[GAME-3|GAME-3]]):** builds and patch manifests signed with an offline key that never touches CI; the launcher verifies before running anything; Windows code signing. A compromised update server then cannot push code to players.

---

↑ [[Security|Security]] · ← [[DDoS|DDoS]] · [[Moderation|Moderation]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › Supply chain and releases · exported 2026-11-03
