import asyncio
from datetime import datetime, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = "8769022359:AAFQzUiJoUQzJXDmYk54P2eo4OGecvZxgpk"
CHAT_ID = 311875077

CONTENT_PLAN = [
    {"date": "03.05", "platform": "Instagram", "rubric": "Свадьба в Ставрополе", "format": "Reels · 60 сек", "hook": "Мы едем на свадьбу. 1200 км. Две дочки. Один муж."},
    {"date": "03.05", "platform": "Telegram", "rubric": "Свадьба в Ставрополе", "format": "Пост · 1200–1500 зн.", "hook": "Почему я не боюсь 1200 км с двумя детьми"},
    {"date": "05.05", "platform": "Instagram", "rubric": "Я устала", "format": "Reels · 5–7 сек", "hook": "Выходные не спасут. Спасёт — перестать ждать"},
    {"date": "05.05", "platform": "Telegram", "rubric": "Я устала", "format": "Пост · 1000 зн.", "hook": "Я ждала выходных. Они пришли. Ничего не изменилось."},
    {"date": "06.05", "platform": "Instagram", "rubric": "Дочки", "format": "Lifestyle clip", "hook": "Сестра выходит замуж. Моя старшая — подружка невесты."},
    {"date": "06.05", "platform": "Telegram", "rubric": "Дочки", "format": "Пост · 600–800 зн.", "hook": "Моя старшая на свадьбе сестры. Я смотрю — и думаю."},
    {"date": "07.05", "platform": "Instagram", "rubric": "Проект: Шпагат", "format": "Reels · 60–75 сек", "hook": "Я сутулая собака. И я снова пробую шпагат. В декрете."},
    {"date": "07.05", "platform": "Telegram", "rubric": "Проект: Шпагат", "format": "Карусель · 6 слайдов", "hook": "Я объявляю проект. И мне уже страшно."},
    {"date": "08.05", "platform": "Instagram", "rubric": "Решение принято", "format": "Reels · 45–60 сек", "hook": "Я умею сдаваться. Именно поэтому — не сдаюсь."},
    {"date": "08.05", "platform": "Telegram", "rubric": "Решение принято", "format": "Карусель · 6 слайдов", "hook": "Меня держит страх того, как легко сдаться."},
    {"date": "09.05", "platform": "Instagram", "rubric": "10 минут для себя", "format": "Карусель · 6 слайдов", "hook": "Я не знаю, как отдыхать. Без сна — вообще не знаю."},
    {"date": "09.05", "platform": "Telegram", "rubric": "Тело · Дело · Душа", "format": "Итог недели", "hook": "Неделя 1. Ставрополь, шпагат и страх лёгкого пути."},
    {"date": "12.05", "platform": "Instagram", "rubric": "Проект: Отдых", "format": "Reels · 60–75 сек", "hook": "Мозг не умеет отдыхать сам. Его надо учить."},
    {"date": "12.05", "platform": "Telegram", "rubric": "Проект: Отдых", "format": "Пост-анонс + опрос", "hook": "Я не умею отдыхать. Объявляю об этом официально."},
    {"date": "13.05", "platform": "Instagram", "rubric": "Проект: Шпагат", "format": "Lifestyle clip", "hook": "День 1 после возвращения. Тело говорит «нет»."},
    {"date": "13.05", "platform": "Telegram", "rubric": "Я устала", "format": "Пост · 800–1000 зн.", "hook": "Доехали. Молчу. Это хорошее молчание."},
    {"date": "14.05", "platform": "Instagram", "rubric": "Дочки", "format": "Reels · 60–90 сек", "hook": "Я не знаю, как это назвать. Но это работает."},
    {"date": "14.05", "platform": "Telegram", "rubric": "Дочки", "format": "Пост · 600–800 зн.", "hook": "Она не запомнит твои слова. Она запомнит — разжала ли ты руки первой."},
    {"date": "19.05", "platform": "Instagram", "rubric": "Проект: Отдых", "format": "Reels · 60 сек", "hook": "Я спросила — вы ответили. Три варианта, которые попробую."},
    {"date": "19.05", "platform": "Telegram", "rubric": "Проект: Отдых", "format": "Пост-эксперимент", "hook": "Эксперимент №1. Тихий час без телефона. Отчёт."},
    {"date": "21.05", "platform": "Instagram", "rubric": "Выход из декрета", "format": "Reels · 60–75 сек", "hook": "Я возвращаюсь на работу. Мне страшно."},
    {"date": "21.05", "platform": "Telegram", "rubric": "Выход из декрета", "format": "Лонгрид · Часть 1", "hook": "Выход из декрета как проект: этапы, страхи, план"},
    {"date": "27.05", "platform": "Instagram", "rubric": "Проект: Шпагат", "format": "Lifestyle clip", "hook": "Месяц шпагата. Честный итог."},
    {"date": "27.05", "platform": "Telegram", "rubric": "Проект: Шпагат", "format": "Пост-итог", "hook": "Месяц к шпагату: что изменилось, что нет, и что я поняла"},
    {"date": "30.05", "platform": "Instagram", "rubric": "Тело · Дело · Душа", "format": "Карусель · 6 слайдов", "hook": "МАЙ. Итог месяца по триаде."},
    {"date": "30.05", "platform": "Telegram", "rubric": "Тело · Дело · Душа", "format": "Итог месяца", "hook": "МАЙ — честный итог. Тело, дело, душа."},
]

def get_today_posts():
    today = datetime.now().strftime("%d.%m")
    return [p for p in CONTENT_PLAN if p["date"] == today]

def format_post(p):
    emoji = "📸" if p["platform"] == "Instagram" else "✈️"
    return f"{emoji} *{p['platform']}* · {p['rubric']}\n📝 {p['format']}\n💬 _{p['hook']}_"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 Сегодня", callback_data="today")],
        [InlineKeyboardButton("🔮 3 дня вперёд", callback_data="upcoming")],
        [InlineKeyboardButton("💡 Идея для поста", callback_data="idea")],
    ]
    await update.message.reply_text(
        "Привет. Знаю твой контент-план на май. Напомню что публиковать.",
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
        await query.message.reply_text(text if found else "Ближайших постов нет.", parse_mode="Markdown")
    elif query.data == "idea":
        import random
        ideas = [
            "Покажи утро до и после кофе — без слов",
            "Честный провал этой недели — и что он дал",
            "5 минут в кадре с дочкой без сценария",
            "Что перестала делать в декрете — и не жалеешь",
            "Один инструмент без которого не обходится день",
        ]
        await query.message.reply_text(f"💡 {random.choice(ideas)}")

async def morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    posts = get_today_posts()
    if not posts:
        return
    text = "☀️ *Доброе утро. Контент на сегодня:*\n\n"
    for p in posts:
        text += format_post(p) + "\n\n"
    await context.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown")

async def evening_check(context: ContextTypes.DEFAULT_TYPE):
    posts = get_today_posts()
    if not posts:
        return
    text = f"🌙 *Вечерняя проверка.* Сегодня {len(posts)} поста. Всё опубликовано?"
    keyboard = [[
        InlineKeyboardButton("✅ Да", callback_data="done"),
        InlineKeyboardButton("❌ Не всё", callback_data="notdone")
    ]]
    await context.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown",
                                    reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(w in text for w in ["сегодня", "план", "что постить"]):
        posts = get_today_posts()
        if posts:
            reply = "*Сегодня:*\n\n" + "\n\n".join(format_post(p) for p in posts)
            await update.message.reply_text(reply, parse_mode="Markdown")
        else:
            await update.message.reply_text("На сегодня в плане ничего нет.")
    elif "завтра" in text:
        today = datetime.now()
        try:
            tomorrow = today.replace(day=today.day + 1).strftime("%d.%m")
        except:
            tomorrow = ""
        posts = [p for p in CONTENT_PLAN if p["date"] == tomorrow]
        if posts:
            await update.message.reply_text("*Завтра:*\n\n" + "\n\n".join(format_post(p) for p in posts), parse_mode="Markdown")
        else:
            await update.message.reply_text("Завтра в плане ничего нет.")
    else:
        await update.message.reply_text("Напиши 'сегодня', 'завтра' или нажми /start")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_daily(morning_reminder, time=time(5, 30))
    app.job_queue.run_daily(evening_check, time=time(18, 0))
    app.run_polling()

if __name__ == "__main__":
    main()
