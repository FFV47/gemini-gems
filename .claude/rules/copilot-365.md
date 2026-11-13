---
paths:
  - "Copilot 365/**"
---

# Copilot 365

Agents built in Microsoft 365 Copilot Agent Builder. The user creates each agent by hand: pastes name, description and instructions into the Configure tab, and uploads each skill as a `.zip` package. Microsoft now calls the product Microsoft Copilot Chat; its docs use both names.

## Layout

```text
Copilot 365/<Agent>/
  INSTRUCOES.md, INSTRUCOES V2.md, ...   instructions (versions: root CLAUDE.md)
  <skill-name>/   SKILL.md, scripts/, resource files
```

`<Agent>` is the agent's exact name in Agent Builder.

## Plan

The user's tenant has Microsoft 365 Copilot Chat without a Copilot license and without pay-as-you-go billing. Capabilities per [prerequisites](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/prerequisites), read 2026-10-01:

- Available to agents: custom instructions, web search, scoped web search, code interpreter (toggle "Create documents, charts, and code"), image generator (toggle "Create images").
- Unavailable: SharePoint, OneDrive, embedded files, Copilot connectors, Dataverse, email, people, Teams messages and meetings. Instructions rely on the available list only; naming an unavailable source makes the agent claim access it lacks.
- Skills appear in Agent Builder since 2026-10-01, although [Add skills in Agent Builder](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills) lists a Copilot license or pay-as-you-go as the prerequisite (read 2026-11-10; neither that page nor prerequisites mentions the Frontier Program any more). Unresolved: when an upload or run fails, suspect licensing first.

## Web search

Read 2026-10-01 from [Add knowledge in Agent Builder](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge), [Knowledge sources](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/knowledge-sources) and [Web search data and privacy](https://learn.microsoft.com/en-us/microsoft-365/copilot/manage-public-web-access):

- The "Search all websites" toggle (Knowledge section) lets the agent use any web data. Scoped search takes up to four public URLs, at most two path levels deep, without query parameters.
- Agents ground on Bing's index rather than live pages; content that loads dynamically can be missing or stale.
- Copilot sends Bing a query of a few words derived from the prompt; the whole prompt goes only when it is very short.
- "Only use specified sources" makes the agent prefer the configured sources for lookups and answer with a fallback message when they hold nothing; general knowledge still answers simple questions. Agent Builder can't block general knowledge.
- When an admin disables web search, agents with it enabled report no error and answer without the web.

## Code interpreter

Read 2026-10-01 from [Code interpreter](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/code-interpreter) and [Build agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-build-agents):

- The sources disagree on the switch. Code interpreter says the capability is always enabled in Agent Builder; Build agents describes the toggle "Create documents, charts, and code". The user saw the toggle in Agent Builder on 2026-10-01.
- Files it generates stay available for download only during the active session.
- Users can upload Word, Excel, PowerPoint, PDF, CSV/TSV and TXT/UTF8 files for analysis.

## Agent fields

Read 2026-10-01 from [Build agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-build-agents):

- Name: 30 characters. Description: 1,000. Instructions: 8,000.
- The description helps the model pick the agent and is shown to users.
- `INSTRUCOES.md` opens with YAML front matter holding `name` and `description`. The user pastes those into the Name and Description fields and pastes only the body into Instructions, so the 8,000 limit applies to the body.
- Microsoft does not document whether a line break counts as 1 or 2 characters, and agent files here use CRLF. A draft fits only when both counts fit. The command drops the front matter and counts the body:

  ```bash
  python3 -c 'import re, sys; t = open(sys.argv[1], encoding="utf-8", newline="").read().replace("\r\n", "\n"); t = re.sub(r"\A---\n.*?\n---\n+", "", t, flags=re.S); print("LF:", len(t), "CRLF:", len(t) + t.count("\n"))' "<file>"
  ```

## Writing instructions

From [Write effective instructions](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions), read 2026-10-01:

- Components: purpose, general guidelines, skills. State what the agent does, with precise verbs.
- Refer to each skill by name at a high level; its steps live in its `SKILL.md`.
- For a skill the agent must always run, order its invocation by name (`invoque sempre a skill X`), as Senior VBA does with `planejar-codigo`. The user reported on 2026-11-12 that Agent Builder says an explicit order by name makes Copilot call the skill regardless of its own judgment; the Microsoft pages read 2026-11-11 don't document it.
- Past 8,000 characters, move detail into skills. Knowledge files never carry instructions: Microsoft treats their content as untrusted and may block or truncate directive text (XPIA classifiers).

## Skills

Read 2026-10-01 from [Add skills in Agent Builder](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills) and [Custom skills](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills):

- `SKILL.md` holds `name` and `description` in YAML front matter; its instructions stay under 20,000 characters.
- Per agent: up to 8 skills. Per `.zip`: 50 MB, 25 MB per file. 350 files across all skills. Directory depth 3.
- Supported files: .json, .xml, .yaml, .yml, .ini, .config, .utf8, .docx, .doc, .docm, .pdf, .txt, .rtf, .md, .ppt, .pptx, .ppsm, .xlsx, .xls, .xlsm, .csv, .tsv, .html, .htm, .png, .jpg, .jpeg, .gif, .bmp, .log. Scripts: .py, .js, .mjs, .cjs, .ts, .mts, .sh, .bash.
- Preview limits: a skill can't be shared across agents, and an agent can't combine skills with embedded files.
- Script sandbox: no network, no package installation, only packages already present. Microsoft: "Don't depend on a package unless its availability is confirmed."

Conventions:

- Folder name equals `name`: lowercase, hyphens.
- `description`: third person; what the skill does, then "Use quando…" with concrete situations; up to 1,024 characters (Gemini's limit; Microsoft documents none).
- Body: the sections Agent Builder generates, in this order: `## Purpose`, `## Uses`, `## Instructions` (numbered steps), `## Parameters`, `## Output`. Headings in English, content in Portuguese. `Uses` names the agent capabilities the skill needs, as in `- Agent capabilities: codeInterpreter`. Source: `Doc VBA/doc-vba/SKILL.md`, which the user generated in Agent Builder (reported 2026-11-10), for the first four; the user reported on 2026-11-12 that Agent Builder adds `## Output` to every skill it generates, although `doc-vba` came without it (its `## Output` was written by hand on 2026-11-12). Microsoft documents only the front matter, and `codeInterpreter` is the only capability identifier seen so far: use no other until a generated skill shows it.

## Line endings

`.gitattributes` gives every file under `Copilot 365/` (instructions, `SKILL.md`, resource files) CRLF in the working tree and everything under a skill's `scripts/` LF, because scripts run in a Linux sandbox. Git converts only on checkout, so a file you create keeps the endings you wrote. Convert each new instructions file and `SKILL.md`:

```bash
python3 -c 'import pathlib, sys; p = pathlib.Path(sys.argv[1]); p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))' "<file>"
```

Check with `git ls-files --eol -- "Copilot 365"`: instructions and `SKILL.md` show `w/crlf`, scripts `w/lf`.
