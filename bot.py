Offer Bridge Telegram Bot - Production Ready Starter Code

Author: ChatGPT

Description: Multi-niche Telegram bot with tasks, referrals, points, daily bonus, and broadcast system

Designed for deployment on Render.com or any Python hosting service

import logging import sqlite3 import datetime import os from telegram import Update, ReplyKeyboardMarkup from telegram.ext import ( ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, )

=============================

CONFIGURATION

=============================

TOKEN = os.getenv("BOT_TOKEN")  # Put your bot token in environment variable ADMIN_ID = 123456789  # Replace with your Telegram user ID

logging.basicConfig( format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, )

=============================

DATABASE SETUP

=============================

conn = sqlite3.connect("offer_bridge.db", check_same_thread=False) cursor = conn.cursor()

cursor.execute( """ CREATE TABLE IF NOT EXISTS users ( user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0, referrals INTEGER DEFAULT 0, last_claim TEXT ) """ )

conn.commit()

=============================

MENU

=============================

menu = ReplyKeyboardMarkup( [ ["🎮 Game Tasks", "🎬 Movie Tasks"], ["📚 Course Tasks", "💰 Check Balance"], ["📅 Daily Bonus", "👥 Invite Friends"], ], resize_keyboard=True, )

=============================

DATABASE FUNCTIONS

=============================

def add_user(user_id): cursor.execute( "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,), ) conn.commit()

def add_points(user_id, amount): cursor.execute( "UPDATE users SET points = points + ? WHERE user_id=?", (amount, user_id), ) conn.commit()

def get_points(user_id): cursor.execute( "SELECT points FROM users WHERE user_id=?", (user_id,), ) result = cursor.fetchone() return result[0] if result else 0

=============================

START / REFERRAL SYSTEM

=============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user user_id = user.id

add_user(user_id)

# Referral tracking
if context.args:
    referrer_id = context.args[0]

    if str(referrer_id) != str(user_id):
        cursor.execute(
            "UPDATE users SET referrals = referrals + 1 WHERE user_id=?",
            (referrer_id,),
        )
        add_points(referrer_id, 10)
        conn.commit()

referral_link = f"https://t.me/OfferBridgeBot?start={user_id}"

await update.message.reply_text(
    f"Welcome to Offer Bridge, {user.first_name}!\n"
    "Complete tasks and earn rewards.\n\n"
    f"Invite friends using this link:\n{referral_link}",
    reply_markup=menu,
)

=============================

TASK HANDLERS

=============================

async def game_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "🎮 Game Tasks Available:\n" "1. Download new mobile game\n" "2. Install gaming app\n" "3. Try new game features\n\n" "Complete a task to earn points." )

async def movie_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "🎬 Movie Tasks Available:\n" "1. Watch movie trailer\n" "2. Install streaming app\n" "3. Join movie community" )

async def course_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "📚 Course Tasks Available:\n" "1. Try free online course\n" "2. Download learning app\n" "3. Explore skill training" )

=============================

BALANCE

=============================

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id points = get_points(user_id)

await update.message.reply_text(
    f"💰 Your current points: {points}"
)

=============================

DAILY BONUS

=============================

async def daily_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id today = str(datetime.date.today())

cursor.execute(
    "SELECT last_claim FROM users WHERE user_id=?",
    (user_id,),
)

result = cursor.fetchone()

if result and result[0] == today:
    await update.message.reply_text(
        "You have already claimed today's bonus."
    )
    return

add_points(user_id, 20)

cursor.execute(
    "UPDATE users SET last_claim=? WHERE user_id=?",
    (today, user_id),
)

conn.commit()

await update.message.reply_text(
    "Daily bonus claimed! You received 20 points."
)

=============================

INVITE FRIENDS

=============================

async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id

referral_link = f"https://t.me/OfferBridgeBot?start={user_id}"

await update.message.reply_text(
    f"Invite friends using your link:\n{referral_link}"
)

=============================

BROADCAST (ADMIN ONLY)

=============================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE): if update.effective_user.id != ADMIN_ID: return

message = " ".join(context.args)

cursor.execute("SELECT user_id FROM users")
users = cursor.fetchall()

sent = 0

for user in users:
    try:
        await context.bot.send_message(
            chat_id=user[0],
            text=message,
        )
        sent += 1
    except Exception:
        pass

await update.message.reply_text(
    f"Broadcast sent to {sent} users."
)

=============================

MAIN FUNCTION

=============================

def main(): app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT("🎮 Game Tasks"), game_tasks)
)

app.add_handler(
    MessageHandler(filters.TEXT("🎬 Movie Tasks"), movie_tasks)
)

app.add_handler(
    MessageHandler(filters.TEXT("📚 Course Tasks"), course_tasks)
)

app.add_handler(
    MessageHandler(filters.TEXT("💰 Check Balance"), balance)
)

app.add_handler(
    MessageHandler(filters.TEXT("📅 Daily Bonus"), daily_bonus)
)

app.add_handler(
    MessageHandler(filters.TEXT("👥 Invite Friends"), invite)
)

app.add_handler(CommandHandler("broadcast", broadcast))

print("Offer Bridge Bot is running...")

app.run_polling()

if name == "main": main()
