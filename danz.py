import os
import sys
from utils.banner import show_banner
from modules.nik import nik_menu
from modules.ip import ip_menu_wrapper  

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        show_banner()
        
        print("\n[1] NIK Xscan")
        print("[2] Lacak IP")           
        print("[0] Exit")
        
        try:
            choice = input("\n[?] Pilih: ").strip()
            
            if choice == '1':
                nik_menu()
            elif choice == '2':
                ip_menu_wrapper()
            elif choice == '0':
                print("\n[!] Thanks for using DanzXploit!")
                sys.exit(0)
            else:
                print("\n[!] Pilihan tidak valid!")
                input("\n[*] Tekan Enter untuk melanjutkan...")
                
        except KeyboardInterrupt:
            print("\n\n[!] Exit by user!")
            sys.exit(0)

if __name__ == "__main__":
    main()