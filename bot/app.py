import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext

# Load environment variables

load_dotenv()
spotify_login_url = os.getenv("SPOTIFY_LOGIN_URL")

# Pre-assign button text
SPOTIFY_MENU = "<b>Menu</b>\n\nLog in to Spotify to continue."
LOGIN_SPOTIFY_BUTTON = "Log in to Spotify"
LOGIN_SPOTIFY_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton(
        LOGIN_SPOTIFY_BUTTON, url=spotify_login_url)]
])

SUCCESS_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton('Success', callback_data='success')]
])


async def spotify_login_menu(update: Update, context: CallbackContext) -> None:

    await context.bot.send_message(
        update.message.from_user.id,
        SPOTIFY_MENU,
        parse_mode='HTML',
        reply_markup=LOGIN_SPOTIFY_MARKUP
    )


async def spotify_login_callback(update: Update, context: CallbackContext) -> None:
    data = update.callback_query.data
    text = 'BOBOBOBOB'
    markup = None

    print(data)

    await update.callback_query.answer()

    # Update message content with corresponding menu section
    await update.callback_query.message.edit_text(
        text,
        parse_mode='HTML',
        reply_markup=markup
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, thanks for chating with! I am BobMusik Bot')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is the help command')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here')


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('login', spotify_login_menu))

    # Callbacks

    app.add_handler(CallbackQueryHandler(spotify_login_callback))

    # Errors
    app.add_error_handler(error)

    # Polls the bot and check for updates every 3 seconds
    print('Polling...')
    app.run_polling(poll_interval=3)
