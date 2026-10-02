---
paths:
  - "Copilot 365/**"
---

# Copilot 365

Agents built in Microsoft 365 Copilot Agent Builder. The user creates each agent by hand: pastes name, description and instructions into the Configure tab, and uploads each skill as a `.zip` package.

## Layout

```text
Copilot 365/<Agent>/
  <Agent>.md, <Agent> V2.md, ...   instructions (versions: root CLAUDE.md)
  <Agent> - Descrição.txt          description: one file, edited in place
  skills/<skill-name>/             SKILL.md, scripts/, resource files
```

`<Agent>` is the agent's exact name in Agent Builder. `Teste de Skills/` is a test agent (see Diagnostic).

## Plan

The user's tenant has Microsoft 365 Copilot Chat without a Copilot license and without pay-as-you-go billing. Capabilities per [prerequisites](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/prerequisites), read 2026-10-01:

- Available to agents: custom instructions, web search, scoped web search, code interpreter (toggle "Create documents, charts, and code"), image generator (toggle "Create images").
- Unavailable: SharePoint, OneDrive, embedded files, Copilot connectors, Dataverse, email, people, Teams messages and meetings. Instructions rely on the available list only; naming an unavailable source makes the agent claim access it lacks.
- Skills appear in Agent Builder since 2026-10-01, although Microsoft lists a Copilot license or pay-as-you-go, plus the Frontier Program, as prerequisites. Unresolved: when an upload or run fails, suspect licensing first.

## Agent fields

Read 2026-10-01 from [Build agents](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-build-agents):

- Name: 30 characters. Description: 1,000. Instructions: 8,000.
- The description helps the model pick the agent and is shown to users.
- Microsoft does not document whether a line break counts as 1 or 2 characters, and agent files here use CRLF. A draft fits only when both counts fit:

  ```bash
  python3 -c 'import sys; t = open(sys.argv[1], encoding="utf-8", newline="").read().replace("\r\n", "\n"); print("LF:", len(t), "CRLF:", len(t) + t.count("\n"))' "<file>"
  ```

## Writing instructions

From [Write effective instructions](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-instructions), read 2026-10-01:

- Components: purpose, general guidelines, skills. State what the agent does, with precise verbs.
- Refer to each skill by name at a high level; its steps live in its `SKILL.md`.
- Past 8,000 characters, move detail into skills. Knowledge files never carry instructions: Microsoft treats their content as untrusted and may block or truncate directive text (XPIA classifiers).

## Skills

Read 2026-10-01 from [Add skills in Agent Builder](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills) and [Custom skills](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-skills):

- `SKILL.md` holds `name` and `description` in YAML front matter; its instructions stay under 20,000 characters.
- Per agent: up to 8 skills. Per `.zip`: 50 MB, 25 MB per file. 350 files across all skills. Directory depth 3.
- Supported files: .json, .xml, .yaml, .yml, .ini, .config, .utf8, .docx, .doc, .docm, .pdf, .txt, .rtf, .md, .ppt, .pptx, .ppsm, .xlsx, .xls, .xlsm, .csv, .tsv, .html, .htm, .png, .jpg, .jpeg, .gif, .bmp, .log. Scripts: .py, .js, .mjs, .cjs, .ts, .mts, .sh, .bash.
- Preview limits: a skill can't be shared across agents, and an agent can't combine skills with embedded files.
- Script sandbox: no network, no package installation, only packages already present. Microsoft: "Don't depend on a package unless its availability is confirmed."

Conventions:

- Folder name equals `name`: lowercase, hyphens, starting with a verb (`formatar-changelog`).
- `description`: third person; what the skill does, then "Use quando…" with concrete situations; up to 1,024 characters (Gemini's limit; Microsoft documents none).
- Scripts use only the Python standard library until the diagnostic lists the sandbox packages. Run each script locally with `python3` before packaging.
- Package with `SKILL.md` at the archive root, as Microsoft documents (untested, see Diagnostic):

  ```bash
  python3 -c 'import os, shutil, sys; d = sys.argv[1].rstrip("/"); print(shutil.make_archive("dist/" + os.path.basename(d), "zip", root_dir=d))' "Copilot 365/<Agent>/skills/<skill-name>"
  ```

## Line endings

`.gitattributes` gives agent files (instructions, descriptions) CRLF in the working tree and everything under `skills/` LF. Git converts only on checkout, so a file you create keeps the endings you wrote. Convert each new agent file:

```bash
python3 -c 'import pathlib, sys; p = pathlib.Path(sys.argv[1]); p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))' "<file>"
```

Check with `git ls-files --eol -- "Copilot 365"`: agent files show `w/crlf`, skill files `w/lf`.

## Diagnostic

`Teste de Skills/skills/diagnosticar-sandbox/` prints the sandbox's Python version, OS, extracted skill files and installed packages. The user uploads `dist/diagnosticar-sandbox.zip` (`SKILL.md` at the root) and, if that fails, `dist/diagnosticar-sandbox-com-pasta.zip` (skill folder inside). Build the second with `root_dir` set to the skill's parent folder and `base_dir` to the skill's name.

Results: not tested yet. When the user reports them, record here with the date: which layout uploaded, Python version, OS, packages that matter, and whether the script ran. Then update the packaging and script rules above.
