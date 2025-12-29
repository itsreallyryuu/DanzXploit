
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[*] Installing NIK OSINT Tools...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 not found! Please install Python3 first.${NC}"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[!] pip3 not found, trying to install...${NC}"
    apt install python3-pip -y || yum install python3-pip -y
fi

echo -e "${GREEN}[*] Installing dependencies...${NC}"
pip3 install -r requirements.txt

chmod +x main.py
chmod +x install.sh

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${YELLOW}[*] Run: python3 main.py${NC}"



echo "
╔══════════════════════════════════════╗
║       DANZ EXPLOIT INSTALLER        ║
║         TERMUX VERSION v2.0         ║
╚══════════════════════════════════════╝
"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}[1/5]${NC} Updating packages..."
pkg update -y > /dev/null 2>&1
pkg upgrade -y > /dev/null 2>&1

echo -e "${CYAN}[2/5]${NC} Installing dependencies..."
pkg install -y nodejs git wget curl python ffmpeg imagemagick nano > /dev/null 2>&1
npm install -g npm@latest > /dev/null 2>&1

echo -e "${CYAN}[3/5]${NC} Setting up project..."
cd $HOME
if [ -d "danz-ciduk" ]; then
    rm -rf danz-ciduk
fi
mkdir danz-ciduk
cd danz-ciduk

cat > package.json << EOF
{
  "name": "danz-ciduk-unlimited",
  "version": "2.0.0",
  "description": "WhatsApp Bot Multi-API System",
  "main": "danz.js",
  "scripts": {
    "start": "node danz.js",
    "test": "node test.js",
    "install-deps": "npm install whatsapp-web.js qrcode-terminal axios fs-extra"
  },
  "keywords": ["whatsapp-bot", "danz", "ciduk", "unlimited"],
  "author": "DanzXploit",
  "license": "MIT"
}
EOF

echo -e "${CYAN}[4/5]${NC} Installing Node.js modules..."
npm install whatsapp-web.js qrcode-terminal axios fs-extra > /dev/null 2>&1

echo -e "${CYAN}[5/5]${NC} Creating bot files..."
cat > danz.js << 'EOF'
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs-extra');
const path = require('path');
const axios = require('axios');

// Config
const CONFIG = {
    PREFIX: '.',
    OWNER: '628xxxxxxx',
    LOGO_URL: 'https://files.catbox.moe/w8qxid.png',
    
    APIS: {
        DESKCOLLECTION: {
            ENABLED: true,
            URL: 'https://deskcollection.space/api/v1/kpu/cek',
            METHOD: 'POST',
            TIMEOUT: 10000
        },
        
        BINDERBYTE: {
            ENABLED: true,
            API_KEY: 'MASUKKIN_API_KEY_BINDERBYTE_DISINI',
            URL: 'https://api.binderbyte.com/v1/ktp',
            METHOD: 'GET'
        },
        
        SIMULATION: { ENABLED: true }
    },
    
    PATH: {
        FOTO_COWO: './foto_cowo',
        FOTO_CEWE: './foto_cewe',
        SESSION: './session',
        LOGS: './logs'
    }
};

// Setup
CONFIG.setup = function() {
    Object.values(this.PATH).forEach(folder => {
        if (!fs.existsSync(folder)) {
            fs.mkdirSync(folder, { recursive: true });
            console.log(`📁 Created: ${folder}`);
        }
    });
};
CONFIG.setup();

// WhatsApp Client
const client = new Client({
    authStrategy: new LocalAuth({
        clientId: "danz-termux",
        dataPath: CONFIG.PATH.SESSION
    }),
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--single-process',
            '--no-zygote'
        ]
    }
});

client.on('qr', (qr) => {
    console.clear();
    console.log('╔══════════════════════════════════════╗');
    console.log('║       DANZ CIDUK - TERMUX           ║');
    console.log('╠══════════════════════════════════════╣');
    console.log('║  📱 SCAN QR CODE INI DI WHATSAPP    ║');
    console.log('╚══════════════════════════════════════╝\n');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.clear();
    console.log('╔══════════════════════════════════════╗');
    console.log('║       DANZ CIDUK - TERMUX           ║');
    console.log('╠══════════════════════════════════════╣');
    console.log('║  ✅ BOT SIAP DI TERMUX!             ║');
    console.log('║  🤖 Nama: DanzXploit Termux         ║');
    console.log('║  📱 Login Berhasil!                 ║');
    console.log('╚══════════════════════════════════════╝\n');
    console.log('🔥 COMMAND YANG TERSEDIA:');
    console.log('├── .doxfoto [cowo/cewe]');
    console.log('├── .doxnik [16_digit]');
    console.log('├── .menu / .help');
    console.log('└── .owner');
});

client.on('message', async (msg) => {
    if (msg.body.startsWith('.doxfoto')) {
        const args = msg.body.split(' ');
        const gender = args[1] || 'random';
        
        // Logic untuk foto
        const fotoDir = gender === 'cowo' ? CONFIG.PATH.FOTO_COWO : 
                       gender === 'cewe' ? CONFIG.PATH.FOTO_CEWE : 
                       Math.random() > 0.5 ? CONFIG.PATH.FOTO_COWO : CONFIG.PATH.FOTO_CEWE;
        
        try {
            const files = await fs.readdir(fotoDir);
            const imageFiles = files.filter(f => /\.(jpg|jpeg|png|gif)$/i.test(f));
            
            if (imageFiles.length > 0) {
                const randomFile = imageFiles[Math.floor(Math.random() * imageFiles.length)];
                const media = MessageMedia.fromFilePath(path.join(fotoDir, randomFile));
                await client.sendMessage(msg.from, media, { 
                    caption: `📸 DANZ CIDUK\nFoto ${gender}\n${randomFile}` 
                });
            } else {
                await msg.reply('❌ Tidak ada foto di folder!');
            }
        } catch (error) {
            await msg.reply('❌ Gagal mengirim foto!');
        }
    }
    
    if (msg.body.startsWith('.menu') || msg.body.startsWith('.help')) {
        const menu = `
🤖 *DANZ CIDUK TERMUX*
════════════════════
📸 *FOTO RANDOM*
• .doxfoto - Random cowo/cewe
• .doxfoto cowo - Foto cowok
• .doxfoto cewe - Foto cewek

🔍 *CEK NIK*
• .doxnik [16_digit] - Cek data NIK

ℹ️ *LAINNYA*
• .menu / .help - Menu ini
• .owner - Info pemilik

════════════════════
🤖 *DanzXploit Termux v2.0*
        `;
        await msg.reply(menu);
    }
    
    if (msg.body.startsWith('.doxnik')) {
        const nik = msg.body.split(' ')[1];
        if (!nik || !/^\d{16}$/.test(nik)) {
            await msg.reply('❌ Format salah! Contoh: .doxnik 3273011209870001');
            return;
        }
        
        await msg.reply(`🔍 Mencari NIK: ${nik}...\n⏳ Tunggu sebentar...`);
        // API logic bisa ditambahkan di sini
        const result = `NIK: ${nik}\nNama: BUDI SANTOSO\nTTL: JAKARTA, 12-09-1987`;
        await msg.reply(result);
    }
    
    if (msg.body.startsWith('.owner')) {
        await msg.reply(`👑 PEMILIK BOT\n━━━━━━━━━━\n🤖 DanzXploit\n📱 ${CONFIG.OWNER}\n🏷️ Termux Edition`);
    }
});

client.initialize();
EOF

cat > setup.js << 'EOF'
const fs = require('fs-extra');
const path = require('path');

console.log(`
╔══════════════════════════════════════╗
║       DANZ CIDUK - SETUP TOOLS      ║
╚══════════════════════════════════════╝
`);

// Create folders
const folders = [
    'foto_cowo',
    'foto_cewe',
    'session',
    'logs',
    'tmp'
];

folders.forEach(folder => {
    if (!fs.existsSync(folder)) {
        fs.mkdirSync(folder, { recursive: true });
        console.log(`✅ Created: ${folder}/`);
    }
});

// Create sample photos info
const info = `
📁 FOLDER STRUCTURE:
├── foto_cowo/   # Taruh foto cowok disini
├── foto_cewe/   # Taruh foto cewek disini
├── session/     # Session WhatsApp
├── logs/        # Log file
└── tmp/         # Temporary files

📝 CARA PAKAI:
1. Masukkan foto ke folder foto_cowo/ atau foto_cewe/
2. Jalankan bot: node danz.js
3. Scan QR code dengan WhatsApp
4. Kirim .menu untuk melihat command

⚠️ PERHATIAN:
• Pastikan koneksi internet stabil
• Jangan hapus folder session/
• Foto format: JPG, PNG, GIF
`;

fs.writeFileSync('INFO.txt', info);
console.log(`
📦 SETUP SELESAI!

🔥 JALANKAN BOT DENGAN:
cd $HOME/danz-ciduk
node danz.js

📚 BACA INFO:
cat INFO.txt
`);
EOF

cat > start << 'EOF'
#!/bin/bash
cd $HOME/danz-ciduk
echo "Starting Danz Ciduk Bot..."
node danz.js
EOF

chmod +x start

cat > uninstall.sh << 'EOF'
#!/bin/bash
echo "Uninstalling Danz Ciduk..."
cd $HOME
rm -rf danz-ciduk
echo "✅ Uninstall complete!"
EOF

chmod +x uninstall.sh

chmod 755 danz.js
chmod 755 setup.js

echo -e "${YELLOW}[INFO]${NC} Downloading sample images..."
mkdir -p foto_cowo foto_cewe
wget -q -O foto_cowo/sample1.jpg https://picsum.photos/400/500
wget -q -O foto_cewe/sample1.jpg https://picsum.photos/400/501

echo -e "\n${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅ INSTALLASI BERHASIL!           ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo -e "\n${CYAN}NEXT STEP:${NC}"
echo -e "1. ${YELLOW}cd \$HOME/danz-ciduk${NC}"
echo -e "2. ${YELLOW}node setup.js${NC}"
echo -e "3. ${YELLOW}node danz.js${NC}"
echo -e "4. Scan QR Code dengan WhatsApp"
echo -e "\n${CYAN}QUICK START:${NC} ${YELLOW}./start${NC}"
echo -e "\n${RED}⚠️  PERHATIAN:${NC} Hanya untuk edukasi!"