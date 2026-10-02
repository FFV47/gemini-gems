---
paths:
  - "Gemini/**"
---

# Gemini

Instructions for the Gemini app on the user's personal Google account.

## Gems are legacy

Google replaces Gems with skills. Personal-account Gems convert automatically in November 2026; Google's help page gives the month, and press reports name November 17. The conversion keeps each Gem's name, description, instructions and supported files.

Until then, the existing files stay in Gem format and the user pastes edits into the matching Gem:

- `<Gem>.md`: instructions.
- `<Gem> - Descrição.txt`: description.

New Gemini work is a skill, in the layout under Migration.

## Migration

After the conversion:

1. The user downloads each converted skill as a `.zip` with `SKILL.md`.
2. Unpack it to `Gemini/<skill-name>/`, the folder named exactly like the skill, knowledge files beside `SKILL.md`.
3. Keep the names Google generated.
4. Rewrite each `description` to the format below. The four Concurseiro skills (Controle, Fiscal, Fiscal e Controle, Geral) overlap: give each description the situations that set it apart, so Gemini picks the right one.
5. Remove the Gem files in the same commit.

## Skills

Read 2026-10-01 from [Create & manage skills](https://support.google.com/gemini/answer/17094296), [Write effective skills](https://support.google.com/gemini/answer/17102773) and [Transition from Gems to skills](https://support.google.com/gemini/answer/18560919):

- Gemini reads only the name and the description to decide whether a skill fits a task.
- `name`: lowercase with hyphens, starting with a verb (Google's advice). The folder name equals the skill name.
- `description`: third person; what the skill does, then "Use quando…" with concrete situations; up to 1,024 characters.
- Upload a `SKILL.md`, or a folder or `.zip` with `SKILL.md` in its main folder. Uploaded files total up to 100 MB. Up to 100 skills active at once.
- Supported files: .txt, .md, .rst, .rtf, .tex, .log, .py, .sh, .json, .yaml, .csv, .toml, .xml, .env, .sql, .html, .css, .svg, Makefile, Dockerfile, .pdf, images. Unsupported: .docx, .doc, .xlsx. Scripts can't reach the internet.
- Requirements: 18 or older, personal account, Keep Activity on.
- Lost in the conversion: the Create video, Create music, Canvas, Deep research and Guided learning tools, and GitHub knowledge files.
