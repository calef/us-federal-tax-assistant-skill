# US Federal Tax Return Preparation Skill

A [Claude Code](https://claude.ai/claude-code) skill for preparing US federal individual income tax returns.

## What This Skill Does

This skill helps you:

- **Plan document collection** — Analyze a prior year return to generate a checklist of expected tax documents for the current year
- **Identify required forms** — Determine which IRS forms are needed based on your source documents
- **Complete form PDFs** — Fill out IRS form PDFs directly from your source documents with built-in validation
- **Audit completed returns** — Cross-check forms against source documents to catch common errors before filing

## What This Skill Does NOT Do

- Tax advice or tax planning
- State tax returns (vary significantly by jurisdiction)
- E-filing (output is completed PDFs for printing and mailing)

## Installation

Skills are markdown files placed in a `skills/` directory that Claude Code discovers automatically.

**Personal install** (available across all your projects):

```bash
git clone https://github.com/calef/us-federal-tax-assistant-skill.git \
  ~/.claude/skills/us-federal-tax-assistant
```

**Project install** (current project only):

```bash
git clone https://github.com/calef/us-federal-tax-assistant-skill.git \
  .claude/skills/us-federal-tax-assistant
```

IRS form PDFs are **not bundled** in the repo. Download them separately after cloning:

```bash
cd ~/.claude/skills/us-federal-tax-assistant

# Download forms for a specific year (fast, ~few dozen MB)
python3 download-forms.py 2025

# Download forms for multiple years
python3 download-forms.py 2024 2025 2026

# Download all ~700 forms
python3 download-forms.py
```

Forms download into a local `forms/<year>/` directory that is not committed to git. Requires Python 3 (stdlib only — no extra dependencies).

## Usage

Once installed, Claude will automatically apply this skill when you mention:

- "tax return" / "tax filing"
- "1040" or IRS form names
- W-2, 1099, and related document types
- Requests to help with taxes

### Typical Workflow

**Step 1 — Document checklist**
Upload last year's tax return and ask Claude to generate a document checklist for this year.

**Step 2 — Form identification**
Once you have your documents, upload them and ask Claude which IRS forms you'll need. Claude will provide direct links to download current blank forms from irs.gov.

**Step 3 — Form completion**
Upload the blank forms along with your source documents. Claude will fill them out, performing validation checks as it goes.

**Step 4 — Audit**
Ask Claude to audit the completed return, comparing source document values against what was entered.

### Important: Always Use Current Year Forms

IRS form layouts and line numbers change annually. When completing forms, always download fresh copies from [irs.gov](https://www.irs.gov/forms-instructions) and upload them — do not rely on cached copies.

## Supported Forms

| Form | Purpose |
|------|---------|
| 1040 | Main individual return |
| Schedule 1 | Additional income and adjustments |
| Schedule 2 | Additional taxes |
| Schedule 3 | Additional credits |
| Schedule A | Itemized deductions |
| Schedule B | Interest and dividends |
| Schedule D | Capital gains and losses |
| Form 8949 | Sales of capital assets |
| Form 8889 | HSA contributions and distributions |
| Form 8995 | Qualified business income deduction |
| Form 1116 | Foreign tax credit |
| Schedule 8812 | Child tax credit |

## License

GPL v3 — see [LICENSE.md](LICENSE.md)
