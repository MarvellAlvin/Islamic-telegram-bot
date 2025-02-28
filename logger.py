from telegram import Update
from telegram.ext import CallbackContext
import functools

def log_command(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user = update.message.from_user.username or update.message.from_user.first_name
        print(f"{user} mengirim pesan: {update.message.text}")
        
        result = await func(update, context, *args, **kwargs)
        
        print(f"Bot telah mengirim pesan ke {user} = {update.message.text}")
        return result
    return wrapper
