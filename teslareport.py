import logging
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import jdatetime

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot
token = os.getenv("BOT_TOKEN")
bot = Bot(token)

# Check webhook status
def check_webhook():
    try:
        webhook_info = bot.get_webhook_info()
        print("Webhook Info: ", webhook_info)
    except Exception as e:
        print(f"Error fetching webhook info: {e}")

# Call check_webhook function to verify
check_webhook()

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    greeting_message = f"سلام {user.first_name} @{user.username}!\nتاریخ امروز: {jdatetime.datetime.now().strftime('%Y/%m/%d')}\n\nنام پروژه امروز چیست؟"
    await update.message.reply_text(greeting_message)
    ask_project_name(update)

# Function to ask for the project name
async def ask_project_name(update: Update):
    await update.message.reply_text("نام پروژه امروز چیست؟")

# Handle other messages
async def handle_message(update: Update, context: CallbackContext):
    # Handle responses as per your bot's logic
    pass

def main():
    # Create Application instance and dispatcher
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
