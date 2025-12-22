import requests, json, time, random, urllib3, ssl, datetime, sys, os
from colorama import Fore, Style, init
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from wilayah_mapping_complete import get_nama_wilayah, WILAYAH_MAPPING


init(autoreset=True)
urllib3.disable_warnings()

RED_GLOW = Fore.LIGHTRED_EX
GREEN_GLOW = Fore.LIGHTGREEN_EX
YELLOW_GLOW = Fore.LIGHTYELLOW_EX
CYAN_GLOW = Fore.LIGHTCYAN_EX
WHITE_GLOW = Fore.LIGHTWHITE_EX

DC_API_URL = "https://deskcollection.space/api/v1/kpu/cek"
DC_API_KEY = "dc_9712ee4c40eadde0ca70f262400b163a3144460ce0d00e8e"
RAPIDAPI_KEY = "9faaa2b50fmsh5b48ae01005e119p1ff81djsn05fe4be86bf4"
RAPIDAPI_URL = "https://nik-parser.p.rapidapi.com/ektp"
WILAYAH_API = "https://api.andriannus.site/api/daerah"
KEMENDAGRI_API = "https://www.kemendagri.go.id/api/cekekode"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

class SSLAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

def make_api_request(url, method="GET", headers=None, data=None, params=None, timeout=15):
    """Fungsi umum untuk melakukan request API"""
    session = requests.Session()
    session.mount("https://", SSLAdapter())
    
    if headers is None:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    
    try:
        if method.upper() == "GET":
            response = session.get(url, headers=headers, params=params, timeout=timeout, verify=False)
        else:
            response = session.post(url, headers=headers, json=data, timeout=timeout, verify=False)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return None
        elif response.status_code == 429:
            print(f"{YELLOW_GLOW}[!] Tunggu beberapa saat...")
            time.sleep(5)
            return None
        else:
            print(f"{YELLOW_GLOW}[!] HTTP {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"{YELLOW_GLOW}[!] Timeout saat menghubungi API")
        return None
    except Exception as e:
        print(f"{YELLOW_GLOW}[!] Error API: {str(e)}")
        return None
    
def parse_nik_structure(nik):
    """Parse struktur NIK tanpa data buatan"""
    if len(nik) != 16 or not nik.isdigit():
        return None

    try:
        kode_kecamatan = nik[:6]
        tgl_raw = int(nik[6:8])
        bln = int(nik[8:10])
        thn_raw = int(nik[10:12])

        thn = thn_raw + 1900 if thn_raw > 30 else thn_raw + 2000

        if tgl_raw > 40:
            jenis_kelamin = "PEREMPUAN"
            tgl_lahir = tgl_raw - 40
        else:
            jenis_kelamin = "LAKI-LAKI"
            tgl_lahir = tgl_raw

        if not (1 <= tgl_lahir <= 31) or not (1 <= bln <= 12):
            return None

        wilayah_data = parse_wilayah_from_kode(kode_kecamatan)

        return {
            "kode_kecamatan": kode_kecamatan,
            "tgl_lahir": tgl_lahir,
            "bln_lahir": bln,
            "thn_lahir": thn,
            "jenis_kelamin": jenis_kelamin,
            "wilayah": wilayah_data
        }

    except Exception as e:
        print(f"{RED_GLOW}[!] Error parsing NIK: {str(e)}")
        return None

def get_data_from_dc_api(nik):
    """Mengambil data NIK dari Desk Collection API"""
    print(f"{CYAN_GLOW}[*] Mencoba Desk Collection API...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DC_API_KEY}",
        "User-Agent": random.choice(USER_AGENTS)
    }
    
    data = {"nik": nik}
    
    response = make_api_request(DC_API_URL, method="POST", headers=headers, data=data)
    
    if response:
        if response.get("success"):
            print(f"{GREEN_GLOW}[+] Data ditemukan di Desk Collection API")
            return response.get("data", {})
        else:
            print(f"{YELLOW_GLOW}[!] Desk Collection API: {response.get('message', 'Data tidak ditemukan')}")
    
    return None

def get_data_from_rapidapi(nik):
    """Mengambil data dari RapidAPI (backup)"""
    print(f"{CYAN_GLOW}[*] Mencoba DanzXploit...")
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "nik-parser.p.rapidapi.com",
        "User-Agent": random.choice(USER_AGENTS)
    }
    
    params = {"nik": nik}
    
    response = make_api_request(RAPIDAPI_URL, method="GET", headers=headers, params=params)
    
    if response:
        print(f"{GREEN_GLOW}[+] Data ditemukan")
        return response
    
    return None

def fetch_kemendagri(kode: str):
    """Coba ambil nama kecamatan dari API Kemendagri (cadangan)"""
    if len(kode) != 6 or not kode.isdigit():
        return None
    try:
        r = requests.get(
            KEMENDAGRI_API,
            params={"kode": kode, "level": "kecamatan"},
            headers={"User-Agent": random.choice(USER_AGENTS)},
            timeout=6,
            verify=False
        )
        if r.status_code == 200 and r.json().get("status") == "OK":
            return r.json()["data"]
    except Exception:
        pass
    return None


def parse_wilayah_from_kode(kode_kecamatan: str):
    """Return dict prov/kab/kec/kodepos; prioritas mapping lokal"""
    if len(kode_kecamatan) != 6:
        return {"provinsi": "UNKNOWN", "kota": "UNKNOWN",
                "kecamatan": "UNKNOWN", "kodepos": "00000"}

    prov = get_nama_wilayah(kode_kecamatan[:2])   
    kota = get_nama_wilayah(kode_kecamatan[:4])   
    kec  = get_nama_wilayah(kode_kecamatan)    

    if not kec.startswith("KECAMATAN KODE"):
        return {"provinsi": prov, "kota": kota,
                "kecamatan": kec, "kodepos": "00000"}

    api_data = fetch_kemendagri(kode_kecamatan)
    if api_data:
        return {"provinsi": api_data["nama_prov"],
                "kota": api_data["nama_kab"],
                "kecamatan": api_data["nama"],
                "kodepos": "00000"}

    return {"provinsi": prov,
            "kota": kota,
            "kecamatan": f"KECAMATAN KODE {kode_kecamatan}",
            "kodepos": "00000"}

def hitung_usia_pasaran(tgl, bln, thn):
    """Hitung usia dengan akurasi penuh"""
    try:
        tgl_lahir = date(thn, bln, tgl)
        hari_ini = date.today()
        
        delta = relativedelta(hari_ini, tgl_lahir)
        
        ultah_tahun_ini = tgl_lahir.replace(year=hari_ini.year)
        if ultah_tahun_ini < hari_ini:
            ultah_tahun_depan = tgl_lahir.replace(year=hari_ini.year + 1)
            hari_menuju = (ultah_tahun_depan - hari_ini).days
        else:
            hari_menuju = (ultah_tahun_ini - hari_ini).days
        
        bulan_menuju = hari_menuju // 30
        hari_sisa = hari_menuju % 30
        
        
        hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        
        ref_date = date(2000, 1, 1)
        # ref_pasaran = 2 
        
        days_diff = (tgl_lahir - ref_date).days
        # pasaran_index = (ref_pasaran + days_diff) % 5
        hari_index = tgl_lahir.weekday()
        
        usia_str = f"{delta.years} Tahun {delta.months} Bulan {delta.days} Hari"
        ultah_str = f"{bulan_menuju} Bulan {hari_sisa} Hari Lagi" if hari_menuju > 0 else "HARI INI ULANG TAHUN!"
        pasaran_str = f"{hari_list[hari_index]}, {tgl_lahir.strftime('%d %B %Y')}"
        
        return {
            "usia": usia_str,
            "ultah": ultah_str,
            "pasaran": pasaran_str,
            "tgl_lahir": tgl_lahir
        }
        
    except Exception as e:
        print(f"{RED_GLOW}[!] Error menghitung usia: {str(e)}")
        return None

def cek_nik_online(nik):
    print(f"{CYAN_GLOW}[*] Memproses NIK: {nik}")
    
    data = get_data_from_dc_api(nik)
    api_source = "deskcollection"
    
    if not data:
        data = get_data_from_rapidapi(nik)
        api_source = "rapidapi"
    
    parsed = parse_nik_structure(nik)
    if not parsed:
        print(f"{RED_GLOW}[!] NIK tidak valid!")
        return None
    
    usia_data = hitung_usia_pasaran(
        parsed["tgl_lahir"], 
        parsed["bln_lahir"], 
        parsed["thn_lahir"]
    )
    
    if not usia_data:
        print(f"{RED_GLOW}[!] Gagal menghitung usia!")
        return None
    
    tgl_lahir_str = f"{parsed['tgl_lahir']:02d}/{parsed['bln_lahir']:02d}/{parsed['thn_lahir']}"
    tgl_lahir_iso = f"{parsed['thn_lahir']}-{parsed['bln_lahir']:02d}-{parsed['tgl_lahir']:02d}"
    
    data_lengkap = {
        "nik": nik,
        "no_kartu": data.get("no_kartu", "N/A") if data else "N/A",
        "nama": data.get("nama", "DATA DARI API TIDAK DITEMUKAN") if data else "DATA DARI API TIDAK DITEMUKAN",
        "hub_kel": data.get("hubungan_keluarga", "N/A") if data else "N/A",
        "jenis_kelamin": parsed["jenis_kelamin"],
        "tanggal_lahir": tgl_lahir_iso,
        "lahir": tgl_lahir_str,
        
        "provinsi": parsed["wilayah"]["provinsi"],
        "kotakab": parsed["wilayah"]["kota"],
        "kecamatan": parsed["wilayah"]["kecamatan"],
        "uniqcode": nik[-4:],
        "kodepos": parsed["wilayah"]["kodepos"],
        
        "pasaran": usia_data["pasaran"],
        "usia": usia_data["usia"],
        "ultah": usia_data["ultah"],
        
        "alamat": data.get("alamat", parsed["wilayah"]["kecamatan"]) if data else parsed["wilayah"]["kecamatan"],
        "no_hp": data.get("no_hp", "N/A") if data else "N/A",
        "email": data.get("email", "N/A") if data else "N/A",
        "perusahaan": data.get("perusahaan", "N/A") if data else "N/A",
        "kode_perusahaan": data.get("kode_perusahaan", "N/A") if data else "N/A",
        "kelas": data.get("kelas", "N/A") if data else "N/A",
        "status": data.get("status", "N/A") if data else "N/A",
        "segmen": data.get("segmen", "N/A") if data else "N/A",
        "pisa": data.get("pisa", "N/A") if data else "N/A",
        "tmt": data.get("tmt", "N/A") if data else "N/A",
        "ppk": data.get("ppk", "N/A") if data else "N/A",
        
        "source": api_source,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if data:
        print(f"{GREEN_GLOW}[+] Data berhasil diambil dari {api_source.upper()} API")
    else:
        print(f"{YELLOW_GLOW}[!] Hanya data struktur NIK yang tersedia")
    
    return data_lengkap

def display_nik_data(data):
    """Tampilkan data NIK"""
    if not data:
        print(f"{RED_GLOW}[!] Tidak ada data untuk ditampilkan")
        return
    
    print(f"\n{RED_GLOW}‣‣‣‣‣ DATA DITEMUKAN [DanzXploit] ‣‣‣‣‣")
    
    fields_main = [
        ("NIK", data['nik']),
        ("No Kartu", data['no_kartu']),
        ("Nama", data['nama']),
        ("Hub Kel", data['hub_kel']),
        ("Jenis Kelamin", data['jenis_kelamin']),
        ("Tanggal Lahir", data['tanggal_lahir']),
        ("No HP", data['no_hp']),
        ("Email", data['email']),
        ("Alamat", data['alamat']),
    ]
    
    for label, value in fields_main:
        print(f"{RED_GLOW}‣ {label}: {WHITE_GLOW}{value}")
    
    print(f"\n{RED_GLOW}‣‣‣‣‣ DATA BPJS KESEHATAN ‣‣‣‣‣")
    fields_bpjs = [
        ("Perusahaan", data['perusahaan']),
        ("Kode Perusahaan", data['kode_perusahaan']),
        ("Kelas", data['kelas']),
        ("Status", data['status']),
        ("Segmen", data['segmen']),
        ("PISA", data['pisa']),
        ("TMT", data['tmt']),
        ("PPK", data['ppk']),
    ]
    
    for label, value in fields_bpjs:
        print(f"{RED_GLOW}‣ {label}: {WHITE_GLOW}{value}")
    
    print(f"\n{RED_GLOW}‣‣‣‣‣ INFORMASI TAMBAHAN ‣‣‣‣‣")
    fields_extra = [
        ("Provinsi", data['provinsi']),
        ("Kota/Kab", data['kotakab']),
        ("Kecamatan", data['kecamatan']),
        ("Kode Pos", data['kodepos']),
        ("Kode Unik", data['uniqcode']),
        ("Hari Pasaran", data['pasaran']),
        ("Usia Saat Ini", data['usia']),
        ("Menuju Ulang Tahun", data['ultah']),
    ]
    
    for label, value in fields_extra:
        print(f"{RED_GLOW}‣ {label}: {WHITE_GLOW}{value}")
    
    print(f"\n{RED_GLOW}‣‣‣‣‣ METADATA ‣‣‣‣‣")
    print(f"{RED_GLOW}‣ Timestamp: {GREEN_GLOW}{data['timestamp']}")

def nik_menu():
    """Menu utama program - INI YANG DIIMPORT"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{RED_GLOW}{'-' * 70}")
        print(f"{RED_GLOW}{' ' * 20} NIK OSINT - DanzXploit")
        print(f"{RED_GLOW}{'-' * 70}")
        
        print(f"\n{YELLOW_GLOW}[?] Masukkan NIK atau 'x' untuk keluar")
        print(f"{RED_GLOW}{'─' * 70}")
        
        nik_input = input(f"{GREEN_GLOW}[>] NIK: ").strip()
        
        if nik_input.lower() in ['x', 'exit', 'quit']:
            print(f"\n{RED_GLOW}[*] Keluar dari program...")
            break
        
        if len(nik_input) != 16 or not nik_input.isdigit():
            print(f"\n{RED_GLOW}[!] ERROR: NIK harus 16 digit angka!")
            print(f"{YELLOW_GLOW}[*] Contoh: 3515163008090001")
            input(f"\n{CYAN_GLOW}[*] Tekan Enter untuk melanjutkan...")
            continue
        
        print(f"\n{CYAN_GLOW}[*] Memproses NIK: {nik_input}")
        print(f"{RED_GLOW}{'─' * 70}")
        
        start_time = time.time()
        data = cek_nik_online(nik_input)
        end_time = time.time()
        
        if data:
            display_nik_data(data)
            print(f"\n{CYAN_GLOW}[*] Waktu proses: {end_time - start_time:.2f} detik")
        else:
            print(f"\n{RED_GLOW}[!] Data tidak ditemukan atau NIK tidak valid!")
        
        print(f"\n{RED_GLOW}{'█' * 70}")
        choice = input(f"{YELLOW_GLOW}[?] Cek NIK lain? (y/n): ").strip().lower()
        
        if choice != 'y':
            print(f"\n{RED_GLOW}[*] Terima kasih telah menggunakan DanzXploit")
            break

def batch_process_nik(nik_list):
    """Proses multiple NIKs (untuk import dari main.py)"""
    results = []
    
    print(f"{CYAN_GLOW}[*] Memproses {len(nik_list)} NIK...")
    
    for i, nik in enumerate(nik_list, 1):
        print(f"{YELLOW_GLOW}[{i}/{len(nik_list)}] Memproses: {nik}")
        
        data = cek_nik_online(nik)
        if data:
            results.append(data)
        
        if i < len(nik_list):
            time.sleep(1)
    
    return results

if __name__ == "__main__":
    
    try:
        import requests, colorama, dateutil
        print(f"{GREEN_GLOW}[+] Semua dependency terpenuhi")
    except ImportError:
        print(f"{RED_GLOW}[!] Install dependencies: pip install requests colorama python-dateutil")
        exit(1)
    
    print(f"{CYAN_GLOW}[*] Memulai program...")
    nik_menu()