import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Must be like: https://yourdomain.com/webhook

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("BOT_TOKEN or WEBHOOK_URL not set in environment.")

# Flask app init
app = Flask(__name__)

# Telegram Application
telegram_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# ✅ /start handler with message + button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📬 /start command received!")

    try:
        # Hebrew instructions
        message_text = (
            'לכניסה לערוץ ש"בכ – קריפטו יש להשלים את השלבים הבאים:\n\n'
            '1. להזין שם, אימייל, טלפון (מאובטח באופן פרטי)\n\n'
            '2. להירשם עם Blofin כדי להיכנס לאיתותים שלי ולסחור איתנו\n\n'
            '3. להירשם עם Axiom כדי להיכנס לאיתותים שלי ולסחור איתנו\n\n'
            '4. להיכנס\n\n'
            '📺 צפה במדריך: https://youtu.be/bdWkdX1pRjA'
        )

        # Step message
        await update.message.reply_text(message_text)

        # WebApp button
        keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "🚀 Open Gem Hunters",
                    web_app=WebAppInfo(url="https://telegrambot-swart.vercel.app/")
                )
            ]]
        )

        await update.message.reply_text("👇 Launch the Mini App below:", reply_markup=keyboard)

    except Exception as e:
        print(f"❌ Error sending /start message: {e}")

# Add handler
telegram_app.add_handler(CommandHandler("start", start))

# ✅ Webhook route — with required event loop setup
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("Webhook received data:", data)
    update = Update.de_json(data, telegram_app.bot)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(telegram_app.initialize())
        loop.run_until_complete(telegram_app.process_update(update))
    finally:
        loop.close()

    return "ok", 200

# ✅ Home route
@app.route("/", methods=["GET"])
def home():
    return "Bot is live!", 200

# ✅ Set webhook on startup
async def setup():
    print("🔧 Initializing bot and setting webhook...")
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print("✅ Bot initialized & webhook set.")

# Run setup before Flask starts
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())

# ✅ Flask entrypoint
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
