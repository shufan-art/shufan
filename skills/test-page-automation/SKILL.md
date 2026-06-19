---
name: test-page-automation
description: Create and maintain viral-style Chinese H5 personality/self-discovery test pages for WeChat/Xiaohongshu monetization funnels. Use when the user asks to generate tests from titles, expand topics into 30-question tests, fix repeated options, preserve old links, prepare GitHub Pages output, diagnose publishing failures, or automate the existing 通用测试壳 workflow.
---

# Test Page Automation

## Core Workflow

Use this skill to run the user's existing `通用测试壳` system as a repeatable production line:

1. Understand the requested topic set: one title, multiple titles, or a markdown question bank.
2. Generate each test as an independent page with a stable slug; never overwrite older tests unless the user explicitly asks.
3. Ensure every test has at least 30 questions when the user requests batch/viral tests.
4. Ensure options are not identical across all questions. Options must vary by question shape:
   - “A 还是 B” questions should offer the two sides plus mixed/unclear choices.
   - “会不会/有没有/能不能/是否” questions should offer frequency/state choices tied to that question.
   - “哪种/什么/哪里/哪类” questions should offer four theme-relevant directions.
5. Run the publishing preparation step, copy `site/` to the repo root, and validate local files.
6. Commit local changes. Only push to GitHub when network and credentials allow it.
7. If publishing fails, diagnose credentials, network, permission, or branch divergence before changing page content.

## Project Defaults

Default project path:

`/Users/astars/Library/Mobile Documents/com~apple~CloudDocs/obsidian/第一个仓库/通用测试壳`

Default GitHub Pages base URL:

`https://shufan-art.github.io/shufan/`

Preferred output paths:

- Local generated pages: `output/<slug>/`
- Publish staging: `site/tests/<slug>/`
- GitHub Pages root copy: `tests/<slug>/`

Preferred style:

- Female-facing emotional tests: soft pink/cream, rounded cards, gentle copy, no black-white grid.
- Career/money/life direction tests: neutral cream, gray-green, restrained cards.
- Avoid dark grid-heavy reference visuals unless the user explicitly asks.

Read `references/xiong-test-pages.md` when you need the detailed content, visual, and publishing rules.

## Automation Script

Use `scripts/run_pipeline.py` for the common workflow:

```bash
python3 <skill-dir>/scripts/run_pipeline.py --project "/absolute/path/to/通用测试壳" --mode prepare
```

Modes:

- `prepare`: generate existing batch tests, build `site/`, copy to root, validate.
- `diagnose`: run checks for generated pages, Git status, remote, and GitHub credential presence.
- `links`: print expected GitHub Pages links for the known 10-test batch.

The script is a helper, not a replacement for judgment. If the user gives new titles, update or create the project generator/config first, then run `prepare`.

## Publishing Rules

If push fails:

- `Authentication failed`: tell the user to run `首次GitHub授权.command`.
- `Could not resolve host`: network cannot reach GitHub.
- `403`, `Permission`, or `Repository not found`: token permission/account/repo is wrong.
- `ahead/behind`, non-fast-forward, or branch divergence: for this static-site repo, prefer preserving the local final site and using the diagnostic publisher or `--force` only when the user understands it overwrites the remote static output.

Do not tell the user the page is broken when the generated local tests pass validation. Separate content generation issues from publishing issues.

## Validation Checklist

Before final response:

- Confirm every requested test exists in `tests/<slug>/index.html`.
- Confirm every requested test has `test_config.json`.
- Confirm each requested test has the required question count.
- Check the first two questions do not have identical options.
- Provide the final links and say whether they are already pushed or still need the user to run publishing.
