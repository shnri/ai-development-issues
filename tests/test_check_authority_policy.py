from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'scripts'))

from check_authority import reviewed_direct_delivery_errors  # noqa: E402


class ReviewedDirectDeliveryPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        state = REPO / '.ai-intelligence' / 'ai-development'
        cls.automation_policy = json.loads((state / 'automation-policy.json').read_text(encoding='utf-8'))
        cls.target_registry = json.loads((state / 'target-registry.json').read_text(encoding='utf-8'))

    def errors(self, automation_policy=None, target_registry=None, version='0.9.0') -> list[str]:
        return reviewed_direct_delivery_errors(
            copy.deepcopy(automation_policy or self.automation_policy),
            copy.deepcopy(target_registry or self.target_registry),
            version,
        )

    def test_current_reviewed_direct_policy_passes(self) -> None:
        self.assertEqual([], self.errors())

    def test_direct_delivery_requires_every_safety_invariant(self) -> None:
        mutations = [
            ('require_independent_review', False),
            ('release.allow_direct_push', False),
            ('release.allow_force_push', True),
            ('release.allow_branch_delete', True),
            ('release.allow_merge_bypass', True),
            ('release.require_clean_base', False),
            ('release.require_validation_commands', False),
        ]
        for dotted_key, value in mutations:
            with self.subTest(dotted_key=dotted_key):
                policy = copy.deepcopy(self.automation_policy)
                target = policy
                parts = dotted_key.split('.')
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = value
                self.assertTrue(self.errors(automation_policy=policy))

    def test_target_validation_protection_and_strategy_are_required(self) -> None:
        for field, value in [
            ('validation_commands', ['npm run check']),
            ('protected_paths', ['.git/**']),
            ('release.strategy', 'pull-request'),
            ('release.base_branch', 'release'),
        ]:
            with self.subTest(field=field):
                registry = copy.deepcopy(self.target_registry)
                shared = next(item for item in registry['targets'] if item['id'] == 'shared-agent-plugins')
                target = shared
                parts = field.split('.')
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = value
                self.assertTrue(self.errors(target_registry=registry))

    def test_compatible_plugin_is_required(self) -> None:
        self.assertTrue(self.errors(version='0.7.1'))
        self.assertEqual([], self.errors(version='0.8.0'))
        self.assertTrue(self.errors(version='not-semver'))


if __name__ == '__main__':
    unittest.main()
