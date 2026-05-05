import os
import traceback
from datetime import datetime
from supabase import create_client, Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

try:
    # ---------- SUPABASE ----------
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # ---------- BOT ----------
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Обработчик /start
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        sb.table("users").upsert({
            "user_id": user.id,
            "username": user.username,
            "source": "organic",
            "segment": "cold",
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        await update.message.reply_text("Привет! Я бот-воронка. Напиши свой запрос или имя.")

    # Обработчик текстовых сообщений (лиды)
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        text = update.message.text
        sb.table("leads").insert({
            "user_id": user.id,
            "name": user.full_name,
            "need": text,
            "area": "не указано",
            "city": "не указано",
            "phone": "не указано",
            "status": "new",
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        state = sb.table("funnel_state").select("*").eq("user_id", user.id).execute()
        if not state.data:
            sb.table("funnel_state").insert({
                "user_id": user.id,
                "day": 1,
                "started": True,
                "last_update": datetime.utcnow().isoformat()
            }).execute()
            await update.message.reply_text("Спасибо! Ты в воронке. День 1 начат.")
        else:
            await update.message.reply_text("Ты уже в воронке. Жди следующих шагов.")

    # Команда /segment — назначить сегмент
    async def set_segment_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Укажи сегмент: /segment warm")
            return
        segment = context.args[0]
        sb.table("users").update({"segment": segment}).eq("user_id", update.effective_user.id).execute()
        await update.message.reply_text(f"Сегмент изменён на {segment}")

    # Точка входа
    if __name__ == "__main__":
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("segment", set_segment_cmd))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("Бот запущен...")
        app.run_polling()

except Exception:
    print("ОШИБКА ЗАПУСКА:")
    traceback.print_exc()
