import datetime
import requests
from telegram import Update
from telegram.ext import CallbackContext
from api import get_jadwal

async def select_city(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    # Prioritaskan pending untuk /maghrib
    if "pending_maghrib" in context.user_data:
        pending = context.user_data["pending_maghrib"]
        matching = [city for city in pending if city[0] == text]
        if matching:
            kode_kota, lokasi = matching[0]
            tanggal = context.user_data.get("pending_maghrib_tanggal", datetime.datetime.today().strftime('%Y-%m-%d'))
            url = f"https://api.myquran.com/v2/sholat/jadwal/{kode_kota}/{tanggal}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                if data["status"]:
                    jadwal = data["data"]["jadwal"]
                    maghrib_time = jadwal.get("maghrib", "Tidak ada data")
                    lokasi = data["data"]["lokasi"]
                    daerah = data["data"]["daerah"]
                    await update.message.reply_text(
                        f"Waktu Maghrib di {lokasi} ({daerah}) pada {jadwal['tanggal']} adalah {maghrib_time}"
                    )
                else:
                    await update.message.reply_text("Jadwal sholat tidak ditemukan.")
            except requests.exceptions.RequestException:
                await update.message.reply_text("Gagal mengambil data jadwal sholat.")
            context.user_data.pop("pending_maghrib")
            context.user_data.pop("pending_maghrib_tanggal", None)
            context.user_data["skip_echo"] = True
            return
    # Jika tidak ada pending maghrib, periksa pending untuk jadwalsholat
    if "pending_cities" in context.user_data:
        pending = context.user_data["pending_cities"]
        matching = [city for city in pending if city[0] == text]
        if matching:
            kode_kota, lokasi = matching[0]
            tanggal = context.user_data.get("pending_tanggal", datetime.datetime.today().strftime('%Y-%m-%d'))
            hasil_jadwal = get_jadwal(kode_kota, tanggal)
            await update.message.reply_text(hasil_jadwal)
            context.user_data.pop("pending_cities")
            context.user_data.pop("pending_tanggal", None)
            context.user_data["skip_echo"] = True
        else:
            await update.message.reply_text("ID kota tidak valid. Silakan coba lagi.")

async def echo(update: Update, context: CallbackContext):
    if context.user_data.pop("skip_echo", False):
        return
    message = update.message.text
    await update.message.reply_text(message)
    print(f"Pesan dari user: {message}")
