#!/usr/bin/env python3
"""Quick syntax verification by direct import."""

import traceback

# Files to check
files_to_check = [
    r"C:\Users\loganf\Documents\IDAHO-VAULT\.github\scripts\wayback_audit.py",
    r"C:\Users\loganf\Documents\IDAHO-VAULT\.github\scripts\validate_content.py",
]

for fpath in files_to_check:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, fpath, 'exec')
        print(f"✓ PASS: {fpath}")
    except SyntaxError as e:
        print(f"✗ FAIL: {fpath}")
        print(f"  SyntaxError: {e}")
    except Exception as e:
        print(f"✗ FAIL: {fpath}")
        print(f"  Error: {e}")
        traceback.print_exc()
