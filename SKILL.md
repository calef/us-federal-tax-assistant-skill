---
name: us-federal-tax-assistant
description: "Use this skill when helping users prepare US federal tax returns. Triggers include: any mention of 'tax return', '1040', 'tax filing', 'IRS forms', W-2, 1099, or requests to help with taxes. Use for analyzing tax documents, identifying required forms, filling out tax form PDFs, creating document checklists from prior year returns, and auditing completed returns. Do NOT use for tax advice, tax planning, or state tax returns (which vary significantly by jurisdiction)."
---

# US Federal Tax Return Preparation

## Overview

This skill helps users prepare US federal individual income tax returns by analyzing source documents, identifying required forms, filling out IRS form PDFs, and auditing completed returns for errors.

## Workflow

### Phase 1: Document Collection Planning

When the user provides a prior year tax return:

1. Analyze the return to identify all income sources, deductions, and credits claimed
2. Generate a comprehensive checklist of expected tax documents for the current year
3. Organize the checklist by institution and expected availability date (most 1099s arrive late January to mid-February)

Example checklist categories:
- W-2s (employers)
- 1099-R (retirement distributions)
- 1099-DIV (dividends)
- 1099-INT (interest)
- 1099-B (brokerage transactions)
- 1099-SA (HSA distributions)
- 5498-SA (HSA contributions)
- 1098 (mortgage interest)
- 1095-A/B/C (health coverage)

### Phase 2: Form Identification

Once source documents are collected:

1. Analyze all source documents to determine which IRS forms are required
2. Provide the user with a list of forms and direct links to download current versions from irs.gov
3. **CRITICAL**: Request that the user upload the current year blank forms. Do not rely on training data for form layouts—the IRS updates forms annually and line numbers change.

Common forms and their purposes:
| Form | Purpose |
|------|---------|
| 1040 | Main individual return |
| Schedule 1 | Additional income and adjustments (HSA deduction, etc.) |
| Schedule 2 | Additional taxes |
| Schedule 3 | Additional credits (foreign tax credit, etc.) |
| Schedule A | Itemized deductions |
| Schedule B | Interest and dividends over $1,500 |
| Schedule D | Capital gains and losses |
| Form 8949 | Sales of capital assets |
| Form 8889 | HSA contributions and distributions |
| Form 8995 | Qualified business income (Section 199A) deduction |
| Form 1116 | Foreign tax credit |
| Schedule 8812 | Child tax credit |

### Phase 3: Form Completion

With source documents and blank forms uploaded:

1. Extract values from source documents systematically
2. Map values to appropriate form lines
3. Complete calculations per IRS instructions
4. Fill out the PDF forms directly
5. **Self-validate**: After completing each form, verify totals against source documents before proceeding

Key validation checks:
- Total withholding across all 1099-Rs matches sum of individual Box 4 values
- Interest income on Schedule B matches sum of all 1099-INT Box 1 values
- Dividend income matches 1099-DIV totals
- Foreign tax paid matches 1099-DIV Box 7 totals
- HSA distribution on Form 8889 matches 1099-SA Box 1

### Phase 4: Audit

Before finalizing:

1. **Visual verification**: Compare source document images against entered values—do not rely solely on extracted text
2. Verify all cross-form references (e.g., Schedule D total flows to 1040 Line 7)
3. Check that worksheets (Qualified Dividends, Credit Limit, etc.) are completed correctly
4. Validate withholding totals match across all forms

Common error categories to check:
- **Misread source documents**: Confusing similar boxes (e.g., federal withholding vs. Social Security tax on W-2)
- **Incomplete worksheets**: Supporting calculations that don't auto-populate
- **Rounding mismatches**: When systems round before summing vs. after
- **Outdated form knowledge**: Line numbers that changed from prior year

## Form-Specific Guidance

### W-2 (Wage and Tax Statement)
- Box 1: Wages (1040 Line 1a)
- Box 2: Federal income tax withheld (1040 Line 25a)
- Box 4: Social Security tax withheld (NOT federal income tax—common confusion point)
- Box 12 codes: Watch for Code W (HSA employer contributions), Code DD (health coverage cost)

### 1099-R (Retirement Distributions)
- Box 1: Gross distribution
- Box 2a: Taxable amount
- Box 4: Federal income tax withheld
- Box 7: Distribution code
  - Code 4: Death distribution (beneficiary IRA)
  - Code 7: Normal distribution
  - Code G: Direct rollover (not taxable)
  - Code 2: Early distribution, exception applies

### 1099-DIV (Dividends)
- Box 1a: Total ordinary dividends
- Box 1b: Qualified dividends (taxed at capital gains rates)
- Box 5: Section 199A dividends (REIT dividends eligible for QBI deduction)
- Box 7: Foreign tax paid
- Box 12: Exempt-interest dividends (not taxable but may affect other calculations)

### Schedule D and Form 8949
- Capital loss carryforwards from prior year must be tracked
- Net capital loss deduction limited to $3,000 per year
- Remaining losses carry forward indefinitely

### Form 8889 (HSA)
- Line 2: Personal contributions only (not employer)
- Contribution limits vary by coverage type (self-only vs. family) and age (catch-up contributions)
- 5498-SA Box 2 shows total contributions; may include employer amounts not deductible by taxpayer

## Output

The final deliverable should be:
1. Completed PDF forms ready for printing and mailing
2. A summary showing key figures (total income, AGI, taxable income, total tax, total payments, refund/amount due)
3. Any items requiring taxpayer attention or decision

## Form Location

If this skill was installed as a full directory (not just the SKILL.md), current year blank forms are available locally. Check the following path before asking the user to upload or download forms:

```
~/.claude/skills/us-federal-tax-assistant/forms/<year>/
```

For example, to find the 2025 Form 1040: `~/.claude/skills/us-federal-tax-assistant/forms/2025/f1040.pdf`

Forms are organized by their IRS revision year. Most forms needed to prepare a 2025 tax return are in `forms/2025/` (314 forms), with some in `forms/2024/` (81 forms) or `forms/2026/` (25 forms, including current W-2 and W-4).

Over 700 IRS forms are present when installed, including:
- **Form 1040** and all Schedules (1, 2, 3, A, B, C, D, E, F, H, J, SE, 8812)
- **Form 1041** (fiduciary) and all schedules
- **Form 1065** (partnership) and all schedules
- **Form 1120/1120-S** (corporate) and variants
- **All 1099 series** (B, C, DIV, G, INT, K, MISC, NEC, OID, Q, R, S, SA, etc.)
- **All 1098 series** (mortgage interest, student loan, tuition, etc.)
- **Form 1095-A/B/C** (health coverage)
- **W-2, W-3, W-4, W-7, W-9** and variants
- **All 8xxx forms** (8949, 8889, 8995, 8812, 8962, 8606, 8829, etc.)
- **Form 706** (estate tax) and all schedules
- **Form 709** (gift tax)
- **Forms 940–945** (employment taxes)
- **Forms 2106, 2210, 2441, 2555, 3520, 4562, 4684, 4797, 4868, 5329, 5498, 5695, 6251, 7004** and many more

Files are named using IRS conventions (e.g., `f1040.pdf`, `f1040s1.pdf` for Schedule 1, `fw2.pdf` for W-2).

If forms are not present, ask the user to run `python3 scripts/download-forms.py` from the skill directory, or download forms manually from irs.gov.

## Important Limitations

- **Not tax advice**: This skill helps with form preparation, not tax planning or strategy
- **Federal only**: State returns vary significantly and are not covered
- **Form currency**: Always request current year forms from the user; do not assume training data reflects current form layouts
- **IRS website access**: The IRS blocks automated access to irs.gov; provide links for the user to download forms manually
