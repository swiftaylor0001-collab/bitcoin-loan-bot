import os
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8314103727:AAHHLQyPigR03LrEjOClxuXvxSYqOf9B9qA")

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    user_id INTEGER,
    collateral REAL,
    loan_amount REAL,
    repayment REAL,
    status TEXT
)
""")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Welcome to BTC Loan Bot\n\n"
        "Use /apply to request a loan."
    )

async def apply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter collateral amount in BTC:")
    context.user_data["step"] = "collateral"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("step") == "collateral":
        try:
            collateral = float(update.message.text)
            loan_amount = collateral * 0.6
            repayment = loan_amount * 1.1

            cursor.execute(
                "INSERT INTO loans VALUES (?, ?, ?, ?, ?)",
                (update.effective_user.id, collateral, loan_amount, repayment, "Pending")
            )
            conn.commit()

            await update.message.reply_text(
                f"✅ Loan Submitted\n\n"
                f"Collateral: {collateral} BTC\n"
                f"Loan: {loan_amount} BTC\n"
                f"Repayment: {repayment} BTC"
            )

            context.user_data.clear()
        except:
            await update.message.reply_text("Enter a valid number.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("apply", apply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()