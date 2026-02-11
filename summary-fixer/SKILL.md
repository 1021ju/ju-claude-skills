---
name: summary-fixer
description: Fix and improve summary fields in blog index.md files. Use when user wants to batch review/fix summaries, when summaries are too long, when summaries repeat H1 content, or when user says "fix summary" or "改summary". Triggers on index.md files with frontmatter containing summary field.
---

# Summary Fixer

Fix `summary` field in blog `index.md` frontmatter to be concise and complement the H1 title.

## Workflow

1. Read the target `index.md` file
2. Extract `title` (H1) and `summary` from frontmatter
3. Analyze issues and rewrite summary
4. Show before/after comparison, ask user to confirm
5. Apply edit if approved

## Summary Rules

**Length:** 60-80 characters MAX. Shorter is better.

**Format:**
- Short phrase or fragment, NOT a full sentence
- Always end with a period

**Forbidden patterns:**
- Starting with "This paper...", "The authors...", "本文...", "作者..."
- Starting with dash/hyphen "— ..."
- Repeating Hero Entity name already in H1
- Repeating the key metric/number already in H1
- Generic filler phrases

**Complement H1:**
- H1 = result/finding → Summary = method/how
- H1 = question → Summary = teaser hint
- H1 = metric → Summary = implication/"so what"
- H1 = what → Summary = why it matters

## Examples

**Good:**
```
H1: "Why 99% of MD Simulations Waste Compute"
Summary: "A conformal prediction fix for uncertainty."

H1: "AlphaFold Meets Active Learning"
Summary: "10x fewer DFT calculations, same accuracy."

H1: "当大模型学会读懂晶体结构"
Summary: "无需人工特征，直接从CIF预测材料性质。"
```

**Bad (too long):**
```
❌ "This paper introduces a novel approach combining conformal prediction with molecular dynamics"
❌ "本文提出了一种结合主动学习和密度泛函理论的新方法来加速材料筛选"
```

**Bad (repeats H1):**
```
H1: "AlphaFold Meets Active Learning"
❌ "AlphaFold combined with active learning achieves SOTA"
```

**Bad (dash opener):**
```
❌ "— A new framework for uncertainty quantification"
❌ "— 一种新的不确定性量化框架"
```

**Bad (full sentence with filler):**
```
❌ "Researchers propose an innovative method that significantly improves..."
❌ "研究人员提出了一种创新方法，显著提升了..."
```

## Output Format

Show diff-style comparison:
```
📝 Summary Fix

H1: [current h1 title]

Before: [old summary] (XX chars)
After:  [new summary] (XX chars)

Changes: [brief explanation]

Apply this change? (y/n)
```
