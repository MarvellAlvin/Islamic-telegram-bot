import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from command import info, button_callback  # Import fungsi yang sudah dibuat

# Import handler dan command dari file lain
from command import start, info, jadwal, maghrib, dzikir, renungan, husna, alhusna, listsurat, surah, ayat, hijriyah, doa, hadist
from handler import select_city, echo

# Load token dari .env
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

# Inisialisasi bot dengan Application
app = Application.builder().token(bot_token).build()

# Daftarkan command handler
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('info', info))
app.add_handler(CommandHandler('jadwal', jadwal))
app.add_handler(CommandHandler('maghrib', maghrib))
app.add_handler(CommandHandler('dzikir', dzikir))
app.add_handler(CommandHandler('renungan', renungan))
app.add_handler(CommandHandler('husna', husna))
app.add_handler(CommandHandler('alhusna', alhusna))
app.add_handler(CommandHandler('listsurat', listsurat))
app.add_handler(CommandHandler('surah', surah))
app.add_handler(CommandHandler('ayat', ayat))
app.add_handler(CommandHandler('hijriyah', hijriyah))
app.add_handler(CommandHandler('doa', doa))
app.add_handler(CommandHandler('hadist', hadist))
app.add_handler(CallbackQueryHandler(button_callback))  # Handler untuk tombol

# Daftarkan message handler (untuk menangani input numerik dan echo)
app.add_handler(MessageHandler(filters.Regex(r'^\d+$'), select_city))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == '__main__':
    print("Bot Telegram terhubung...")
    app.run_polling()
