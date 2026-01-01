import requests, json, time, random, os, re, datetime, ssl, urllib3
from datetime import date, datetime as dt
from dateutil.relativedelta import relativedelta
from colorama import Fore, init; init(autoreset=True)

urllib3.disable_warnings()

R = Fore.LIGHTRED_EX
G = Fore.LIGHTGREEN_EX
Y = Fore.LIGHTYELLOW_EX
C = Fore.LIGHTCYAN_EX
W = Fore.LIGHTWHITE_EX

DC_API_URL = "https://deskcollection.space/api/v1/kpu/cek"
DC_API_KEY = "dc_9712ee4c40eadde0ca70f262400b8a6c"
RAPID_KEY  = "9faaa2b50fmsh5b48ae01005e119p1ff81djsn05fe4be86bf4"
RAPID_URL  = "https://nik-parser.p.rapidapi.com/ektp"

API_KEYS = {
    "BINDERBYTE": "030c902dc62cdb4f6638d65ab617132ef8022a831c9ecafdc86376823079506b",
    "NUMVERIFY" : "1989c1d3b270a2ea108ef337088b8a6c",
    "TRUECALLER": "46c5b2438022267b1af91aa7f3fe6904"
}

UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def sect(title, color=W, w=60):
    p = (w - len(title) - 4) // 2
    print(f"\n{color}{'─' * w}\n{' ' * p}[ {title} ]{' ' * (w - p - len(title) - 4)}\n{'─' * w}")

def stat(msg, tp="info"):
    ic = "✓" if tp == "ok" else "!" if tp == "warn" else "✗"
    print(W + f"[{ic}] {msg}")

def req(url, headers=None, params=None, data=None, method="GET", timeout=20):
    try:
        hdr = {"User-Agent": random.choice(UA)}
        if headers: hdr.update(headers)
        if method.upper() == "GET":
            r = requests.get(url, headers=hdr, params=params, timeout=timeout, verify=False)
        else:
            r = requests.post(url, headers=hdr, json=data, timeout=timeout, verify=False)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def parse_nik_structure(nik):
    if len(nik) != 16 or not nik.isdigit(): return None
    try:
        kec = nik[:6]
        tgl_raw = int(nik[6:8])
        bln = int(nik[8:10])
        thn = int(nik[10:12])
        thn += 1900 if thn > 30 else 2000
        jk = "PEREMPUAN" if tgl_raw > 40 else "LAKI-LAKI"
        tgl = tgl_raw - 40 if tgl_raw > 40 else tgl_raw
        if not (1 <= tgl <= 31 and 1 <= bln <= 12): return None
        return {"kec": kec, "tgl": tgl, "bln": bln, "thn": thn, "jk": jk}
    except: return None

def get_wil(kec):
    big = {
        "317101": ("DKI Jakarta", "Kota Jakarta Pusat", "Gambir"),
        "317102": ("DKI Jakarta", "Kota Jakarta Pusat", "Johar Baru"),
        "327301": ("Jawa Barat", "Kota Bandung", "Bandung"),
        "332401": ("Jawa Tengah", "Kota Semarang", "Semarang"),
        "352401": ("Jawa Timur", "Kota Surabaya", "Surabaya"),
    }
    return big.get(kec, ("", "", ""))

def hitung_usia(tgl, bln, thn):
    try:
        lahir = date(thn, bln, tgl)
        hari_ini = date.today()
        delta = relativedelta(hari_ini, lahir)
        ultah_tahun_ini = lahir.replace(year=hari_ini.year)
        if ultah_tahun_ini < hari_ini:
            ultah_tahun_depan = lahir.replace(year=hari_ini.year + 1)
            menuju = (ultah_tahun_depan - hari_ini).days
        else:
            menuju = (ultah_tahun_ini - hari_ini).days
        return f"{delta.years} Tahun {delta.months} Bulan {delta.days} Hari", f"{menuju} hari lagi"
    except: return "-", "-"

def api_deskcoll(nik):
    hdr = {"Content-Type": "application/json", "Authorization": f"Bearer {DC_API_KEY}"}
    res = req(DC_API_URL, headers=hdr, data={"nik": nik}, method="POST")
    if res and res.get("success"):
        print(G + "[+] DC API ditemukan")
        return res.get("data", {})
    return None

def api_rapid(nik):
    hdr = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "nik-parser.p.rapidapi.com"}
    res = req(RAPID_URL, headers=hdr, params={"nik": nik})
    if res:
        print(G + "[+] RapidAPI ditemukan")
        return res
    return None

def cek_nik(nik):
    parsed = parse_nik_structure(nik)
    if not parsed: return None
    data = api_deskcoll(nik) or api_rapid(nik) or {}
    usia, ultah = hitung_usia(parsed["tgl"], parsed["bln"], parsed["thn"])
    prov, kab, kec = get_wil(parsed["kec"])
    return {
        "nik": nik,
        "nama": data.get("nama", "-"),
        "jk": parsed["jk"],
        "lahir": f"{parsed['thn']}-{parsed['bln']:02d}-{parsed['tgl']:02d}",
        "prov": prov or "-",
        "kab": kab or "-",
        "kec": kec or "-",
        "usia": usia,
        "ultah": ultah,
        "alamat": data.get("alamat", "-"),
        "hp": data.get("no_hp", "-"),
        "email": data.get("email", "-"),
        "source": "dc-api" if data else "nik-parser"
    }

def display_nik(data):
    if not data: return
    sect("HASIL DOX NIK", R)
    garis = f"{C}│ {W}"
    print(f"{garis}NIK          : {data['nik']}")
    print(f"{garis}Nama         : {G}{data['nama']}{W}")
    print(f"{garis}Jenis Kel.   : {data['jk']}")
    print(f"{garis}Tgl Lahir    : {data['lahir']}")
    print(f"{garis}Usia         : {data['usia']}")
    print(f"{garis}Ultah Berik. : {data['ultah']}")
    print(f"{garis}Provinsi     : {data['prov']}")
    print(f"{garis}Kota/Kab     : {data['kab']}")
    print(f"{garis}Kecamatan    : {data['kec']}")
    print(f"{garis}Alamat       : {data['alamat']}")
    print(f"{garis}No HP        : {data['hp']}")
    print(f"{garis}Email        : {data['email']}")
    print(f"{garis}Source       : {data['source']}")
    print(C + "─" * 64)

def menu_nik():
    while True:
        clear()
        print(f"{R}╔════════════════════════════════════════════════════════════╗")
        print(f"{R}║              D O X   N I K  –  D a n z 6                   ║")
        print(f"{R}╚════════════════════════════════════════════════════════════╝{W}")
        nik = input("\n[?] NIK (16 digit) / 0 = back : ").strip()
        if nik == "0": break
        if len(nik) != 16 or not nik.isdigit():
            stat("NIK harus 16 digit angka!", "warn")
            input("  Tekan Enter…"); continue
        data = cek_nik(nik)
        display_nik(data)
        if input("\n[?] Simpan JSON? (y/n): ").lower() == "y":
            fn = f"dox_nik_{nik}_{dt.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(fn, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            stat(f"Tersimpan → {fn}", "ok")
        if input("\n[?] Lagi? (y/n): ").lower() != "y": break

def fix_num(nom):
    n = re.sub(r"\D", "", nom)
    if n.startswith("0"):     return "+62" + n[1:]
    if n.startswith("62"):    return "+" + n
    if n.startswith("8"):     return "+62" + n
    return "+62" + n

def osint_telp(num):
    out = {"number": num, "nik": "", "nama": "", "email": "", "usia": "",
           "imei": "", "ip": "", "carrier": "", "country": "", "line_type": "",
           "source": [], "extra": {}}
    intl = fix_num(num)
    print(f"Tracking: {num} → {intl}")

    nv = req("http://apilayer.net/api/validate",
             params={"access_key": API_KEYS["NUMVERIFY"], "number": intl, "format": 1})
    if nv and nv.get("valid"):
        out["carrier"] = nv.get("carrier", "-")
        out["country"] = nv.get("country_name", "-")
        out["line_type"] = nv.get("line_type", "-")
        # out["source"].append("numverify"); print(" ✓")
    # else: print(" ✗")

    # print("TrueCaller...", end='', flush=True)
    tc = req("https://api.truecaller-dev.com/v1/lookup",
             headers={"x-api-key": API_KEYS["TRUECALLER"]}, params={"phone": intl})
    if tc:
        out["nama"] = tc.get("name", "")
        out["email"] = tc.get("email", "")
        out["nik"] = tc.get("nik", "")
        if tc.get("age"): out["usia"] = f"{tc['age']} Tahun"
        # out["source"].append("truecaller"); print(" ✓")
    # else: print(" ✗")

    # print("IP-API...", end='', flush=True)
    ip = req(f"http://ip-api.com/json/{intl}?fields=status,query,isp,org,country,regionName,city")
    if ip and ip.get("status") == "success":
        out["ip"] = ip.get("query", "-")
        out["extra"]["ip_isp"] = ip.get("isp", "-")
        out["extra"]["ip_city"] = ip.get("city", "-")
        out["extra"]["ip_region"] = ip.get("regionName", "-")
        # out["source"].append("ip-api"); print(" ✓")
    # else: print(" ✗")

    # print("Google dork...", end='', flush=True)
    try:
        queries = [f'"{num}" site:facebook.com', f'"{intl}" site:whatsapp.com']
        gdata = {}
        for q in queries:
            r = requests.get("https://www.google.com/search", params={"q": q},
                             headers={"User-Agent": random.choice(UA)}, timeout=8)
            if r.status_code == 200:
                txt = r.text.lower()
                names = re.findall(r'([a-z]{4,}\s+[a-z]{4,})', txt)
                if names: gdata["name"] = names[0].title(); break
        if gdata:
            if not out["nama"]: out["nama"] = gdata["name"]
            out["extra"]["google"] = gdata
            # out["source"].append("google"); print(" ✓")
        # else: print(" ✗")
    except: print(" ✗")

    # print("Social check...", end='', flush=True)
    soc = {}
    try:
        if requests.head(f"https://wa.me/{intl}", timeout=8).status_code in [200, 301, 302]:
            soc["whatsapp"] = f"https://wa.me/{intl}"
    except: pass
    try:
        if requests.head(f"https://t.me/{intl}", timeout=8).status_code in [200, 301, 302]:
            soc["telegram"] = f"https://t.me/{intl}"
    except: pass
    if soc:
        out["extra"]["social"] = soc
        # out["source"].append("social"); print(" ✓")
    # else: print(" ✗")
    return out

def display_telp(d):
    if not d: return
    sect("HASIL DOX NOMOR – ENHANCED", G)
    garis = f"{C}│ {W}"
    print(f"{garis}Nomor        : {d['number']}")
    fields = [("NIK", d["nik"]), ("Nama", d["nama"]), ("Email", d["email"]),
              ("Usia", d["usia"]), ("IMEI", d["imei"]), ("IP", d["ip"])]
    ok = 0
    for lbl, val in fields:
        if val:
            print(f"{garis}{lbl:17}: {G}{val}{W}"); ok += 1
        else:
            print(f"{garis}{lbl:17}: {W}")
    print(f"{garis}Carrier      : {d['carrier']}")
    print(f"{garis}Country      : {d['country']}")
    print(f"{garis}Line Type    : {d['line_type']}")
    if d["extra"].get("ip_city"):
        print(f"{garis}Location     : {d['extra']['ip_city']}, {d['extra'].get('ip_region','')}")
    if d["extra"].get("social"):
        print(f"{garis}Social       : {len(d['extra']['social'])} platform")
    print(f"{garis}Data Found   : {ok}/6")
    # print(f"{garis}Sources      : {', '.join(d['source'])}")
    print(C + "─" * 64)

def menu_telp():
    while True:
        clear()
        print(f"{R}╔════════════════════════════════════════════════════════════╗")
        print(f"{R}║           D O X   N O M O R  –  E N H A N C E D            ║")
        print(f"{R}╚════════════════════════════════════════════════════════════╝{W}")
        nom = input("\n[?] Nomor (08/62/+) / 0 = back : ").strip()
        if nom == "0": break
        if not nom:
            stat("Nomor kosong!", "warn")
            input(); continue
        data = osint_telp(nom)
        display_telp(data)
        if input("\n[?] Simpan JSON? (y/n): ").lower() == "y":
            fn = f"dox_nomor_{nom}_{dt.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(fn, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            stat(f"Tersimpan → {fn}", "ok")
        if input("\n[?] Lagi? (y/n): ").lower() != "y": break

# ---------- MENU UTAMA ----------
def main():
    while True:
        clear()
        print(f"{R}╔════════════════════════════════════════════════════════════╗")
        print(f"{R}║   ▓▓   D O X – B L A C K A R C H – V 6   ▓▓               ║")
        print(f"{R}║         NIK (Danz)  |  Nomor (Enhanced)                   ║")
        print(f"{R}╚════════════════════════════════════════════════════════════╝{W}")
        print("\n  1. DOX NIK\n  2. DOX Nomor\n  0. Exit")
        ch = input("\n[?] Pilih : ").strip()
        if ch == "1": menu_nik()
        elif ch == "2": menu_telp()
        elif ch == "0":
            stat("Keluar...", "ok"); break
        else:
            stat("Pilihan tidak valid!", "warn")
            input()

def dox_menu():      # tambahkan wrapper
    main()

if __name__ == "__main__":
    dox_menu()