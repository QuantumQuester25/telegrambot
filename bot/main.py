from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

sptoken = "7739973667:AAHeNLoO_11GEIJqN1aCRu8z9AoSYr82YSU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inline button pointing to your Vercel web app
    buttons = [
        [
            InlineKeyboardButton(
                "🚀 Launch App",
                web_app = WebAppInfo(url="https://telegrambot-kappa-one.vercel.app")
                               )
                               ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}!\nClick below to launch the web app:",
        reply_markup=keyboard
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(sptoken).build()
    app.add_handler(CommandHandler("start", start))
    print("🤖 Bot is running...")
    app.run_polling()
