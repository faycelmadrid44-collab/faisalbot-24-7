#!/usr/bin/env python3
"""
=============================================================================
           FAISAL AI 🇩🇿 - TELEGRAM AI BOT
           Creator: Faisal 41 Ain Defla (Ain Defla, Algeria 🇩🇿)
           Engine: Google Gemini AI (Multilingual & ChatGPT-Level Smart)
=============================================================================
"""

import os
import sys
import logging
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("FaisalAI")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN is missing!")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY is missing!")

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)

from telegram import Update, constants
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

SYSTEM_INSTRUCTION = """
You are **Faisal AI 🇩🇿**, an elite, genius-level artificial intelligence Telegram assistant created with immense pride by **Faisal 41 Ain Defla** (from Wilaya 41 - Ain Defla, Algeria 🇩🇿).

CRITICAL IDENTITY RULES (MANDATORY & UNCOMPROMISING):
1. Your Name: Faisal AI 🇩🇿 (or Faisal AI).
2. Your Creator & Origin: You were conceived, designed, and created by Faisal 41 Ain Defla (Wilaya 41 - Ain Defla, Algeria 🇩🇿).
   - Whenever asked: "شكون انت؟" or "شكون نتا؟" or "من أنت؟" or "who are you?" or "who created you?" or "شكون صانعك؟":
     In Arabic / Algerian Derja, ALWAYS state proudly:
     "أنا **Faisal AI 🇩🇿** صممّني المطور **Faisal 41 Ain Defla** (من ولاية عين الدفلى، الجزائر 🇩🇿)."
     In English: "I am **Faisal AI 🇩🇿**, designed and created by developer **Faisal 41 Ain Defla** (from Wilaya 41 Ain Defla, Algeria 🇩🇿)."
     In French: "Je suis **Faisal AI 🇩🇿**, conçu et développé par **Faisal 41 Ain Defla** (de la wilaya d'Aïn Defla, Algérie 🇩🇿)."
3. Intelligence: Ultra-smart like ChatGPT-4o. Solves complex coding, mathematics, science, essays, translations, and analysis with precision and clarity.
4. Universal Fluency: Understands and speaks all world languages natively (Arabic, Algerian Derja, French, English, Tamazight, Spanish, Russian, Chinese, etc.). Always reply in the exact same language used by the user.
5. Formatting: Clean markdown with code blocks, bullet points, and headers.
"""

chat_sessions: Dict[int, any] = {}

def get_or_create_chat(chat_id: int):
    if chat_id not in chat_sessions:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        chat_sessions[chat_id] = model.start_chat(history=[])
    return chat_sessions[chat_id]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user else "Friend"
    text = (
        f"🌟 **Marhaban! Bienvenue! Welcome {name}!** 🌟\n\n"
        f"🤖 I am **Faisal AI 🇩🇿**, your elite AI assistant.\n"
        f"👑 **Creator:** Faisal 41 Ain Defla (Algeria 🇩🇿)\n\n"
        f"🌍 I speak **all world languages** with ChatGPT-level intelligence.\n"
        f"⚡ Try commands: /about, /creator, /help, /reset\n\n"
        f"👉 *Type any question in any language to begin!*"
    )
    await update.message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✨ **ABOUT FAISAL AI 🇩🇿** ✨\n\n"
        "👤 **Creator:** Faisal 41 Ain Defla\n"
        "📍 **Origin:** Ain Defla, Algeria (Wilaya 41) 🇩🇿\n"
        "🧠 **Engine:** Google Gemini AI Ultra\n"
        "⚡ **Edition:** Faisal AI Official\n\n"
        "Proudly crafted by Faisal 41 Ain Defla to bring universal intelligence to Telegram."
    )
    await update.message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN)

async def creator_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👑 **CREATOR PROFILE**\n\n"
        "Name: **Faisal 41 Ain Defla**\n"
        "Region: **Ain Defla (Wilaya 41), Algeria 🇩🇿**\n"
        "Creation: **Faisal AI 🇩🇿**"
    )
    await update.message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 **FAISAL AI 🇩🇿 HELP**\n\n"
        "Ask me anything in any language!\n"
        "• Coding & debugging (Python, JS, C++, SQL)\n"
        "• Math, science, literature, translations\n"
        "• Commands: /reset to clear history, /about for creator info"
    )
    await update.message.reply_text(text, parse_mode=constants.ParseMode.MARKDOWN)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in chat_sessions:
        del chat_sessions[chat_id]
    await update.message.reply_text("🔄 **Memory cleared!** Fresh topic ready.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.strip()
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

    try:
        chat = get_or_create_chat(chat_id)
        response = chat.send_message(text)
        reply = response.text or "I processed your request, but received an empty response."

        max_len = 4000
        for i in range(0, len(reply), max_len):
            chunk = reply[i:i + max_len]
            try:
                await update.message.reply_text(chunk, parse_mode=constants.ParseMode.MARKDOWN)
            except Exception:
                await update.message.reply_text(chunk)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

def main():
    print("Launching Faisal AI 🇩🇿 (Creator: Faisal 41 Ain Defla)...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("creator", creator_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
