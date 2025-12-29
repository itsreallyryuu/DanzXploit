
import requests, datetime, os, webbrowser
from colorama import Fore, init; init()

RED    = Fore.LIGHTRED_EX
GREEN  = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
CYAN   = Fore.LIGHTCYAN_EX
WHITE  = Fore.LIGHTWHITE_EX
GREY   = Fore.BLACK

API_IP = "http://ip-api.com/json/{}{}".format
FIELDS = "status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"

def clear(): os.system('cls' if os.name=='nt' else 'clear')

def header():
    clear()
    print(f"""
{CYAN}--------------------------------------------------------
{RED} 1. Lacak IP
{RED} 2. IP Saya
{RED} 0. Kembali
{CYAN}--------------------------------------------------------
{GREY}          Real-time data – 100 % akurat – no dummy{WHITE}
""")

def stat(msg, tp="info"):
    if tp=="ok":   print(GREEN +f"[✓] {msg}")
    elif tp=="warn":print(YELLOW+f"[!] {msg}")
    elif tp=="err": print(RED   +f"[✗] {msg}")
    else:           print(CYAN  +f"[*] {msg}")

def req(url):
    try: r=requests.get(url,timeout=10); return r.json() if r.status_code==200 else None
    except Exception as e: stat(f"Request gagal: {e}","err"); return None

def utc_to_iso(offset_sec):
    try:
        now = datetime.datetime.utcnow()
        local = now + datetime.timedelta(seconds=offset_sec)
        return local.strftime("%Y-%m-%dT%H:%M:%S") + f"+{offset_sec//3600:02d}:00"
    except: return "-"

def flag(cc):
    if not cc or len(cc)!=2: return ""
    return chr(ord(cc[0])+0x1F1A5)+chr(ord(cc[1])+0x1F1A5)

def lacak_ip(ip):
    stat(f"Melacak IP: {ip}")
    data=req(API_IP(ip,f"?fields={FIELDS}"))
    if data and data.get("status")=="success":
        offset = data.get("offset",0)
        cc = data.get("countryCode","")
        lat = data.get("lat")
        lon = data.get("lon")
        maps = f"https://www.google.com/maps/search/{lat},{lon}" if lat and lon else "-"
        return {
            "IP Target"     : data.get("query"),
            "Type IP"       : "IPv4" if "." in data.get("query","") else "IPv6",
            "Country"       : f"{data.get('country','')} {flag(cc)}",
            "Country Code"  : cc,
            "City"          : data.get("city"),
            "Region"        : data.get("regionName"),
            "District"      : data.get("district") or "-",
            "ZIP"           : data.get("zip") or "-",
            "Latitude"      : lat,
            "Longitude"     : lon,
            "Maps"          : maps,
            "ISP"           : data.get("isp"),
            "ORG"           : data.get("org"),
            "AS"            : data.get("as"),
            "Timezone"      : data.get("timezone"),
            "Currency"      : data.get("currency"),
            "Mobile"        : "Yes" if data.get("mobile") else "No",
            "Proxy"         : "Yes" if data.get("proxy")  else "No",
            "Hosting"       : "Yes" if data.get("hosting") else "No",
            "Offset"        : offset,
            "UTC"           : f"+{offset//3600:02d}:00",
            "Current Time"  : utc_to_iso(offset)
        }
    return {}

def ip_saya(): return lacak_ip("")

def box_ip(d,title="HASIL PELACAKAN IP"):
    print(f"\n{RED}{'─'*64}")
    print(f"{RED} {title.center(64)} ")
    print(f"{RED}{'─'*64}")
    for k,v in d.items():
        if k=="Maps" and v!="-":
            print(f"{CYAN}│ {WHITE}{k:17} {CYAN}: \033[4m{WHITE}{v}\033[0m")
        else:
            print(f"{CYAN}│ {WHITE}{k:17} {CYAN}: {WHITE}{v}")
    print(f"{CYAN}{'─'*64}")
    if "Maps" in d and d["Maps"]!="-":
        ask=input(f"\n{CYAN}[>] Buka maps di browser? (y/n): {WHITE}").strip().lower()
        if ask=="y":
            webbrowser.open(d["Maps"],new=2)

def ip_menu():
    while True:
        header()
        opt=input(f"\n{CYAN}[>] Pilih: {WHITE}").strip()
        if opt=="1":
            ip=input(f"\n{CYAN}[>] Masukkan IP: {WHITE}").strip()
            if ip:
                data=lacak_ip(ip)
                if data: box_ip(data)
                else: stat("IP tidak valid / tidak ditemukan","warn")
            else: stat("IP kosong","err")
            input(f"\n{YELLOW}[*] Enter untuk kembali...")
        elif opt=="2":
            data=ip_saya()
            if data: box_ip(data,"IP PUBLIK ANDA")
            else: stat("Gagal mendapatkan IP publik","warn")
            input(f"\n{YELLOW}[*] Enter untuk kembali...")
        elif opt=="0":
            break
        else:
            stat("Pilihan tidak valid","warn")
            input(f"\n{YELLOW}[*] Enter untuk kembali...")

def ip_menu_wrapper():
    ip_menu()

if __name__=="__main__":
    try: ip_menu()
    except KeyboardInterrupt: print(f"\n{RED}[!] Dibatalkan pengguna")