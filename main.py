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


# =========================================================
# /start
# =========================================================

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


# =========================================================
# TRADER ID VERIFICATION
# =========================================================

async def trader(update: Update, context: ContextTypes.DEFAULT_TYPE):

    trader_id = update.message.text.strip()

    # -----------------------------------------------------
    # Trader ID validation
    # -----------------------------------------------------

    if not trader_id.isdigit():

        await update.message.reply_text(
            "❌ Please send a valid Trader ID."
        )

        return

    # -----------------------------------------------------
    # Checking message
    # -----------------------------------------------------

    msg = await update.message.reply_text(
        "⏳ Checking your account..."
    )

    try:

        # -------------------------------------------------
        # Get trader information from partner bot
        # -------------------------------------------------

        data = await get_trader_info(trader_id)

        print("========== DATA ==========")
        print(data)
        print("==========================")

        # -------------------------------------------------
        # Affiliate Validation
        # -------------------------------------------------

        if data.get("link_id", "") != "2112381":

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

Your account is not registered using our Official API Link.

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

        # -------------------------------------------------
        # Account Details
        # -------------------------------------------------

        verified_trader_id = str(
            data.get("trader_id", "")
        ).strip()

        # If partner response doesn't contain ID,
        # use the ID submitted by the user.
        if not verified_trader_id:
            verified_trader_id = trader_id

        deposit = float(data.get("deposit", 0) or 0)
        balance = float(data.get("balance", 0) or 0)
        withdrawals = float(data.get("withdrawals", 0) or 0)

        net_deposit = deposit - withdrawals

        country = str(
            data.get("country", "")
        ).strip()

        # -------------------------------------------------
        # Basic Eligibility
        # -------------------------------------------------

        if net_deposit < 30 or balance < 30:

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

⚠️ <b>Minimum Requirements</b>

• Net Deposit must be at least <b>$30</b>

• Balance must be at least <b>$30</b>

Please deposit again and send your Trader ID.

💬 Support:
@AIQuotextrader
""",
                parse_mode="HTML",
                reply_markup=keyboard
            )

            return

        # -------------------------------------------------
        # Already Active Check
        # -------------------------------------------------

        if is_active(verified_trader_id):

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

<code>{verified_trader_id}</code>

This Trader ID already has an ACTIVE API.

🌐 https://www.quotexremixai.com/

💬 @AIQuotextrader
""",
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )

            return

        # -------------------------------------------------
        # MEMBERSHIP PLAN
        #
        # Plan requires BOTH:
        # Net Deposit AND Balance
        #
        # Core    = $30
        # Pro     = $100
        # Premium = $200
        # Ultra   = $500
        # Elite   = $1000
        # Master  = $2000
        # -------------------------------------------------

        if net_deposit >= 2000 and balance >= 2000:

            plan = "Master"

        elif net_deposit >= 1000 and balance >= 1000:

            plan = "Elite"

        elif net_deposit >= 500 and balance >= 500:

            plan = "Ultra"

        elif net_deposit >= 200 and balance >= 200:

            plan = "Premium"

        elif net_deposit >= 100 and balance >= 100:

            plan = "Pro"

        elif net_deposit >= 30 and balance >= 30:

            plan = "Core"

        else:

            plan = None

        # -------------------------------------------------
        # Plan Validation
        # -------------------------------------------------

        if plan is None:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Deposit Now",
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
                f"""❌ <b>Deposit / Balance Not Sufficient</b>

━━━━━━━━━━━━━━

💰 Deposit : ${deposit:.2f}

💸 Withdrawals : ${withdrawals:.2f}

📊 Net Deposit : ${net_deposit:.2f}

💵 Balance : ${balance:.2f}

━━━━━━━━━━━━━━

⚠️ <b>Minimum Requirement</b>

Net Deposit ≥ <b>$30</b>
Balance ≥ <b>$30</b>

Please deposit funds and try again.

💬 Support:
@AIQuotextrader
""",
                parse_mode="HTML",
                reply_markup=keyboard
            )

            return

        # -------------------------------------------------
        # Save License
        # -------------------------------------------------

        save_license(
            verified_trader_id,
            country,
            deposit,
            plan
        )

        # -------------------------------------------------
        # Success Keyboard
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Success Message
        # -------------------------------------------------

        await msg.edit_text(
            f"""✅ <b>API Activated Successfully</b>

🔑 <b>Your API ID</b>

<code>{verified_trader_id}</code>

━━━━━━━━━━━━━━

🌍 Country
{country}

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

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        print("========== ERROR ==========")
        print(repr(e))
        print("===========================")

        try:

            await msg.edit_text(
                """❌ <b>Something went wrong</b>

Please try again later or contact support.

💬 @AIQuotextrader
""",
                parse_mode="HTML"
            )

        except Exception:

            pass


# =========================================================
# BOT SETUP
# =========================================================

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        trader
    )
)


# =========================================================
# START BOT
# =========================================================

print("✅ Quotex Remix AI Bot Running...")

app.run_polling()
