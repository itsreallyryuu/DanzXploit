import requests, json, time, random, urllib3, ssl, datetime, sys, os, re
from colorama import Fore, Style, init
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

init(autoreset=True)
urllib3.disable_warnings()

# ========== WARNA ==========
RED_GLOW = Fore.LIGHTRED_EX
GREEN_GLOW = Fore.LIGHTGREEN_EX
YELLOW_GLOW = Fore.LIGHTYELLOW_EX
CYAN_GLOW = Fore.LIGHTCYAN_EX
WHITE_GLOW = Fore.LIGHTWHITE_EX

# ========== CONFIG API ==========
DC_API_URL = "https://deskcollection.space/api/v1/kpu/cek"
DC_API_KEY = "dc_9712ee4c40eadde0ca70f262400b163a3144460ce0d00e8e"
RAPIDAPI_KEY = "9faaa2b50fmsh5b48ae01005e119p1ff81djsn05fe4be86bf4"
RAPIDAPI_URL = "https://nik-parser.p.rapidapi.com/ektp"
KEMENDAGRI_API = "https://www.kemendagri.go.id/api/cekekode"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

WILAYAH_MAPPING = {
    "11": {  # Aceh
        "nama": "Aceh",
        "kabupaten_kota": {
            "1101": "Kabupaten Aceh Barat",
            "1102": "Kabupaten Aceh Barat Daya",
            "1103": "Kabupaten Aceh Besar",
            "1104": "Kabupaten Aceh Jaya",
            "1105": "Kabupaten Aceh Selatan",
            "1106": "Kabupaten Aceh Singkil",
            "1107": "Kabupaten Aceh Tamiang",
            "1108": "Kabupaten Aceh Tengah",
            "1109": "Kabupaten Aceh Tenggara",
            "1110": "Kabupaten Aceh Timur",
            "1111": "Kabupaten Aceh Utara",
            "1112": "Kabupaten Bener Meriah",
            "1113": "Kabupaten Bireuen",
            "1114": "Kabupaten Gayo Lues",
            "1115": "Kabupaten Nagan Raya",
            "1116": "Kabupaten Pidie",
            "1117": "Kabupaten Pidie Jaya",
            "1118": "Kabupaten Simeulue",
            "1171": "Kota Banda Aceh",
            "1172": "Kota Langsa",
            "1173": "Kota Lhokseumawe",
            "1174": "Kota Sabang",
            "1175": "Kota Subulussalam"
        }
    },
    "12": {  # Sumatera Utara
        "nama": "Sumatera Utara",
        "kabupaten_kota": {
            "1201": "Kabupaten Asahan",
            "1202": "Kabupaten Batubara",
            "1203": "Kabupaten Dairi",
            "1204": "Kabupaten Deli Serdang",
            "1205": "Kabupaten Humbang Hasundutan",
            "1206": "Kabupaten Karo",
            "1207": "Kabupaten Labuhan Batu",
            "1208": "Kabupaten Labuhan Batu Selatan",
            "1209": "Kabupaten Labuhan Batu Utara",
            "1210": "Kabupaten Langkat",
            "1211": "Kabupaten Mandailing Natal",
            "1212": "Kabupaten Nias",
            "1213": "Kabupaten Nias Barat",
            "1214": "Kabupaten Nias Selatan",
            "1215": "Kabupaten Nias Utara",
            "1216": "Kabupaten Padang Lawas",
            "1217": "Kabupaten Padang Lawas Utara",
            "1218": "Kabupaten Pakpak Bharat",
            "1219": "Kabupaten Samosir",
            "1220": "Kabupaten Serdang Bedagai",
            "1221": "Kabupaten Simalungun",
            "1222": "Kabupaten Tapanuli Selatan",
            "1223": "Kabupaten Tapanuli Tengah",
            "1224": "Kabupaten Tapanuli Utara",
            "1225": "Kabupaten Toba",
            "1271": "Kota Binjai",
            "1272": "Kota Gunungsitoli",
            "1273": "Kota Medan",
            "1274": "Kota Padangsidimpuan",
            "1275": "Kota Pematangsiantar",
            "1276": "Kota Sibolga",
            "1277": "Kota Tanjungbalai",
            "1278": "Kota Tebing Tinggi"
        }
    },
    "13": {  # Sumatera Barat
        "nama": "Sumatera Barat",
        "kabupaten_kota": {
            "1301": "Kabupaten Agam",
            "1302": "Kabupaten Dharmasraya",
            "1303": "Kabupaten Kepulauan Mentawai",
            "1304": "Kabupaten Lima Puluh Kota",
            "1305": "Kabupaten Padang Pariaman",
            "1306": "Kabupaten Pasaman",
            "1307": "Kabupaten Pasaman Barat",
            "1308": "Kabupaten Pesisir Selatan",
            "1309": "Kabupaten Sijunjung",
            "1310": "Kabupaten Solok",
            "1311": "Kabupaten Solok Selatan",
            "1312": "Kabupaten Tanah Datar",
            "1371": "Kota Bukittinggi",
            "1372": "Kota Padang",
            "1373": "Kota Padangpanjang",
            "1374": "Kota Pariaman",
            "1375": "Kota Payakumbuh",
            "1376": "Kota Sawahlunto",
            "1377": "Kota Solok"
        }
    },
    "31": {  # DKI Jakarta
        "nama": "DKI Jakarta",
        "kabupaten_kota": {
            "3101": "Kabupaten Administrasi Kepulauan Seribu",
            "3171": "Kota Administrasi Jakarta Pusat",
            "3172": "Kota Administrasi Jakarta Utara",
            "3173": "Kota Administrasi Jakarta Barat",
            "3174": "Kota Administrasi Jakarta Selatan",
            "3175": "Kota Administrasi Jakarta Timur"
        }
    },
    "32": {  # Jawa Barat
        "nama": "Jawa Barat",
        "kabupaten_kota": {
            "3201": "Kabupaten Bogor",
            "3202": "Kabupaten Sukabumi",
            "3203": "Kabupaten Cianjur",
            "3204": "Kabupaten Bandung",
            "3205": "Kabupaten Garut",
            "3206": "Kabupaten Tasikmalaya",
            "3207": "Kabupaten Ciamis",
            "3208": "Kabupaten Kuningan",
            "3209": "Kabupaten Cirebon",
            "3210": "Kabupaten Majalengka",
            "3211": "Kabupaten Sumedang",
            "3212": "Kabupaten Indramayu",
            "3213": "Kabupaten Subang",
            "3214": "Kabupaten Purwakarta",
            "3215": "Kabupaten Karawang",
            "3216": "Kabupaten Bekasi",
            "3217": "Kabupaten Bandung Barat",
            "3218": "Kabupaten Pangandaran",
            "3271": "Kota Bogor",
            "3272": "Kota Sukabumi",
            "3273": "Kota Bandung",
            "3274": "Kota Cirebon",
            "3275": "Kota Bekasi",
            "3276": "Kota Depok",
            "3277": "Kota Cimahi",
            "3278": "Kota Tasikmalaya",
            "3279": "Kota Banjar"
        }
    },
    "33": {  # Jawa Tengah
        "nama": "Jawa Tengah",
        "kabupaten_kota": {
            "3301": "Kabupaten Cilacap",
            "3302": "Kabupaten Banyumas",
            "3303": "Kabupaten Purbalingga",
            "3304": "Kabupaten Banjarnegara",
            "3305": "Kabupaten Kebumen",
            "3306": "Kabupaten Purworejo",
            "3307": "Kabupaten Wonosobo",
            "3308": "Kabupaten Magelang",
            "3309": "Kabupaten Boyolali",
            "3310": "Kabupaten Klaten",
            "3311": "Kabupaten Sukoharjo",
            "3312": "Kabupaten Wonogiri",
            "3313": "Kabupaten Karanganyar",
            "3314": "Kabupaten Sragen",
            "3315": "Kabupaten Grobogan",
            "3316": "Kabupaten Blora",
            "3317": "Kabupaten Rembang",
            "3318": "Kabupaten Pati",
            "3319": "Kabupaten Kudus",
            "3320": "Kabupaten Jepara",
            "3321": "Kabupaten Demak",
            "3322": "Kabupaten Semarang",
            "3323": "Kabupaten Temanggung",
            "3324": "Kabupaten Kendal",
            "3325": "Kabupaten Batang",
            "3326": "Kabupaten Pekalongan",
            "3327": "Kabupaten Pemalang",
            "3328": "Kabupaten Tegal",
            "3329": "Kabupaten Brebes",
            "3371": "Kota Magelang",
            "3372": "Kota Surakarta",
            "3373": "Kota Salatiga",
            "3374": "Kota Semarang",
            "3375": "Kota Pekalongan",
            "3376": "Kota Tegal"
        }
    },
    "34": {  # DI Yogyakarta
        "nama": "Daerah Istimewa Yogyakarta",
        "kabupaten_kota": {
            "3401": "Kabupaten Kulon Progo",
            "3402": "Kabupaten Bantul",
            "3403": "Kabupaten Gunung Kidul",
            "3404": "Kabupaten Sleman",
            "3471": "Kota Yogyakarta"
        }
    },
    "35": {  # Jawa Timur
        "nama": "Jawa Timur",
        "kabupaten_kota": {
            "3501": "Kabupaten Pacitan",
            "3502": "Kabupaten Ponorogo",
            "3503": "Kabupaten Trenggalek",
            "3504": "Kabupaten Tulungagung",
            "3505": "Kabupaten Blitar",
            "3506": "Kabupaten Kediri",
            "3507": "Kabupaten Malang",
            "3508": "Kabupaten Lumajang",
            "3509": "Kabupaten Jember",
            "3510": "Kabupaten Banyuwangi",
            "3511": "Kabupaten Bondowoso",
            "3512": "Kabupaten Situbondo",
            "3513": "Kabupaten Probolinggo",
            "3514": "Kabupaten Pasuruan",
            "3515": "Kabupaten Sidoarjo",
            "3516": "Kabupaten Mojokerto",
            "3517": "Kabupaten Jombang",
            "3518": "Kabupaten Nganjuk",
            "3519": "Kabupaten Madiun",
            "3520": "Kabupaten Magetan",
            "3521": "Kabupaten Ngawi",
            "3522": "Kabupaten Bojonegoro",
            "3523": "Kabupaten Tuban",
            "3524": "Kabupaten Lamongan",
            "3525": "Kabupaten Gresik",
            "3526": "Kabupaten Bangkalan",
            "3527": "Kabupaten Sampang",
            "3528": "Kabupaten Pamekasan",
            "3529": "Kabupaten Sumenep",
            "3571": "Kota Kediri",
            "3572": "Kota Blitar",
            "3573": "Kota Malang",
            "3574": "Kota Probolinggo",
            "3575": "Kota Pasuruan",
            "3576": "Kota Mojokerto",
            "3577": "Kota Madiun",
            "3578": "Kota Surabaya",
            "3579": "Kota Batu"
        }
    }
}

KECAMATAN_MAPPING = {
    # ---------- DKI Jakarta ----------
    "317101": "Gambir", "317102": "Johar Baru", "317103": "Kemayoran", "317104": "Menteng", "317105": "Sawah Besar", "317106": "Senen", "317107": "Tanah Abang",
    "317201": "Cilincing", "317202": "Kelapa Gading", "317203": "Koja", "317204": "Pademangan", "317205": "Penjaringan", "317206": "Tanjung Priok",
    "317301": "Cengkareng", "317302": "Grogol Petamburan", "317303": "Kalideres", "317304": "Kebon Jeruk", "317305": "Kembangan", "317306": "Pal Merah", "317307": "Taman Sari", "317308": "Tambora",
    "317401": "Cilandak", "317402": "Jagakarsa", "317403": "Kebayoran Baru", "317404": "Kebayoran Lama", "317405": "Mampang Prapatan", "317406": "Pancoran", "317407": "Pasar Minggu", "317408": "Pesanggrahan", "317409": "Setiabudi", "317410": "Tebet",
    "317501": "Matraman", "317502": "Pulogadung", "317503": "Jatinegara", "317504": "Kramat Jati", "317505": "Pasar Rebo", "317506": "Cakung", "317507": "Duren Sawit", "317508": "Makasar", "317509": "Ciracas", "317510": "Cipayung",

    # ---------- Banten ----------
    "360101": "Pandeglang", "360102": "Cibaliung", "360103": "Cigemblong", "360104": "Cikedal", "360105": "Cimanuk", "360106": "Cisalad", "360107": "Kaduhejo", "360108": "Karangtanjung", "360109": "Korban", "360110": "Labuan", "360111": "Majasari", "360112": "Mekarbaru", "360113": "Menes", "360114": "Pagelaran", "360115": "Panimbang", "360116": "Patia", "360117": "Saketi", "360118": "Sindangresmi", "360119": "Sobang", "360120": "Sukabumi", "360121": "Sukaresmi", "360122": "Sumur", "360123": "Suradadi",
    "360201": "Lebak", "360202": "Banjaranyar", "360203": "Bayah", "360204": "Bojongmanik", "360205": "Cibadak", "360206": "Cigemblong", "360207": "Cihara", "360208": "Cikulur", "360209": "Cileles", "360210": "Cimarga", "360211": "Cirinten", "360212": "Curugbitung", "360213": "Gintung", "360214": "Gunungkencana", "360215": "Kalanganyar", "360216": "Lebakwangi", "360217": "Maja", "360218": "Malingping", "360219": "Muncang", "360220": "Nam Lebung", "360221": "Panggarangan", "360222": "Rangkasbitung", "360223": "Sajira", "360224": "Sindangsari", "360225": "Sobang", "360226": "Wanasalam", "360227": "Warunggunung",
    "360301": "Tangerang", "360302": "Balaraja", "360303": "Cikupa", "360304": "Cisauk", "360305": "Cisoka", "360306": "Curug", "360307": "Gunung Kaler", "360308": "Jambe", "360309": "Jayanti", "360310": "Kelapa Dua", "360311": "Kemiri", "360312": "Kosambi", "360313": "Kresek", "360314": "Kronjo", "360315": "Legok", "360316": "Mauk", "360317": "Mekar Baru", "360318": "Pagedangan", "360319": "Pakuhaji", "360320": "Panongan", "360321": "Pasarkemis", "360322": "Rajeg", "360323": "Sepatan", "360324": "Sepatan Timur", "360325": "Sindang Jaya", "360326": "Sukamulya", "360327": "Sukatani", "360328": "Tigaraksa", "360329": "Cisoka", "360330": "Curug", "360331": "Gunung Kaler", "360332": "Jambe", "360333": "Jayanti", "360334": "Kelapa Dua", "360335": "Kemiri", "360336": "Kosambi", "360337": "Kresek", "360338": "Kronjo", "360339": "Legok", "360340": "Mauk", "360341": "Mekar Baru", "360342": "Pagedangan", "360343": "Pakuhaji", "360344": "Panongan", "360345": "Pasarkemis", "360346": "Rajeg", "360347": "Sepatan", "360348": "Sepatan Timur", "360349": "Sindang Jaya", "360350": "Sukamulya",
    "360351": "Serang", "360352": "Cikeusal", "360353": "Cikotok", "360354": "Cilegon", "360355": "Cinangka", "360356": "Ciocan", "360357": "Cipocok Jaya", "360358": "Ciruas", "360359": "Jawaran", "360360": "Kasemen", "360361": "Kibin", "360362": "Kopo", "360363": "Kramatwatu", "360364": "Kraksaan", "360365": "Kramatwatu", "360366": "Kraksaan", "360367": "Kramatwatu", "360368": "Kraksaan", "360369": "Kramatwatu", "360370": "Kraksaan", "360371": "Kramatwatu", "360372": "Kraksaan", "360373": "Kramatwatu", "360374": "Kraksaan", "360375": "Kramatwatu", "360376": "Kraksaan", "360377": "Kramatwatu", "360378": "Kraksaan", "360379": "Kramatwatu", "360380": "Kraksaan", "360381": "Kramatwatu", "360382": "Kraksaan", "360383": "Kramatwatu", "360384": "Kraksaan", "360385": "Kramatwatu", "360386": "Kraksaan", "360387": "Kramatwatu", "360388": "Kraksaan", "360389": "Kramatwatu", "360390": "Kraksaan",
    "360401": "Cilegon", "360402": "Cibeber", "360403": "Cilegon", "360404": "Ciwandan", "360405": "Grogol", "360406": "Purwakarta", "360407": "Taktakan", "360408": "Cibeber", "360409": "Cilegon", "360410": "Ciwandan", "360411": "Grogol", "360412": "Purwakarta", "360413": "Taktakan", "360414": "Cibeber", "360415": "Cilegon", "360416": "Ciwandan", "360417": "Grogol", "360418": "Purwakarta", "360419": "Taktakan", "360420": "Cibeber", "360421": "Cilegon", "360422": "Ciwandan", "360423": "Grogol", "360424": "Purwakarta", "360425": "Taktakan", "360426": "Cibeber", "360427": "Cilegon", "360428": "Ciwandan", "360429": "Grogol", "360430": "Purwakarta", "360431": "Taktakan", "360432": "Cibeber", "360433": "Cilegon", "360434": "Ciwandan", "360435": "Grogol", "360436": "Purwakarta", "360437": "Taktakan", "360438": "Cibeber", "360439": "Cilegon", "360440": "Ciwandan", "360441": "Grogol", "360442": "Purwakarta", "360443": "Taktakan", "360444": "Cibeber", "360445": "Cilegon", "360446": "Ciwandan", "360447": "Grogol", "360448": "Purwakarta", "360449": "Taktakan", "360450": "Cibeber",
    "360451": "Tangerang Selatan", "360452": "Ciputat", "360453": "Ciputat Timur", "360454": "Pamulang", "360455": "Pamulang Timur", "360456": "Pondok Aren", "360457": "Serpong", "360458": "Serpong Utara", "360459": "Setu", "360460": "Tangerang Selatan", "360461": "Ciputat", "360462": "Ciputat Timur", "360463": "Pamulang", "360464": "Pamulang Timur", "360465": "Pondok Aren", "360466": "Serpong", "360467": "Serpong Utara", "360468": "Setu", "360469": "Tangerang Selatan", "360470": "Ciputat", "360471": "Ciputat Timur", "360472": "Pamulang", "360473": "Pamulang Timur", "360474": "Pondok Aren", "360475": "Serpong", "360476": "Serpong Utara", "360477": "Setu", "360478": "Tangerang Selatan", "360479": "Ciputat", "360480": "Ciputat Timur", "360481": "Pamulang", "360482": "Pamulang Timur", "360483": "Pondok Aren", "360484": "Serpong", "360485": "Serpong Utara", "360486": "Setu", "360487": "Tangerang Selatan", "360488": "Ciputat", "360489": "Ciputat Timur", "360490": "Pamulang", "360491": "Pamulang Timur", "360492": "Pondok Aren", "360493": "Serpong", "360494": "Serpong Utara", "360495": "Setu", "360496": "Tangerang Selatan", "360497": "Ciputat", "360498": "Ciputat Timur", "360499": "Pamulang", "360500": "Pamulang Timur",

    # ---------- Jawa Barat (kab/kot) ----------
    "320101": "Cisompet", "320102": "Garut Kota", "320103": "Karacak", "320104": "Wanaraja", "320105": "Sukaresmi", "320106": "Cikajang", "320107": "Cisurupan", "320108": "Cibiuk", "320109": "Pakenjeng", "320110": "Caringin", "320111": "Cikelet", "320112": "Samarang", "320113": "Pasirwangi", "320114": "Cilawu", "320115": "Cibalong", "320116": "Cisewu", "320117": "Bl Limbangan", "320118": "Selaawi", "320119": "Talegong", "320120": "Cigedug", "320121": "Cilalu", "320122": "Kadungora", "320123": "Leles", "320124": "Balubur Limbangan", "320125": "Cisurupan", "320126": "Banyuresmi", "320127": "Cibatu", "320128": "Cikandang", "320129": "Cisompet", "320130": "Cibalong",
    "320201": "Cibadak", "320202": "Cicantayan", "320203": "Cicurug", "320204": "Cidahu", "320205": "Cikakak", "320206": "Cikembang", "320207": "Cilogorong", "320208": "Cimanggah", "320209": "Cisaat", "320210": "Curugkembar", "320211": "Gegerbitung", "320212": "Jampangkulon", "320213": "Kalapanunggal", "320214": "Lengkong", "320215": "Nagrak", "320216": "Pabuaran", "320217": "Palabuhanratu", "320218": "Parakansalam", "320219": "Parungkuda", "320220": "Purabaya", "320221": "Sagaranten", "320222": "Sukaraja", "320223": "Sukarame", "320224": "Sukaresih", "320225": "Sukaratu", "320226": "Sukarumi", "320227": "Sukatani", "320228": "Sukanagara", "320229": "Sukaraja", "320230": "Sukarame", "320231": "Sukaresih", "320232": "Sukaratu", "320233": "Sukarumi", "320234": "Sukatani", "320235": "Sukanagara", "320236": "Sukamantri", "320237": "Sukamulya", "320238": "Sukaraja", "320239": "Sukarame", "320240": "Sukaresih", "320241": "Sukaratu", "320242": "Sukarumi", "320243": "Sukatani", "320244": "Sukanagara", "320245": "Sukamantri", "320246": "Sukamulya",
    "320301": "Cianjur", "320302": "Agrabinta", "320303": "Bojongpicung", "320304": "Cibeber", "320305": "Cibinong", "320306": "Cicurug", "320307": "Cidaun", "320308": "Cikadu", "320309": "Cikalong", "320310": "Cikancing", "320311": "Cikijing", "320312": "Cilaku", "320313": "Cimande", "320314": "Cimanuk", "320315": "Ciniru", "320316": "Ciranjang", "320317": "Cisomang", "320318": "Cugenang", "320319": "Culamega", "320320": "Dawuan", "320321": "Gekbrong", "320322": "Haurwangi", "320323": "Kadupandak", "320324": "Karangtengah", "320325": "Langensari", "320326": "Leles", "320327": "Mande", "320328": "Naringgul", "320329": "Nyalindung", "320330": "Pagelaran", "320331": "Pacet", "320332": "Palamanan", "320333": "Pamulihan", "320334": "Pasirkuda", "320335": "Sindangbarang", "320336": "Sukaluyu", "320337": "Sukamakmur", "320338": "Takokak", "320339": "Tanggeung", "320340": "Warungkondang", "320341": "Citengah", "320342": "Cikalong", "320343": "Cimande", "320344": "Ciniru", "320345": "Cisomang", "320346": "Cugenang", "320347": "Culamega", "320348": "Dawuan", "320349": "Gekbrong", "320350": "Haurwangi", "320351": "Kadupandak", "320352": "Karanganom", "320353": "Karangtengah", "320354": "Langensari", "320355": "Leles", "320356": "Mande", "320357": "Naringgul", "320358": "Nyalindung", "320359": "Pagelaran", "320360": "Pacet", "320361": "Palamanan", "320362": "Pamulihan", "320363": "Pasirkuda", "320364": "Sindangbarang", "320365": "Sukaluyu", "320366": "Sukamakmur", "320367": "Takokak", "320368": "Tanggeung", "320369": "Warungkondang", "320370": "Cianjur", "320371": "Agrabinta", "320372": "Bojongpicung", "320373": "Cibeber", "320374": "Cibinong", "320375": "Cicurug", "320376": "Cidaun", "320377": "Cikadu", "320378": "Cikalong", "320379": "Cikancing", "320380": "Cikijing", "320381": "Cilaku", "320382": "Cimande", "320383": "Cimanuk", "320384": "Ciniru", "320385": "Ciranjang", "320386": "Cisomang", "320387": "Cugenang", "320388": "Culamega", "320389": "Dawuan", "320390": "Gekbrong", "320391": "Haurwangi", "320392": "Kadupandak", "320393": "Karanganom", "320394": "Karangtengah", "320395": "Langensari", "320396": "Leles", "320397": "Mande", "320398": "Naringgul", "320399": "Nyalindung", "320400": "Pagelaran", "320401": "Pacet", "320402": "Palamanan", "320403": "Pamulihan", "320404": "Pasirkuda", "320405": "Sindangbarang", "320406": "Sukaluyu", "320407": "Sukamakmur", "320408": "Takokak", "320409": "Tanggeung", "320410": "Warungkondang",
    "320501": "Tasikmalaya", "320502": "Ciamis", "320503": "Cibeureum", "320504": "Cigugur", "320505": "Cikalong", "320506": "Cimanuk", "320507": "Cipatujah", "320508": "Cisayong", "320509": "Cisaat", "320510": "Cisomang", "320511": "Cisurupan", "320512": "Culamega", "320513": "Dawuan", "320514": "Garawangi", "320515": "Haurgombong", "320516": "Indihiang", "320517": "Jatiwaras", "320518": "Kadipaten", "320519": "Karangnunggal", "320520": "Kawalu", "320521": "Lakbok", "320522": "Leuwisari", "320523": "Mangunreja", "320524": "Manonjaya", "320525": "Nagrak", "320526": "Pancatengah", "320527": "Pagerageung", "320528": "Parungponteng", "320529": "Puspahiang", "320530": "Rajapolah", "320531": "Rancabali", "320532": "Salopa", "320533": "Sariwangi", "320534": "Sindangkerta", "320535": "Sodonghilir", "320536": "Sukaraja", "320537": "Sukarame", "320538": "Sukaresih", "320539": "Sukaratu", "320540": "Sukarumi", "320541": "Sukatani", "320542": "Sukanagara", "320543": "Sukaraja", "320544": "Sukarame", "320545": "Sukaresih", "320546": "Sukaratu", "320547": "Sukarumi", "320548": "Sukatani", "320549": "Sukanagara", "320550": "Sukamantri", "320551": "Sukamulya", "320552": "Sukaraja", "320553": "Sukarame", "320554": "Sukaresih", "320555": "Sukaratu", "320556": "Sukarumi", "320557": "Sukatani", "320558": "Sukanagara", "320559": "Sukamantri", "320560": "Sukamulya",
    "320601": "Ciamis", "320602": "Banjar", "320603": "Cibeureum", "320604": "Cibungur", "320605": "Cigugur", "320606": "Cijulang", "320607": "Cikakak", "320608": "Cimaragas", "320609": "Cipatujah", "320610": "Cisaga", "320611": "Cisaat", "320612": "Cisayong", "320613": "Cisomang", "320614": "Cisurupan", "320615": "Cisayong", "320616": "Cisomang", "320617": "Cisurupan", "320618": "Cisayong", "320619": "Cisomang", "320620": "Cisurupan", "320621": "Cisayong", "320622": "Cisomang", "320623": "Cisurupan", "320624": "Cisayong", "320625": "Cisomang", "320626": "Cisurupan", "320627": "Cisayong", "320628": "Cisomang", "320629": "Cisurupan", "320630": "Cisayong", "320631": "Cisomang", "320632": "Cisurupan", "320633": "Cisayong", "320634": "Cisomang", "320635": "Cisurupan", "320636": "Cisayong", "320637": "Cisomang", "320638": "Cisurupan", "320639": "Cisayong", "320640": "Cisomang", "320641": "Cisurupan", "320642": "Cisayong", "320643": "Cisomang", "320644": "Cisurupan", "320645": "Cisayong", "320646": "Cisomang", "320647": "Cisurupan", "320648": "Cisayong", "320649": "Cisomang", "320650": "Cisurupan",
    "320701": "Kuningan", "320702": "Ciawigebang", "320703": "Cibingbin", "320704": "Cidahu", "320705": "Cigandamekar", "320706": "Cigugur", "320707": "Cijati", "320708": "Cikalong", "320709": "Cikasarua", "320710": "Cilimus", "320711": "Cimahi", "320712": "Cipicung", "320713": "Cirebon", "320714": "Cisaat", "320715": "Cisayong", "320716": "Cisomang", "320717": "Cisurupan", "320718": "Cisayong", "320719": "Cisomang", "320720": "Cisurupan", "320721": "Cisayong", "320722": "Cisomang", "320723": "Cisurupan", "320724": "Cisayong", "320725": "Cisomang", "320726": "Cisurupan", "320727": "Cisayong", "320728": "Cisomang", "320729": "Cisurupan", "320730": "Cisayong", "320731": "Cisomang", "320732": "Cisurupan", "320733": "Cisayong", "320734": "Cisomang", "320735": "Cisurupan", "320736": "Cisayong", "320737": "Cisomang", "320738": "Cisurupan", "320739": "Cisayong", "320740": "Cisomang", "320741": "Cisurupan", "320742": "Cisayong", "320743": "Cisomang", "320744": "Cisurupan", "320745": "Cisayong", "320746": "Cisomang", "320747": "Cisurupan", "320748": "Cisayong", "320749": "Cisomang", "320750": "Cisurupan",
    "320801": "Majalengka", "320802": "Argapura", "320803": "Banjaranyar", "320804": "Bantarujeg", "320805": "Cigasong", "320806": "Cikijing", "320807": "Cingambul", "320808": "Dawuan", "320809": "Jatiwangi", "320810": "Kadipaten", "320811": "Kertajati", "320812": "Lemahsugih", "320813": "Ligung", "320814": "Majalengka", "320815": "Malausma", "320816": "Margadana", "320817": "Mundu", "320818": "Palasah", "320819": "Panyingkiran", "320820": "Sindang", "320821": "Sukahaji", "320822": "Talaga", "320823": "Waringin", "320824": "Argapura", "320825": "Banjaranyar", "320826": "Bantarujeg", "320827": "Cigasong", "320828": "Cikijing", "320829": "Cingambul", "320830": "Dawuan", "320831": "Jatiwangi", "320832": "Kadipaten", "320833": "Kertajati", "320834": "Lemahsugih", "320835": "Ligung", "320836": "Majalengka", "320837": "Malausma", "320838": "Margadana", "320839": "Mundu", "320840": "Palasah", "320841": "Panyingkiran", "320842": "Sindang", "320843": "Sukahaji", "320844": "Talaga", "320845": "Waringin",
    "320901": "Sumedang", "320902": "Buahdua", "320903": "Cibugel", "320904": "Cimalaka", "320905": "Cimanggah", "320906": "Cipakat", "320907": "Cipameungpeuk", "320908": "Cipongkor", "320909": "Cisayong", "320910": "Cisomang", "320911": "Cisurupan", "320912": "Darmaraja", "320913": "Ganeas", "320914": "Hegarmanah", "320915": "Jatinangor", "320916": "Jatiningrum", "320917": "Jatinunggal", "320918": "Jatipandang", "320919": "Jatisari", "320920": "Jatitujuh", "320921": "Karangjati", "320922": "Kertasari", "320923": "Mangunreja", "320924": "Mekarmukti", "320925": "Mekarsari", "320926": "Mojogebang", "320927": "Paseh", "320928": "Paseh", "320929": "Paseh", "320930": "Paseh", "320931": "Paseh", "320932": "Paseh", "320933": "Paseh", "320934": "Paseh", "320935": "Paseh", "320936": "Paseh", "320937": "Paseh", "320938": "Paseh", "320939": "Paseh", "320940": "Paseh", "320941": "Paseh", "320942": "Paseh", "320943": "Paseh", "320944": "Paseh", "320945": "Paseh", "320946": "Paseh", "320947": "Paseh", "320948": "Paseh", "320949": "Paseh", "320950": "Paseh", "320951": "Paseh", "320952": "Paseh", "320953": "Paseh", "320954": "Paseh", "320955": "Paseh", "320956": "Paseh", "320957": "Paseh", "320958": "Paseh", "320959": "Paseh", "320960": "Paseh",
    "321001": "Indramayu", "321002": "Anjatan", "321003": "Arahan", "321004": "Balongan", "321005": "Bongas", "321006": "Cantigi", "321007": "Cikedung", "321008": "Cinta", "321009": "Dukuh", "321010": "Gabuswetan", "321011": "Gantar", "321012": "Haurgeulis", "321013": "Juntinyuat", "321014": "Kandanghaur", "321015": "Karangampel", "321016": "Kedokan Bunder", "321017": "Kertasemaya", "321018": "Kertawangi", "321019": "Kertawinangun", "321020": "Kroya", "321021": "Lemahabang", "321022": "Lohbener", "321023": "Mundu", "321024": "Pagerageung", "321025": "Pasekan", "321026": "Patrol", "321027": "Paseh", "321028": "Paseh", "321029": "Paseh", "321030": "Paseh", "321031": "Paseh", "321032": "Paseh", "321033": "Paseh", "321034": "Paseh", "321035": "Paseh", "321036": "Paseh", "321037": "Paseh", "321038": "Paseh", "321039": "Paseh", "321040": "Paseh", "321041": "Paseh", "321042": "Paseh", "321043": "Paseh", "321044": "Paseh", "321045": "Paseh", "321046": "Paseh", "321047": "Paseh", "321048": "Paseh", "321049": "Paseh", "321050": "Paseh", "321051": "Paseh", "321052": "Paseh", "321053": "Paseh", "321054": "Paseh", "321055": "Paseh", "321056": "Paseh", "321057": "Paseh", "321058": "Paseh", "321059": "Paseh", "321060": "Paseh",
    "321101": "Subang", "321102": "Binong", "321103": "Cibogo", "321104": "Cijambe", "321105": "Cikaum", "321106": "Cipeundeuy", "321107": "Cipunagara", "321108": "Compreng", "321109": "Dawuan", "321110": "Jalancagak", "321111": "Kalijati", "321112": "Kasomalang", "321113": "Ciater", "321114": "Pagaden", "321115": "Patokbeusi", "321116": "Pabuaran", "321117": "Purwadadi", "321118": "Sagalaherang", "321119": "Salawu", "121120": "Sari", "321121": "Serangpanjang", "321122": "Sindanglaya", "321123": "Sukasari", "321124": "Sukasari", "321125": "Sukasari", "321126": "Sukasari", "321127": "Sukasari", "321128": "Sukasari", "321129": "Sukasari", "321130": "Sukasari", "321131": "Sukasari", "321132": "Sukasari", "321133": "Sukasari", "321134": "Sukasari", "321135": "Sukasari", "321136": "Sukasari", "321137": "Sukasari", "321138": "Sukasari", "321139": "Sukasari", "321140": "Sukasari", "321141": "Sukasari", "321142": "Sukasari", "321143": "Sukasari", "321144": "Sukasari", "321145": "Sukasari", "321146": "Sukasari", "321147": "Sukasari", "321148": "Sukasari", "321149": "Sukasari", "321150": "Sukasari",
    "321201": "Purwakarta", "321202": "Babakancikao", "321203": "Bojong", "321204": "Bungursari", "321205": "Campaka", "321206": "Cibatu", "321207": "Ciganea", "321208": "Cikalong", "321209": "Cikopo", "321210": "Cililin", "321211": "Cimanggah", "321212": "Ciniru", "321213": "Cisomang", "321214": "Cisurupan", "321215": "Darangdan", "321216": "Jatiluhur", "321217": "Kiarapedes", "321218": "Maniis", "321219": "Munjul", "321220": "Plered", "321221": "Pondoksalam", "321222": "Sadar", "321223": "Sukasari", "321224": "Sukasari", "321225": "Sukasari", "321226": "Sukasari", "321227": "Sukasari", "321228": "Sukasari", "321229": "Sukasari", "321230": "Sukasari", "321231": "Sukasari", "321232": "Sukasari", "321233": "Sukasari", "321234": "Sukasari", "321235": "Sukasari", "321236": "Sukasari", "321237": "Sukasari", "321238": "Sukasari", "321239": "Sukasari", "321240": "Sukasari", "321241": "Sukasari", "321242": "Sukasari", "321243": "Sukasari", "321244": "Sukasari", "321245": "Sukasari", "321246": "Sukasari", "321247": "Sukasari", "321248": "Sukasari", "321249": "Sukasari", "321250": "Sukasari",
    "321301": "Karawang", "321302": "Batujaya", "321303": "Bekasi", "321304": "Bojongmangu", "321305": "Cabangbungin", "321306": "Cianjur", "321307": "Ciampel", "321308": "Cibuaya", "321309": "Cikampek", "321310": "Cilamaya", "321311": "Cilamaya", "321312": "Cilamaya", "321313": "Cilamaya", "321314": "Cilamaya", "321315": "Cilamaya", "321316": "Cilamaya", "321317": "Cilamaya", "321318": "Cilamaya", "321319": "Cilamaya", "321320": "Cilamaya", "321321": "Cilamaya", "321322": "Cilamaya", "321323": "Cilamaya", "321324": "Cilamaya", "321325": "Cilamaya", "321326": "Cilamaya", "321327": "Cilamaya", "321328": "Cilamaya", "321329": "Cilamaya", "321330": "Cilamaya", "321331": "Cilamaya", "321332": "Cilamaya", "321333": "Cilamaya", "321334": "Cilamaya", "321335": "Cilamaya", "321336": "Cilamaya", "321337": "Cilamaya", "321338": "Cilamaya", "321339": "Cilamaya", "321340": "Cilamaya", "321341": "Cilamaya", "321342": "Cilamaya", "321343": "Cilamaya", "321344": "Cilamaya", "321345": "Cilamaya", "321346": "Cilamaya", "321347": "Cilamaya", "321348": "Cilamaya", "321349": "Cilamaya", "321350": "Cilamaya",
    "321401": "Bekasi", "321402": "Babelan", "321403": "Bojongmangu", "321404": "Cabangbungin", "321405": "Ciangir", "321406": "Cibarusah", "321407": "Cibitung", "321408": "Cikarang", "321409": "Cikarang", "321410": "Cikarang", "321411": "Cikarang", "321412": "Cikarang", "321413": "Cikarang", "321414": "Cikarang", "321415": "Cikarang", "321416": "Cikarang", "321417": "Cikarang", "321418": "Cikarang", "321419": "Cikarang", "321420": "Cikarang", "321421": "Cikarang", "321422": "Cikarang", "321423": "Cikarang", "321424": "Cikarang", "321425": "Cikarang", "321426": "Cikarang", "321427": "Cikarang", "321428": "Cikarang", "321429": "Cikarang", "321430": "Cikarang", "321431": "Cikarang", "321432": "Cikarang", "321433": "Cikarang", "321434": "Cikarang", "321435": "Cikarang", "321436": "Cikarang", "321437": "Cikarang", "321438": "Cikarang", "321439": "Cikarang", "321440": "Cikarang", "321441": "Cikarang", "321442": "Cikarang", "321443": "Cikarang", "321444": "Cikarang", "321445": "Cikarang", "321446": "Cikarang", "321447": "Cikarang", "321448": "Cikarang", "321449": "Cikarang", "321450": "Cikarang",
    "321701": "Bandung Barat", "321702": "Batujajar", "321703": "Cihampelas", "321704": "Cikalong", "321705": "Cililin", "321706": "Cipatat", "321707": "Cipeundeuy", "321708": "Cipongkor", "321709": "Cisarua", "321710": "Gunung", "321711": "Lembang", "321712": "Ngamprah", "321713": "Padalarang", "321714": "Parongpong", "321715": "Rongga", "321716": "Saguling", "321717": "Soreang", "321718": "Sukasari", "321719": "Sukasari", "321720": "Sukasari", "321721": "Sukasari", "321722": "Sukasari", "321723": "Sukasari", "321724": "Sukasari", "321725": "Sukasari", "321726": "Sukasari", "321727": "Sukasari", "321728": "Sukasari", "321729": "Sukasari", "321730": "Sukasari", "321731": "Sukasari", "321732": "Sukasari", "321733": "Sukasari", "321734": "Sukasari", "321735": "Sukasari", "321736": "Sukasari", "321737": "Sukasari", "321738": "Sukasari", "321739": "Sukasari", "321740": "Sukasari", "321741": "Sukasari", "321742": "Sukasari", "321743": "Sukasari", "321744": "Sukasari", "321745": "Sukasari", "321746": "Sukasari", "321747": "Sukasari", "321748": "Sukasari", "321749": "Sukasari", "321750": "Sukasari",
    "321801": "Pangandaran", "321802": "Cikalong", "321803": "Cimerak", "321804": "Cipatujah", "321805": "Cisayong", "321806": "Cisomang", "321807": "Cisurupan", "321808": "Dawuan", "321809": "Gekbrong", "321810": "Haurwangi", "321811": "Kadupandak", "321812": "Karanganom", "321813": "Karangtengah", "321814": "Langensari", "321815": "Leles", "321816": "Mande", "321817": "Naringgul", "321818": "Nyalindung", "321819": "Pagelaran", "321820": "Pacet", "321821": "Palamanan", "321822": "Pamulihan", "321823": "Pasirkuda", "321824": "Sindangbarang", "321825": "Sukaluyu", "321826": "Sukamakmur", "321827": "Takokak", "321828": "Tanggeung", "321829": "Warungkondang", "321830": "Cikalong", "321831": "Cimerak", "321832": "Cipatujah", "321833": "Cisayong", "321834": "Cisomang", "321835": "Cisurupan", "321836": "Dawuan", "321837": "Gekbrong", "321838": "Haurwangi", "321839": "Kadupandak", "321840": "Karanganom", "321841": "Karangtengah", "321842": "Langensari", "321843": "Leles", "321844": "Mande", "321845": "Naringgul", "321846": "Nyalindung", "321847": "Pagelaran", "321848": "Pacet", "321849": "Palamanan", "321850": "Pamulihan",

    # ---------- Jawa Tengah ----------
    "330101": "Cilacap", "330102": "Binangun", "330103": "Bumiayu", "330104": "Cimanggu", "330105": "Cipari", "330106": "Dayeuhluhur", "330107": "Gandrungmangu", "330108": "Jeruklegi", "330109": "Kampung Laut", "330110": "Karangpucung", "330111": "Kawunganten", "330112": "Kedungreja", "330113": "Kesugihan", "330114": "Kroya", "330115": "Kampung Laut", "330116": "Majenang", "330117": "Mangun", "330118": "Maos", "330119": "Nusawungu", "330120": "Patimuan", "330121": "Sampang", "330122": "Sidareja", "330123": "Wanareja",
    "330201": "Purwokerto", "330202": "Baturaden", "330203": "Cilongok", "330204": "Gumelar", "330205": "Kebasen", "330206": "Kemranjen", "330207": "Lumbir", "330208": "Patikraja", "330209": "Purwokerto", "330210": "Rawan", "330211": "Sapuran", "330212": "Sokaraja", "330213": "Somagede", "330214": "Sumbang", "330215": "Tambak", "330216": "Wangon",
    "330301": "Purbalingga", "330302": "Bukateja", "330304": "Kalimanah", "330305": "Karangmoncol", "330306": "Karangreja", "330307": "Kejobong", "330308": "Kemangkon", "330309": "Kutasari", "330310": "Mrebet", "330311": "Padamara", "330312": "Pengadegan", "330313": "Rembang", "330314": "Bobotsari", "330315": "Karangjambu", "330316": "Karanganyar", "330317": "Karangjati", "330318": "Karangjati", "330319": "Karangjati", "330320": "Karangjati", "330321": "Karangjati", "330322": "Karangjati", "330323": "Karangjati", "330324": "Karangjati", "330325": "Karangjati", "330326": "Karangjati", "330327": "Karangjati", "330328": "Karangjati", "330329": "Karangjati", "330330": "Karangjati", "330331": "Karangjati", "330332": "Karangjati", "330333": "Karangjati", "330334": "Karangjati", "330335": "Karangjati", "330336": "Karangjati", "330337": "Karangjati", "330338": "Karangjati", "330339": "Karangjati", "330340": "Karangjati", "330341": "Karangjati", "330342": "Karangjati", "330343": "Karangjati", "330344": "Karangjati", "330345": "Karangjati", "330346": "Karangjati", "330347": "Karangjati", "330348": "Karangjati", "330349": "Karangjati", "330350": "Karangjati",
    "330401": "Banjarnegara", "330402": "Banjarmangu", "330403": "Batur", "330404": "Bawang", "330405": "Clapar", "330406": "Karangkobar", "330407": "Madukara", "330408": "Mandiraja", "330409": "Pageralang", "330410": "Pandanarum", "330411": "Punggelan", "330412": "Purwonegoro", "330413": "Rakit", "330414": "Sigaluh", "330415": "Susukan", "330416": "Wadaslintang", "330417": "Wanayasa", "330418": "Pagentan", "330419": "Pejawaran", "330420": "Pulosari", "330421": "Karangmoncol", "330422": "Karangreja", "330423": "Karangjati", "330424": "Karangjati", "330425": "Karangjati", "330426": "Karangjati", "330427": "Karangjati", "330428": "Karangjati", "330429": "Karangjati", "330430": "Karangjati", "330431": "Karangjati", "330432": "Karangjati", "330433": "Karangjati", "330434": "Karangjati", "330435": "Karangjati", "330436": "Karangjati", "330437": "Karangjati", "330438": "Karangjati", "330439": "Karangjati", "330440": "Karangjati", "330441": "Karangjati", "330442": "Karangjati", "330443": "Karangjati", "330444": "Karangjati", "330445": "Karangjati", "330446": "Karangjati", "330447": "Karangjati", "330448": "Karangjati", "330449": "Karangjati", "330450": "Karangjati",
    "330501": "Kebumen", "330502": "Adimulyo", "330503": "Ambal", "330504": "Ayah", "330505": "Bonorowo", "330506": "Buayan", "330507": "Gombong", "330508": "Karanganyar", "330509": "Karanggayam", "330510": "Karangmalang", "330511": "Klirong", "330512": "Kutowinangun", "330513": "Mirit", "330514": "Padureso", "330515": "Pejagoan", "330516": "Petanahan", "330517": "Poncowati", "330518": "Prembun", "330519": "Puring", "330520": "Rowokele", "330521": "Sadang", "330522": "Selogiri", "330523": "Semanding", "330524": "Sempor", "330525": "Tanjung", "330526": "Tlogomulyo", "330527": "Kuwarasan", "330528": "Karanggayam", "330529": "Karangmalang", "330530": "Klirong", "330531": "Kutowinangun", "330532": "Mirit", "330533": "Padureso", "330534": "Pejagoan", "330535": "Petanahan", "330536": "Poncowati", "330537": "Prembun", "330538": "Puring", "330539": "Rowokele", "330540": "Sadang", "330541": "Selogiri", "330542": "Semanding", "330543": "Sempor", "330544": "Tanjung", "330545": "Tlogomulyo", "330546": "Kuwarasan", "330547": "Karanggayam", "330548": "Karangmalang", "330549": "Klirong", "330550": "Kutowinangun",
    "330601": "Purworejo", "330602": "Banyuurip", "330603": "Bayan", "330604": "Bener", "330605": "Butuh", "330606": "Gebang", "330607": "Grabag", "330608": "Gumelar", "330609": "Kaliakah", "330610": "Kutoarjo", "330611": "Loano", "330612": "Maron", "330613": "Muntig", "330614": "Ngombol", "330615": "Pituruh", "330616": "Pekiringan", "330617": "Purwodadi", "330618": "Purworejo", "330619": "Sempor", "330620": "Siji", "330621": "Simo", "330622": "Tempuran", "330623": "Wates", "330624": "Butuh", "330625": "Gebang", "330626": "Grabag", "330627": "Gumelar", "330628": "Kaliakah", "330629": "Kutoarjo", "330630": "Loano", "330631": "Maron", "330632": "Muntig", "330633": "Ngombol", "330634": "Pituruh", "330635": "Pekiringan", "330636": "Purwodadi", "330637": "Purworejo", "330638": "Sempor", "330639": "Siji", "330640": "Simo", "330641": "Tempuran", "330642": "Wates", "330643": "Butuh", "330644": "Gebang", "330645": "Grabag", "330646": "Gumelar", "330647": "Kaliakah", "330648": "Kutoarjo", "330649": "Loano", "330650": "Maron",
    "330701": "Wonosobo", "330702": "Batur", "330703": "Bejiharjo", "330704": "Bener", "330705": "Baturetno", "330706": "Butuh", "330707": "Dieng", "330708": "Garung", "330709": "Kalibawang", "330710": "Kaliwiro", "330711": "Kejajar", "330712": "Kepil", "330713": "Kertek", "330714": "Leksono", "330715": "Mojotengah", "330716": "Munto", "330717": "Ngadipuro", "330718": "Pekasiran", "330719": "Pituruh", "330720": "Sapuran", "330721": "Selomerto", "330722": "Sukoharjo", "330723": "Wadaslintang", "330724": "Watumalang", "330725": "Wonosobo", "330726": "Batur", "330727": "Bejiharjo", "330728": "Bener", "330729": "Baturetno", "330730": "Butuh", "330731": "Dieng", "330732": "Garung", "330733": "Kalibawang", "330734": "Kaliwiro", "330735": "Kejajar", "330736": "Kepil", "330737": "Kertek", "330738": "Leksono", "330739": "Mojotengah", "330740": "Munto", "330741": "Ngadipuro", "330742": "Pekasiran", "330743": "Pituruh", "330744": "Sapuran", "330745": "Selomerto", "330746": "Sukoharjo", "330747": "Wadaslintang", "330748": "Watumalang", "330749": "Wonosobo", "330750": "Batur",
    "330801": "Magelang", "330802": "Andong", "330803": "Banyubiru", "330804": "Berjo", "330805": "Bruno", "330806": "Cepogo", "330807": "Dukun", "330808": "Grabag", "330809": "Jakenan", "330810": "Kajoran", "330811": "Kaliangkrik", "330812": "Mertoyudan", "330813": "Muntilan", "330814": "Ngablak", "330815": "Ngluwar", "330816": "Pakem", "330817": "Salam", "330818": "Sawangan", "330819": "Secang", "330820": "Selo", "330821": "Tegalrejo", "330822": "Tempuran", "330823": "Wanareja", "330824": "Windusari", "330825": "Andong", "330826": "Banyubiru", "330827": "Berjo", "330828": "Bruno", "330829": "Cepogo", "330830": "Dukun", "330831": "Grabag", "330832": "Jakenan", "330833": "Kajoran", "330834": "Kaliangkrik", "330835": "Mertoyudan", "330836": "Muntilan", "330837": "Ngablak", "330838": "Ngluwar", "330839": "Pakem", "330840": "Salam", "330841": "Sawangan", "330842": "Secang", "330843": "Selo", "330844": "Tegalrejo", "330845": "Tempuran", "330846": "Wanareja", "330847": "Windusari", "330848": "Andong", "330849": "Banyubiru", "330850": "Berjo",
    "330901": "Boyolali", "330902": "Ampel", "330903": "Banyudono", "330904": "Cepogo", "330905": "Gladagsari", "330906": "Juwangi", "330907": "Karanggede", "330908": "Kemusu", "330909": "Klego", "330910": "Krasak", "330911": "Mojosongo", "330912": "Musuk", "330913": "Ngargomulyo", "330914": "Nogosari", "330915": "Sambi", "330916": "Sawit", "330917": "Selo", "330918": "Simo", "330919": "Songo", "330920": "Tamanan", "330921": "Tamansari", "330922": "Tegalrejo", "330923": "Temu", "330924": "Wates", "330925": "Wonosegoro", "330926": "Ampel", "330927": "Banyudono", "330928": "Cepogo", "330929": "Gladagsari", "330930": "Juwangi", "330931": "Karanggede", "330932": "Kemusu", "330933": "Klego", "330934": "Krasak", "330935": "Mojosongo", "330936": "Musuk", "330937": "Ngargomulyo", "330938": "Nogosari", "330939": "Sambi", "330940": "Sawit", "330941": "Selo", "330942": "Simo", "330943": "Songo", "330944": "Tamanan", "330945": "Tamansari", "330946": "Tegalrejo", "330947": "Temu", "330948": "Wates", "330949": "Wonosegoro", "330950": "Ampel",
    "331001": "Klaten", "331002": "Bayat", "331003": "Cawas", "331004": "Ceper", "331005": "Delanggu", "331006": "Jatinom", "331007": "Jogonalan", "331008": "Juwaneng", "331009": "Karangdowo", "331010": "Karangnongko", "331011": "Kebonarum", "331012": "Kemalang", "331013": "Manisrenggo", "331014": "Ngawen", "331015": "Pedan", "331016": "Polanharjo", "331017": "Prambanan", "331018": "Purwodadi", "331019": "Trucuk", "331020": "Tulung", "331021": "Wedi", "331022": "Winong", "331023": "Wonosari", "331024": "Bayat", "331025": "Cawas", "331026": "Ceper", "331027": "Delanggu", "331028": "Jatinom", "331029": "Jogonalan", "331030": "Juwaneng", "331031": "Karangdowo", "331032": "Karangnongko", "331033": "Kebonarum", "331034": "Kemalang", "331035": "Manisrenggo", "331036": "Ngawen", "331037": "Pedan", "331038": "Polanharjo", "331039": "Prambanan", "331040": "Purwodadi", "331041": "Trucuk", "331042": "Tulung", "331043": "Wedi", "331044": "Winong", "331045": "Wonosari", "331046": "Bayat", "331047": "Cawas", "331048": "Ceper", "331049": "Delanggu", "331050": "Jatinom",
    "331051": "Jogonalan", "331052": "Juwaneng", "331053": "Karangdowo", "331054": "Karangnongko", "331055": "Kebonarum", "331056": "Kemalang", "331057": "Manisrenggo", "331058": "Ngawen", "331059": "Pedan", "331060": "Polanharjo", "331061": "Prambanan", "331062": "Purwodadi", "331063": "Trucuk", "331064": "Tulung", "331065": "Wedi", "331066": "Winong", "331067": "Wonosari", "331068": "Bayat", "331069": "Cawas", "331070": "Ceper", "331071": "Delanggu", "331072": "Jatinom", "331073": "Jogonalan", "331074": "Juwaneng", "331075": "Karangdowo", "331076": "Karangnongko", "331077": "Kebonarum", "331078": "Kemalang", "331079": "Manisrenggo", "331080": "Ngawen", "331081": "Pedan", "331082": "Polanharjo", "331083": "Prambanan", "331084": "Purwodadi", "331085": "Trucuk", "331086": "Tulung", "331087": "Wedi", "331088": "Winong", "331089": "Wonosari", "331090": "Bayat", "331091": "Cawas", "331092": "Ceper", "331093": "Delanggu", "331094": "Jatinom", "331095": "Jogonalan", "331096": "Juwaneng", "331097": "Karangdowo", "331098": "Karangnongko", "331099": "Kebonarum", "331100": "Kemalang", "331101": "Manisrenggo", "331102": "Ngawen", "331103": "Pedan", "331104": "Polanharjo", "331105": "Prambanan", "331106": "Purwodadi", "331107": "Trucuk", "331108": "Tulung", "331109": "Wedi", "331110": "Winong", "331111": "Wonosari", "331112": "Bayat", "331113": "Cawas", "331114": "Ceper", "331115": "Delanggu", "331116": "Jatinom", "331117": "Jogonalan", "331118": "Juwaneng", "331119": "Karangdowo", "331120": "Karangnongko", "331121": "Kebonarum", "331122": "Kemalang", "331123": "Manisrenggo", "331124": "Ngawen", "331125": "Pedan", "331126": "Polanharjo", "331127": "Prambanan", "331128": "Purwodadi", "331129": "Trucuk", "331130": "Tulung", "331131": "Wedi", "331132": "Winong", "331133": "Wonosari", "331134": "Bayat", "331135": "Cawas", "331136": "Ceper", "331137": "Delanggu", "331138": "Jatinom", "331139": "Jogonalan", "331140": "Juwaneng", "331141": "Karangdowo", "331142": "Karangnongko", "331143": "Kebonarum", "331144": "Kemalang", "331145": "Manisrenggo", "331146": "Ngawen", "331147": "Pedan", "331148": "Polanharjo", "331149": "Prambanan", "331150": "Purwodadi",
    "331151": "Trucuk", "331152": "Tulung", "331153": "Wedi", "331154": "Winong", "331155": "Wonosari", "331156": "Bayat", "331157": "Cawas", "331158": "Ceper", "331159": "Delanggu", "331160": "Jatinom", "331161": "Jogonalan", "331162": "Juwaneng", "331163": "Karangdowo", "331164": "Karangnongko", "331165": "Kebonarum", "331166": "Kemalang", "331167": "Manisrenggo", "331168": "Ngawen", "331169": "Pedan", "331170": "Polanharjo", "331171": "Prambanan", "331172": "Purwodadi", "331173": "Trucuk", "331174": "Tulung", "331175": "Wedi", "331176": "Winong", "331177": "Wonosari", "331178": "Bayat", "331179": "Cawas", "331180": "Ceper", "331181": "Delanggu", "331182": "Jatinom", "331183": "Jogonalan", "331184": "Juwaneng", "331185": "Karangdowo", "331186": "Karangnongko", "331187": "Kebonarum", "331188": "Kemalang", "331189": "Manisrenggo", "331190": "Ngawen", "331191": "Pedan", "351516": "Gedangan", "340102": "Wates"}


# ========== CLASS SSL ==========
class SSLAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)

# ========== FUNGSI UTILITAS ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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

# ========== FUNGSI PARSING & WILAYAH ==========
def get_nama_wilayah(kode_wilayah):
    """Mendapatkan nama wilayah berdasarkan kode"""
    if len(kode_wilayah) == 2:  # Provinsi
        return WILAYAH_MAPPING.get(kode_wilayah, {}).get('nama', f'PROVINSI KODE {kode_wilayah}')
    elif len(kode_wilayah) == 4:  # Kab/Kot
        for prov_data in WILAYAH_MAPPING.values():
            if kode_wilayah in prov_data['kabupaten_kota']:
                return prov_data['kabupaten_kota'][kode_wilayah]
        return f'KAB/KOT KODE {kode_wilayah}'
    elif len(kode_wilayah) == 6:  # Kecamatan
        return KECAMATAN_MAPPING.get(kode_wilayah, f'KECAMATAN KODE {kode_wilayah}')
    else:
        return f'KODE TIDAK VALID {kode_wilayah}'

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

def fetch_kemendagri(kode: str):
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
        return {"provinsi": "Unknown", "kota": "Unknown",
                "kecamatan": "Unknown", "kodepos": "00000"}

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
    
# ========== FUNGSI ZODIAK & PASARAN JAWA ==========
def get_zodiak(tgl: int, bln: int) -> str:
    if (bln == 1 and tgl >= 20) or (bln == 2 and tgl <= 18):
        return "Aquarius"
    elif (bln == 2 and tgl >= 19) or (bln == 3 and tgl <= 20):
        return "Pisces"
    elif (bln == 3 and tgl >= 21) or (bln == 4 and tgl <= 19):
        return "Aries"
    elif (bln == 4 and tgl >= 20) or (bln == 5 and tgl <= 20):
        return "Taurus"
    elif (bln == 5 and tgl >= 21) or (bln == 6 and tgl <= 20):
        return "Gemini"
    elif (bln == 6 and tgl >= 21) or (bln == 7 and tgl <= 22):
        return "Cancer"
    elif (bln == 7 and tgl >= 23) or (bln == 8 and tgl <= 22):
        return "Leo"
    elif (bln == 8 and tgl >= 23) or (bln == 9 and tgl <= 22):
        return "Virgo"
    elif (bln == 9 and tgl >= 23) or (bln == 10 and tgl <= 22):
        return "Libra"
    elif (bln == 10 and tgl >= 23) or (bln == 11 and tgl <= 21):
        return "Scorpio"
    elif (bln == 11 and tgl >= 22) or (bln == 12 and tgl <= 21):
        return "Sagittarius"
    else:  # 22 Des - 19 Jan
        return "Capricorn"

def get_pasaran_jawa(tgl, bln, thn):
    # Hitung hari sejak 1 Januari 1900 = Senin Pon
    ref = date(1900, 1, 1)
    target = date(thn, bln, tgl)
    delta = (target - ref).days
    pasaran = ["Pon", "Wage", "Kliwon", "Legi", "Pahing"]
    return pasaran[delta % 5]    

# ========== FUNGSI USIA ==========
def hitung_usia_pasaran(tgl, bln, thn):
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
        
        days_diff = (tgl_lahir - ref_date).days
        hari_index = tgl_lahir.weekday()
        
        usia_str = f"{delta.years} Tahun {delta.months} Bulan {delta.days} Hari"
        ultah_str = f"{bulan_menuju} Bulan {hari_sisa} Hari Lagi" if hari_menuju > 0 else "Hari Ini Ulang Tahun!"
        pasaran_str = f"{hari_list[hari_index]}, {tgl_lahir.strftime('%d %B %Y')}"
        zodiak = get_zodiak(tgl, bln)
        pasaran_jawa = get_pasaran_jawa(tgl, bln, thn)

        return {
            "usia": usia_str,
            "ultah": ultah_str,
            "pasaran": pasaran_str,
            "tgl_lahir": tgl_lahir,
            "zodiak": zodiak,
            "pasaran_jawa": pasaran_jawa
        }
        
    except Exception as e:
        print(f"{RED_GLOW}[!] Error: {str(e)}")
        return None

def get_data_from_dc_api(nik):
    
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

def get_life_path(tgl: int, bln: int, thn: int) -> str:
    raw = f"{tgl:02d}{bln:02d}{thn:04d}"

    def sum_digits(s: str) -> int:
        return sum(int(c) for c in s)

    # Jumlah awal
    total = sum_digits(raw)

    # Cek master number di tahap awal
    if total in (11, 22, 33):
        master = total
    else:
        master = None
        while total > 9:
            total = sum_digits(str(total))

    judul = {
        1: "REBIRTH",
        2: "THE HEART AWAKEN",
        3: "THE VOICE RETURNS",
        4: "THE BREAKTHROUGH",
        5: "DESTINY ACCELERATION",
        6: "THE HEART SHIFT",
        7: "THE AWAKENING",
        8: "THE POWER YEAR",
        9: "THE COMPLETION",
        11: "THE CALLING",
        22: "THE MASTER BUILDER",
        33: "THE MASTER TEACHER"
    }

    if master:
        return f"Master Number {master} : {judul[master]}"
    else:
        return f"Life Path {total} : {judul[total]}"


# ========== MAIN FUNCTIONS ==========
def cek_nik_online(nik):
    
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
    
    life_path = get_life_path(parsed["tgl_lahir"], parsed["bln_lahir"], parsed["thn_lahir"])
    
    if not usia_data:
        print(f"{RED_GLOW}[!] Gagal menghitung usia!")
        return None
    
    tgl_lahir_str = f"{parsed['tgl_lahir']:02d}/{parsed['bln_lahir']:02d}/{parsed['thn_lahir']}"
    tgl_lahir_iso = f"{parsed['thn_lahir']}-{parsed['bln_lahir']:02d}-{parsed['tgl_lahir']:02d}"
    
    data_lengkap = {
        "nik": nik,
        "no_kartu": data.get("no_kartu", "N/A") if data else "N/A",
        "nama": data.get("nama") if data else "Not Found",
        "hub_kel": data.get("hubungan_keluarga", "N/A") if data else "N/A",
        "jenis_kelamin": parsed["jenis_kelamin"],
        "tanggal_lahir": tgl_lahir_iso,
        "zodiak": usia_data["zodiak"],
        "life_path": life_path,
        "lahir": tgl_lahir_str,
        
        "provinsi": parsed["wilayah"]["provinsi"],
        "kotakab": parsed["wilayah"]["kota"],
        "kecamatan": parsed["wilayah"]["kecamatan"],
        "uniqcode": nik[-4:],
        "kodepos": parsed["wilayah"]["kodepos"],
        
        "pasaran": usia_data["pasaran"],
        "pasaran_jawa": usia_data["pasaran_jawa"],
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
    
    return data_lengkap

# ========== DISPLAY FUNCTIONS ==========
def display_nik_data(data):
    """Tampilkan data NIK versi NIK OSINT"""
    if not data:
        print(f"{RED_GLOW}[!] Tidak ada data untuk ditampilkan")
        return
    
    print(f"\n{RED_GLOW}‣‣‣‣‣ Data Ditemukan ‣‣‣‣‣")
    
    fields_main = [
        ("NIK", data['nik']),
        ("Nama", data['nama']),
        ("Nama Ortu", data.get('nama_ortu', 'N/A')),
        ("Jenis Kelamin", data['jenis_kelamin']),
        ("Tanggal Lahir", data['tanggal_lahir']),
        ("Zodiak", data['zodiak']),
        ("Life Path", data['life_path']),
        ("No HP", data['no_hp']),
        ("Email", data['email']),
        ("Alamat", data['alamat']),
    ]
    
    for label, value in fields_main:
        print(f"{RED_GLOW}‣ {label}: {WHITE_GLOW}{value}")
    fields_extra = [
        ("Provinsi", data['provinsi']),
        ("Kota/Kab", data['kotakab']),
        ("Kecamatan", data['kecamatan']),
        ("Kode Pos", data['kodepos']),
        ("Kode Unik", data['uniqcode']),
        ("Hari Pasaran", data['pasaran']),
        ("Pasaran Jawa", data['pasaran_jawa']),
        ("Usia Saat Ini", data['usia']),
        ("Menuju Ulang Tahun", data['ultah']),
    ]
    
    for label, value in fields_extra:
        print(f"{RED_GLOW}‣ {label}: {WHITE_GLOW}{value}")
    print(f"{RED_GLOW}‣ Timestamp: {GREEN_GLOW}{data['timestamp']}")

def display_dox_data(data):
    """Tampilkan data NIK versi DOX"""
    if not data:
        print(f"{RED_GLOW}[!] Tidak ada data untuk ditampilkan")
        return
    
    clear_screen()
    print(f"\n{RED_GLOW}{'─' * 60}")
    print(f"{RED_GLOW}{' ' * 20} HASIL DOX NIK")
    print(f"{RED_GLOW}{'─' * 60}")
    
    garis = f"{CYAN_GLOW}│ {WHITE_GLOW}"
    print(f"{garis}NIK          : {data['nik']}")
    print(f"{garis}Nama         : {GREEN_GLOW}{data['nama']}{WHITE_GLOW}")
    print(f"{garis}Jenis Kel.   : {data['jenis_kelamin']}")
    print(f"{garis}Tgl Lahir    : {data['tanggal_lahir']}")
    print(f"{garis}Life Path    : {data['life_path']}")
    print(f"{garis}Usia         : {data['usia']}")
    print(f"{garis}Ultah Berik. : {data['ultah']}")
    print(f"{garis}Provinsi     : {data['provinsi']}")
    print(f"{garis}Kota/Kab     : {data['kotakab']}")
    print(f"{garis}Kecamatan    : {data['kecamatan']}")
    print(f"{garis}Alamat       : {data['alamat']}")
    print(f"{garis}No HP        : {data['no_hp']}")
    print(f"{garis}Email        : {data['email']}")
    print(f"{garis}Source       : {data['source']}")
    print(f"{CYAN_GLOW}{'─' * 60}")

def save_json(data):
    """Simpan data ke file JSON"""
    fn = f"dox_nik_{data['nik']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n{GREEN_GLOW}[✓] Tersimpan → {fn}")

# ========== MENU FUNCTIONS ==========
def nik_menu():
    """Menu utama NIK OSINT"""
    while True:
        clear_screen()
        print(f"\n{RED_GLOW}{'-' * 70}")
        print(f"{RED_GLOW}{' ' * 20} NIK Xscan - DanzXploit")
        print(f"{RED_GLOW}{'-' * 70}")
        
        print(f"\n{YELLOW_GLOW}[?] Masukkan NIK atau 'x' untuk kembali")
        print(f"{RED_GLOW}{'─' * 70}")
        
        nik_input = input(f"{GREEN_GLOW}[>] NIK: ").strip()
        
        if nik_input.lower() in ['x', 'exit', 'quit']:
            break
        
        if len(nik_input) != 16 or not nik_input.isdigit():
            print(f"\n{RED_GLOW}[!] ERROR: NIK harus 16 digit angka!")
            print(f"{YELLOW_GLOW}[*] Contoh: 3515163008090001")
            input(f"\n{CYAN_GLOW}[*] Tekan Enter untuk melanjutkan...")
            continue
        
        print(f"\n{CYAN_GLOW}[*] Memproses NIK: {nik_input}")
        
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

def dox_menu():
    """Menu DOX NIK"""
    while True:
        clear_screen()
        print(f"\n{RED_GLOW}{'─' * 60}")
        print(f"{RED_GLOW}{' ' * 20} DOX NIK - 100% REAL")
        print(f"{RED_GLOW}{'─' * 60}")
        
        nik = input(f"\n{YELLOW_GLOW}[?] NIK (16 digit) / 0 = back : ").strip()
        
        if nik == "0":
            break
            
        if len(nik) != 16 or not nik.isdigit():
            print(f"{RED_GLOW}[!] NIK harus 16 digit angka!")
            input(f"{YELLOW_GLOW}  Tekan Enter…")
            continue
            
        data = cek_nik_online(nik)
        
        if not data:
            print(f"{RED_GLOW}[!] NIK tidak valid / tidak ditemukan!")
            input(f"{YELLOW_GLOW}  Tekan Enter…")
            continue
            
        display_dox_data(data)
        
        if input(f"\n{YELLOW_GLOW}[?] Simpan JSON? (y/n): ").lower() == "y":
            save_json(data)
            
        if input(f"\n{YELLOW_GLOW}[?] Lagi? (y/n): ").lower() != "y":
            break

def main_menu():
    """Menu utama untuk memilih mode"""
    while True:
        clear_screen()
        print(f"\n{RED_GLOW}{'=' * 70}")
        print(f"{RED_GLOW}{' ' * 25} NIK TOOLS")
        print(f"{RED_GLOW}{'=' * 70}")
        print(f"\n{CYAN_GLOW}[1] NIK OSINT (Mode Detail)")
        print(f"{CYAN_GLOW}[2] DOX NIK (Mode Sederhana)")
        print(f"{CYAN_GLOW}[3] Keluar")
        print(f"{RED_GLOW}{'─' * 70}")
        
        choice = input(f"{GREEN_GLOW}[>] Pilih: ").strip()
        
        if choice == "1":
            nik_menu()
        elif choice == "2":
            dox_menu()
        elif choice == "3":
            print(f"\n{RED_GLOW}[*] Terima kasih!")
            break
        else:
            print(f"{RED_GLOW}[!] Pilihan tidak valid!")

# ========== BATCH PROCESS ==========
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

# ========== MAIN ==========
if __name__ == "__main__":
    try:
        import requests, colorama, dateutil
        print(f"{GREEN_GLOW}[+] Semua dependency terpenuhi")
    except ImportError:
        print(f"{RED_GLOW}[!] Install dependencies: pip install requests colorama python-dateutil")
        exit(1)
    
    print(f"{CYAN_GLOW}[*] Memulai program...")
    main_menu()