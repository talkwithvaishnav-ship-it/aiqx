import gspread
from google.oauth2.service_account import Credentials
import random
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# =========================================================
# GOOGLE CREDENTIALS
# =========================================================

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


# =========================================================
# GOOGLE SHEET
# =========================================================

SHEET_ID = os.getenv(
    "GOOGLE_SHEET_ID",
    "16iCjst2Fib5w4e1SmfB_Lfm9nAx2Wz45w2q-NCfoh4Q"
)

print("Google Sheet ID:", SHEET_ID)

try:

    spreadsheet = client.open_by_key(SHEET_ID)

    print("✅ Google Sheet connected successfully")
    print("📄 Sheet:", spreadsheet.title)

except Exception as e:

    print("❌ GOOGLE SHEET CONNECTION FAILED")
    print("Error:", repr(e))

    raise


# First worksheet/tab
sheet = spreadsheet.sheet1


# =========================================================
# GENERATE LICENSE
# =========================================================

def generate_license():

    while True:

        key = str(random.randint(10000000, 99999999))

        try:

            sheet.find(key)

        except gspread.exceptions.CellNotFound:

            return key


# =========================================================
# CHECK ACTIVE
# =========================================================

def is_active(trader_id):

    trader_id = str(trader_id).strip()

    if not trader_id:

        return False

    values = sheet.get_all_values()

    for row in values[1:]:

        if len(row) >= 3:

            license_key = str(row[0]).strip()
            status = str(row[2]).strip().lower()

            if (
                license_key == trader_id
                and status == "active"
            ):

                return True

    return False


# =========================================================
# SAVE LICENSE
# =========================================================

def save_license(
    trader_id,
    country,
    deposit,
    plan
):

    sheet.append_row([
        str(trader_id),
        str(plan),
        "Active",
        "",
        ""
    ])

    return trader_id
