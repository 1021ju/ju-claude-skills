---
name: blog-image-gen
description: >
  Generate cover and body images for blog index.md files that are missing them.
  Use when user says "generate images", "补图", "生成封面", "生成body图",
  "missing cover image", "缺封面图", or when scanning index.md files reveals
  empty image: fields or body_image_url placeholders.
  Also triggers when user asks to "check images" or "检查图片" for blog posts.
---

# Blog Image Generator

Generate cover and body images for blog posts via GPUGeek API (Gemini-3-Pro-Image).

## Detection

An index.md **needs a cover image** when its frontmatter has `image: ""`.
An index.md **needs a body image** when body contains `](body_image_url)`.

## Usage

Run the bundled script:

```bash
python3 ~/.claude/skills/blog-image-gen/scripts/generate_images.py <blog_dir> [--cover-only] [--body-only] [--output-dir <dir>]
```

- `blog_dir`: single blog folder or parent containing multiple blog folders
- Script auto-detects which files need cover/body images
- Skips already-generated images
- Output naming: `-{url_slug}-cover-image.png` / `-{url_slug}-body-image.png`
- Default output: `<blog_dir>/generated_images/`

## API Details

- Endpoint: `https://api.gpugeek.com/predictions`
- Key: env `GPUGEEK_API_KEY` (hardcoded fallback in script)
- Model: `Vendor2/Gemini-3-Pro-Image`
- Each image takes 30s-2min; add 3s delay between calls to avoid rate limits
- Content truncated to 2000 chars to stay within token limits

## After Generation

Images land in `generated_images/` with `-` prefix for COS upload compatibility.
CDN URL pattern after upload:
```
https://cdn.bohrium.com/bohrium/blog/images/content/-{url_slug}-cover-image.png
```

Update index.md files:
1. **Cover**: set `image:` field to the CDN URL
2. **Body**: replace `![image_alt_prefix](body_image_url)` with real `![alt](cdn_url)`
