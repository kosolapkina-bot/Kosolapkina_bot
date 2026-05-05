from datetime import datetime, time as dtime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import random

TOKEN = "8769022359:AAFQzUiJoUQzJXDmYk54P2eo4OGecvZxgpk"
CHAT_ID = 311875077

PLAN = [
    ("03.05","Instagram","Svadba Stavropol","Reels 60s","Edem na svadbu. 1200 km. Dve dochki."),
    ("03.05","Telegram","Svadba Stavropol","Post","Pochemu ne boyus 1200 km s detmi"),
    ("05.05","Instagram","Ya ustala","Reels 7s","Vykhodnye ne spasut. Perestat zhdat."),
    ("05.05","Telegram","Ya ustala","Post","Zhdala vykhodnykh. Nichego ne izmenilos."),
    ("06.05","Instagram","Dochki","Clip","Sestra zamuzh. Starshaya podruzhka nevesty."),
    ("06.05","Telegram","Dochki","Post","Starshaya na svadbe. Smotryu i dumayu."),
    ("07.05","Instagram","Shpagat","Reels 75s","Sutulay sobaka. Probuyu shpagat v dekrete."),
    ("07.05","Telegram","Shpagat","Karusel","Obyavlyayu proekt. Mne uzhe strashno."),
    ("08.05","Instagram","Reshenie","Reels 60s","Umeyu sdavatsya. Imenno poetomu ne sdayus."),
    ("08.05","Telegram","Reshenie","Karusel","Derzhit strakh togo kak legko sdatsya."),
    ("09.05","Instagram","10 minut","Karusel","Ne znayu kak otdykhat bez sna."),
    ("09.05","Telegram","Telo Delo Dusha","Itog","Nedelya 1. Stavropol shpagat strakh."),
    ("12.05","Instagram","Otdykh","Reels 75s","Mozg ne umeet otdykhat. Nado uchit."),
    ("12.05","Telegram","Otdykh","Anons","Ne umeyu otdykhat. Obyavlyayu."),
    ("13.05","Instagram","Shpagat","Clip","Den 1 posle vozvrashcheniya. Telo net."),
    ("13.05","Telegram","Ya ustala","Post","Doekhal. Molchu. Khorosheye molchaniye."),
    ("14.05","Instagram","Dochki","Reels 90s","Ne znayu kak nazvat. No rabotayet."),
    ("14.05","Telegram","Dochki","Post","Ne zapomit slova. Zapomit razzhala li ruki."),
    ("19.05","Instagram","Otdykh 2","Reels","Sprosila otvetili. Tri varianta."),
    ("19.05","Telegram","Otdykh 3","Eksperiment","Tikhiy chas bez telefona. Otchet."),
    ("21.05","Instagram","Dekret","Reels 75s","Vozvrashchayus na rabotu. Strashno."),
    ("21.05","Telegram","Dekret","Longrid","Vykhod iz dekreta etapy plan"),
    ("27.05","Instagram","Shpagat","Clip","Mesyats shpagata. Chestnyy itog."),
    ("27.05","Telegram","Shpagat","Post","Chto izmenilos chto net chto ponyala"),
    ("30.05","Instagram","Telo Delo Dusha","Karusel","MAY. Itog mesyatsa."),
    ("30.05","Telegram","Telo Delo Dusha","Itog","MAY chestnyy itog."),
]

IDEAS = [
    "Morning before and after coffee - no words",
    "Honest fail this week - what it gave",
    "5 min on camera with daughter no script",
    "What you stopped doing in maternity leave",
    "One tool you cannot live without",
]

def today_posts():
    t = datetime.now().strftime("%d.%m")
    return [p for p in PLAN if p[0] == t]

def fmt(p):
    e = "Instagram" if p[1] == "Instagram" else "Telegram"
    return "[" + e + "] " + p[2] + "\nFormat: " + p[3] + "\nHook: " + p[4]

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("Today", callback_data="today")],
        [InlineKeyboardButton("Next 3 days", callback_data="soon")],
        [InlineKeyboardButton("Idea", callback_data="idea")],
    ]
    await update.message.reply_text("Hello. I know your content plan for May.", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "today":
        posts = today_posts()
        if not posts:
            await q.message.reply_text("Nothing planned for today.")
            return
        text = "Today " + datetime.now().strftime("%d.%m") + ":\n\n" + "\n\n".join(fmt(p) for p in posts)
        await q.message.reply_text(text)
    elif q.data == "soon":
        now = datetime.now()
        lines = []
        for p in PLAN:
            try:
                d, m = p[0].split(".")
                diff = (datetime(now.year, int(m), int(d)) - now).days
                if 0 <= diff <= 3:
                    label = "Today" if diff == 0 else ("Tomorrow" if diff == 1 else "In " + str(diff) + " days")
                    lines.append(label + "\n" + fmt(p))
            except:
                pass
        await q.message.reply_text("\n\n".join(lines) if lines else "Nothing upcoming.")
    elif q.data == "idea":
        await q.message.reply_text(random.choice(IDEAS))

async def msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text.lower()
    if "today" in t or "plan" in t:
        posts = today_posts()
        text = "Today:\n\n" + "\n\n".join(fmt(p) for p in posts) if posts else "Nothing today."
        await update.message.reply_text(text)
    elif "tomorrow" in t:
        now = datetime.now()
        try:
            tm = now.replace(day=now.day + 1).strftime("%d.%m")
        except:
            tm = ""
        posts = [p for p in PLAN if p[0] == tm]
        text = "Tomorrow:\n\n" + "\n\n".join(fmt(p) for p in posts) if posts else "Nothing tomorrow."
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Write today, tomorrow, or /start")

async def morning(ctx: ContextTypes.DEFAULT_TYPE):
    posts = today_posts()
    if posts:
        text = "Good morning. Today:\n\n" + "\n\n".join(fmt(p) for p in posts)
        await ctx.bot.send_message(CHAT_ID, text)

async def evening(ctx: ContextTypes.DEFAULT_TYPE):
    posts = today_posts()
    if posts:
        kb = [[InlineKeyboardButton("Yes", callback_data="done"), InlineKeyboardButton("No", callback_data="no")]]
        await ctx.bot.send_message(CHAT_ID, "Evening. " + str(len(posts)) + " posts. All published?", reply_markup=InlineKeyboardMarkup(kb))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(btn))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
app.job_queue.run_daily(morning, dtime(5, 30))
app.job_queue.run_daily(evening, dtime(18, 0))
app.run_polling()
