import requests, json, time, random, os, re, datetime
from colorama import Fore, init; init()
from datetime import date
from dateutil.relativedelta import relativedelta
try:
    from wilayah_mapping_complete import KECAMATAN_MAPPING
except:
    KECAMATAN_MAPPING = {}

RED   = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
WHITE = Fore.LIGHTWHITE_EX
CYAN  = Fore.LIGHTCYAN_EX
GREY  = Fore.BLACK

API_KEYS = {
    "BINDERBYTE": "030c902dc62cdb4f6638d65ab617132ef8022a831c9ecafdc86376823079506b",
    "NUMVERIFY" : "1989c1d3b270a2ea108ef337088b8a6c",
    "TRUECALLER": "46c5b2438022267b1af91aa7f3fe6904"
}

UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sect(title, color=WHITE, w=60):
    p = (w - len(title) - 4) // 2
    print(f"\n{color}{'─' * w}\n{' ' * p}[ {title} ]{' ' * (w - p - len(title) - 4)}\n{'─' * w}")

def stat(msg, tp="info"):
    ic = "✓" if tp == "ok" else "!" if tp == "warn" else "✗"
    print(WHITE + f"[{ic}] {msg}")

def req(url, headers=None, params=None, timeout=20):
    try:
        r = requests.get(url, headers={"User-Agent": random.choice(UA), **(headers or {})}, params=params, timeout=timeout)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def osint_api_cepat(phone_number: str) -> dict:
    out = {}
    try:
        clean_num = re.sub(r"\D", "", phone_number)
        if clean_num.startswith('0'):
            e164_num = '+62' + clean_num[1:]
        elif clean_num.startswith('62'):
            e164_num = '+' + clean_num
        else:
            e164_num = '+62' + clean_num
        print(f"OSINT API: {e164_num}", end='', flush=True)
        response = requests.get(f"https://some-osint-api.com/search?phone={e164_num}", headers={"User-Agent": random.choice(UA)}, timeout=10)
        print(f" Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                result = data.get("data", {})
                out["nik"]            = result.get("national_id", "")
                out["nama_lengkap"]   = result.get("full_name", "")
                out["nama_ayah"]      = result.get("father_name", "")
                out["nama_ibu"]       = result.get("mother_name", "")
                out["email"]          = result.get("email", "")
                out["usia"]           = f"{result.get('age', 0)} Tahun" if result.get('age') else ""
                out["imei"]           = result.get("device_imei", "")
                out["device_brand"]   = result.get("device_brand", "")
                out["device_model"]   = result.get("device_model", "")
                out["address"]        = result.get("address", "")
                out["birth_date"]     = result.get("birth_date", "")
                out["occupation"]     = result.get("occupation", "")
                out["bank_accounts"]  = result.get("bank_accounts", [])
                out["social_profiles"]= result.get("social_profiles", {})
                out["carrier"]        = result.get("carrier", "")
                out["location"]       = result.get("location", "")
                print(" ✓ WORK 100%")
                return out
        print(" ✗ API Error")
        return {}
    except Exception as e:
        print(f" ✗ Exception: {e}")
        return {}

def track_phone_realistic(number: str) -> dict:
    out = {}
    num   = re.sub(r"\D", "", number)
    if num.startswith('0'):
        intl_num = '+62' + num[1:]
    elif num.startswith('62'):
        intl_num = '+' + num
    else:
        intl_num = '+62' + num
    print(f"Tracking: {num} → {intl_num}")

    print("Numverify...", end='', flush=True)
    nv = req("http://apilayer.net/api/validate", params={"access_key": API_KEYS["NUMVERIFY"], "number": intl_num, "format": 1})
    if nv and nv.get("valid"):
        out["carrier"]   = nv.get("carrier", "-")
        out["country"]   = nv.get("country_name", "-")
        out["line_type"] = nv.get("line_type", "-")
        out["location"]  = nv.get("location", "-")
        print(" ✓")
    else:
        print(" ✗")

    print("TrueCaller...", end='', flush=True)
    headers = {"x-api-key": API_KEYS["TRUECALLER"], "User-Agent": random.choice(UA)}
    tc = req("https://api.truecaller-dev.com/v1/lookup", headers=headers, params={"phone": intl_num})
    if tc:
        out["nama_lengkap"] = tc.get("name", "")
        out["email"]        = tc.get("email", "")
        out["nik"]          = tc.get("nik", "")
        if tc.get("age"):
            out["usia"] = f"{tc.get('age')} Tahun"
        print(" ✓")
    else:
        print(" ✗")

    print("PhoneInfoga...", end='', flush=True)
    try:
        local_result = requests.post("http://localhost:5000/api/v2/numbers", json={"number": intl_num}, timeout=10)
        if local_result.status_code == 200:
            scanners = ["local", "numverify", "ovh"]
            for scanner in scanners:
                scan_result = requests.post(f"http://localhost:5000/api/v2/scanners/{scanner}/run", json={"number": intl_num}, timeout=15)
                if scan_result.status_code == 200:
                    data = scan_result.json()
                    if data.get("success"):
                        out[f"phoneinfoga_{scanner}"] = data.get("data", {})
            print(" ✓")
        else:
            print(" ✗")
    except:
        print(" ✗")

    print("IP Location...", end='', flush=True)
    ip_data = req(f"http://ip-api.com/json/{intl_num}?fields=status,query,isp,org,country,regionName,city,lat,lon,timezone")
    if ip_data and ip_data.get("status") == "success":
        out["ip"]        = ip_data.get("query", "-")
        out["ip_isp"]    = ip_data.get("isp", "-")
        out["ip_city"]   = ip_data.get("city", "-")
        out["ip_region"] = ip_data.get("regionName", "-")
        print(" ✓")
    else:
        print(" ✗")

    print("Google search...", end='', flush=True)
    try:
        search_queries = [
            f'"{num}" facebook indonesia',
            f'"{intl_num}" whatsapp business',
            f'"{num}" nama orang',
            f'"{num}" ktp indonesia'
        ]
        google_data = {}
        for query in search_queries[:2]:
            g_response = requests.get("https://www.google.com/search", params={"q": query}, headers={"User-Agent": random.choice(UA)}, timeout=10)
            if g_response.status_code == 200:
                content = g_response.text.lower()
                name_patterns = [r'([a-z]+\s+[a-z]+\s+[a-z]+)', r'([a-z]+\s+[a-z]+)']
                for pattern in name_patterns:
                    names = re.findall(pattern, content)
                    if names and len(names[0]) > 6:
                        google_data["possible_name"] = names[0].title()
                        break
                emails = re.findall(r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b', content)
                if emails:
                    google_data["possible_email"] = emails[0]
                niks = re.findall(r'\b\d{16}\b', content)
                if niks:
                    google_data["possible_nik"] = niks[0]
                if google_data:
                    break
        if google_data:
            out["google_search"] = google_data
            if not out.get("nama_lengkap") and google_data.get("possible_name"):
                out["nama_lengkap"] = google_data["possible_name"]
            if not out.get("email") and google_data.get("possible_email"):
                out["email"] = google_data["possible_email"]
            if not out.get("nik") and google_data.get("possible_nik"):
                out["nik"] = google_data["possible_nik"]
            print(" ✓")
        else:
            print(" ✗")
    except:
        print(" ✗")

    print("Social media...", end='', flush=True)
    social_data = {}
    try:
        wa_url = f"https://wa.me/{num}"
        if requests.head(wa_url, timeout=10).status_code in [200, 301, 302]:
            social_data["whatsapp"] = wa_url
    except:
        pass
    try:
        tg_url = f"https://t.me/{num}"
        if requests.head(tg_url, timeout=10).status_code in [200, 301, 302]:
            social_data["telegram"] = tg_url
    except:
        pass
    if social_data:
        out["social_media"] = social_data
        print(" ✓")
    else:
        print(" ✗")
    return out

def dox_number_enhanced(number: str) -> dict:
    num = re.sub(r"\D", "", number)
    out = {
        "number": num,
        "nik": "",
        "nama_lengkap": "",
        "nama_ortu": "",
        "email": "",
        "usia": "",
        "imei": "",
        "ip": "",
        "carrier": "",
        "country": "",
        "line_type": "",
        "source": [],
        "additional_data": {}
    }
    print(f"Input: {number} → Processing: {num}")
    print("OSINT API BARU...", end='', flush=True)
    osint_data = osint_api_cepat(num)
    if osint_data:
        out["nik"]          = osint_data.get("nik", "")
        out["nama_lengkap"] = osint_data.get("nama_lengkap", "")
        out["email"]        = osint_data.get("email", "")
        out["usia"]         = osint_data.get("usia", "")
        out["imei"]         = osint_data.get("imei", "")
        out["merek_hp"]     = osint_data.get("device_brand", "")
        out["model_hp"]     = osint_data.get("device_model", "")
        if osint_data.get("nama_ayah") and osint_data.get("nama_ibu"):
            out["nama_ortu"] = f"Ayah: {osint_data['nama_ayah']}, Ibu: {osint_data['nama_ibu']}"
        elif osint_data.get("nama_ayah"):
            out["nama_ortu"] = osint_data["nama_ayah"]
        elif osint_data.get("nama_ibu"):
            out["nama_ortu"] = osint_data["nama_ibu"]
        out["carrier"]   = osint_data.get("carrier", "")
        out["country"]   = "Indonesia"
        out["line_type"] = "mobile"
        out["additional_data"] = {
            "osint_api": osint_data,
            "address": osint_data.get("address", ""),
            "birth_date": osint_data.get("birth_date", ""),
            "occupation": osint_data.get("occupation", ""),
            "bank_accounts": osint_data.get("bank_accounts", []),
            "social_profiles": osint_data.get("social_profiles", {})
        }
        out["source"] = ["osint-api-100"]
        print(" Complete! WORK 100%")
        return out
    print("Backup APIs...", end='', flush=True)
    realistic_data = track_phone_realistic(num)
    if realistic_data:
        out["nik"]          = realistic_data.get("nik", "")
        out["nama_lengkap"] = realistic_data.get("nama_lengkap", "")
        out["email"]        = realistic_data.get("email", "")
        out["usia"]         = realistic_data.get("usia", "")
        out["imei"]         = realistic_data.get("imei", "")
        out["ip"]           = realistic_data.get("ip", "")
        out["carrier"]      = realistic_data.get("carrier", "")
        out["country"]      = realistic_data.get("country", "")
        out["line_type"]    = realistic_data.get("line_type", "")
        if realistic_data.get("nama_ayah") and realistic_data.get("nama_ibu"):
            out["nama_ortu"] = f"Ayah: {realistic_data['nama_ayah']}, Ibu: {realistic_data['nama_ibu']}"
        elif realistic_data.get("nama_ayah"):
            out["nama_ortu"] = realistic_data["nama_ayah"]
        elif realistic_data.get("nama_ibu"):
            out["nama_ortu"] = realistic_data["nama_ibu"]
        out["additional_data"] = {
            "location": realistic_data.get("location", ""),
            "ip_info": {
                "isp": realistic_data.get("ip_isp", ""),
                "city": realistic_data.get("ip_city", ""),
                "region": realistic_data.get("ip_region", "")
            },
            "social_media": realistic_data.get("social_media", {}),
            "google_search": realistic_data.get("google_search", {}),
            "phoneinfoga": realistic_data.get("phoneinfoga_local", {})
        }
        sources = ["numverify"]
        if realistic_data.get("nama_lengkap"): sources.append("truecaller")
        if realistic_data.get("ip"): sources.append("ip-api")
        if realistic_data.get("google_search"): sources.append("google-search")
        if realistic_data.get("social_media"): sources.append("social-check")
        if realistic_data.get("phoneinfoga_local"): sources.append("phoneinfoga")
        out["source"] = sources
        print(" Complete!")
    else:
        print(" No data found!")
    return out

def display_number_enhanced(data):
    if not data:
        stat("Data tidak tersedia")
        return
    sect("HASIL DOX NOMOR - ENHANCED REALISTIC")
    print(f"{CYAN}│ {WHITE}Nomor        : {data.get('number','-')}")
    main_data = [
        ("NIK", data.get("nik","")),
        ("Nama Lengkap", data.get("nama_lengkap","")),
        ("Nama Ortu", data.get("nama_ortu","")),
        ("Email", data.get("email","")),
        ("Usia", data.get("usia","")),
        ("IMEI", data.get("imei","")),
        ("IP Address", data.get("ip",""))
    ]
    success_count = 0
    for label, value in main_data:
        if value:
            print(f"{CYAN}│ {WHITE}{label:17}: {GREEN}{value}{WHITE}")
            success_count += 1
        else:
            print(f"{CYAN}│ {WHITE}{label:17}: {GREY}-{WHITE}")
    print(f"{CYAN}│ {WHITE}Carrier      : {data.get('carrier','-')}")
    print(f"{CYAN}│ {WHITE}Country      : {data.get('country','-')}")
    print(f"{CYAN}│ {WHITE}Line Type    : {data.get('line_type','-')}")
    if data.get("additional_data"):
        add_data = data["additional_data"]
        if add_data.get("ip_info", {}).get("city"):
            print(f"{CYAN}│ {WHITE}Location     : {add_data['ip_info']['city']}, {add_data['ip_info'].get('region', '')}")
        if add_data.get("social_media"):
            print(f"{CYAN}│ {WHITE}Social Media : {len(add_data['social_media'])} platform")
    print(f"{CYAN}│ {WHITE}Data Found   : {success_count}/7 utama")
    print(f"{CYAN}│ {WHITE}Sources      : {', '.join(data.get('source',[]))}")
    print(f"{CYAN}{'─' * 64}")

def dox_menu():
    while True:
        clear()
        print(f"""
{RED}╔════════════════════════════════════════════════════════════╗
{RED}║   ▓▓   D O X – B L A C K A R C H – V 5.0   ▓▓             ║
{RED}║           ENHANCED REALISTIC APIs                          ║
{RED}║                                                            ║
{RED}║   1. NIK Parser          2. Nomor (Enhanced)   0.Back     ║
{RED}╚════════════════════════════════════════════════════════════╝{WHITE}
""")
        ch = input("\n[?] Pilih: ").strip()
        if ch == "1":
            while True:
                clear()
                sect("DOX NIK")
                nik = input("\n[?] NIK 16 digit: ").strip()
                if nik.lower() == "0":
                    break
                if not nik.isdigit() or len(nik) != 16:
                    stat("NIK harus 16 digit!")
                    input()
                    continue
                out = {"nik": nik, "source": [], "foto_ktp": None}
                bb = req("https://api.binderbyte.com/v1/ktp", params={"nik": nik, "api_key": API_KEYS["BINDERBYTE"]})
                if bb and bb.get("status") == 200:
                    out.update(bb["data"])
                    out["source"].append("binderbyte")
                    if bb["data"].get("foto"):
                        out["foto_ktp"] = bb["data"]["foto"]
                sect("HASIL DOX NIK")
                print(f"{CYAN}│ {WHITE}NIK        : {out.get('nik','-')}")
                for k, v in out.items():
                    if k not in ["nik", "source", "foto_ktp"]:
                        print(f"{CYAN}│ {WHITE}{k:17}: {v}")
                if out.get("foto_ktp"):
                    print(f"{CYAN}│ {WHITE}Foto KTP   : {GREEN}tersimpan base64 di file")
                print(f"{CYAN}{'─' * 64}")
                if input("\n[?] Simpan? (y/n): ").lower() == "y":
                    fn = f"dox_nik_{nik}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(fn, "w", encoding="utf-8") as f:
                        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
                    stat(f"Tersimpan → {fn}", "ok")
                if input("\n[?] Lagi? (y/n): ").lower() != "y":
                    break
        elif ch == "2":
            while True:
                clear()
                sect("DOX NOMOR - ENHANCED REALISTIC")
                num = input("\n[?] Nomor (08/62/+): ").strip()
                if num.lower() == "0":
                    break
                if not num:
                    stat("Nomor kosong!")
                    input()
                    continue
                data = dox_number_enhanced(num)
                display_number_enhanced(data)
                if input("\n[?] Simpan? (y/n): ").lower() == "y":
                    fn = f"enhanced_dox_{num}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(fn, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                    stat(f"Tersimpan → {fn}", "ok")
                if input("\n[?] Lagi? (y/n): ").lower() != "y":
                    break
        elif ch == "0":
            stat("Kembali ke menu utama...", "ok")
            break
        else:
            stat("Pilihan tidak valid", "warn")
            input()

if __name__ == "__main__":
    dox_menu()