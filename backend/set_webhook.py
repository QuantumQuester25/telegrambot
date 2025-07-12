# set_webhook.py

import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = "https://your-render-url.onrender.com"  # ⛔ Replace this with your actual Render app URL

webhook_url = f"{RENDER_URL}/webhook/{BOT_TOKEN}"

response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}"
)

print("Webhook set response:", response.json())
