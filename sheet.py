import gspread
from google.oauth2.service_account import Credentials
import random
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Railway: use GOOGLE_CREDENTIALS environment variable.
# Local fallback: google/credentials.json
if "GOOGLE_CREDENTIALS" in os.environ:
    credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(
        credentials,
        scopes=SCOPES
    )
else:
    creds = Credentials.from_service_account_file(
        "google/credentials.json",
        scopes=SCOPES
    )

client = gspread.authorize(creds)

SHEET_ID = os.getenv(
    "GOOGLE_SHEET_ID",
    "16iCjst2Fib5w4e1SmfB_Lfm9nAx2Wz45w2q-NCfoh4Q"
)

print("Google Sheet ID:", SHEET_ID)

spreadsheet = client.open_by_key(SHEET_ID)
print("✅ Google Sheet connected successfully")
print("📄 Sheet:", spreadsheet.title)

sheet = spreadsheet.sheet1
print("📑 Worksheet:", sheet.title)


def generate_license():
    while True:
        key = str(random.randint(10000000, 99999999))
        try:
            sheet.find(key)
        except gspread.exceptions.CellNotFound:
            return key


def is_active(trader_id):
    trader_id = str(trader_id).strip()

    if not trader_id:
        return False

    values = sheet.get_all_values()

    for row in values[1:]:
        if len(row) >= 3:
            license_key = str(row[0]).strip()
            status = str(row[2]).strip().lower()

            if license_key == trader_id and status == "active":
                return True

    return False


def save_license(trader_id, country, deposit, plan):
    trader_id = str(trader_id).strip()
    plan = str(plan).strip()

    print("========================================")
    print("📝 SAVING LICENSE")
    print("🆔 Trader ID:", trader_id)
    print("👑 Plan:", plan)
    print("🌍 Country:", country)
    print("💰 Deposit:", deposit)
    print("========================================")

    if not trader_id:
        raise ValueError("Trader ID is empty")

    # Prevent duplicate active entries.
    if is_active(trader_id):
        print("⚠️ Trader ID already ACTIVE in Google Sheet:", trader_id)
        return trader_id

    row = [
        trader_id,
        plan,
        "Active",
        "",
        ""
    ]

    print("➡️ Appending row:", row)

    result = sheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )

    print("📌 Google Sheets append response:", result)

    # Verify that the ID was actually written.
    values = sheet.get_all_values()

    found = False
    for sheet_row in values[1:]:
        if len(sheet_row) >= 3:
            saved_id = str(sheet_row[0]).strip()
            status = str(sheet_row[2]).strip().lower()

            if saved_id == trader_id and status == "active":
                found = True
                print("✅ VERIFIED: Trader ID is ACTIVE in Google Sheet")
                print("🆔 Saved ID:", saved_id)
                print("🟢 Status:", sheet_row[2])
                print("👑 Plan:", sheet_row[1])
                break

    if not found:
        print("❌ VERIFY FAILED: Row was not found after append")
        raise RuntimeError(
            "Google Sheet append completed but ACTIVE Trader ID "
            "could not be verified."
        )

    print("========================================")
    return trader_id
