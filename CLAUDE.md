# AI agent instructions

This repository stores instructions for AI agents on four platforms. The user publishes each file by hand, pasting it into a settings field or uploading a skill package. The only code is the Python scripts inside skills.

| Folder | Platform | Published to | Rules |
| --- | --- | --- | --- |
| `Claude Code/` | Claude Code | `~/.claude/CLAUDE.md`, as a manual copy | `.claude/rules/claude-code.md` |
| `Claude Web/` | claude.ai, web and desktop | Profile preferences | `.claude/rules/claude-web.md` |
| `Copilot 365/` | Microsoft 365 Copilot Agent Builder | Agent fields and skill packages | `.claude/rules/copilot-365.md` |
| `Gemini/` | Gemini app | Gems (legacy), then skills | `.claude/rules/gemini.md` |

A folder's rules file loads when you read a file in that folder. Before creating a file in a folder you have not read from, read its rules file.

## Conventions

- Language: agent content in Brazilian Portuguese. `CLAUDE.md` and `.claude/rules/` in English. Commit messages in English, imperative mood.
- Versions: `<Name>.md` is V1; later versions sit beside it as `<Name> V2.md`, `<Name> V3.md`. The highest number is the published version: edit that file, and create the next number only when the user asks. Skills are the exception: one folder per skill, edited in place, history in git.
- `CLAUDE.md` and `CLAUDE.local.md` as exact file names belong to this root only: Claude Code loads any file with those names as instructions for this repository. Templates carry a qualifier, as in `CLAUDE EN-US.md`.
- Models: name the family (Opus), never a version number. Versions change faster than these files.
- The repository is public on GitHub: keep employer names, tenant details and credentials out of every file.
- Skill packages: build them into `dist/`, which git ignores.

## Platform facts

The rules files record limits and capabilities with the source URL and the date read. Platforms change them without notice, and several features are in preview. Re-open the source before a limit decides something, and whenever a draft comes within 5% of a limit. When a fact changes, update the rules file and its date in the same edit.
