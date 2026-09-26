import os
import time
import pickle
from telegram import Update, Bot, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import BadRequest

if os.path.exists('blocked.pkl'):
    with open('blocked.pkl', 'rb') as bfile:
        try:
            blocked_words = pickle.load(bfile)
        except (EOFError, pickle.UnpicklingError):
            blocked_words = {}
        finally:
            bfile.close()
else:
    blocked_words = {}
    print("file doesn't exist")

# Dictionary to store blocked words for each chat
blocked_words = {}
def show_blocked_words(update: Update, context: CallbackContext) -> None:
    if os.path.exists('blocked.pkl'):
        with open('blocked.pkl', 'rb') as bfile:
            try:
                blocked_words = pickle.load(bfile)
            except (EOFError, pickle.UnpicklingError):
                blocked_words = {}
            finally:
                bfile.close()
    else:
        blocked_words = {}
        print("file doesn't exist")

    chat_id = update.effective_chat.id
    if chat_id in blocked_words:
        update.message.reply_text(str(blocked_words[chat_id])[1:-1])
    else:
        update.message.reply_text("No word blacklisted YET...")

# Function to ask admin for blocked words
def set_blocked_words(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    context.user_data['mess_to_del'] = update.message.message_id
    if update.effective_chat.get_member(user_id).status in ['administrator', 'creator']:
        reply_message = update.message.reply_text('Please send the words to be blacklisted, separated by commas.')
        context.user_data['waiting_for_words'] = True
        context.user_data['reply_mess_to_del'] = reply_message.message_id
        context.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, update_blocked_words), group=1)
    else:
        update.message.reply_text('Only admins can blacklist words.')
def update_blocked_words(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    if context.user_data.get('waiting_for_words'):
        words = update.message.text.lower().split(',')
        context.bot.delete_message(chat_id, message_id)
        
        if os.path.exists('blocked.pkl'):
            with open('blocked.pkl', 'rb') as bfile:
                try:
                    blocked_words = pickle.load(bfile)
                except (EOFError, pickle.UnpicklingError):
                    blocked_words = {}
                finally:
                    bfile.close()
        else:
            blocked_words = {}
        
        if chat_id not in blocked_words:
            blocked_words[chat_id] = [word.strip() for word in words]
        else:
            blocked_words[chat_id].extend(word.strip() for word in words)

        mess_to_del = context.user_data.get('mess_to_del')
        reply_mess_to_del = context.user_data.get('reply_mess_to_del')
        if mess_to_del:
            context.bot.delete_message(chat_id, mess_to_del)
            context.user_data['mess_to_del'] = None
        if reply_mess_to_del:
            context.bot.delete_message(chat_id, reply_mess_to_del)
            context.user_data['reply_mess_to_del'] = None

        with open('blocked.pkl', 'wb') as bfile:
            pickle.dump(blocked_words, bfile)

        try:
            update.message.reply_text(f'Blacklisted words: {", ".join(blocked_words[chat_id])}')
        except BadRequest as e:
            print(f"BadRequest error: {e.message}")

        print(f'Admin set blocked words: {blocked_words[chat_id]} in chat {chat_id}')
        context.user_data['waiting_for_words'] = False
        context.dispatcher.remove_handler(MessageHandler, group=1)

# Function to monitor messages and block users
def monitor_chats(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_text = update.message.text.lower()
    message_id = update.message.message_id

    if os.path.exists('blocked.pkl'):
        with open('blocked.pkl', 'rb') as bfile:
            try:
                blocked_words = pickle.load(bfile)
            except (EOFError, pickle.UnpicklingError):
                blocked_words = {}
            finally:
                bfile.close()
    else:
        blocked_words = {}

    permission = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False)

    # Check for blocked words
    if chat_id in blocked_words:
        for word in blocked_words[chat_id]:
            if word in message_text:
                context.bot.restrict_chat_member(chat_id, user_id,permissions=permission , until_date=time.time() + 300)
                context.bot.delete_message(chat_id, message_id)
                update.message.reply_text(f'User {update.effective_user.first_name} has been blocked for using a blacklisted word')
                print(f'User {user_id} blocked for using a blck-listed word in chat {chat_id}')
                return

    # Check for links
    if 'http://' in message_text or 'https://' in message_text:
        context.bot.ban_chat_member(chat_id, user_id, until_date=time.time() + 7200)
        update.message.reply_text(f'User {update.effective_user.first_name} has been blocked for sharing a link.')
        print(f'User {user_id} blocked for sharing a link in chat {chat_id}')

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! \nI am LISA, your group manager bot.', allow_sending_without_reply=True)

# Define a function to handle the /help command
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('For any complaints or reports, contact developer')

# Main function to set up the bot
def main():
    # Replace with your actual Telegram Bot API token
    bot_token = 'Enter your Telegram / Bot API token here'
    updater = Updater(bot_token)

    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("setblockedwords", set_blocked_words))
    dispatcher.add_handler(CommandHandler("showblockedwords", show_blocked_words))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, monitor_chats))

    # Start the webhook to listen for messages
    updater.start_webhook(listen='0.0.0.0',
                          port=int(os.environ.get('PORT', 5000)),
                          url_path=bot_token,
                          webhook_url=f'https://telegrambot-dvnr.onrender.com/{bot_token}')

    updater.idle()

if __name__ == '__main__':
    main()
