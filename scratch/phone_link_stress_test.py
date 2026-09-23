import os
import time
from pathlib import Path

# Config
downloads_dir = Path.home() / "Downloads" / "Phone Link"
vault_dir = Path(r"C:\Users\loganf\Documents\IDAHO-VAULT")
intake_script = vault_dir / ".github/scripts/phone_link_intake.py"
inbox_dir = vault_dir / "!" / "INBOX"

# Test files to simulate
test_files = [
    ("test_image.jpg", b"fake image content"),
    ("test_screenshot_2026.png", b"fake screenshot content"),
    ("test_audio.m4a", b"fake audio content"),
    ("test_document.pdf", b"fake pdf content"),
    ("test_unknown.xyz", b"fake unknown content"),
]

def setup():
    downloads_dir.mkdir(parents=True, exist_ok=True)
    # Clear downloads
    for f in downloads_dir.iterdir():
        if f.is_file():
            f.unlink()

def simulate_drops():
    print(f"Simulating drops into {downloads_dir}...")
    for name, content in test_files:
        p = downloads_dir / name
        p.write_bytes(content)
        print(f"  Dropped: {name}")
        #time.sleep(0.1) # Rapid drop

def verify():
    print("\nVerifying intake...")
    # Give the watcher/intake a moment if running, but here we will run intake manually for the test
    import subprocess
    result = subprocess.run(["python", str(intake_script), "--live-write"], capture_output=True, text=True)
    print("Intake Output:")
    print(result.stdout)
    
    # Check !/INBOX categories
    expected = {
        "images/": "test_image.jpg",
        "screenshots/": "test_screenshot_2026.png",
        "audio/": "test_audio.m4a",
        "docs/": "test_document.pdf",
        "other/": "test_unknown.xyz",
    }
    
    for folder, file_prefix in expected.items():
        search_dir = inbox_dir / folder.strip("/")
        if not search_dir.exists():
            print(f"FAILED: Category folder {folder} missing")
            continue
            
        found = list(search_dir.glob(f"*-{file_prefix}")) # Date prefix handled by script
        if found:
            print(f"SUCCESS: Found {file_prefix} in {folder}")
        else:
            print(f"FAILED: Could not find {file_prefix} in {folder}")

if __name__ == "__main__":
    setup()
    simulate_drops()
    verify()
