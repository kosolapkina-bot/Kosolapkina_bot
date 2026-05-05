from datetime import datetime, time as dtime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import random

TOKEN = "8769022359:AAFQzUiJoUQzJXDmYk54P2eo4OGecvZxgpk"
CHAT_ID = 311875077

PLAN = [
    ("03.05","Instagram","Свадьба Ставрополь","Reels 60s","Едем на свадьбу. 1200 км. Две дочки."),
    ("03.05","Telegram","Свадьба Ставрополь","Пост","Почему не боюсь 1200 км с детьми"),
    ("05.05","Instagram","Я устала","Reels 7s","Выходные не спасут. Перестать ждать."),
    ("05.05","Telegram","Я устала","Пост","Ждала выходных. Ничего не изменилось."),
    ("06.05","Instagram","Дочки","Clip","Сестра замуж. Старшая подружка невесты."),
    ("06.05","Telegram","Дочки","Пост","Старшая на свадьбе. Смотрю и думаю."),
    ("07.05","Instagram","Шпагат","Reels 75s","Сутулая собака. Пробую шпагат в декрете."),
    ("07.05","Telegram","Шпагат","Карусель","Объявляю проект. Мне уже страшно."),
    ("08.05","Instagram","Решение","Reels 60s","Умею сдаваться. Именно поэтому не сдаюсь."),
    ("08.05","Telegram","Решение","Карусель","Держит страх того как легко сдаться."),
    ("09.05","Instagram","10 минут","Карусель","Не знаю как отдыхать без сна."),
    ("09.05","Telegram","Тело Дело Душа","Итог","Неделя 1. Ставрополь шпагат страх."),
    ("12.05","Instagram","Отдых","Reels 75s","Мозг не умеет отдыхать. Надо учить."),
    ("12.05","Telegram","Отдых","Анонс","Не умею отдыхать. Объявляю."),
    ("13.05","Instagram","Шпагат","Clip","День 1 после возвращения. Тело говорит нет."),
    ("13.05","Telegram","Я устала","Пост","Доехали. Молчу. Хорошее молчание."),
    ("14.05","Instagram","Дочки","Reels 90s","Не знаю как назвать. Но работает."),
    ("14.05","Telegram","Дочки","Пост","Не запомнит слова. Запомнит разжала ли руки."),
    ("19.05","Instagram","Отдых 2","Reels","Спросила вы ответили. Три варианта."),
    ("19.05","Telegram","Отдых 3","Эксперимент","Тихий час без телефона. Отчёт."),
    ("21.05","Instagram","Декрет","Reels 75s","Возвращаюсь на работу. Страшно."),
    ("21.05","Telegram","Декрет","Лонгрид","Выход из декрета этапы план"),
    ("27.05","Instagram","Шпагат","Clip","Месяц шпагата. Честный итог."),
    ("27.05","Telegram","Шпагат","Пост","Что изменилось что нет что поняла"),
    ("30.05","Instagram","Тело Дело Душа","Карусель","МАЙ. Итог месяца по триаде."),
    ("30.05","Telegram","Тело Дело Душа","Итог","МАЙ честный итог."),
]

IDEAS = [
    "Утро до и после кофе без слов только кадры",
    "Честный провал этой недели и что он дал",
    "5 минут в кадре с дочкой без сценария",
    "Что перестала делать в декрете и не жалеешь",
    "Один инструмент без которого не обходится день",
]

def today_posts():
    t = datetime.now().strftime("%d.%m")
    return [p for p in PLAN if p[0] == t]

def fmt(p):
    e = "Instagram" if p[1] == "Instagram" else "Telegram"
    return "[" + e + "] " + p[2] + "\nФормат: " + p[3] + "\nХук: " + p[4]

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("Сегодня", callback_data="today")],
        [InlineKeyboardButton("Ближайшие 3 дня", callback_data="soon")],
        [InlineKeyboardButton("Идея для поста", callback_data="idea")],
    ]
    await update.message.reply_text("Привет. Знаю твой контент-план на май. Напомню что публиковать.", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "today":
        posts = today_posts()
        if not posts:
            await q.message.reply_text("На сегодня в плане ничего нет.")
            return
        text = "Сегодня " + datetime.now().strftime("%d.%m") + ":\n\n" + "\n\n".join(fmt(p) for p in posts)
        await q.message.reply_text(text)
    elif q.data == "soon":
        now = datetime.now()
        lines = []
        for p in PLAN:
            try:
                d, m = p[0].split(".")
                diff = (datetime(now.year, int(m), int(d)) - now).days
                if 0 <= diff <= 3:
                    label = "Сегодня" if diff == 0 else ("Завтра" if diff == 1 else "Через " + str(diff) + " дня")
                    lines.append(label + "\n" + fmt(p))
            except:
                pass
        await q.message.reply_text("\n\n".join(lines) if lines else "Ближайших постов нет.")
    elif q.data == "idea":
        await q.message.reply_text(random.choice(IDEAS))

async def msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.lower()
    if any(w in t for w in ["сегодня", "план", "что постить"]):
        posts = today_posts()
        text = "Сегодня:\n\n" + "\n\n".join(fmt(p) for p in posts) if posts else "На сегодня ничего нет."
        await update.message.reply_text(text)
    elif "завтра" in t:
        now = datetime.now()
        try:
            tm = now.replace(day=now.day + 1).strftime("%d.%m")
        except:
            tm = ""
        posts = [p for p in PLAN if p[0] == tm]
        text = "Завтра:\n\n" + "\n\n".join(fmt(p) for p in posts) if posts else "Завтра ничего нет."
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Напиши сегодня, завтра или нажми /start")

async def morning(ctx: ContextTypes.DEFAULT_TYPE):
    posts = today_posts()
    if posts:
        text = "Доброе утро. Контент на сегодня:\n\n" + "\n\n".join(fmt(p) for p in posts)
        await ctx.bot.send_message(CHAT_ID, text)

async def evening(ctx: ContextTypes.DEFAULT_TYPE):
    posts = today_posts()
    if posts:
        kb = [[InlineKeyboardButton("Да всё", callback_data="done"), InlineKeyboardButton("Не всё", callback_data="no")]]
        await ctx.bot.send_message(CHAT_ID, "Вечерняя проверка. " + str(len(posts)) + " поста. Всё опубликовано?", reply_markup=InlineKeyboardMarkup(kb))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(btn))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
app.job_queue.run_daily(morning, dtime(5, 30))
app.job_queue.run_daily(evening, dtime(18, 0))
app.run_polling()
