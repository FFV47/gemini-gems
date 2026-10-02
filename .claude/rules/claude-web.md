---
paths:
  - "Claude Web/**"
---

# Claude Web

Instructions the user pastes into the claude.ai profile preferences ("Instruções para o Claude"), used on web and desktop. They apply to every conversation and stack with project instructions, so each protocol states when it applies.

- Target: Opus, whichever version is current. Plan: Pro.
- Web search is always on; instructions assume it is available.
- The folder holds profile preferences only. Rules for Projects or skills come with the first such file.
- Files: `<Name> - Claude.md`, then `<Name> V2 - Claude.md` and so on (versions: root CLAUDE.md).
- Prompting guidance: Anthropic's [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), the living reference with tuning for the latest models.
- What Claude already receives: the [claude.ai system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/overview) Anthropic publishes; read the page for the current Opus.
