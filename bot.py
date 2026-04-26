==============================================

FULL TELEGRAM BOT TEMPLATE WITH MENUS (AUTO-UNLOCK VERSION)

==============================================

FEATURES:

- Main menu system

- Content Locker integration

- Telegram deep link auto-unlock

- Auto content delivery (no fake confirmation button)

- Invite system

- Social links

==============================================

from telegram import ( Update, ReplyKeyboardMarkup )

from telegram.ext import ( ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters )

==============================================

CONFIG

==============================================

BOT_TOKEN = "8731154877:AAES_bPDVwaWGSs7yGFUfY8ySsN0woYmDak"

CONTENT LOCKER (CPA LINK)

SMART_LINK = "https://authenticateapp.online/cl/i/o4emw2"

TELEGRAM DEEP LINK FOR AUTO UNLOCK

UNLOCK_URL = "https://t.me/offerbridgebot?start=unlock"

LINKS

TELEGRAM_CHANNEL = "https://t.me/offerbridge" WHATSAPP_LINK = "https://wa.me/2347081356988" TIKTOK_LINK = "https://www.tiktok.com/@offer_bridge?_r=1&_t=ZS-95rXVNGsbFi" CONTACT_EMAIL = "donaldpanebi@gmail.com"

==============================================

MAIN MENU

==============================================

MAIN_MENU = ReplyKeyboardMarkup( [ ["🎮 Game Mods", "📚 Online Courses"], ["🛠 Free Tools", "📖 eBooks"], ["🎓 Study Tools"], ["👥 Invite Friends", "📱 Social Media"], ["📞 Contact Us"] ], resize_keyboard=True )

==============================================

START COMMAND (AUTO DETECT UNLOCK)

==============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user.first_name

# CHECK DEEP LINK PARAMETER
if context.args and "unlock" in context.args:
    await update.message.reply_text("🔓 Verified from content locker... delivering your content.")
    await send_content(update, context)
    return

message = f"""

Welcome {user}! 🚀

Choose an option below:

Game Mods

Online Courses

Free Tools

eBooks

Study Tools


Complete a quick task to unlock premium content. """

await update.message.reply_text(message, reply_markup=MAIN_MENU)

==============================================

CONTENT LOCKER FLOW

==============================================

async def send_smart_link(update: Update):

message = f"""

🔓 Unlock required:

Click below and complete one task:

{SMART_LINK}

After completion you will be redirected back automatically. """

await update.message.reply_text(message)

==============================================

MENU HANDLERS

==============================================

async def game_mods(update: Update, context: ContextTypes.DEFAULT_TYPE): await send_smart_link(update)

async def online_courses(update: Update, context: ContextTypes.DEFAULT_TYPE): await send_smart_link(update)

async def free_tools(update: Update, context: ContextTypes.DEFAULT_TYPE): await send_smart_link(update)

async def ebooks(update: Update, context: ContextTypes.DEFAULT_TYPE): await send_smart_link(update)

async def study_tools(update: Update, context: ContextTypes.DEFAULT_TYPE): await send_smart_link(update)

==============================================

AUTO CONTENT DELIVERY (NO FAKE BUTTON)

==============================================

async def send_content(update: Update, context: ContextTypes.DEFAULT_TYPE):

await update.message.reply_text(
    "🎉 Access granted! Here is your content:",
    reply_markup=MAIN_MENU
)

try:
    await update.message.reply_document(open("sample_ebook.pdf", "rb"))
except:
    await update.message.reply_text("eBook file missing.")

try:
    await update.message.reply_document(open("sample_course.pdf", "rb"))
except:
    await update.message.reply_text("Course file missing.")

==============================================

INVITE FRIENDS

==============================================

async def invite_friends(update: Update, context: ContextTypes.DEFAULT_TYPE): bot_username = context.bot.username invite_link = f"https://t.me/{bot_username}"

await update.message.reply_text(
    f"👥 Invite friends and grow rewards:\n{invite_link}"
)

==============================================

SOCIAL MEDIA

==============================================

async def social_media(update: Update, context: ContextTypes.DEFAULT_TYPE):

await update.message.reply_text(
    f"📱 Social Media:\n\nTelegram: {TELEGRAM_CHANNEL}\nWhatsApp: {WHATSAPP_LINK}\nTikTok: {TIKTOK_LINK}"
)

==============================================

CONTACT

==============================================

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):

await update.message.reply_text(f"📞 Email: {CONTACT_EMAIL}")

==============================================

MESSAGE HANDLER

==============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

text = update.message.text

if text == "🎮 Game Mods":
    await game_mods(update, context)

elif text == "📚 Online Courses":
    await online_courses(update, context)

elif text == "🛠 Free Tools":
    await free_tools(update, context)

elif text == "📖 eBooks":
    await ebooks(update, context)

elif text == "🎓 Study Tools":
    await study_tools(update, context)

elif text == "👥 Invite Friends":
    await invite_friends(update, context)

elif text == "📱 Social Media":
    await social_media(update, context)

elif text == "📞 Contact Us":
    await contact(update, context)

==============================================

MAIN

==============================================

def main(): app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()

if name == "main": main()
