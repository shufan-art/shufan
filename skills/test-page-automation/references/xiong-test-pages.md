# 熊测试页自动化参考

## Business Pattern

The account model is a static H5 test funnel:

- Use viral emotional/career/money titles to attract readers.
- Use 30-question self-discovery tests to create completion and sharing desire.
- Use result pages as the emotional payoff.
- Later add low-priced paid links, report upsells, or comment/private-message funnels.

The content product is the test itself. Keep each page lightweight, static, and cheap to reproduce.

## Content Standards

Each viral test should include:

- A curiosity title with “你/测一测/到底/哪种/适合/第几级/真正”.
- A short opening that names a common anxiety or desire.
- Four dimensions displayed near the start.
- At least 30 questions for batch viral tests.
- Four result types A/B/C/D with emotionally useful summaries.
- A screenshot-friendly share sentence.

Avoid:

- Identical options on every question.
- Overly clinical wording.
- Making medical, psychological, legal, or financial claims.
- Copying competitor wording verbatim.

## Visual Standards

Female-facing romance/emotion tests:

- Use soft cream, blush pink, rose, warm white.
- Use gentle rounded panels, readable spacing, emotional copy.
- Avoid black-white grid and heavy masculine layouts.

Career/money/life-direction tests:

- Use neutral cream, sage gray-green, soft charcoal.
- Keep the page restrained and credible.
- Emphasize clarity, choices, direction, and low-pressure decision-making.

## Stable Slug Rules

Use stable English slugs, not raw Chinese folder names, for public links:

- `hard-or-change`
- `be-controlled`
- `sensitive-type`
- `hot-or-steady-love`
- `money-talent`
- `life-script`
- `wrong-person`
- `strong-or-growth-love`
- `like-signals`
- `love-clarity`

Preserve old slugs unless the user explicitly asks to replace them.

## Local Publishing Flow

From the project root `通用测试壳`:

1. Run the generator, such as `python3 generate_10_hot_tests.py`.
2. Run `python3 publish_to_github_pages.py`.
3. Copy `site/.` to the repo root.
4. Validate `tests/<slug>/test_config.json`.
5. Commit changes.
6. Push only if credentials/network allow.

If the user wants one-click publishing, maintain:

- `首次GitHub授权.command`
- `一键发布.command`
- `发布诊断.command`

The diagnostic command should show actionable failure reasons without exposing tokens.
