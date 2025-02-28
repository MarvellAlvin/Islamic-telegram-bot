import random
import datetime
import requests
import aiohttp
from telegram import Update
from telegram.ext import CallbackContext
from logger import log_command

# Impor fungsi API dari file api.py
from api import (
    get_kode_kota,
    get_jadwal,
    get_husna_by_number,
    get_all_husna,
    get_all_surahs,
    get_surat_by_number,
    get_ayat_by_number,
    get_hijriyah,
    get_doa,
    get_hadist,
)
# Impor list eksternal
from data_lists import list_dzikir, list_renungan

@log_command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Halo! Selamat datang di bot tele saya.")

@log_command
async def info(update: Update, context: CallbackContext):
    text_info = "Bercahayalah jika kamu ingin dicintai setiap lawan jenis. 😉"
    await update.message.reply_text(text_info)

@log_command
async def jadwal(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Gunakan format: `/jadwal [nama_kota]`", parse_mode="Markdown")
        return

    nama_kota = context.args[0]
    tanggal = datetime.datetime.today().strftime('%Y-%m-%d')
    hasil = get_kode_kota(nama_kota)
    if not hasil:
        await update.message.reply_text("Kota tidak ditemukan. Coba masukkan nama kota yang lebih spesifik.")
        return

    if isinstance(hasil, list):
        pilihan_kota = "\n".join([f"{i+1}. {kota[1]} (ID: {kota[0]})" for i, kota in enumerate(hasil)])
        await update.message.reply_text(
            f"Ditemukan beberapa hasil untuk `{nama_kota}`:\n\n{pilihan_kota}\n\n"
            "Silakan pilih kota dengan mengetik ID kota (misal: `1609`)",
            parse_mode="Markdown"
        )
        context.user_data["pending_cities"] = hasil
        context.user_data["pending_tanggal"] = tanggal
        return

    kode_kota, lokasi = hasil
    hasil_jadwal = get_jadwal(kode_kota, tanggal)
    await update.message.reply_text(hasil_jadwal)

@log_command
async def maghrib(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Gunakan format: `/maghrib [nama_kota]`", parse_mode="Markdown")
        return

    nama_kota = context.args[0]
    tanggal = datetime.datetime.today().strftime('%Y-%m-%d')
    hasil = get_kode_kota(nama_kota)
    if not hasil:
        await update.message.reply_text("Kota tidak ditemukan. Coba masukkan nama kota yang lebih spesifik.")
        return

    if isinstance(hasil, list):
        pilihan_kota = "\n".join([f"{i+1}. {kota[1]} (ID: {kota[0]})" for i, kota in enumerate(hasil)])
        await update.message.reply_text(
            f"Ditemukan beberapa hasil untuk `{nama_kota}`:\n\n{pilihan_kota}\n\n"
            "Silakan pilih kota dengan mengetik ID kota (misal: `1609`)",
            parse_mode="Markdown"
        )
        context.user_data["pending_maghrib"] = hasil
        context.user_data["pending_maghrib_tanggal"] = tanggal
        return

    kode_kota, lokasi = hasil
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

@log_command
async def dzikir(update: Update, context: CallbackContext):
    await update.message.reply_text(random.choice(list_dzikir))

@log_command
async def renungan(update: Update, context: CallbackContext):
    await update.message.reply_text(random.choice(list_renungan))

@log_command
async def husna(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Gunakan format: `/husna [nomor]` (contoh: `/husna 5`)", parse_mode="Markdown")
        return
    try:
        nomor = int(context.args[0])
        if nomor < 1 or nomor > 99:
            await update.message.reply_text("Nomor tidak valid. Masukkan angka antara 1 hingga 99.")
            return
    except ValueError:
        await update.message.reply_text("Nomor tidak valid. Masukkan angka.")
        return

    pesan = get_husna_by_number(nomor)
    await update.message.reply_text(pesan)

@log_command
async def alhusna(update: Update, context: CallbackContext):
    pesan = get_all_husna()
    if len(pesan) > 4000:
        parts = [pesan[i:i+4000] for i in range(0, len(pesan), 4000)]
        for part in parts:
            await update.message.reply_text(part)
    else:
        await update.message.reply_text(pesan)

@log_command
async def listsurat(update: Update, context: CallbackContext):
    surahs = get_all_surahs()
    if surahs:
        message = "Daftar Surat Al-Quran (Nomor 1-114):\n\n"
        for i, surat in enumerate(surahs):
            message += f"{i+1}. {surat['name_id']}\n"
        if len(message) > 4000:
            parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(message)
    else:
        await update.message.reply_text("Gagal mendapatkan daftar surat.")

@log_command
async def surah(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Gunakan format: `/surah [nomor]` (contoh: `/surah 1`)", parse_mode="Markdown")
        return
    try:
        number = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Nomor surat harus berupa angka.")
        return
    if number < 1 or number > 114:
        await update.message.reply_text("Nomor surat tidak valid. Masukkan antara 1 hingga 114.")
        return
    data = get_surat_by_number(number)
    if data:
        message = (
            f"Informasi Surat Al-Quran Nomor {number}:\n\n"
            f"Nama Surat: {data['name_id']} ({data['name_short']})\n"
            f"Nama Panjang: {data['name_long']}\n"
            f"Arti: {data['translation_id']}\n"
            f"Jumlah Ayat: {data['number_of_verses']}\n"
            f"Jenis Wahyu: {data['revelation_id']}\n"
            f"Tafsir: {data['tafsir']}\n"
            f"Audio URL: {data['audio_url']}"
        )
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Data surat tidak ditemukan.")

@log_command
async def ayat(update: Update, context: CallbackContext):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Gunakan format: `/ayat [nomor_surat] [nomor_ayat]` (contoh: `/ayat 1 1`)", parse_mode="Markdown")
        return
    try:
        surat_number = int(context.args[0])
        ayat_number = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Nomor surat dan ayat harus berupa angka.")
        return
    data = get_ayat_by_number(surat_number, ayat_number)
    if data:
        message = (
            f"Ayat {ayat_number} dari Surat {surat_number}:\n\n"
            f"Ayat (Arab): {data['arab']}\n"
            f"Ayat (Latin): {data['latin']}\n"
            f"Terjemahan: {data['text']}\n"
            f"Audio URL: {data['audio']}"
        )
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Data ayat tidak ditemukan.")

async def hijriyah(update: Update, context: CallbackContext):
    user = update.message.from_user.username or update.message.from_user.first_name
    print(f"User {user} mengirim pesan: /hijriyah")

    data = get_hijriyah()  # Hapus `await`
    
    if data:
        message = (
            f"📅 **Kalender Hijriyah**\n\n"
            f"🕌 Hari: *{data['hari']}*\n"
            f"📆 Tanggal Hijriyah: *{data['tanggal_hijriyah']}*\n"
            f"📅 Tanggal Masehi: *{data['tanggal_masehi']}*"
        )
    else:
        message = "❌ Gagal mendapatkan data kalender Hijriyah."

    await update.message.reply_text(message, parse_mode="Markdown")
    print(f"Bot telah mengirim hijriyah ke {user}")

async def doa(update: Update, context: CallbackContext):
    user = update.message.from_user.username or update.message.from_user.first_name
    print(f"User {user} mengirim pesan: /doa")

    data = get_doa()  # Hapus `await`
    
    if data:
        message = (
            f"📖 *{data['judul']}*\n\n"
            f"📜 _{data['arab']}_\n\n"
            f"🇮🇩 {data['indo']}"
        )
    else:
        message = "Gagal mengambil doa. Coba lagi nanti."

    await update.message.reply_text(message, parse_mode="Markdown")
    print(f"Bot telah mengirim doa ke {user}")

async def hadist(update: Update, context: CallbackContext):
    user = update.message.from_user.username or update.message.from_user.first_name
    print(f"User {user} mengirim pesan: /hadist")

    data = await get_hadist()
    if data:
        message = (
            f"📖 *{data['kitab']}* (No. {data['nomor']})\n\n"
            f"*{data['judul']}*\n\n"
            f"_{data['arab']}_\n\n"
            f"➖ {data['terjemah']}"
        )
    else:
        message = "Gagal mengambil hadist. Coba lagi nanti."

    await update.message.reply_text(message, parse_mode="Markdown")
    print(f"Bot telah mengirim hadist ke {user}")
