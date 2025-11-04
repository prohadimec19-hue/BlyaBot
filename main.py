# 8346062021:AAG3mxCGK5_7ZyAgXRg1QSdbGAt7NU9g3qg

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes, MessageHandler, filters
import random
from uuid import uuid4

TOKEN = "8346062021:AAG3mxCGK5_7ZyAgXRg1QSdbGAt7NU9g3qg"

# Загружаем предсказания из файла
with open("predictions.txt", encoding="utf-8") as f:
    predictions = [line.strip() for line in f if line.strip()]

# Загружаем особые предсказания
with open("special_predictions.txt", encoding="utf-8") as f:
    special_predictions = [line.strip() for line in f if line.strip()]


import random
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes

# --- Список особых пользователей ---
SPECIAL_USERS = {
    "mouse_pi314",       # Бля
    "naprimer_alina",    # Алина
    "Anarxusttt",        # Юра/Анархист
    "aagutova"           # Этери
}

# --- Особые предсказания ---
special_predictions = {}  # индивидуальные
general_special = []      # общие для всех особых

with open("special_predictions.txt", encoding="utf-8") as f:
    for line in f:
        if ":" in line:
            key, text = line.strip().split(":", 1)
            key = key.strip()
            text = text.strip()
            if key == "*":
                general_special.append(text)  # общие для всех особых
            else:
                special_predictions.setdefault(key, []).append(text)  # индивидуальные

# История предсказаний
user_history = {}

# --- Функция inline-запроса с поддержкой особых пользователей ---
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.inline_query.from_user
    user_id = user.id
    username = user.username or ""

    # История пользователя
    history = user_history.get(user_id, set())

    # 10% шанс получить спец. предсказание
    use_special = username in SPECIAL_USERS and random.random() < 0.1

    if use_special:
        available = [p for p in special_predictions.get(username, []) if p not in history]
        if not available:
            available = [p for p in general_special if p not in history]
        source = "🔥 особое"
    else:
        available = [p for p in predictions if p not in history]
        source = "🌑 обычное"

    # Если всё исчерпано, сбрасываем историю
    if not available:
        history.clear()
        if use_special:
            available = special_predictions.get(username, []) or general_special
        else:
            available = predictions

    choice = random.choice(available)
    history.add(choice)
    user_history[user_id] = history

    print(f"⚡ {username or user.first_name} получил {source} предсказание: {choice}")

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="😈 Ща погадаю",
            input_message_content=InputTextMessageContent(choice),
            description="Тыкай и все выясним..."
        )
    ]
    await update.inline_query.answer(results, cache_time=0)



# --- НОВАЯ ЧАСТЬ: обработка личных сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    # Сохраняем предложение пользователя в файл
    with open("user_predictions.txt", "a", encoding="utf-8") as f:
        f.write(f"{user.username or user.id}: {text}\n")
    # Отправляем пользователю ответ
    await update.message.reply_text("Спасибо бля! Чтоб я без тебя делала.")

# --- СОЗДАНИЕ И ДОБАВЛЕНИЕ ХЕНДЛЕРОВ ---
app = ApplicationBuilder().token(TOKEN).build()

# Хендлер для inline-запросов
app.add_handler(InlineQueryHandler(inline_query))

# Хендлер для личных сообщений
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота
app.run_polling()
