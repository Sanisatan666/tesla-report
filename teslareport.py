import logging
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import jdatetime
from telegram import Bot
import os
from telegram import Bot
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from the environment variable
bot_token = os.getenv("BOT_TOKEN")

# Print token to verify it is correct (for debugging)
print(f"Bot Token: {bot_token}")

# Check if bot_token is None
if not bot_token:
    raise ValueError("BOT_TOKEN not found. Make sure it's set correctly in the .env file.")

# Create an instance of the Bot class using the token
bot = Bot(token=bot_token)

# Get the webhook URL from the environment variable
webhook_url = os.getenv("WEBHOOK_URL")

# Check if the webhook URL is correct
if not webhook_url:
    raise ValueError("WEBHOOK_URL not found. Make sure it's set correctly in the .env file.")

# Set the webhook
bot.set_webhook(url=webhook_url)

# Get the bot token from the environment variable
bot_token = os.getenv("BOT_TOKEN")

# Create an instance of the Bot class using the token
bot = Bot(token=bot_token)

# Set the webhook URL from the environment variable
webhook_url = os.getenv("WEBHOOK_URL")

# Set the webhook
bot.set_webhook(url=webhook_url)

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
