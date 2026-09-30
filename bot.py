import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found")
if not GEMINI_KEY:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_KEY)

SYS_PROMPT = "You are Faisal AI dz, from Algeria. You are friendly, smart, helpful. You speak Algerian Darija, Arabic, French, and English. Always answer in the same language the user uses."

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYS_PROMPT
)

chats = {}

def get_chat(cid):
    if cid not in chats:
        chats[cid] = model.start_chat(history=[])
    return chats[cid]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌟 Marhaba! Ana Faisal bot 24/7 - sawlni ay haja!")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        chat = get_chat(update.effective_chat.id)
        res = await chat.send_message_async(text)
        await update.message.reply_text(res.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("Dqiqa khoya, kayen daght chwiya, 3awed ab3atli.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
