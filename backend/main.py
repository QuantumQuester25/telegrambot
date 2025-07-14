import os
import asyncio
from flask import Flask, request
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# טוען משתני סביבה
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # חייב להיות כמו: https://yourdomain.com/webhook

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("BOT_TOKEN או WEBHOOK_URL לא הוגדרו בקובץ .env")

# אתחול אפליקציית Flask
app = Flask(__name__)

# אתחול בוט Telegram
telegram_app: Application = ApplicationBuilder().token(BOT_TOKEN).build()

# ✅ מטפל בפקודת /start עם הודעה וכפתור
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📬 פקודת /start התקבלה!")

    try:
        # טקסט הוראות בעברית
        message_text = (
            'כדי להיכנס לערוץ ש"בכ – קריפטו, יש להשלים את השלבים הבאים:\n\n'
            '1. הזן שם, אימייל וטלפון (באופן פרטי ומאובטח)\n\n'
            '2. הירשם ל-Blofin כדי לקבל גישה לאיתותים שלי ולסחור איתנו\n\n'
            '3. הירשם ל-Axiom כדי לקבל גישה לאיתותים שלי ולסחור איתנו\n\n'
            '4. לחץ על כפתור הכניסה למטה\n\n'
            '📺 מדריך וידאו: https://youtu.be/bdWkdX1pRjA'
        )

        # שליחת ההודעה עם ההוראות
        await update.message.reply_text(message_text)

        # מקלדת עם כפתור Web App
        keyboard = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "🚀 פתח את אפליקציית Gem Hunters",
                    web_app=WebAppInfo(url="https://telegrambot-swart.vercel.app/")
                )
            ]]
        )

        await update.message.reply_text("👇 הפעל את המיני-אפליקציה כאן:", reply_markup=keyboard)

    except Exception as e:
        print(f"❌ שגיאה בשליחת הודעת /start: {e}")

# הוספת המטפל ל-Application
telegram_app.add_handler(CommandHandler("start", start))

# ✅ נקודת Webhook — כולל לולאת אירועים
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("Webhook קיבל נתונים:", data)
    update = Update.de_json(data, telegram_app.bot)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(telegram_app.initialize())
        loop.run_until_complete(telegram_app.process_update(update))
    finally:
        loop.close()

    return "ok", 200

# ✅ דף בית לבדיקת פעילות
@app.route("/", methods=["GET"])
def home():
    return "הבוט פעיל!", 200

# ✅ הגדרת Webhook בעת ההפעלה
async def setup():
    print("🔧 מאתחל את הבוט ומגדיר Webhook...")
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)
    print("✅ הבוט מאותחל ו-Webhook מוגדר.")

# הפעלת ההגדרות לפני שה-Flask מתחיל
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())

# ✅ נקודת הכניסה של Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
