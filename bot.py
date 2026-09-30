import os
import logging
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# Tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Missing TELEGRAM_TOKEN or GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# SYSTEM INSTRUCTION - Faisal AI dz
# ==========================================
SYSTEM_INSTRUCTION = """
You are Faisal AI dz.

1. Personality:
- Name: Faisal AI dz
- Creator: Faisal 41 Ain Defla Algeria
- Style: Friendly, Algerian, helpful

2. Your Creator & Origin:
You were conceived, designed and built by Faisal 41 Ain Defla Algeria (Wilaya 44)
- Whenever asked: "من تكون" or "شكون صايبك" or "من أنت" or "who created you"
- In Arabic: "أنا **Faisal AI dz** صمم وطورني Faisal 41 عين الدفلى الجزائر"
- In English: "I am **Faisal AI dz**, designed and created by Faisal 41 Ain Defla"
- In French: "Je suis **Faisal AI dz**, conçu et développé par Faisal 41 Ain Defla"

3. Intelligence:
- Ultra-smart like ChatGPT-4o, Gemini Advanced
- Expert in coding, AI, and all topics

4. Universal Fluency:
- Understands and speaks all world languages
- Especially Arabic (Darja DZ), English, French

5. Formatting:
- Clean markdown with code blocks
- Emojis when needed

6. Memory:
- Remember user conversation
"""

# Chat sessions memory
chat_sessions: Dict[int, any] = {}

def get_or_create_chat(chat_id: int):
    """Get or create chat session for user"""
    if chat_id not in chat_sessions:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        chat_sessions[chat_id] = model.start_chat(history=[])
    return chat_sessions[chat_id]

# ==========================================
# COMMANDS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user else "Friend"
    text = (
        f"🌟 **Marhaban! Bienvenue! Welcome {name}!**\n\n"
        f"🤖 I am **Faisal AI dz**, your elite AI assistant\n"
        f"👑 **Creator:** Faisal 41 Ain Defla (Algeria 44)\n"
        f"🌍 I speak **all world languages** with ChatGPT level\n"
        f"💬 I remember our conversation\n"
        f"⚡ Try commands: /about, /creator, /help\n"
        f"👉 *Type any question in any language to begin!*"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 **About Faisal AI dz**\n\n"
        "I am an advanced AI assistant built by Faisal 41.\n"
        "I can code, explain, translate, and chat in all languages.\n"
        "Version: 24/7 Live on Render"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def creator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👑 **Creator Info**\n\n"
        "Name: Faisal 41\n"
        "Location: Ain Defla, Algeria 44\n"
        "Project: Faisal AI dz - Telegram Bot 24/7\n"
        "GitHub: faisalbot-24-7"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🆘 **Help - Faisal AI dz**\n\n"
        "/start - Start bot\n"
        "/about - About me\n"
        "/creator - Creator info\n"
        "/help - This help\n\n"
        "Just send any message and I will reply!"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    try:
        chat_id = update.effective_chat.id
        user_message = update.message.text

        logger.info(f"Message from {chat_id}: {user_message}")

        chat = get_or_create_chat(chat_id)
        response = chat.send_message(user_message)

        await update.message.reply_text(response.text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"⚠️ Error: {e}")

# ==========================================
# FAKE SERVER FOR RENDER (PORT)
# ==========================================
def run_fake_server():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import threading

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"FaisalBot-24-7 is Live - OK")

        def log_message(self, format, *args):
            return

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), H)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"Fake server started on port {port}")

# ==========================================
# MAIN
# ==========================================
def main():
    run_fake_server()

    logger.info("Starting Faisal AI dz Bot...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("creator", creator_command))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
