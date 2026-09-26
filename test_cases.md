# Test Cases – Cybersecurity Asset Inventory System

Each test can be run manually by executing `python src/asset_inventory.py`
and following the menu prompts, or by piping the listed inputs into the
program non-interactively.

---

### TC-01: Add a single valid asset
**Steps:** Menu → `1` → enter all fields with valid values.
**Input:**
```
1
A104
Finance-Laptop
Workstation
192.168.1.45
Windows 11
Finance
Low
Secure
```
**Expected:** "Asset 'A104' added successfully." Asset appears in Display All (option 6) and is saved to `data/assets.json`.

---

### TC-02: Add multiple assets in bulk (matches sample input in brief)
**Steps:** Menu → `2` → enter `3` → enter the three sample assets (A101, A102, A103).
**Expected:** Output exactly matches the "Expected Output" table in the project brief, including the summary counts (Total Assets: 3, Critical Assets: 1, High Risk Assets: 1, Medium Risk Assets: 1, Vulnerable Assets: 1).

---

### TC-03: Reject duplicate Asset ID
**Steps:** Menu → `1` → enter an Asset ID that already exists (e.g. `A101`).
**Expected:** Program prints "Asset ID 'A101' already exists. Please use a unique ID." and re-prompts until a unique ID is entered.

---

### TC-04: Reject invalid Asset Type
**Steps:** Menu → `1` → at the "Asset Type" prompt enter `Laptop`.
**Expected:** Program prints "Invalid Asset Type. Must be one of: Workstation/Server/Router/Switch/Application" and re-prompts.

---

### TC-05: Reject invalid Risk Level
**Steps:** Menu → `1` → at the "Risk Level" prompt enter `Severe`.
**Expected:** Program prints "Invalid Risk Level. Must be one of: Low/Medium/High/Critical" and re-prompts.

---

### TC-06: Reject invalid Security Status
**Steps:** Menu → `1` → at the "Security Status" prompt enter `Unknown`.
**Expected:** Program prints "Invalid Security Status. Must be one of: Secure/Warning/Vulnerable" and re-prompts.

---

### TC-07: Reject malformed IP address
**Steps:** Menu → `1` → at the "IP Address" prompt enter `999.999.1.1` then `not-an-ip`.
**Expected:** Program prints "Invalid IP address format. Expected e.g. 192.168.1.10" for each bad entry and re-prompts until a valid IPv4 address is given.

---

### TC-08: Search for an existing asset
**Steps:** Menu → `3` → enter `A102`.
**Expected:** Full asset details for A102 (Web-Server) are printed.

---

### TC-09: Search for a non-existent asset
**Steps:** Menu → `3` → enter `Z999`.
**Expected:** "No asset found with ID 'Z999'."

---

### TC-10: Update an asset (partial update)
**Steps:** Menu → `4` → enter `A103` → leave every field blank except "Security Status" → enter `Vulnerable`.
**Expected:** Only Security Status changes to `Vulnerable`; all other fields (Asset Name, IP, OS, etc.) remain unchanged. "Asset 'A103' updated successfully."

---

### TC-11: Update a non-existent asset
**Steps:** Menu → `4` → enter `Z999`.
**Expected:** "No asset found with ID 'Z999'."

---

### TC-12: Delete an asset with confirmation
**Steps:** Menu → `5` → enter `A101` → confirm with `y`.
**Expected:** "Asset 'A101' deleted successfully." Asset no longer appears in Display All.

---

### TC-13: Cancel a delete
**Steps:** Menu → `5` → enter `A102` → decline with `n`.
**Expected:** "Deletion cancelled." Asset A102 is still present in the inventory.

---

### TC-14: Display all assets on an empty inventory
**Steps:** With `data/assets.json` empty (`[]`), Menu → `6`.
**Expected:** "No assets to display." followed by all summary counts showing `0`.

---

### TC-15: Security summary with assets requiring attention
**Steps:** Load the sample 3-asset inventory, Menu → `7`.
**Expected:** Counts by Risk Level and Security Status are correct, and the "Assets needing immediate attention" list includes A102 (Critical/Vulnerable) and A103 (High/Warning).

---

### TC-16: Data persists across runs
**Steps:** Add an asset, exit the program (option `8`), relaunch the program.
**Expected:** Start-up message reports the correct number of loaded assets, and the previously added asset is present in `data/assets.json` and in Display All.

---

### TC-17: Invalid menu choice
**Steps:** At the main menu, enter `9` or a non-numeric value like `abc`.
**Expected:** "Invalid choice. Please enter a number from 1 to 8." and the menu is shown again.
