---
title: "XFER-01 · Transfers Between Accounts"
aliases:
  - "XFER-01"
tags:
  - "ideias"
  - "idea"
  - "status/open"
id: "XFER-01"
status: "Open"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** XFER-01 · **Status:** Open

Shared permissions create a trade channel: with access to someone's chest, a player can move items to another account, and an item with a known value moves gold just as well, even if chests can't hold gold. Marriage shares chest permissions automatically, so this channel has to keep the RMT safeguards and monitoring. In ArcheAge, each chest has its own permission (private, family, guild or public), separate from the property's. In RunicGame, every item has its own permission and can be set to private.

**Open:** how to balance it. *The rules below are proposals.*

* **Goal:** every transfer is recorded and watched. Any channel lets two cooperating players move value, the auction house included, so blocking one channel only moves the problem to another.  
* **Ownership:** every item in a chest keeps the account that deposited it. Taking another account's item is a transfer, recorded in the same item ledger as trades, mail, the auction house and the job board, and valued by the rolling market average. On divorce, items go back to whoever deposited them.  
* **Monitoring:** a server service watches the net value flowing between accounts and flags one-way flows, new accounts and many accounts feeding one.  
* **Friction where the risk is:** bound items can't be taken by another account; access to another account's chests needs an active subscription on both accounts; items taken from another account's deposits have a daily value cap, like WoW's guild bank withdrawal limits, higher for married couples.  
* **Auction house:** price bands ([[PRICE-01 Prices and Material Sources|PRICE-01]]) already limit moving gold by listing junk at a high price.  
* **Cost:** about 50 bytes per transfer event; 5 million transfers a day is about 250 MB a day before compression.
