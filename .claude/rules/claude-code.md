---
paths:
  - "Claude Code/**"
---

# Claude Code

Templates for CLAUDE.md files. Each name carries a qualifier (`CLAUDE EN-US.md`), which keeps Claude Code from loading it as instructions for this repository.

- `CLAUDE EN-US.md` is the source of the user's `~/.claude/CLAUDE.md`, a plain copy. After editing it, ask the user before copying it there.
- `CLAUDE EN-US.md` and `CLAUDE PT-BR.md` are translations of each other: mirror every change in the other file, in the same commit.
- `Karpathy CLAUDE.md` is a verbatim copy of [forrestchang/andrej-karpathy-skills `CLAUDE.md`](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md). Update it only from upstream: download the raw file over this copy and confirm with `diff`.
