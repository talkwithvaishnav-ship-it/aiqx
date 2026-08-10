import gspread
from google.oauth2.service_account import Credentials
import random
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Local VS Code + Railway Support
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

sheet = client.open_by_key(
    "1aQAEq-cc8DR9BNQT3s_QAzx86PTGLGI0jnWZ3mpeQCg"
).worksheet("Licenses")


# Generate License
def generate_license():

    while True:

        key = str(random.randint(10000000, 99999999))

        try:
            sheet.find(key)

        except:
            return key


# Check Trader Already Active
def is_active(trader_id):

    values = sheet.get_all_values()

    for row in values[1:]:

        if len(row) >= 2 and row[1] == str(trader_id):
            return True

    return False


# Save License
def save_license(trader_id, country, deposit, plan):

    sheet.append_row([
        trader_id,
        trader_id,
        plan,
        "active"
    ])

    return trader_id