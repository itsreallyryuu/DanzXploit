
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