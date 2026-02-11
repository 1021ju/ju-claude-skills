---
name: editor-name
description: Add editor_name field to blog index.md frontmatter. Use when user wants to add editor name, or says "加编辑", "add editor". Triggers on index.md files needing editor attribution.
---

# Editor Name

Add `editor_name` field to blog `index.md` frontmatter.

## Workflow

1. Read the target `index.md` file
2. Check if `editor_name` already exists
3. If not exists, ask user which editor to use
4. Add `editor_name` field after `date` line in frontmatter
5. Show before/after comparison, ask user to confirm
6. Apply edit if approved

## Available Editors

- **Laurence Hu**
- **June Chen**

## Format

```yaml
editor_name: "Laurence Hu"  # 编辑
```

or

```yaml
editor_name: "June Chen"  # 编辑
```

## Placement

Insert after the `date` field, before `content_type`:

```yaml
date: 2026-02-03  # 开发填充

editor_name: "Laurence Hu"  # 编辑

# 内容分类
content_type: "research_note"
```

## Output Format

If editor_name already exists:
```
⚠️ editor_name already exists: "[current value]"
Do you want to change it? (y/n)
```

If adding new:
```
📝 Add Editor Name

File: [filename]

Which editor?
1. Laurence Hu
2. June Chen

[After user selects]

Adding:
editor_name: "[selected name]"  # 编辑

Apply this change? (y/n)
```
