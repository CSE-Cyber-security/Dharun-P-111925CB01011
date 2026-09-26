# Week 01 – Cybersecurity Asset Inventory System

A command-line Python application that lets a security administrator add,
search, update, delete, and display an organization's IT assets, and view a
security risk summary across the inventory.

## Problem Statement

Organizations maintain many IT assets — computers, servers, routers,
switches, and applications. Managing these manually makes it hard to track
security status and identify which assets need immediate attention. This
system classifies each asset by **type**, **risk level**, and **security
status** so at-risk assets are easy to spot.

## Features

- **Add Asset** — add a single asset with full input validation.
- **Add Multiple Assets** — bulk entry, mirrors the workflow in the project brief (`Enter number of assets: N`).
- **Search Asset** — look up an asset by Asset ID.
- **Update Asset** — edit any field of an existing asset; blank input keeps the current value.
- **Delete Asset** — remove an asset, with a confirmation prompt.
- **Display All Assets** — formatted inventory report with totals.
- **Security Summary** — counts by risk level / security status, plus a list of assets needing immediate attention (Critical or High risk, or Vulnerable status).
- **Persistence** — inventory is stored in `data/assets.json` and reloaded automatically on the next run.
- **Input validation** — Asset Type, Risk Level, and Security Status are restricted to fixed lists; IP addresses are validated as proper IPv4; Asset IDs must be unique and non-empty.

## Data Fields

| Field              | Notes                                                   |
|--------------------|----------------------------------------------------------|
| Asset ID           | Must be unique                                           |
| Asset Name         | Free text                                                 |
| Asset Type         | Workstation, Server, Router, Switch, Application          |
| IP Address         | Validated IPv4 format                                     |
| Operating System   | Free text                                                 |
| Owner/Department   | Free text                                                 |
| Risk Level         | Low, Medium, High, Critical                                |
| Security Status    | Secure, Warning, Vulnerable                                |

## Repository Structure

```
Week-01-Cybersecurity-Asset-Inventory/
│
├── src/
│   └── asset_inventory.py
│
├── data/
│   └── assets.json
│
├── tests/
│   └── test_cases.md
│
├── screenshots/
│   ├── 01-add-asset.png
│   ├── 02-display-assets.png
│   ├── 03-search-asset.png
│   ├── 04-update-asset.png
│   ├── 05-delete-asset.png
│   ├── 06-security-summary.png
│   └── 07-input-validation.png
│
└── README.md
```

> **Note on screenshots:** the `screenshots/` folder is included so the
> repository matches the required structure, but it is empty in this
> deliverable — screenshots need to be captured from your own terminal
> after running the program (see below) and dropped into that folder
> with the filenames shown above.

## How to Run

Requires Python 3.7+ (standard library only — no external dependencies).

```bash
cd src
python asset_inventory.py
```

The program starts with a sample 3-asset inventory already loaded
(A101, A102, A103, matching the project brief's sample input) so you can
try Search / Update / Delete / Display / Security Summary immediately.

## Sample Run

Choosing **6 (Display All Assets)** on first launch reproduces the exact
expected output from the project brief:

```
=========================================
 CYBERSECURITY ASSET INVENTORY
=========================================
Asset ID     : A101
Asset Name   : HR-PC-01
Asset Type   : Workstation
IP Address   : 192.168.1.10
OS           : Windows 11
Department   : HR
Risk Level   : Medium
Status       : Secure
-----------------------------------------
Asset ID     : A102
Asset Name   : Web-Server
Asset Type   : Server
IP Address   : 192.168.1.20
OS           : Ubuntu
Department   : IT
Risk Level   : Critical
Status       : Vulnerable
-----------------------------------------
Asset ID     : A103
Asset Name   : Core-Router
Asset Type   : Router
IP Address   : 192.168.1.1
OS           : Cisco IOS
Department   : Network
Risk Level   : High
Status       : Warning
=========================================
Total Assets      : 3
Critical Assets   : 1
High Risk Assets  : 1
Medium Risk Assets: 1
Low Risk Assets   : 0
Vulnerable Assets : 1
=========================================
```

## Testing

See [`tests/test_cases.md`](tests/test_cases.md) for 17 manual test cases
covering valid entry, invalid input handling (bad asset type, risk level,
security status, malformed IP, duplicate ID), search/update/delete on
existing and non-existent assets, empty-inventory display, and data
persistence across runs.
