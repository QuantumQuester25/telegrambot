from main import app as telegram_app
from verify_api import app as flask_app
import threading

def run_bot():
    print("🤖 Telegram bot running...")
    telegram_app.run_polling()

def run_api():
    print("🌐 Flask API running...")
    flask_app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_api).start()
