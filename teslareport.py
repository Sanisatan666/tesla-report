import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import jdatetime

# Set up logging to track any issues
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store responses
project = ""
address = ""
iphone = ""
completed_tasks = ""
pending_tasks = ""
with_someone = ""
rack_status = ""

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    # Updated greeting message to ask for the project name
    greeting_message = f"سلام {user.first_name} @{user.username}!\nتاریخ امروز: {jdatetime.datetime.now().strftime('%Y/%m/%d')}\n\nنام پروژه امروز چیست؟"
    await update.message.reply_text(greeting_message)
    ask_project_name(update)  # Directly ask for the project name

# Function to ask for the project name first
async def ask_project_name(update: Update):
    await update.message.reply_text("نام پروژه امروز چیست؟")

# Function to handle the responses to each question
async def handle_message(update: Update, context: CallbackContext):
    global project, address, iphone, completed_tasks, pending_tasks, with_someone, rack_status

    text = update.message.text

    # Store responses based on question order
    if project == "":
        project = text
        await update.message.reply_text("آدرس پروژه امروز چیست؟")
    elif address == "":
        address = text
        await update.message.reply_text("آیفون (iPhone):")
    elif iphone == "":
        iphone = text
        await update.message.reply_text("کارهای انجام شده (Completed Tasks):")
    elif completed_tasks == "":
        completed_tasks = text
        await update.message.reply_text("کارهای مانده (Pending Tasks):")
    elif pending_tasks == "":
        pending_tasks = text
        await update.message.reply_text("همراه (With someone or solo):")
    elif with_someone == "":
        with_someone = text
        await update.message.reply_text("وضعیت رک (Rack Status - Installed or not):")
    elif rack_status == "":
        rack_status = text
        # After collecting all answers, format and send the report
        await send_report(update)

# Function to format and send the report
async def send_report(update: Update):
    report = f"""
پروژه: {project}
تاریخ: {jdatetime.datetime.now().strftime('%Y/%m/%d')}
آدرس: {address}
رک: {rack_status}
آیفون: {iphone}
کارهای انجام شده:
{completed_tasks}
همراه: {with_someone}
کارهای مانده: {pending_tasks}
    """
    await update.message.reply_text("گزارش شما به این شکل است:\n" + report)

    # Reset the global variables for the next report
    reset_variables()

# Function to reset the global variables for the next report
def reset_variables():
    global project, address, iphone, completed_tasks, pending_tasks, with_someone, rack_status
    project = ""
    address = ""
    iphone = ""
    completed_tasks = ""
    pending_tasks = ""
    with_someone = ""
    rack_status = ""

def main():
    # Your bot token
    token = "7882638117:AAGd0KELurHGyRBrhY8I4s96Cox1u1431v0"

    # Create Application instance and dispatcher
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
