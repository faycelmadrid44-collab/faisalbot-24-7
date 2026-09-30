import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

# الإعدادات
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logging.basicConfig(level=logging.INFO)

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا فيصل! أنا البوت تاعك راهو خدام 24/7 ✅")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("صرا خطأ، عاود جرب")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # هذا السيرفر باش Render ما يطيحش
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=HTTPServer(("0.0.0.0", port), H).serve_forever, daemon=True).start()

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
