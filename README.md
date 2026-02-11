# ju-claude-skills

A collection of Claude Code skills for science content operations.

## Skills

| Skill | Description |
|-------|-------------|
| **sciencepedia** | Search and look up SciencePedia concept URLs from sitemap (~145k entries) |
| **x-news-post** | Draft X (Twitter) posts for science/tech news stories for the Bohrium News account |
| **paper-scout** | Discover and rank trending papers as candidates for Paper of the Day |
| **paper-post-prep** | Prepare Paper of the Day assets for LinkedIn + X posting |
| **author-finder** | Find researcher profiles on LinkedIn and X for @mentioning in posts |
| **blog-image-gen** | Generate cover and body images for blog `index.md` files |
| **editor-name** | Add `editor_name` field to blog `index.md` frontmatter |
| **summary-fixer** | Batch review and fix `summary` fields in blog `index.md` files |
| **skill-creator** | Best practices guide for creating new Claude Code skills |

## Installation

Copy the desired skill directory into `~/.claude/skills/`:

```bash
# Install a single skill
cp -r sciencepedia ~/.claude/skills/

# Install all skills
cp -r */ ~/.claude/skills/
```
