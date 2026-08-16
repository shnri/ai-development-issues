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
    'decisions',
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

REQUIRED_VALIDATION_COMMANDS = {'npm ci', 'npm run check'}
REQUIRED_PROTECTED_PATHS = {'.git/**', '**/.env*', '**/*secret*', '**/*credential*'}
MINIMUM_DIRECT_DELIVERY_PLUGIN_VERSION = (0, 8, 0)


def parse_version(value: str) -> tuple[int, int, int] | None:
    parts = value.split('.')
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        return None
    return tuple(int(part) for part in parts)


def reviewed_direct_delivery_errors(
    automation_policy: dict,
    target_registry: dict,
    plugin_version: str,
) -> list[str]:
    errors = []
    release = automation_policy.get('release', {})
    shared_target = next(
        (target for target in target_registry.get('targets', []) if target.get('id') == 'shared-agent-plugins'),
        None,
    )
    if automation_policy.get('require_independent_review') is not True:
        errors.append('independent review must remain required')
    if release.get('allow_direct_push') is not True:
        errors.append('automation policy must explicitly allow direct push')
    if release.get('allow_force_push') is not False:
        errors.append('force push must remain disabled')
    if release.get('allow_branch_delete') is not False:
        errors.append('branch deletion must remain disabled')
    if release.get('allow_merge_bypass') is not False:
        errors.append('repository protection bypass must remain disabled')
    if release.get('require_clean_base') is not True:
        errors.append('clean base must remain required')
    if release.get('require_validation_commands') is not True:
        errors.append('validation commands must remain required')
    if not REQUIRED_PROTECTED_PATHS.issubset(set(automation_policy.get('protected_patterns', []))):
        errors.append('automation policy protected patterns are incomplete')
    if shared_target is None:
        errors.append('shared-agent-plugins target is missing')
    else:
        target_release = shared_target.get('release', {})
        if target_release.get('strategy') != 'direct':
            errors.append('shared target strategy must be direct')
        if target_release.get('base_branch') != 'main':
            errors.append('shared target direct base branch must be main')
        if not REQUIRED_VALIDATION_COMMANDS.issubset(set(shared_target.get('validation_commands', []))):
            errors.append('shared target validation commands are incomplete')
        if not REQUIRED_PROTECTED_PATHS.issubset(set(shared_target.get('protected_paths', []))):
            errors.append('shared target protected paths are incomplete')
    parsed_version = parse_version(plugin_version)
    if parsed_version is None or parsed_version < MINIMUM_DIRECT_DELIVERY_PLUGIN_VERSION:
        errors.append('pinned ai-development-improvement Plugin does not preserve reviewed direct delivery')
    return errors


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
    automation_policy = json.loads((STATE / 'automation-policy.json').read_text(encoding='utf-8'))
    target_registry = json.loads((STATE / 'target-registry.json').read_text(encoding='utf-8'))
    plugin_manifest = json.loads(
        (SKILL.parents[1] / 'plugin.json').read_text(encoding='utf-8')
    )
    direct_delivery_errors = reviewed_direct_delivery_errors(
        automation_policy,
        target_registry,
        plugin_manifest.get('version', ''),
    )
    reviewed_direct_ok = not direct_delivery_errors
    print(f'{"PASS" if reviewed_direct_ok else "FAIL"} shared target uses reviewed direct delivery')
    for error in direct_delivery_errors:
        print(f'    {error}')
    results.append(reviewed_direct_ok)
    results.append(run('authority policy regression tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'], True))
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
