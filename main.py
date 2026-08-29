from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN
from partner import get_trader_info
from sheet import save_license, is_active


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🚀 Create Quotex Account",
                url="https://broker-qx.pro/sign-up/?lid=2112381"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 Open Quotex Remix AI",
                url="https://www.quotexremixai.com/"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 API Support",
                url="https://t.me/AIQuotextrader"
            )
        ]
    ])

    await update.message.reply_text(
        """🤖 <b>Welcome to Quotex Remix AI</b>

🎁 <b>Get Lifetime AI Bot Access FREE</b>

📌 Steps

1️⃣ Create Quotex Account

2️⃣ Deposit Minimum <b>$30</b>

3️⃣ Send your Trader ID

4️⃣ API activates automatically after verification

👇 <b>Send your Quotex Trader ID now.</b>
""",
        parse_mode="HTML",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


async def trader(update: Update, context: ContextTypes.DEFAULT_TYPE):

    trader_id = update.message.text.strip()

    if not trader_id.isdigit():
        await update.message.reply_text(
            "❌ Please send a valid Trader ID."
        )
        return

    msg = await update.message.reply_text(
        "⏳ Checking your account..."
    )

    try:

        data = await get_trader_info(trader_id)

        print("========== DATA ==========")
        print(data)
        print("==========================")
                # -----------------------------
        # Affiliate Validation
        # -----------------------------

        if data["link_id"] != "2112381":

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🚀 Create Quotex Account",
                        url="https://broker-qx.pro/sign-up/?lid=2112381"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 API Support",
                        url="https://t.me/AIQuotextrader"
                    )
                ]
            ])

            await msg.edit_text(
"""❌ <b>Invalid Trader ID</b>

Your account is not registered using our Official api Link.

🎁 <b>Get FREE Lifetime Quotex Remix AI Access</b>

1️⃣ Create a new Quotex account

2️⃣ Deposit at least <b>$30</b>

3️⃣ Send your Trader ID here

👇 Click below to register.
""",
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )

            return


        # -----------------------------
        # Account Details
        # -----------------------------

        deposit = float(data["deposit"])
        balance = float(data["balance"])
        withdrawals = float(data["withdrawals"])

        net_deposit = deposit - withdrawals


        # -----------------------------
        # Net Deposit Validation
        # -----------------------------

        if net_deposit < 30 or balance <= 0:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Deposit Again",
                        url="https://broker-qx.pro/sign-up/?lid=2112381"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 API Support",
                        url="https://t.me/AIQuotextrader"
                    )
                ]
            ])

            await msg.edit_text(
f"""❌ <b>API Activation Failed</b>

Your account is not eligible.

━━━━━━━━━━━━━━

💰 Deposit : ${deposit:.2f}

💸 Withdrawals : ${withdrawals:.2f}

💵 Balance : ${balance:.2f}

📊 Net Deposit : ${net_deposit:.2f}

━━━━━━━━━━━━━━

⚠️ <b>Requirements</b>

• Net Deposit must be at least <b>$30</b>

• Balance must be greater than <b>$0</b>

Please deposit again and send your Trader ID.

💬 Support:
@AIQuotextrader
""",
                parse_mode="HTML",
                reply_markup=keyboard
            )

            return
                # -----------------------------
        # Already Active
        # -----------------------------

        if is_active(data["trader_id"]):

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🌐 Open Quotex Remix AI",
                        url="https://www.quotexremixai.com/"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 API Support",
                        url="https://t.me/AIQuotextrader"
                    )
                ]
            ])

            await msg.edit_text(
f"""⚠️ <b>API Already Activated</b>

🆔 <b>API ID</b>

<code>{data['trader_id']}</code>

This Trader ID already has an ACTIVE API.

🌐 https://www.quotexremixai.com/

💬 @AIQuotextrader
""",
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )

            return


        # -----------------------------
        # Membership
        # -----------------------------

        if deposit >= 1000:
            plan = "Elite"
        elif deposit >= 500:
            plan = "Ultra"
        elif deposit >= 200:
            plan = "Premium"
        elif deposit >= 100:
            plan = "Pro"
        elif deposit >= 30:
            plan = "Core"
        else:
            plan = None


        # -----------------------------
        # Deposit Validation
        # -----------------------------

        if plan is None:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Deposit Now",
                        url="https://broker-qx.pro/sign-up/?lid=2112381"
                    )
                ]
            ])

            await msg.edit_text(
"""❌ <b>Deposit Not Found</b>

Minimum Deposit Required

💰 <b>$30</b>

Complete your deposit and send your Trader ID again.
""",
                parse_mode="HTML",
                reply_markup=keyboard
            )

            return


        # -----------------------------
        # Save License
        # -----------------------------

        save_license(
            data["trader_id"],
            data["country"],
            deposit,
            plan
        )


        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🤖 Open Quotex Remix AI",
                    url="https://www.quotexremixai.com/"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 API Support",
                    url="https://t.me/AIQuotextrader"
                )
            ]
        ])

        await msg.edit_text(
f"""✅ <b>API Activated Successfully</b>

🔑 <b>Your API ID</b>

<code>{data['trader_id']}</code>

━━━━━━━━━━━━━━

🌍 Country
{data['country']}

💰 Deposit
${deposit:.2f}

💸 Withdrawals
${withdrawals:.2f}

💵 Balance
${balance:.2f}

📊 Net Deposit
${net_deposit:.2f}

👑 Membership
{plan}

🟢 Status
ACTIVE

━━━━━━━━━━━━━━

🚀 Open:
https://www.quotexremixai.com/

Use your <b>Trader ID as API ID</b>.

💬 Support:
@AIQuotextrader
""",
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )

    except Exception as e:

        print(e)

        await msg.edit_text(
            f"❌ Error\n\n<code>{e}</code>",
            parse_mode="HTML"
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        trader
    )
)

print("✅ Quotex Remix AI Bot Running...")

app.run_polling()
