import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Simple user storage (temporary)
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"referrals": 0, "balance": 0}

    await update.message.reply_text(
        "🚀 Welcome to Offer Bridge Bot!\n\n"
        "Earn rewards by completing tasks and inviting friends.\n"
        "Use /referral to get your link."
    )

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = (await context.bot.get_me()).username
    user_id = update.effective_user.id

    link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"🔗 Your referral link:\n{link}\n\nInvite friends to earn rewards!"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {"referrals": 0, "balance": 0}

    await update.message.reply_text(
        f"💰 Your balance: ${users[user_id]['balance']}"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start bot\n"
        "/referral - Get referral link\n"
        "/balance - Check earnings"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("referral", referral))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("help", help_cmd))

print("Offer Bridge Bot is running...")
app.run_polling()
