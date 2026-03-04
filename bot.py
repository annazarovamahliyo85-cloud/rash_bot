from flask import Flask, request, send_from_directory
import requests
import os

TOKEN = "8729054033:AAE2xeYYkXJfXl_msRabF_7R12hGjtffV-k"
BOT_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)
def send_message(chat_id, text, keyboard=None):
    data = {"chat_id": chat_id, "text": text}
    if keyboard:
        data["reply_markup"] = keyboard
    requests.post(BOT_URL + "sendMessage", json=data)

@app.route("/")
def home():
    return "Bot ishlayapti!"

@app.route("/webapp.html")
def webapp():
    return send_from_directory(".", "webapp.html")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.json

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]

        # /start bosilganda
        if update["message"].get("text") == "/start":
            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "📊 Testni boshlash",
                            "web_app": {
                                "url": os.environ.get("RENDER_EXTERNAL_URL") + "/webapp.html"
                            }
                        }
                    ]
                ]
            }

            send_message(chat_id, "Testni boshlash uchun bosing:", keyboard)

        # WebApp dan kelgan javob
        if "web_app_data" in update["message"]:
            data = update["message"]["web_app_data"]["data"]
            send_message(chat_id, f"📊 Javoblaringiz:\n{data}")

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
