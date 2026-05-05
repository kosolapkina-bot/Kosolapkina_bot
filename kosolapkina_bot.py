import asyncio
import json
import re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = "8769022359:AAFQzUiJoUQzJXDmYk54P2eo4OGecvZxgpk"
CHAT_ID = 311875077

CONTENT_PLAN = [
    {"date": "03.05", "platform": "Instagram", "rubric": "Проект: Свадьба в Ставрополе", "format": "Reels · 60 сек", "hook": "Мы едем на свадьбу. 1200 км. Две дочки. Один муж."},
    {"date": "03.05", "platform": "Telegram", "rubric": "Проект: Свадьба в Ставрополе", "format": "Пост · 1200–1500 зн.", "hook": "Почему я не боюсь 1200 км с двумя детьми"},
    {"date": "05.05", "platform": "Instagram", "rubric": "Я устала", "format": "Reels · 5–7 сек", "hook": "Выходные не спасут. Спасёт — перестать ждать"},
    {"date": "05.05", "platform": "Telegram", "rubric": "Я устала", "format": "Пост · 1000 зн.", "hook": "Я ждала выходных. Они пришли. Ничего не изменилось."},
    {"date": "06.05", "platform": "Instagram", "rubric": "Дочки", "format": "Lifestyle clip · 15–30 сек", "hook": "Сестра выходит замуж. Моя старшая — подружка невесты."},
    {"date": "06.05", "platform": "Telegram", "rubric": "Дочки", "format": "Пост · 600–800 зн.", "hook": "Моя старшая на свадьбе сестры. Я смотрю — и думаю."},
    {"date": "07.05", "platform": "Instagram", "rubric": "Проект: Шпагат", "format": "Reels · 60–75 сек", "hook": "Я сутулая собака. И я снова пробую шпагат. В декрете."},
    {"date": "07.05", "platform": "Telegram", "rubric": "Проект: Шпагат", "format": "Карусель · 6 слайдов", "hook": "Я объявляю проект. И мне уже страшно."},
    {"date": "08.05", "platform": "Instagram", "rubric": "Решение принято", "format": "Reels · 45–60 сек", "hook": "Я умею сдаваться. Именно поэтому — не сдаюсь."},
    {"date": "08.05", "platform": "Telegram", "rubric": "Решение принято", "format": "Карусель · 6 слайдов", "hook": "Меня держит страх того, как легко сдаться."},
    {"date": "09.05", "platform": "Instagram", "rubric": "10 минут для себя", "format": "Карусель · 6 слайдов", "hook": "Я не знаю, как отдыхать. Без сна — вообще не знаю."},
    {"date": "09.05", "platform": "Telegram", "rubric": "Тело · Дело · Душа", "format": "Итог недели", "hook": "Неделя 1. Ставрополь, шпагат и страх лёгкого пути."},
    {"date": "12.05", "platform": "Instagram", "rubric": "Проект: Отдых · Серия 1", "format": "Reels · 60–75 сек", "hook": "Мозг не умеет отдыхать сам. Его надо учить."},
    {"date": "12.05", "platform": "Telegram", "rubric": "Проект: Отдых · Старт", "format": "Пост-анонс + опрос", "hook": "Я не умею отдыхать. Объявляю об этом официально."},
    {"date": "13.05", "platform": "Instagram", "rubric": "Проект: Шпагат", "format": "Lifestyle clip · 15–30 сек", "hook": "День 1 после возвращения. Тело говорит «нет»."},
    {"date": "13.05", "platform": "Telegram", "rubric": "Я устала", "format": "Пост · 800–1000 зн.", "hook": "Доехали. Молчу. Это хорошее молчание."},
    {"date": "14.05", "platform": "Instagram", "rubric": "Дочки", "format": "Reels · 60–90 сек", "hook": "Я не знаю, как это назвать. Но это работает."},
    {"date": "14.05", "platform": "Telegram", "rubric": "Дочки", "format": "Пост · 600–800 зн.", "hook": "Она не запомнит твои слова. Она запомнит — разжала ли ты руки первой."},
    {"date": "15.05", "platform": "Instagram", "rubric": "Читаю / смотрю / думаю", "format": "Reels · 60–75 сек", "hook": "Я смотрела фильм. На первых минутах — слёзы."},
    {"date": "15.05", "platform": "Telegram", "rubric": "Дочки", "format": "Пост · 1200–1500 зн.", "hook": "Три дня я думаю об одном: как уберечь дочек."},
    {"date": "16.05", "platform": "Instagram", "rubric": "Тело · Дело · Душа", "format": "Карусель · 5 слайдов", "hook": "Неделя 2. Вернулась домой — и сразу в ритм."},
    {"date": "16.05", "platform": "Telegram", "rubric": "Тело · Дело · Душа", "format": "Итог недели", "hook": "Неделя 2 — возвращение и три больших вопроса"},
    {"date": "19.05", "platform": "Instagram", "rubric": "Проект: Отдых · Серия 2", "format": "Reels · 60 сек", "hook": "Я спросила — вы ответили. Три варианта, которые попробую."},
    {"date": "19.05", "platform": "Telegram", "rubric": "Проект: Отдых · Серия 3", "format": "Пост-эксперимент", "hook": "Эксперимент №1. Тихий час без телефона. Отчёт."},
    {"date": "20.05", "platform": "Instagram", "rubric": "Читаю / смотрю / думаю", "format": "Reels · 60–75 сек", "hook": "Врачи сказали: ты больше не будешь ходить. Он вышел на ринг через год."},
    {"date": "20.05", "platform": "Telegram", "rubric": "Решение принято", "format": "Пост · 1000–1200 зн.", "hook": "Все хотят, чтобы ты сдался. Я три дня думаю о своей жизни."},
    {"date": "21.05", "platform": "Instagram", "rubric": "Проект: Выход из декрета", "format": "Reels · 60–75 сек", "hook": "Я возвращаюсь на работу. Мне страшно."},
    {"date": "21.05", "platform": "Telegram", "rubric": "Проект: Выход из декрета", "format": "Лонгрид · Часть 1", "hook": "Выход из декрета как проект: этапы, страхи, план"},
    {"date": "22.05", "platform": "Instagram", "rubric": "Мамский стиль", "format": "Lifestyle clip · 15–30 сек", "hook": "В чём я вышла сегодня. Без постановки."},
    {"date": "22.05", "platform": "Telegram", "rubric": "10 минут для себя", "format": "Пост · 800–1000 зн.", "hook": "10 минут, которые я охраняю как государственную тайну"},
    {"date": "23.05", "platform": "Instagram", "rubric": "Тело · Дело · Душа", "format": "Карусель · 5 слайдов", "hook": "Неделя 3. Эксперименты, страхи и «Пазманский дьявол»."},
    {"date": "23.05", "platform": "Telegram", "rubric": "Сделай сейчас", "format": "Короткий пост", "hook": "Одно действие из триады — прямо сегодня"},
    {"date": "26.05", "platform": "Instagram", "rubric": "Проект: Отдых · Серия 4", "format": "Reels · 60–75 сек", "hook": "Я не хочу, чтобы она выросла и не знала, как отдыхать."},
    {"date": "26.05", "platform": "Telegram", "rubric": "Проект: Выход из декрета", "format": "Лонгрид · Часть 2", "hook": "Няня или сад: как я принимала решение без правильного ответа"},
    {"date": "27.05", "platform": "Instagram", "rubric": "Проект: Шпагат", "format": "Lifestyle clip · 15–30 сек", "hook": "Месяц шпагата. Честный итог."},
    {"date": "27.05", "platform": "Telegram", "rubric": "Проект: Шпагат", "format": "Пост-итог · 800–1000 зн.", "hook": "Месяц к шпагату: что изменилось, что нет, и что я поняла"},
    {"date": "28.05", "platform": "Instagram", "rubric": "Карусель: Ловушка «потом»", "format": "Карусель · 7 слайдов", "hook": "Я 3 года откладывала отпуск. Потом взяла детей — и улетела."},
    {"date": "28.05", "platform": "Telegram", "rubric": "Решение принято", "format": "Пост · 1000–1200 зн.", "hook": "3 вопроса, которые я задаю перед любым решением"},
    {"date": "29.05", "platform": "Instagram", "rubric": "Я устала", "format": "Reels · 5–7 сек", "hook": "Май был сложным. Май был настоящим."},
    {"date": "29.05", "platform": "Telegram", "rubric": "Я устала", "format": "Честный пост · 800–1000 зн.", "hook": "Май — месяц, когда я чаще хотела остановиться, чем продолжать"},
    {"date": "30.05", "platform": "Instagram", "rubric": "Тело · Дело · Душа", "format": "Карусель · 6 слайдов", "hook": "МАЙ. Итог месяца по триаде."},
    {"date": "30.05", "platform": "Telegram", "rubric": "Тело · Дело · Душа", "format": "Итог месяца", "hook": "МАЙ — честный итог. Тело, дело, душа."},
    {"date": "31.05", "platform": "Instagram", "rubric": "Карусель: Декрет и я", "format": "Карусель · 7 слайдов", "hook": "День сурка в декрете. Как я нахожу себя внутри него."},
    {"date": "31.05", "platform": "Telegram", "rubric": "Анонс июня", "format": "Пост-анонс · 800–1000 зн.", "hook": "Что будет в июне — проекты, эксперименты, честность"},
]

def get_today_posts():
    today = datetime.now().strftime("%d.%m")
    return [p for p in CONTENT_PLAN if p["date"] == today]

def format_post(p):
    emoji = "📸" if p["platform"] == "Instagram" else "✈️"
    return f"{emoji} *{p['platform']}* · {p['rubric']}\n📝 {p['format']}\n💬 _{p['hook']}_"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Контент сегодня", callback_data="today")],
        [InlineKeyboardButton("🔮 Ближайшие 3 дня", callback_data="upcoming")],
        [InlineKeyboardButton("💡 Идея для поста", callback_data="idea")],
    ]
    await update.message.reply_text(
        "Привет. Я знаю твой контент-план на май. Напомню что и когда публиковать.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "today":
        posts = get_today_posts()
        if not posts:
            await query.message.reply_text("На сегодня в плане ничего нет.")
            return
        text = f"*Сегодня — {datetime.now().strftime('%d.%m')}:*\n\n"
        for p in posts:
            text += format_post(p) + "\n\n"
        await query.message.reply_text(text, parse_mode="Markdown")
    elif query.data == "upcoming":
        today = datetime.now()
        text = "*Ближайшие посты:*\n\n"
        found = False
        for p in CONTENT_PLAN:
            try:
                d, m = p["date"].split(".")
                post_date = datetime(today.year, int(m), int(d))
                diff = (post_date - today).days
                if 0 <= diff <= 3:
                    label = "Сегодня" if diff == 0 else ("Завтра" if diff == 1 else f"Через {diff} дня")
                    text += f"📌 *{label}*\n{format_post(p)}\n\n"
                    found = True
            except:
                pass
        if not found:
            text = "Ближайших постов не найдено."
        await query.message.reply_text(text, parse_mode="Markdown")
    elif query.data == "idea":
        import random
        ideas = [
            "Покажи утро до и после кофе — без слов, только кадры",
            "Честный провал этой недели — и что он тебе дал",
            "5 минут в кадре с дочкой без сценария — просто жизнь",
            "Что ты перестала делать в декрете — и не жалеешь",
            "Один инструмент или привычка, без которой не обходится день",
        ]
        await query.message.reply_text(f"💡 {random.choice(ideas)}")

async def send_morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    posts = get_today_posts()
    if not posts:
        return
    text = f"☀️ *Доброе утро. Контент на сегодня:*\n\n"
    for p in posts:
        text += format_post(p) + "\n\n"
    await context.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown")

async def send_evening_check(context: ContextTypes.DEFAULT_TYPE):
    posts = get_today_posts()
    if not posts:
        return
    text = f"🌙 *Вечерняя проверка.* Сегодня было {len(posts)} поста. Всё опубликовано?"
    keyboard = [[InlineKeyboardButton("✅ Да", callback_data="done"), InlineKeyboardButton("❌ Не всё", callback_data="not_done")]]
    await context.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(w in text for w in ["сегодня", "план", "что постить"]):
        posts = get_today_posts()
        if posts:
            reply = f"*Сегодня по плану:*\n\n" + "\n\n".join(format_post(p) for p in posts)
            await update.message.reply_text(reply, parse_mode="Markdown")
        else:
            await update.message.reply_text("На сегодня в плане ничего нет.")
    elif "завтра" in text:
        today = datetime.now()
        tomorrow = (today.replace(day=today.day+1)).strftime("%d.%m")
        posts = [p for p in CONTENT_PLAN if p["date"] == tomorrow]
        if posts:
            reply = f"*Завтра:*\n\n" + "\n\n".join(format_post(p) for p in posts)
            await update.message.reply_text(reply, parse_mode="Markdown")
        else:
            await update.message.reply_text("Завтра в плане ничего нет.")
    else:
        await update.message.reply_text("Напиши 'сегодня', 'завтра' или нажми /start")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_daily(send_morning_reminder, time=datetime.strptime("08:30", "%H:%M").time())
    app.job_queue.run_daily(send_evening_check, time=datetime.strptime("21:00", "%H:%M").time())
    print("Бот запущен.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
