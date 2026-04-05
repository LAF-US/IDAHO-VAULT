import os
import sys
import json
import yaml
from pathlib import Path

# Fix Windows Console Unicode errors
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# VAULT CONFIGURATION
VAULT_ROOT = Path("C:/Users/loganf/Documents/IDAHO-VAULT")
PROPOSAL_PATH = VAULT_ROOT / "!/CREWAI/LINKER-PROPOSAL-v1.json"
DRY_RUN = False  # Set to True for validation

# STOP LIST (High-frequency linguistic noise to exclude)
STOP_LIST = {
    "and", "without", "people", "system", "URL", "file", 
    "context", "authority", "action", "future", "notes", 
    "note", "text", "term", "individual", "May", "100",
    "VAULT", "IDAHO-VAULT", "SWARM"
}

def hydrate_note(file_path, related_links):
    if not file_path.exists():
        return False
    
    # Filter links against stop list
    filtered_links = [l for l in related_links if l not in STOP_LIST]
    if not filtered_links:
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple frontmatter parsing
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                # Update 'related'
                existing_related = fm.get("related", [])
                if isinstance(existing_related, str):
                    existing_related = [existing_related]
                
                updated_related = list(set(existing_related + filtered_links))
                fm["related"] = sorted(updated_related)
                
                # Stability check: ensure authority
                if "authority" not in fm:
                    fm["authority"] = "LOGAN"
                
                new_fm_text = yaml.dump(fm, sort_keys=False, allow_unicode=True).rstrip()
                new_content = "---\n" + new_fm_text + "\n---\n" + parts[2].lstrip()
                
                if DRY_RUN:
                    print(f"[DRY-RUN] Hydrated: {file_path.name} with {len(filtered_links)} links.")
                    return True
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
            except yaml.YAMLError:
                print(f"[ERROR] YAML Parse Error in {file_path.name}")
                return False
    else:
        # No frontmatter - Inject it
        fm = {
            "authority": "LOGAN",
            "related": sorted(filtered_links)
        }
        new_fm_text = yaml.dump(fm, sort_keys=False, allow_unicode=True).rstrip()
        new_content = "---\n" + new_fm_text + "\n---\n\n" + content
        
        if DRY_RUN:
            print(f"[DRY-RUN] Created Frontmatter for: {file_path.name}")
            return True
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

def run_hydration():
    if not PROPOSAL_PATH.exists():
        print(f"[FATAL] Proposal not found: {PROPOSAL_PATH}")
        return

    with open(PROPOSAL_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        proposal = data.get("proposal", {})

    # Sort files in Reverse Alphabetical (Omega to Alpha) order
    sorted_files = sorted(proposal.keys(), reverse=True)
    
    count = 0
    total = len(sorted_files)
    
    print(f"🔗 Starting Phase 3: Metadata Hydration ({total} files, Omega -> Alpha)...")
    
    for filename in sorted_files:
        file_path = VAULT_ROOT / filename
        links = proposal[filename]
        
        if hydrate_note(file_path, links):
            count += 1
            if count % 100 == 0:
                print(f"🚀 Progress: {count}/{total} files hydrated.")

    print(f"✅ Hydration COMPLETE. {count} files updated.")

if __name__ == "__main__":
    run_hydration()
