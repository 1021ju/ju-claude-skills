# ju-claude-skills

Ju 的 Claude Code Skills 合集 — 科学内容运营小助手 🧪

## Skills 列表

| Skill | 说明 |
|-------|------|
| **sciencepedia** | SciencePedia 词卡生成 — 从 Bohrium 知识库查找科学概念的 URL |
| **x-news-post** | 新闻采编 — 为 Bohrium News 账号撰写 X (Twitter) 科技新闻帖 |
| **paper-scout** | 论文发现 — 发现和筛选热门论文，为 Paper of the Day 推荐候选 |
| **paper-post-prep** | POTD 推送 — 准备 Paper of the Day 的 LinkedIn + X 帖子素材 |
| **author-finder** | 作者查找 — 查找论文作者的 LinkedIn 和 X 社交资料 |
| **blog-image-gen** | 补图 — 为博客 index.md 生成封面图和正文配图 |
| **editor-name** | 编辑署名 — 为博客 index.md 添加 editor_name 字段 |
| **summary-fixer** | 摘要修复 — 批量检查和修复博客 index.md 的 summary 字段 |
| **skill-creator** | Skill 开发指南 — 创建新 Claude Code Skills 的最佳实践参考 |

## 安装使用

将对应 skill 目录复制到 `~/.claude/skills/` 即可：

```bash
# 安装单个 skill
cp -r sciencepedia ~/.claude/skills/

# 安装全部
cp -r */ ~/.claude/skills/
```
