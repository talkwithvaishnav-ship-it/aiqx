import gspread
from google.oauth2.service_account import Credentials
import random
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Railway + Local VS Code
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

# NEW GOOGLE SHEET
sheet = client.open_by_key(
    "16iCjst2Fib5w4e1SmfB_Lfm9nAx2Wz45w2q-NCfoh4Q"
).worksheet("Quotexbot2.0")


def generate_license():

    while True:

        key = str(random.randint(10000000, 99999999))

        try:
            sheet.find(key)

        except:
            return key


def is_active(trader_id):

    values = sheet.get_all_values()

    for row in values[1:]:

        if len(row) >= 1 and row[0] == str(trader_id):
            return True

    return False


def save_license(trader_id, country, deposit, plan):

    sheet.append_row([
        trader_id,
        plan,
        "Active",
        "",
        ""
    ])

    return trader_id
