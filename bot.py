import os, logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYS = "You are Faisal AI dz, designed and built by Faisal 41 Ain Defla Algeria. You are ultra-smart. You speak all languages."

chats = {}
def get_chat(cid):
    if cid not in chats:
        model = genai.GenerativeModel(model_name="gemini-3.8-flash", system_instruction=SYS)
        chats[cid] = model.start_chat(history=[])
    return chats[cid]

async def start(update, context):
    await update.message.reply_text("🌟 Marhaban! I am *Faisal AI dz* by Faisal 41 Ain Defla. Send me any question!", parse_mode="Markdown")

async def handle(update, context):
    try:
        c = get_chat(update.effective_chat.id)
        r = c.send_message(update.message.text)
        await update.message.reply_text(r.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def fake_server():
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
        def log_message(self,*a): return
    p=int(os.environ.get("PORT",10000))
    HTTPServer(("0.0.0.0",p),H).serve_forever

def main():
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"Live")
        def log_message(self,*a): return
    threading.Thread(target=lambda: HTTPServer(("0.0.0.0",int(os.environ.get("PORT",10000))),H).serve_forever(),daemon=True).start()
    app=ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle))
    app.run_polling()

if __name__=="__main__":
    main()
