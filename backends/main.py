from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import threading

# --- Telegram Bot Setup ---
sptoken = "7739973667:AAHeNLoO_11GEIJqN1aCRu8z9AoSYr82YSU"

bot_app = ApplicationBuilder().token(sptoken).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🚀 Launch App", web_app=WebAppInfo(url="https://telegrambot2797.vercel.app"))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}!\nClick below to launch the web app:",
        reply_markup=keyboard
    )

bot_app.add_handler(CommandHandler("start", start))

# --- Flask Backend Setup ---
flask_app = Flask(__name__)

@flask_app.route('/verify', methods=['POST'])
def verify_uid():
    uid = request.json.get('uid')

    headers = {
        "BF-API-KEY": "9c79690a9dc84a798be00d2d05b31e8d",
        "BF-API-SECRET": "7174cb58836543bca990e1e94325a93c",
        "BF-API-PASSPHRASE": "Shabak123",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get("https://api.blofin.com/api/v1/affiliate/invitees", headers=headers)
        data = response.json().get("data", [])
        match = next((i for i in data if str(i["userId"]) == uid), None)

        if match:
            return jsonify({"verified": True})
        else:
            return jsonify({"verified": False})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"verified": False, "error": "API error"}), 500

# --- Run Both Flask and Telegram Bot Together ---
def run_flask():
    flask_app.run(port=5000)

def run_telegram():
    print("🤖 Telegram Bot is running...")
    bot_app.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    run_telegram()
