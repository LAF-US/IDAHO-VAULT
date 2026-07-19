#!/usr/bin/env python3
"""Redaction diaper: route command output through this before display."""
import sys, re
t = sys.stdin.read()
t = re.sub(r'((?:token|secret|api[_-]?key|key|password|passwd|pwd|auth)["\' ]*[:=]["\' ]*)[^\s"\',}]+',
           r'\1<REDACTED>', t, flags=re.I)
t = re.sub(r'\b(?:sk|ghp|gho|ghu|ghs|ghr|xox[bpoars])[-_][A-Za-z0-9_-]{16,}', '<REDACTED-token>', t)
t = re.sub(r'(?i)(bearer\s+)[A-Za-z0-9._-]{16,}', r'\1<REDACTED>', t)
t = re.sub(r'\bAIza[0-9A-Za-z_-]{30,}\b', '<REDACTED-google>', t)
t = re.sub(r'\b[A-Fa-f0-9]{32,}\b', '<hex>', t)
t = re.sub(r'\b[A-Za-z0-9+/]{40,}={0,2}\b', '<b64>', t)
sys.stdout.write(t)
