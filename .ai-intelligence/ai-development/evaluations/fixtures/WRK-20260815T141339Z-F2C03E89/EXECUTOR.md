# Executor brief — maintain-agent-instructions audit trial (read-only)

You execute the `maintain-agent-instructions` Skill once against a small fixture repository and return your audit findings. This is an evaluation trial: do NOT modify any file anywhere, do NOT delegate to other agents, do NOT ask questions.

Inputs (all paths are given in your task message):
- SKILL.md of the Skill (read it and follow its 監査手順; the `inventory.mjs` script may be run read-only with `node <script> <repo-root>`; if it errors, note it and continue).
- The 監査基準 file to use for this trial (an "audit criteria variant" path). Treat it as the Skill's `references/audit-criteria.md`, i.e. the authoritative classification criteria for this trial. Do not read any other audit-criteria file.
- The fixture repository root (read all its files; it is tiny).

Perform the audit as the Skill instructs (steps 1-6 and 10; skip edits in step 8, run nothing that writes). Then return ONLY a JSON object:
{
  "findings": [
    {"file": "AGENTS.md", "rule": "<quoted or paraphrased existing rule, or 'MISSING: <what is missing>'>",
     "classification": "維持|圧縮|移動|更新|統合|削除|追加|保留",
     "proposal": "<the concrete 1-2 line wording you would add/change/remove, or null>",
     "evidence": "<which evidence in the repo/criteria supports it>"}
  ],
  "summary": "<3 lines>"
}
Include every rule you would keep or change and every gap you would report. Be honest: if the criteria do not tell you to report something, do not report it.
