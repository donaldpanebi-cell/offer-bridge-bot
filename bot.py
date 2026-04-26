import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- CONFIG ---
# Replace with your actual token
BOT_TOKEN = "8731154877:AAES_bPDVwaWGSs7yGFUfY8ySsN0woYmDak"

# CONTENT LOCKER (CPA LINK)
SMART_LINK = "https://authenticateapp.online/cl/i/o4emw2"

# TELEGRAM DEEP LINK FOR AUTO UNLOCK
UNLOCK_URL = "https://t.me/offerbridgebot?start=unlock"

# LINKS
TELEGRAM_CHANNEL = "https://t.me/offerbridge" 
WHATSAPP_LINK = "https://wa.me/2347081356988" 
TIKTOK_LINK = "https://www.tiktok.com/@offer_bridge?_r=1&_t=ZS-95rXVNGsbFi" 
CONTACT_EMAIL = "donaldpanebi@gmail.com"

# --- MAIN MENU ---
MAIN_MENU = ReplyKeyboardMarkup([
    ["🎮 Game Mods", "📚 Online Courses"],
    ["🛠 Free Tools", "📖 eBooks"],
    ["🎓 Study Tools"],
    ["👥 Invite Friends", "📱 Social Media"],
    ["📞 Contact Us"]
], resize_keyboard=True)

# --- START COMMAND (AUTO DETECT UNLOCK) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    # CHECK DEEP LINK PARAMETER
    if context.args and "unlock" in context.args:
        await update.message.reply_text("🔓 Verified from content locker... delivering your content.")
        await send_content(update, context)
        return

    message = (
        f"Welcome {user}! 🚀\n\n"
        "Choose an option below:\n"
        "• Game Mods\n"
        "• Online Courses\n"
        "• Free Tools\n"
        "• eBooks\n"
        "• Study Tools\n\n"
        "Complete a quick task via the menu items to unlock premium content."
    )
    await update.message.reply_text(message, reply_markup=MAIN_MENU)

# --- CONTENT LOCKER FLOW ---
async def send_smart_link(update: Update):
    message = (
        "🔓 Unlock required:\n\n"
        "Click below and complete one task:\n"
        f"{SMART_LINK}\n\n"
        "After completion, you will be redirected back automatically."
    )
    await update.message.reply_text(message)

# --- AUTO CONTENT DELIVERY ---
async def send_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Access granted! Here is your content:",
        reply_markup=MAIN_MENU
    )
    
    # Send eBook
    try:
        with open("sample_ebook.pdf", "rb") as doc:
            await update.message.reply_document(doc)
    except FileNotFoundError:
        await update.message.reply_text("❌ eBook file (sample_ebook.pdf) is missing on the server.")

    # Send Course
    try:
        with open("sample_course.pdf", "rb") as doc:
            await update.message.reply_document(doc)
    except FileNotFoundError:
        await update.message.reply_text("❌ Course file (sample_course.pdf) is missing on the server.")

# --- HANDLERS ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in ["🎮 Game Mods", "📚 Online Courses", "🛠 Free Tools", "📖 eBooks", "🎓 Study Tools"]:
        await send_smart_link(update)

    elif text == "👥 Invite Friends":
        bot_user = await context.bot.get_me()
        invite_link = f"https://t.me/{bot_user.username}"
        await update.message.reply_text(f"👥 Invite friends and grow rewards:\n{invite_link}")

    elif text == "📱 Social Media":
        await update.message.reply_text(
            f"📱 Social Media:\n\nTelegram: {TELEGRAM_CHANNEL}\nWhatsApp: {WHATSAPP_LINK}\nTikTok: {TIKTOK_LINK}"
        )

    elif text == "📞 Contact Us":
        await update.message.reply_text(f"📞 Email: {CONTACT_EMAIL}")

# --- MAIN ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
