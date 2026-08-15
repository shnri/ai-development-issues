#!/usr/bin/env python3
"""Validate the authority repository: catalog integrity, record schemas, public boundary.

Usage: python3 scripts/check_authority.py [--quiet]

Requires the `ai-development-improvement` Plugin checkout at
`vendor/shared-agent-plugins` (git submodule). Exit code 0 when every check passes.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
STATE = REPO / '.ai-intelligence' / 'ai-development'
SKILL = REPO / 'vendor' / 'shared-agent-plugins' / 'plugins' / 'ai-development-improvement' / 'skills' / 'ai-development-improvement'
SCRIPTS = SKILL / 'scripts'

RECORD_DIRS = [
    'catalog/catalog.json',
    'catalog/candidates',
    'catalog/reviews',
    'catalog/events',
    'remedies',
    'work-items',
    'implementations',
    'evaluations',
    'promotions',
    'releases',
    'propagation',
    'capabilities',
    'project-profile.json',
    'automation-policy.json',
    'target-registry.json',
]


def run(label: str, command: list[str], quiet: bool) -> bool:
    cp = subprocess.run(command, cwd=REPO, text=True, capture_output=True)
    ok = cp.returncode == 0
    print(f'{"PASS" if ok else "FAIL"} {label}')
    if not ok or not quiet:
        tail = (cp.stdout + cp.stderr).strip().splitlines()
        for line in tail[-40:]:
            print(f'    {line}')
    return ok


def main() -> int:
    quiet = '--quiet' in sys.argv[1:]
    if not (SCRIPTS / 'check_catalog_integrity.py').is_file():
        print('FAIL plugin checkout missing: run `git submodule update --init --recursive`')
        return 1
    profile = json.loads((STATE / 'project-profile.json').read_text(encoding='utf-8'))
    role_ok = profile.get('catalog', {}).get('role') == 'authority'
    print(f'{"PASS" if role_ok else "FAIL"} project-profile catalog.role == authority')

    results = [role_ok]
    results.append(run('check_catalog_integrity', [sys.executable, str(SCRIPTS / 'check_catalog_integrity.py'), str(REPO)], quiet))
    record_paths = [str(STATE / rel) for rel in RECORD_DIRS if (STATE / rel).exists()]
    # runs/ mixes maintenance-run records (MNT-*) with free-form migration/research run notes; validate the schema-bound ones
    record_paths.extend(str(p) for p in sorted((STATE / 'runs').glob('MNT-*.json')))
    results.append(run('validate_records (all state records)', [sys.executable, str(SCRIPTS / 'validate_records.py'), *record_paths], True))
    results.append(run('check_public_boundary', [sys.executable, str(REPO / 'scripts' / 'check_public_boundary.py')], quiet))
    results.append(run('maintenance_plan dry-run', [sys.executable, str(SCRIPTS / 'maintenance_plan.py'), str(REPO)], True))
    ok = all(results)
    print('ALL CHECKS PASSED' if ok else 'CHECKS FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
