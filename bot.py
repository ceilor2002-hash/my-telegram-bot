import telebot
from datetime import datetime
import pytz
import sys

# ←←← ВСТАВЬ СВОЙ ТОКЕН
import os
API_TOKEN = os.getenv('8755035514:AAFlxYdkYY7YhgSngRnZ0qiTb7fshL5c3ZM') # Теперь бот будет брать токен из настроек Railway

# ←←← ВСТАВЬ СВОЙ chat_id (тот, который дал /getid)
YOUR_CHAT_ID = 5364533844   # ← обязательно замени на свой!

bot = telebot.TeleBot(TOKEN)
TARGET_DATE = datetime(2027, 10, 1).date()
moscow_tz = pytz.timezone('Europe/Moscow')

def get_days_left():
    today = datetime.now(moscow_tz).date()
    delta = TARGET_DATE - today
    return delta.days

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "✅ Бот работает через Scheduled Task.\n\n"
        "Каждый день в ~9:00 по Москве я присылаю уведомление.\n"
        "Команды: /days — показать сейчас"
    )

@bot.message_handler(commands=['days'])
def send_days(message):
    days = get_days_left()
    if days > 0:
        bot.reply_to(message, f"🔥 До 1 октября 2027 года осталось **{days} дней**!")
    elif days == 0:
        bot.reply_to(message, "🎉 Сегодня 1 октября 2027 года!")
    else:
        bot.reply_to(message, "📅 Дата уже прошла.")

@bot.message_handler(commands=['getid'])
def get_id(message):
    bot.reply_to(message, f"Твой chat_id: `{message.chat.id}`")

# === Главная функция для ежедневного уведомления ===
def send_daily_notification():
    days = get_days_left()
    try:
        if days > 0:
            bot.send_message(
                YOUR_CHAT_ID,
                f"🔔 Доброе утро!\n\nДо 1 октября 2027 года осталось **{days} дней** 🔥"
            )
        elif days == 0:
            bot.send_message(YOUR_CHAT_ID, "🎉 Сегодня 1 октября 2027 года!")
        else:
            bot.send_message(YOUR_CHAT_ID, "📅 1 октября 2027 уже прошло.")
        print(f"Уведомление отправлено успешно. Осталось дней: {days}")
    except Exception as e:
        print("Ошибка при отправке:", e)

# Если запускаем как Scheduled Task — сразу отправляем уведомление и выходим
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daily":
        send_daily_notification()
    else:
        # Если запускаешь вручную — запускаем polling (для команд)
        print("✅ Бот запущен в ручном режиме (polling)")
        bot.polling(none_stop=True)