import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Import handler dan command dari file lain
from commands import start, info, jadwal, maghrib, dzikir, renungan, husna, alhusna, listsurat, surah, ayat, hijriyah, doa, hadist
from handlers import select_city, echo

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

# Daftarkan message handler (untuk menangani input numerik dan echo)
app.add_handler(MessageHandler(filters.Regex(r'^\d+$'), select_city))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == '__main__':
    print("Bot Telegram terhubung...")
    app.run_polling()
