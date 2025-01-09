import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()

# States for conversation
(
    PROJECT_NAME,
    PROJECT_ADDRESS,
    COMPLETED_TASKS,
    REMAINING_TASKS,
    COMPANION_STATUS,
    RACK_STATUS,
) = range(6)

# Store user responses (in memory)
user_responses = {}

# Questions in Persian
QUESTIONS = {
    PROJECT_NAME: "نام پروژه امروز چیست؟",
    PROJECT_ADDRESS: "آدرس پروژه امروز چیست؟",
    COMPLETED_TASKS: "کارهای انجام شده",
    REMAINING_TASKS: "کارهای مانده",
    COMPANION_STATUS: "همراه (With someone or solo):",
    RACK_STATUS: "وضعیت رک (Rack Status - Installed or not):",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Initialize storage for this user
    user_responses[user_id] = {
        "start_time": get_tehran_time(),
    }

    # Send welcome message with current Tehran time
    await update.message.reply_text(
        f"زمان شروع: {user_responses[user_id]['start_time']}\n\n"
        f"{QUESTIONS[PROJECT_NAME]}"
    )

    return PROJECT_NAME


def get_tehran_time():
    tehran_tz = pytz.timezone("Asia/Tehran")
    current_time = datetime.now(tehran_tz)
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_state = context.user_data.get("state", PROJECT_NAME)

    # Store the answer
    user_responses[user_id][current_state] = update.message.text

    # Move to next state
    next_state = current_state + 1

    # If we have more questions, ask the next one
    if next_state < RACK_STATUS + 1:
        await update.message.reply_text(QUESTIONS[next_state])
        return next_state

    # If we're done, format and send the final response
    final_response = format_final_response(user_id)
    await update.message.reply_text(final_response)

    # Clear user data
    if user_id in user_responses:
        del user_responses[user_id]

    return ConversationHandler.END


def format_final_response(user_id):
    responses = user_responses[user_id]

    return (
        f"گزارش نهایی:\n\n"
        f"🕒 زمان شروع: {responses['start_time']}\n"
        f"📍 نام پروژه: {responses[PROJECT_NAME]}\n"
        f"📍 آدرس پروژه: {responses[PROJECT_ADDRESS]}\n"
        f"✅ کارهای انجام شده: {responses[COMPLETED_TASKS]}\n"
        f"⏳ کارهای مانده: {responses[REMAINING_TASKS]}\n"
        f"👥 همراه: {responses[COMPANION_STATUS]}\n"
        f"🔧 وضعیت رک: {responses[RACK_STATUS]}\n\n"
        f"🕒 زمان پایان: {get_tehran_time()}"
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_responses:
        del user_responses[user_id]

    await update.message.reply_text(
        "عملیات لغو شد. برای شروع مجدد از /start استفاده کنید."
    )
    return ConversationHandler.END


def main():
    # Create application
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PROJECT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)
            ],
            PROJECT_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)
            ],
            COMPLETED_TASKS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)
            ],
            REMAINING_TASKS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)
            ],
            COMPANION_STATUS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)
            ],
            RACK_STATUS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add conversation handler to application
    application.add_handler(conv_handler)

    # Start polling
    application.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
