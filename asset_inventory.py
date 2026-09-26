"""
Cybersecurity Asset Inventory System
--------------------------------------
Allows a security administrator to add, search, update, delete, and
display information about an organization's IT assets, and to view a
security summary (counts by risk level / security status).

Data is persisted to ../data/assets.json so the inventory survives
between runs.

Author: Weekly Mini Project - 01
"""

import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Configuration / constants
# ---------------------------------------------------------------------------

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "assets.json")

ASSET_TYPES = ["Workstation", "Server", "Router", "Switch", "Application"]
RISK_LEVELS = ["Low", "Medium", "High", "Critical"]
SECURITY_STATUSES = ["Secure", "Warning", "Vulnerable"]

IP_PATTERN = re.compile(
    r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
    r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
    r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
    r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def load_assets():
    """Load the asset list from the JSON data file. Returns [] if missing."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read existing data file. Starting fresh.")
        return []


def save_assets(assets):
    """Persist the asset list to the JSON data file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(assets, f, indent=4)


# ---------------------------------------------------------------------------
# Input validation helpers
# ---------------------------------------------------------------------------

def prompt_nonempty(label):
    """Prompt until the user enters a non-blank value."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"  -> {label} cannot be empty. Please try again.")


def prompt_choice(label, choices):
    """Prompt until the user enters one of the allowed choices (case-insensitive)."""
    choices_display = "/".join(choices)
    while True:
        value = input(f"{label} ({choices_display}): ").strip()
        for choice in choices:
            if value.lower() == choice.lower():
                return choice
        print(f"  -> Invalid {label}. Must be one of: {choices_display}")


def prompt_ip_address(label="IP Address"):
    """Prompt until the user enters a valid IPv4 address."""
    while True:
        value = input(f"{label}: ").strip()
        if IP_PATTERN.match(value):
            return value
        print("  -> Invalid IP address format. Expected e.g. 192.168.1.10")


def prompt_unique_asset_id(assets, label="Asset ID"):
    """Prompt until the user enters an Asset ID not already in use."""
    existing_ids = {a["Asset ID"].lower() for a in assets}
    while True:
        value = prompt_nonempty(label)
        if value.lower() in existing_ids:
            print(f"  -> Asset ID '{value}' already exists. Please use a unique ID.")
        else:
            return value


# ---------------------------------------------------------------------------
# Core features
# ---------------------------------------------------------------------------

def add_asset(assets):
    print("\n--- Add New Asset ---")
    asset_id = prompt_unique_asset_id(assets)
    asset_name = prompt_nonempty("Asset Name")
    asset_type = prompt_choice("Asset Type", ASSET_TYPES)
    ip_address = prompt_ip_address()
    operating_system = prompt_nonempty("Operating System")
    department = prompt_nonempty("Owner/Department")
    risk_level = prompt_choice("Risk Level", RISK_LEVELS)
    security_status = prompt_choice("Security Status", SECURITY_STATUSES)

    asset = {
        "Asset ID": asset_id,
        "Asset Name": asset_name,
        "Asset Type": asset_type,
        "IP Address": ip_address,
        "Operating System": operating_system,
        "Owner/Department": department,
        "Risk Level": risk_level,
        "Security Status": security_status,
    }
    assets.append(asset)
    save_assets(assets)
    print(f"Asset '{asset_id}' added successfully.\n")


def add_multiple_assets(assets):
    """Bulk-add flow that mirrors the sample input in the project brief."""
    while True:
        try:
            count = int(input("Enter number of assets: ").strip())
            if count > 0:
                break
            print("  -> Please enter a positive number.")
        except ValueError:
            print("  -> Please enter a valid whole number.")

    for i in range(1, count + 1):
        print(f"\nAsset {i}")
        add_asset(assets)


def find_asset(assets, asset_id):
    for asset in assets:
        if asset["Asset ID"].lower() == asset_id.lower():
            return asset
    return None


def search_asset(assets):
    print("\n--- Search Asset ---")
    if not assets:
        print("No assets in inventory.\n")
        return
    asset_id = prompt_nonempty("Enter Asset ID to search")
    asset = find_asset(assets, asset_id)
    if asset:
        print("\nAsset found:")
        print_asset(asset)
    else:
        print(f"No asset found with ID '{asset_id}'.\n")


def update_asset(assets):
    print("\n--- Update Asset ---")
    if not assets:
        print("No assets in inventory.\n")
        return
    asset_id = prompt_nonempty("Enter Asset ID to update")
    asset = find_asset(assets, asset_id)
    if not asset:
        print(f"No asset found with ID '{asset_id}'.\n")
        return

    print("Leave a field blank to keep its current value.")
    fields = [
        ("Asset Name", None),
        ("Asset Type", ASSET_TYPES),
        ("IP Address", "ip"),
        ("Operating System", None),
        ("Owner/Department", None),
        ("Risk Level", RISK_LEVELS),
        ("Security Status", SECURITY_STATUSES),
    ]
    for field, kind in fields:
        current = asset[field]
        if kind == "ip":
            value = input(f"{field} [{current}]: ").strip()
            if value:
                while not IP_PATTERN.match(value):
                    print("  -> Invalid IP address format.")
                    value = input(f"{field} [{current}]: ").strip()
                    if not value:
                        break
                if value:
                    asset[field] = value
        elif kind:
            choices_display = "/".join(kind)
            value = input(f"{field} [{current}] ({choices_display}): ").strip()
            if value:
                matched = next((c for c in kind if c.lower() == value.lower()), None)
                while matched is None:
                    print(f"  -> Invalid {field}. Must be one of: {choices_display}")
                    value = input(f"{field} [{current}] ({choices_display}): ").strip()
                    if not value:
                        break
                    matched = next((c for c in kind if c.lower() == value.lower()), None)
                if matched:
                    asset[field] = matched
        else:
            value = input(f"{field} [{current}]: ").strip()
            if value:
                asset[field] = value

    save_assets(assets)
    print(f"Asset '{asset_id}' updated successfully.\n")


def delete_asset(assets):
    print("\n--- Delete Asset ---")
    if not assets:
        print("No assets in inventory.\n")
        return
    asset_id = prompt_nonempty("Enter Asset ID to delete")
    asset = find_asset(assets, asset_id)
    if not asset:
        print(f"No asset found with ID '{asset_id}'.\n")
        return
    confirm = input(f"Are you sure you want to delete '{asset_id}'? (y/n): ").strip().lower()
    if confirm == "y":
        assets.remove(asset)
        save_assets(assets)
        print(f"Asset '{asset_id}' deleted successfully.\n")
    else:
        print("Deletion cancelled.\n")


# ---------------------------------------------------------------------------
# Display / reporting
# ---------------------------------------------------------------------------

def print_asset(asset):
    print(f"Asset ID     : {asset['Asset ID']}")
    print(f"Asset Name   : {asset['Asset Name']}")
    print(f"Asset Type   : {asset['Asset Type']}")
    print(f"IP Address   : {asset['IP Address']}")
    print(f"OS           : {asset['Operating System']}")
    print(f"Department   : {asset['Owner/Department']}")
    print(f"Risk Level   : {asset['Risk Level']}")
    print(f"Status       : {asset['Security Status']}")


def display_assets(assets):
    print("\n=========================================")
    print(" CYBERSECURITY ASSET INVENTORY")
    print("=========================================")

    if not assets:
        print("No assets to display.")
    else:
        for i, asset in enumerate(assets):
            print_asset(asset)
            if i < len(assets) - 1:
                print("-----------------------------------------")

    print("=========================================")
    print(f"Total Assets      : {len(assets)}")
    print(f"Critical Assets   : {count_by(assets, 'Risk Level', 'Critical')}")
    print(f"High Risk Assets  : {count_by(assets, 'Risk Level', 'High')}")
    print(f"Medium Risk Assets: {count_by(assets, 'Risk Level', 'Medium')}")
    print(f"Low Risk Assets   : {count_by(assets, 'Risk Level', 'Low')}")
    print(f"Vulnerable Assets : {count_by(assets, 'Security Status', 'Vulnerable')}")
    print("=========================================\n")


def count_by(assets, field, value):
    return sum(1 for a in assets if a[field] == value)


def security_summary(assets):
    print("\n--- Security Summary ---")
    if not assets:
        print("No assets in inventory.\n")
        return

    print("By Risk Level:")
    for level in RISK_LEVELS:
        print(f"  {level:<9}: {count_by(assets, 'Risk Level', level)}")

    print("By Security Status:")
    for status in SECURITY_STATUSES:
        print(f"  {status:<10}: {count_by(assets, 'Security Status', status)}")

    critical_or_vulnerable = [
        a for a in assets
        if a["Risk Level"] in ("Critical", "High") or a["Security Status"] == "Vulnerable"
    ]
    if critical_or_vulnerable:
        print("\nAssets needing immediate attention:")
        for a in critical_or_vulnerable:
            print(f"  - {a['Asset ID']} ({a['Asset Name']}): "
                  f"Risk={a['Risk Level']}, Status={a['Security Status']}")
    else:
        print("\nNo assets currently require immediate attention.")
    print()


# ---------------------------------------------------------------------------
# Menu / main loop
# ---------------------------------------------------------------------------

MENU = """
=========================================
 CYBERSECURITY ASSET INVENTORY SYSTEM
=========================================
1. Add Asset
2. Add Multiple Assets (bulk entry)
3. Search Asset
4. Update Asset
5. Delete Asset
6. Display All Assets
7. Security Summary
8. Exit
=========================================
"""


def main():
    assets = load_assets()
    print("Cybersecurity Asset Inventory System")
    print(f"Loaded {len(assets)} existing asset(s) from data file.")

    while True:
        print(MENU)
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_asset(assets)
        elif choice == "2":
            add_multiple_assets(assets)
        elif choice == "3":
            search_asset(assets)
        elif choice == "4":
            update_asset(assets)
        elif choice == "5":
            delete_asset(assets)
        elif choice == "6":
            display_assets(assets)
        elif choice == "7":
            security_summary(assets)
        elif choice == "8":
            print("Exiting. All changes have been saved. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number from 1 to 8.\n")


if __name__ == "__main__":
    main()
