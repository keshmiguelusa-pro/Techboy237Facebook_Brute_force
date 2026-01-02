import os, sys, platform, subprocess, signal

def launch():
    if platform.system() != "Windows":
        try: signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        except: pass

    d = os.path.dirname(os.path.abspath(__file__))
    b = os.path.join(d, "techboy237facebook_brute_force_secure")
    p = os.path.join(d, "techboy237facebook_brute_force_protected.py")
    
    if platform.system() != "Windows" and "True" == "True" and os.path.exists(b):
        try:
            if not os.access(b, os.X_OK): os.chmod(b, 0o755)
            ret = subprocess.call([b])
            if ret == 0: return
        except Exception: pass

    if os.path.exists(p):
        try:
            subprocess.call([sys.executable, p])
        except Exception:
            sys.exit(1)
    else:
        sys.exit(1)

if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        sys.exit(0)