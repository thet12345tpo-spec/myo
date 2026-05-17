Import os
import sys
import hashlib
import requests
import subprocess

def get_hwid():
    try:
        model = os.popen("getprop ro.product.model").read().strip()
        serial = os.popen("getprop ro.serialno").read().strip()
        
        if not model or not serial:
            device_info = "GENERIC-DEVICE-777"
        else:
            device_info = f"{model}|{serial}"
    except Exception:
        device_info = "GENERIC-DEVICE-777"
        
    hwid = hashlib.md5(device_info.encode('utf-8')).hexdigest().upper()
    return hwid

def perform_online_check():
    os.system("clear")
    my_id = get_hwid()
    print(f"\033[1;33m[!] YOUR HWID: \033[0mu{my_id}")
    print("\033[1;34m[*] Checking license status...\033[0m")
    
    try:
        response = requests.get(KEY_URL, timeout=15)
        response.encoding = 'utf-8'
        lines = response.text.split("\n")
        
        found_id = False
        for line in lines:
            if not line.strip():
                continue
            if "|" in line:
                parts = line.split("|")
                server_key = parts[0].strip()
                u_keys = parts[1].strip()
                
                if my_id == server_key:
                    found_id = True
                    input_key = input("\033[1;36m[?] Activation Key: \033[0m")
                    
                    if input_key == u_keys:
                        print("\033[1;32m[+] License Verified!\033[0m")
                        return True
                    else:
                        print("\033[1;31m[!] Invalid Key! Please contact admin via Telegram @bot2191\033[0m")
                        return False
                        
        if not found_id:
            print("\033[1;31m[!] HWID Not Registered! Please contact admin via Telegram @bot2191\033[0m")
            return False
            
    except requests.RequestException:
        print("\033[1;31m[!] Connection Error! Please check your internet.\033[0m")
        return False

def manual_id_capturer():
    print("\033[1;32m==================================================\033[0m")
    print("⚡ RUIJIE ASYNC EXTREME (BYPASS MODE) ⚡")
    print("           TELEGRAM @japan50001")
    print("\033[1;32m==================================================\033[0m")
    
    print("\033[1;33m[?] Please copy and paste your Key/ID to update configuration.\033[0m")
    cmd = [sys.executable, "-u", "-c", "import starlink; starlink.main()"]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        
        found_id = False
        while True:
            line = process.stdout.readline()
            if not line:
                break
                
            if "Enter ID:" in line:
                found_id = True
                print("\033[1;32m[+] Enter ID: \033[0m", end="", flush=True)
                user_input = input()
                
                with open("save.txt", "w") as f:
                    f.write(user_input)
                    
                print("\033[1;32m[!] Saved! Please copy and run 'python main.py' to execute.\033[0m")
                break
                
        process.wait()
        if not found_id:
            print("\033[1;31m[-] ID Not Found.\033[0m")
            
    except Exception:
        pass

if __name__ == "__main__":
    if perform_online_check():
        manual_id_capturer()
