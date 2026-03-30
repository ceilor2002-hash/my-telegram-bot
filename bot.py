import os
import telebot
import sys
import pytz
from datetime import datetime

# 1. Получаем токен из переменной окружения (настрой в Railway!)
TOKEN = os.getenv('8755035514:AAFlxYdkYY7YhgSngRnZ0qiTb7fshL5c3ZM')

# 2. Инициализируем бота
bot = telebot.TeleBot(TOKEN)

# 3. Твой chat_id
YOUR_CHAT_ID = 5364533844

TARGET_DATE = datetime(2027, 10, 1).date()
moscow_tz = pytz.timezone('Europe/Moscow')

def get_days_left():
    today = datetime.now(moscow_tz).date()
    delta = TARGET_DATE - today
    return delta.days

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "✅ Бот работает.\n\n"
        "Команды: /days — показать сколько осталось"
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
        print(f"Уведомление отправлено. Осталось дней: {days}")
    except Exception as e:
        print("Ошибка при отправке:", e)

if __name__ == "__main__":
    # Если запуск с аргументом --daily (для расписания)
    if len(sys.argv) > 1 and sys.argv[1] == "--daily":
        send_daily_notification()
    else:
        # Обычный запуск для ответов на команды
        print("✅ Бот запущен в режиме polling")
        bot.polling(none_stop=True)