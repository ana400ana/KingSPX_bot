import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ChatMemberHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
INVITE_LINK = os.environ["INVITE_LINK"]
GROUP_ID = os.environ.get("GROUP_ID")  # اختياري

WELCOME_TEXT = """
أهلاً وسهلاً بك في ملوك سباكس 👋

نورت القروب 🌹
يرجى الالتزام بالقوانين واحترام الأعضاء.

بالتوفيق للجميع.
"""

app_web = Flask(__name__)

@app_web.get("/")
def home():
    return "KingSPX bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"أهلاً بك في ملوك سباكس 👋\n\nاضغط الرابط للدخول إلى القروب:\n{INVITE_LINK}"
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Chat ID:\n{update.effective_chat.id}")

async def member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = update.chat_member
    chat_id = str(chat_member.chat.id)

    if GROUP_ID and chat_id != str(GROUP_ID):
        return

    old_status = chat_member.old_chat_member.status
    new_status = chat_member.new_chat_member.status

    if old_status in ["left", "kicked"] and new_status in ["member", "administrator"]:
        user = chat_member.new_chat_member.user
        try:
            await context.bot.send_message(chat_id=user.id, text=WELCOME_TEXT)
        except Exception:
            pass

def main():
    threading.Thread(target=run_web, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(ChatMemberHandler(member_update, ChatMemberHandler.CHAT_MEMBER))

    app.run_polling(allowed_updates=["message", "chat_member"])

if __name__ == "__main__":
    main()
