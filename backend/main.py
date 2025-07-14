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

# ✅ /start handler with WebApp button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📬 /start command received!")

    try:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🚀 Open Gem Hunters",
                        web_app=WebAppInfo(url="https://telegrambot-swart.vercel.app/")
                    )
                ]
            ]
        )
        await update.message.reply_text("Welcome! Launch the Mini App:", reply_markup=keyboard)
    except Exception as e:
        print(f"❌ Error sending /start message: {e}")

# Add handler
telegram_app.add_handler(CommandHandler("start", start))

# ✅ Webhook route — with proper initialization fix
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("Webhook received data:", data)
    update = Update.de_json(data, telegram_app.bot)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # 👇 REQUIRED fix to avoid RuntimeError
        loop.run_until_complete(telegram_app.initialize())
        loop.run_until_complete(telegram_app.process_update(update))
    finally:
        loop.close()

    return "ok", 200

# Home route
@app.route("/", methods=["GET"])
def home():
    return "Bot is live!", 200

# ✅ Set webhook at startup (one-time on each deploy)
async def setup():
    print("🔧 Initializing bot and setting webhook...")
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print("✅ Bot initialized & webhook set.")

# Run setup before Flask starts
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())

# ✅ Flask entrypoint (if run locally)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
