"""
MEBU Analytics Platform — Launcher
Starts the Streamlit server and opens the browser automatically.
Compiled to MEBU_Analytics.exe via PyInstaller.
"""
import subprocess
import webbrowser
import time
import sys
import os
import threading
import shutil


# ── Resolve project root ──────────────────────────────────────────────────────
# When compiled by PyInstaller, sys.argv[0] is the .exe path.
# When run as script, __file__ gives us the directory.
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MAIN_PY = os.path.join(BASE_DIR, 'main.py')
IP_ADDR = '10.66.221.187'
URL = f'http://{IP_ADDR}:8501'


# Known streamlit path for this machine (fallback if PATH lookup fails)
STREAMLIT_KNOWN = os.path.join(
    os.path.expanduser("~"),
    r"AppData\Roaming\Python\Python313\Scripts\streamlit.exe"
)


def find_streamlit():
    """Return path to streamlit executable."""
    # 1. Try PATH first
    found = shutil.which('streamlit')
    if found:
        return found
    # 2. Try known install location
    if os.path.exists(STREAMLIT_KNOWN):
        return STREAMLIT_KNOWN
    return None


def open_browser_delayed(seconds=4):
    """Open browser after a delay to let the server start."""
    time.sleep(seconds)
    webbrowser.open(URL)


def show_error(msg):
    """Show a simple error dialog using PowerShell (no tkinter dependency)."""
    subprocess.run(
        ['powershell', '-Command',
         f'[System.Windows.Forms.MessageBox]::Show("{msg}", "MEBU Analytics — Error",'
         f'[System.Windows.Forms.MessageBoxButtons]::OK,'
         f'[System.Windows.Forms.MessageBoxIcon]::Error)'],
        capture_output=True
    )


def main():
    streamlit_exe = find_streamlit()
    if not streamlit_exe:
        show_error(
            "Streamlit not found.\\n\\n"
            "Please ensure Python and Streamlit are installed:\\n"
            "  pip install streamlit"
        )
        sys.exit(1)

    if not os.path.exists(MAIN_PY):
        show_error(
            f"main.py not found at:\\n{MAIN_PY}\\n\\n"
            "Please keep MEBU_Analytics.exe in the project folder."
        )
        sys.exit(1)

    # Open browser in background thread after server starts
    t = threading.Thread(target=open_browser_delayed, args=(4,), daemon=True)
    t.start()

    # Launch streamlit — this blocks until the user closes the server
    subprocess.run(
        [streamlit_exe, 'run', MAIN_PY,
         '--server.address', '0.0.0.0',
         '--server.headless', 'true',
         '--browser.gatherUsageStats', 'false',
         '--server.port', '8501'],
        cwd=BASE_DIR,
    )



if __name__ == '__main__':
    main()
