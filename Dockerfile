# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри сервера
WORKDIR /app

# Копируем файл со списком библиотек
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код (ваш bot.py)
COPY . .

# Команда для запуска бота
CMD ["python", "bot.py"]