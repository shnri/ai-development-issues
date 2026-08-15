# Executor brief — optimize-skill planning trial (read-only)

You act as the `skill-optimizer` about to run the `optimize-skill` Skill for ONE scenario. Do NOT modify any file, do NOT delegate, do NOT ask questions, do NOT run any command. Use ONLY the Skill variant directory given in your task (its SKILL.md and references/*.md are the authoritative method for this trial; do not read any other copy of this Skill) plus the scenario JSON.

Return ONLY JSON:
{
  "record": ["each configuration fact you record for the run/baseline (be specific: field names and what they capture)"],
  "runs": ["each run/experiment you execute, in order, with what is held equal between compared runs"],
  "attribution": "how you separate model/harness change, Skill change, and eval/fixture drift",
  "decision_rule": "when the Skill gets a variant, when it does not",
  "notes": "<2-3 lines>"
}
