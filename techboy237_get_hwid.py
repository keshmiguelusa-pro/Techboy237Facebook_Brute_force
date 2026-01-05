import os
import sys
import subprocess
import hashlib
import platform
import re
import shutil

def fetch_hwid():
    """
    STABLE HWID v4: Optimized for Termux (Android), Kali (Linux), and Windows.
    Uses multi-layered hardware fingerprinting.
    """
    hwid_components = []

    # Layer 0: System Architecture (Permanent)
    hwid_components.append(platform.system())
    hwid_components.append(platform.machine())

    try:
        # 1. Android / Termux Specific
        if shutil.which("getprop"):
            try:
                # Use only the most stable hardware-linked properties
                props = [
                    "ro.product.model", 
                    "ro.product.manufacturer", 
                    "ro.serialno", 
                    "ro.build.id",
                    "ro.board.platform"
                ]
                for prop in props:
                    val = subprocess.check_output(f"getprop {prop}", shell=True, stderr=subprocess.DEVNULL).decode().strip()
                    if val and val.lower() != "unknown":
                        hwid_components.append(val)
            except: pass

        # 2. Windows Physical Serials
        if sys.platform == "win32":
            try:
                out = subprocess.check_output("wmic diskdrive get serialnumber", shell=True, stderr=subprocess.DEVNULL).decode()
                serials = [l.strip() for l in out.splitlines() if l.strip() and "SerialNumber" not in l]
                hwid_components.extend(serials)
            except: pass
            try:
                out = subprocess.check_output("wmic baseboard get serialnumber", shell=True, stderr=subprocess.DEVNULL).decode()
                serials = [l.strip() for l in out.splitlines() if l.strip() and "SerialNumber" not in l]
                hwid_components.extend(serials)
            except: pass

        # 3. Linux / Kali (Physical & OS IDs)
        elif sys.platform.startswith("linux"):
            # Try machine-id (standard on Kali/Debian)
            paths = ["/etc/machine-id", "/var/lib/dbus/machine-id"]
            for p in paths:
                if os.path.exists(p):
                    try:
                        with open(p, "r") as f:
                            hwid_components.append(f.read().strip())
                            break
                    except: pass
            
            # Try board serials
            paths = ["/sys/class/dmi/id/board_serial", "/sys/class/dmi/id/product_serial"]
            for p in paths:
                if os.path.exists(p):
                    try:
                        with open(p, "r") as f:
                            val = f.read().strip()
                            if val: hwid_components.append(val)
                    except: pass

            # Try CPU Serial
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "serial" in line.lower():
                            hwid_components.append(line.split(":")[-1].strip())
            except: pass

    except Exception: pass

    # Filter out junk and ensure stability
    hwid_components = [str(x) for x in hwid_components if x and len(x) > 2 and "to be filled" not in str(x).lower()]
    
    # Final Layer: Combine and Hash
    # If list is too short, add platform-specific stable strings
    if len(hwid_components) < 3:
        hwid_components.append(platform.release())
        hwid_components.append(platform.version())

    raw_id = "|".join(sorted(list(set(hwid_components))))
    return hashlib.sha256(raw_id.encode()).hexdigest().upper()

if __name__ == "__main__":
    G, C, Y, W = "\033[38;5;46m", "\033[38;5;51m", "\033[38;5;226m", "\033[0m"
    print(f"\n{G}      TECHBOY237 SUPREME HARDWARE IDENTIFIER v4{W}")
    print(f"{G}" + "="*55 + f"{W}")
    
    hwid = fetch_hwid()
    print(f"\n{C}[+] SYSTEM       : {W}{platform.system()} {platform.machine()}")
    print(f"{C}[+] SUPREME_HWID : {G}{hwid}{W}")
    print(f"\n{Y}  COPY THIS ID FOR LIFETIME AUTHORIZATION{W}\n")
