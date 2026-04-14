import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN missing in environment variables")
    exit()

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"balance": 0}

    await update.message.reply_text(
        "🚀 Welcome to Offer Bridge Bot!\n\n"
        "Commands:\n"
        "/referral - get link\n"
        "/balance - check earnings"
    )

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = (await context.bot.get_me()).username
    user_id = update.effective_user.id

    link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(f"🔗 Your referral link:\n{link}")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    bal = users.get(user_id, {}).get("balance", 0)

    await update.message.reply_text(f"💰 Balance: ${bal}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("referral", referral))
app.add_handler(CommandHandler("balance", balance))

print("Bot is running...")
app.run_polling()
