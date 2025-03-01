import requests
import aiohttp

def get_kode_kota(nama_kota):
    url = f"https://api.myquran.com/v2/sholat/kota/cari/{nama_kota}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") and "data" in data:
            hasil = data["data"]
            if len(hasil) == 1:
                return hasil[0]["id"], hasil[0]["lokasi"]
            elif len(hasil) > 1:
                return [(kota["id"], kota["lokasi"]) for kota in hasil]
        return None
    except requests.exceptions.RequestException:
        return None

def get_jadwal(kode_kota, tanggal):
    url = f"https://api.myquran.com/v2/sholat/jadwal/{kode_kota}/{tanggal}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"]:
            jadwal = data["data"]["jadwal"]
            return (
                f"Jadwal Sholat di {data['data']['lokasi']} ({data['data']['daerah']}) pada {jadwal['tanggal']}:\n\n"
                f"🕌 Imsak: {jadwal['imsak']}\n"
                f"🕌 Subuh: {jadwal['subuh']}\n"
                f"🌅 Terbit: {jadwal['terbit']}\n"
                f"🌞 Dhuha: {jadwal['dhuha']}\n"
                f"🕌 Dzuhur: {jadwal['dzuhur']}\n"
                f"🕌 Ashar: {jadwal['ashar']}\n"
                f"🌇 Maghrib: {jadwal['maghrib']}\n"
                f"🌙 Isya: {jadwal['isya']}"
            )
        return "Jadwal sholat tidak ditemukan."
    except requests.exceptions.RequestException:
        return "Gagal mengambil data jadwal sholat."

def get_husna_by_number(nomor: int) -> str:
    url = f"https://api.myquran.com/v2/husna/{nomor}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            husna = data["data"]
            message = (
                f"Nomor: {husna['id']}\n"
                f"Nama: {husna['indo']} ({husna['arab']})\n"
                f"Latin: {husna['latin']}"
            )
            return message
        else:
            return "Data Asmaul Husna tidak ditemukan."
    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan: {e}"

def get_all_husna() -> str:
    url = "https://api.myquran.com/v2/husna/semua"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            husna_list = data["data"]
            messages = []
            for husna in husna_list:
                pesan = (
                    f"Nomor: {husna['id']}\n"
                    f"Nama: {husna['indo']} ({husna['arab']})\n"
                    f"Latin: {husna['latin']}\n"
                )
                messages.append(pesan)
            return "\n".join(messages)
        else:
            return "Data Asmaul Husna tidak ditemukan."
    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan: {e}"

def get_all_surahs():
    url = "https://api.myquran.com/v2/quran/surat/semua"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return data["data"]
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_surat_by_number(number: int):
    url = f"https://api.myquran.com/v2/quran/surat/{number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return data["data"]
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_ayat_by_number(surat_number: int, ayat_number: int):
    url = f"https://api.myquran.com/v2/quran/ayat/{surat_number}/{ayat_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            if isinstance(data["data"], list) and len(data["data"]) > 0:
                return data["data"][0]
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_hijriyah():
    url_hijriyah = "https://api.myquran.com/v2/cal/hijr/?adj=-1"
    url_bulan = "https://api.myquran.com/v2/cal/list/months"

    response_hijriyah = requests.get(url_hijriyah).json()
    response_bulan = requests.get(url_bulan).json()

    if response_hijriyah["status"] and response_bulan["status"]:
        tanggal_hijriyah = response_hijriyah["data"]["date"][1]
        tanggal_masehi = response_hijriyah["data"]["date"][2]
        hari = response_hijriyah["data"]["date"][0]
        bulan_index = str(response_hijriyah["data"]["num"][5])
        
        bulan_list = response_bulan["data"]
        nama_bulan_hijriyah = bulan_list.get(bulan_index, "Tidak diketahui")

        return {
            "hari": hari,
            "tanggal_hijriyah": tanggal_hijriyah,
            "tanggal_masehi": tanggal_masehi
        }
    return None

def get_doa():
    url = "https://api.myquran.com/v2/doa/acak"
    response = requests.get(url).json()

    if response["status"]:
        return {
            "judul": response["data"]["judul"],
            "arab": response["data"]["arab"],
            "indo": response["data"]["indo"]
        }
    return None

async def get_hadist():
    url = "https://api.myquran.com/v2/hadits/arbain/acak"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            data = await response.json()
            hadits = data["data"]

            return {
                "judul": hadits.get("judul", "Hadits Arbain"),
                "kitab": "Hadits Arbain",
                "nomor": hadits.get("no", "Tidak diketahui"),
                "arab": hadits.get("arab", "Tidak tersedia"),
                "terjemah": hadits.get("indo", "Tidak tersedia"),
            }
    return None
    
