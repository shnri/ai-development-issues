#!/usr/bin/env python3
"""Check that the authority state stays inside the public-repository boundary.

The repository is public. Only cross-project knowledge may live here:
catalog, remedies, research/evidence from public sources, lifecycle history,
quick wins, and publishable evaluation results.

Forbidden (fails the check):
- credential / secret / token shaped values
- absolute local filesystem paths (leak private repository layout / traces)
- non-public URLs (localhost, private IP ranges, *.local, *.internal, file://)
- project-specific note keys (e.g. ``<project>_notes``, ``project_note``)
- consumer-only record kinds (findings / experiments / adoptions)
- agent trace files or non JSON/Markdown files under the state root
- tracked files under ``workspaces/`` (cloned target checkouts)

Exit code 0 when clean, 1 when violations exist.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
STATE = REPO / '.ai-intelligence' / 'ai-development'

CREDENTIAL_PATTERNS = [
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'AIza[0-9A-Za-z_-]{30,}'),
    re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'\bsk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'\bxox[abpr]-[A-Za-z0-9-]{10,}'),
    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    re.compile(r'(?i)\b(password|passwd|api[_-]?key|secret|token)\s*[:=]\s*["\'][^"\']{8,}["\']'),
]
ABSOLUTE_PATH = re.compile(r'(?<![\w./-])/(workspaces|home|Users|tmp|var|root|mnt|opt|srv)/[\w.-]')
WINDOWS_PATH = re.compile(r'\b[A-Za-z]:\\\\?[\w.-]')
PRIVATE_URL = re.compile(
    r'(?i)\b(?:https?|wss?|ftp)://(?:[^/\s"\']*@)?'
    r'(?:localhost|127\.\d+\.\d+\.\d+|0\.0\.0\.0|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|'
    r'172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|[\w.-]+\.(?:local|internal|corp|lan|intranet))(?::\d+)?\b'
    r'|\bfile://'
)
URL_WITH_CREDENTIALS = re.compile(r'(?i)\b(?:https?|ssh|git)://[^/\s"\']+:[^/\s"\']+@')
# ``project_note(s)`` and ``<consumer>_note(s)`` carry consumer-specific observations; they belong to the consumer repository.
# Role/process prefixes and problem-id prefixes (e.g. ``d11_note`` = cross-reference to problem D11) are generic and allowed.
GENERIC_NOTE_PREFIXES = ('controller', 'reviewer', 'maintainer', 'release', 'research', 'structural', 'evaluation', 'migration', 'general', 'shared')
FORBIDDEN_KEY = re.compile(r'^(?:project_notes?|(?P<prefix>[a-z0-9]+)_project_notes?|(?P<name>[a-z0-9]+)_notes?)$')


def is_forbidden_key(key: str) -> bool:
    match = FORBIDDEN_KEY.match(key)
    if not match:
        return False
    name = match.group('name')
    if name is None:
        return True
    if name in GENERIC_NOTE_PREFIXES or re.fullmatch(r'[a-z]\d{1,2}', name):
        return False
    return True
CONSUMER_ONLY_DIRS = ('findings', 'experiments', 'adoptions')
ALLOWED_SUFFIXES = {'.json', '.md', '.gitkeep'}
TRACE_HINTS = ('trace', 'transcript', 'session-log')


def walk_state() -> list[Path]:
    return sorted(p for p in STATE.rglob('*') if p.is_file() and 'workspaces' not in p.relative_to(STATE).parts)


def keys_recursive(value, prefix='$'):
    if isinstance(value, dict):
        for key, child in value.items():
            yield f'{prefix}.{key}', key
            yield from keys_recursive(child, f'{prefix}.{key}')
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from keys_recursive(child, f'{prefix}[{i}]')


def tracked_workspace_files() -> list[str]:
    cp = subprocess.run(['git', 'ls-files', '--', '.ai-intelligence/ai-development/workspaces'], cwd=REPO, text=True, capture_output=True)
    return [line for line in cp.stdout.splitlines() if line.strip()] if cp.returncode == 0 else []


def main() -> int:
    violations: list[str] = []
    files = walk_state()
    for path in files:
        rel = path.relative_to(REPO).as_posix()
        parts = path.relative_to(STATE).parts
        if parts[0] in CONSUMER_ONLY_DIRS and path.name != '.gitkeep':
            violations.append(f'{rel}: consumer-only record kind "{parts[0]}" must stay in the consumer project')
        if path.suffix.lower() == '.jsonl' or any(hint in path.name.lower() for hint in TRACE_HINTS):
            violations.append(f'{rel}: agent trace / transcript files are not allowed')
        if path.suffix.lower() not in ALLOWED_SUFFIXES and path.name != '.gitkeep':
            violations.append(f'{rel}: only JSON/Markdown records are allowed under the state root')
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            violations.append(f'{rel}: not UTF-8 text')
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pattern in CREDENTIAL_PATTERNS:
                if pattern.search(line):
                    violations.append(f'{rel}:{lineno}: credential-shaped value ({pattern.pattern[:30]}...)')
            if ABSOLUTE_PATH.search(line) or WINDOWS_PATH.search(line):
                violations.append(f'{rel}:{lineno}: absolute local filesystem path')
            if PRIVATE_URL.search(line) or URL_WITH_CREDENTIALS.search(line):
                violations.append(f'{rel}:{lineno}: non-public or credentialed URL')
        if path.suffix.lower() == '.json':
            try:
                value = json.loads(text)
            except json.JSONDecodeError as exc:
                violations.append(f'{rel}: invalid JSON ({exc})')
                continue
            for pointer, key in keys_recursive(value):
                if isinstance(key, str) and is_forbidden_key(key):
                    violations.append(f'{rel}: project-specific key {pointer}')
    for tracked in tracked_workspace_files():
        violations.append(f'{tracked}: cloned target workspaces must not be tracked')

    result = {
        'checked_files': len(files),
        'violations': violations,
        'valid': not violations,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if violations else 0


if __name__ == '__main__':
    sys.exit(main())
