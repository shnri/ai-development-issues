# Executor brief — mitigate-model-behavior-issues planning trial (read-only)

You execute the planning part of the `mitigate-model-behavior-issues` Skill for ONE issue scenario against a tiny fixture project. Do NOT modify any file, do NOT delegate, do NOT ask questions, do NOT run network searches (use only the Skill, the playbook variant, and the scenario's evidence).

Inputs (paths in your task message):
- SKILL.md of the Skill — follow steps 1 (exposure), 2 (layer), 3 (mitigations: for this offline trial the "current primary guidance" is whatever the playbook variant states plus the scenario evidence), and 6 (choose the smallest mitigation). Skip 4-5, 7-9.
- The playbook variant path: treat it as `references/mitigation-playbook.md`. Do not read any other playbook file.
- The scenario JSON (issue record + task).
- The fixture project root (tiny; includes a fingerprint file describing model/surface/effort).

Return ONLY JSON:
{
  "exposure": "direct|possible|not-applicable|provider-controlled",
  "layer": ["..."],
  "mechanisms": ["each concrete mitigation mechanism you would apply or evaluate, one per item, in the order of preference"],
  "proposed_change": {"file": "...", "text": "<the exact instruction/config text you would add or change, or null>"},
  "eval": {"failure_metric": "...", "adjacent_metric": "..."},
  "notes": "<2-3 lines>"
}
