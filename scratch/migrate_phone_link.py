import os
import shutil
from pathlib import Path

vault_root = Path(r"C:\Users\loganf\Documents\IDAHO-VAULT")
inbox_dir = vault_root / "!" / "INBOX"
source_dir = inbox_dir / "PHONE-LINK"

def classify(name):
    ext = os.path.splitext(name)[1].lower()
    name_lower = name.lower()
    
    if ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
        if 'screenshot' in name_lower:
            return 'screenshots'
        return 'images'
    if ext in ['.m4a', '.mp3', '.ogg', '.wav']:
        return 'audio'
    if ext in ['.mp4', '.mov', '.webm']:
        return 'video'
    if ext in ['.pdf', '.docx', '.txt']:
        return 'docs'
    return 'other'

if not source_dir.exists():
    print(f"Source {source_dir} not found. Nothing to migrate.")
    exit(0)

# Categories to ensure exist
categories = ['images', 'screenshots', 'audio', 'video', 'docs', 'other']
for cat in categories:
    (inbox_dir / cat).mkdir(parents=True, exist_ok=True)

infrastructure_files = ['phone-link-auto-sweep.ps1', 'START-PHONE-LINK-SWEEP.cmd', '_phone-link-sweep.log']

print(f"Migrating from {source_dir} to {inbox_dir}...")

for item in source_dir.iterdir():
    if item.is_file():
        if item.name in infrastructure_files:
            print(f"Deleting stale infra file: {item.name}")
            item.unlink()
            continue
            
        category = classify(item.name)
        dest = inbox_dir / category / item.name
        
        # Handle collision
        if dest.exists():
            print(f"Collision: {item.name} already exists in {category}. Skipping.")
            continue
            
        print(f"Moving: {item.name} -> {category}/")
        shutil.move(str(item), str(dest))

# Finally remove the source dir if empty
try:
    source_dir.rmdir()
    print(f"Removed empty directory: {source_dir}")
except OSError as e:
    print(f"Could not remove {source_dir}: {e}")
