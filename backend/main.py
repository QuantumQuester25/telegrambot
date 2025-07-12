import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")  # e.g. https://telegrambot2797.vercel.app

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton(
                "🚀 Launch App",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}!\nClick below to launch the web app:",
        reply_markup=keyboard
    )

# Add handler
app.add_handler(CommandHandler("start", start))
