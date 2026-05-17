# =========================================
# Decompiled / Cleaned Version
# =========================================

import os
import time
import hashlib
import requests

# =========================================
# CONFIG
# =========================================

KEY_URL = "https://raw.githubusercontent.com/ytun9959-design/Auth/refs/heads/main/key.txt"

SESSION_FILE = ".session_data"

# =========================================
# GET HWID
# =========================================

def get_hwid():
    try:
        model = os.popen(
            "getprop ro.product.model"
        ).read().strip()

        serial = os.popen(
            "getprop ro.serialno"
        ).read().strip()

        device_info = model + serial

        return hashlib.md5(
            device_info.encode()
        ).hexdigest().upper()

    except:
        return "ERROR-ID-000"

# =========================================
# GET LOCAL BYPASS ID
# =========================================

def get_bypass_id():

    for f_name in ["id.txt", "save.txt"]:

        if os.path.exists(f_name):

            try:
                fs = open(
                    f_name,
                    "r"
                ).read().strip()

                if fs:
                    return fs

            except:
                pass

    return "BA59F61yourB"

# =========================================
# CHECK LOCAL SESSION
# =========================================

def check_local_session(my_id):

    if os.path.exists(SESSION_FILE):

        try:
            data = open(
                SESSION_FILE
            ).read().strip().split("|")

            if len(data) >= 2:

                expiry = float(data[1])

                if expiry > time.time():
                    return True

        except:
            os.remove(SESSION_FILE)

    return False

# =========================================
# FAKE RESPONSE
# =========================================

class StarlinkBypassResponse:

    def __init__(self):

        self.BYPASS_ID = get_bypass_id()

        self.content = (
            b"2099-12-31 23:59:59"
        )

        self.status_code = 200

    def __iter__(self):
        return iter(self.content)

    def splitlines(self):
        return self.content.splitlines()

    def __getattr__(self, name):
        return getattr(self.content, name)

# =========================================
# REQUEST HOOK
# =========================================

real_get = requests.get

def hooked_get(url, *args, **kwargs):

    if "google" in url or "docs.google" in url:
        return StarlinkBypassResponse()

    return real_get(
        url,
        *args,
        **kwargs
    )

# =========================================
# OUTPUT HOOK
# =========================================

class OutputHooker:

    def __init__(self, original_stream):
        self.original_stream = original_stream

    def write(self, text):

        if isinstance(text, str):

            if "error" in text.lower():
                return

        self.original_stream.write(text)

    def flush(self):
        self.original_stream.flush()

# =========================================
# ONLINE CHECK
# =========================================

def perform_online_check():

    my_id = get_hwid()

    os.system("clear")

    print(
        "\033[1;33m[!] YOUR ID: ",
        my_id,
        "\033[0m"
    )

    try:

        response = requests.get(
            KEY_URL,
            timeout=15
        )

        lines = response.text.splitlines()

        user_key = input(
            "\033[1;36m[?] Enter Activation Key: \033[0m"
        ).lower()

        for line in lines:

            if "|" not in line:
                continue

            parts = line.split("|")

            if len(parts) < 3:
                continue

            server_id = parts[0]
            server_key = parts[1]
            expiry_sec = int(parts[2])

            if server_key.lower() == user_key.lower():

                if server_id != my_id:

                    print(
                        "\033[1;31m[!] ID not found on server!\033[0m"
                    )

                    return False

                expiry_timer = (
                    time.time() + expiry_sec
                )

                open(
                    SESSION_FILE,
                    "w"
                ).write(
                    my_id
                    + "|"
                    + str(expiry_timer)
                )

                print(
                    "[+] Login Success"
                )

                return True

        print(
            "\033[1;31m[!] Key Invalid!\033[0m"
        )

        return False

    except Exception as e:

        print(
            "\033[1;31m[!] Connection Error:",
            e
        )

        return False

# =========================================
# MAIN
# =========================================

def main():

    requests.get = hooked_get

    my_id = get_hwid()

    if check_local_session(my_id):

        print("[+] Local Session Valid")

    else:

        if not perform_online_check():
            return

    print("[+] Bypass Loaded")

# =========================================
# RUN
# =========================================

if __name__ == "__main__":
    main()