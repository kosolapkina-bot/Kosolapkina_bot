from datetime import datetime, time as dtime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import random

TOKEN = “8769022359:AAFQzUiJoUQzJXDmYk54P2eo4OGecvZxgpk”
CHAT_ID = 311875077

PLAN = [
(“03.05”,“Instagram”,“Свадьба в Ставрополе”,“Reels 60с”,“Мы едем на свадьбу. 1200 км. Две дочки.”),
(“03.05”,“Telegram”,“Свадьба в Ставрополе”,“Пост”,“Почему я не боюсь 1200 км с двумя детьми”),
(“05.05”,“Instagram”,“Я устала”,“Reels 7с”,“Выходные не спасут. Спасёт — перестать ждать”),
(“05.05”,“Telegram”,“Я устала”,“Пост”,“Я ждала выходных. Ничего не изменилось.”),
(“06.05”,“Instagram”,“Дочки”,“Clip”,“Сестра выходит замуж. Моя старшая — подружка невесты.”),
(“06.05”,“Telegram”,“Дочки”,“Пост”,“Моя старшая на свадьбе. Я смотрю — и думаю.”),
(“07.05”,“Instagram”,“Проект Шпагат”,“Reels 75с”,“Я сутулая собака. Пробую шпагат в декрете.”),
(“07.05”,“Telegram”,“Проект Шпагат”,“Карусель”,“Я объявляю проект. И мне уже страшно.”),
(“08.05”,“Instagram”,“Решение принято”,“Reels 60с”,“Я умею сдаваться. Именно поэтому — не сдаюсь.”),
(“08.05”,“Telegram”,“Решение принято”,“Карусель”,“Меня держит страх того, как легко сдаться.”),
(“09.05”,“Instagram”,“10 минут для себя”,“Карусель”,“Я не знаю, как отдыхать без сна.”),
(“09.05”,“Telegram”,“Тело Дело Душа”,“Итог недели”,“Неделя 1. Ставрополь, шпагат, страх лёгкого пути.”),
(“12.05”,“Instagram”,“Проект Отдых”,“Reels 75с”,“Мозг не умеет отдыхать сам. Его надо учить.”),
(“12.05”,“Telegram”,“Проект Отдых”,“Анонс+опрос”,“Я не умею отдыхать. Объявляю официально.”),
(“13.05”,“Instagram”,“Проект Шпагат”,“Clip”,“День 1 после возвращения. Тело говорит нет.”),
(“13.05”,“Telegram”,“Я устала”,“Пост”,“Доехали. Молчу. Это хорошее молчание.”),
(“14.05”,“Instagram”,“Дочки”,“Reels 90с”,“Я не знаю как это назвать. Но это работает.”),
(“14.05”,“Telegram”,“Дочки”,“Пост”,“Она не запомнит слова. Запомнит — разжала ли ты руки.”),
(“19.05”,“Instagram”,“Проект Отдых 2”,“Reels”,“Я спросила — вы ответили. Три варианта попробую.”),
(“19.05”,“Telegram”,“Проект Отдых 3”,“Эксперимент”,“Тихий час без телефона. Отчёт.”),
(“21.05”,“Instagram”,“Выход из декрета”,“Reels 75с”,“Возвращаюсь на работу. Мне страшно.”),
(“21.05”,“Telegram”,“Выход из декрета”,“Лонгрид”,“Выход из декрета: этапы, страхи, план”),
(“27.05”,“Instagram”,“Проект Шпагат”,“Clip”,“Месяц шпагата. Честный итог.”),
(“27.05”,“Telegram”,“Проект Шпагат”,“Пост”,“Месяц: что изменилось, что нет, что поняла”),
(“30.05”,“Instagram”,“Тело Дело Душа”,“Карусель”,“МАЙ. Итог месяца по триаде.”),
(“30.05”,“Telegram”,“Тело Дело Душа”,“Итог”,“МАЙ — честный итог.”),
]

IDEAS = [
“Покажи утро до и после кофе — без слов”,
“Честный провал этой недели — и что он дал”,
“5 минут в кадре с дочкой без сценария”,
“Что перестала делать в декрете — не жалеешь”,
“Один инструмент без которого не обходится день”,
]

def today_posts():
t = datetime.now().strftime(”%d.%m”)
return [p for p in PLAN if p[0] == t]

def fmt(p):
e = “📸” if p[1] == “Instagram” else “✈️”
return f”{e} *{p[1]}* · {p[2]}\n📝 {p[3]}\n💬 *{p[4]}*”

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
kb = [
[InlineKeyboardButton(“📅 Сегодня”, callback_data=“today”)],
[InlineKeyboardButton(“🔮 3 дня”, callback_data=“soon”)],
[InlineKeyboardButton(“💡 Идея”, callback_data=“idea”)],
]
await update.message.reply_text(
“Привет. Знаю твой контент-план на май. Напомню что публиковать.”,
reply_markup=InlineKeyboardMarkup(kb),
parse_mode=“Markdown”
)

async def btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
q = update.callback_query
await q.answer()
if q.data == “today”:
posts = today_posts()
if not posts:
await q.message.reply_text(“На сегодня ничего нет.”)
return
text = f”*Сегодня {datetime.now().strftime(’%d.%m’)}:*\n\n” + “\n\n”.join(fmt(p) for p in posts)
await q.message.reply_text(text, parse_mode=“Markdown”)
elif q.data == “soon”:
now = datetime.now()
lines = []
for p in PLAN:
try:
d, m = p[0].split(”.”)
diff = (datetime(now.year, int(m), int(d)) - now).days
if 0 <= diff <= 3:
label = “Сегодня” if diff == 0 else (“Завтра” if diff == 1 else f”Через {diff}д”)
lines.append(f”📌 *{label}*\n{fmt(p)}”)
except:
pass
await q.message.reply_text(”\n\n”.join(lines) if lines else “Ничего нет.”, parse_mode=“Markdown”)
elif q.data == “idea”:
await q.message.reply_text(f”💡 {random.choice(IDEAS)}”)

async def msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
t = update.message.text.lower()
if any(w in t for w in [“сегодня”, “план”, “что постить”]):
posts = today_posts()
text = “*Сегодня:*\n\n” + “\n\n”.join(fmt(p) for p in posts) if posts else “На сегодня ничего нет.”
await update.message.reply_text(text, parse_mode=“Markdown”)
elif “завтра” in t:
now = datetime.now()
try:
tm = now.replace(day=now.day + 1).strftime(”%d.%m”)
except:
tm = “”
posts = [p for p in PLAN if p[0] == tm]
text = “*Завтра:*\n\n” + “\n\n”.join(fmt(p) for p in posts) if posts else “Завтра ничего нет.”
await update.message.reply_text(text, parse_mode=“Markdown”)
else:
await update.message.reply_text(“Напиши ‘сегодня’, ‘завтра’ или /start”)

async def morning(ctx: ContextTypes.DEFAULT_TYPE):
posts = today_posts()
if posts:
text = “☀️ *Доброе утро:*\n\n” + “\n\n”.join(fmt(p) for p in posts)
await ctx.bot.send_message(CHAT_ID, text, parse_mode=“Markdown”)

async def evening(ctx: ContextTypes.DEFAULT_TYPE):
posts = today_posts()
if posts:
kb = [[InlineKeyboardButton(“✅ Да”, callback_data=“done”),
InlineKeyboardButton(“❌ Нет”, callback_data=“no”)]]
await ctx.bot.send_message(
CHAT_ID,
f”🌙 *Вечер.* {len(posts)} поста. Всё опубликовано?”,
parse_mode=“Markdown”,
reply_markup=InlineKeyboardMarkup(kb)
)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler(“start”, start))
app.add_handler(CallbackQueryHandler(btn))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
app.job_queue.run_daily(morning, dtime(5, 30))
app.job_queue.run_daily(evening, dtime(18, 0))
app.run_polling()
