#!/usr/bin/env python3
"""
Generate cover and body images for blog index.md files via GPUGeek API.

Usage:
  python3 generate_images.py <blog_dir> [--cover-only] [--body-only] [--output-dir <dir>]

Arguments:
  blog_dir      Directory containing blog folders with index.md files.
                Can be a single blog folder or a parent with multiple blog folders.
  --cover-only  Only generate cover images
  --body-only   Only generate body images
  --output-dir  Output directory for images (default: <blog_dir>/generated_images)

Naming: -{url_slug}-cover-image.png / -{url_slug}-body-image.png
"""

import argparse
import base64
import os
import re
import requests
import sys
import time

GPUGEEK_API_KEY = os.environ.get("GPUGEEK_API_KEY", "30ggn31053e5tv01000dfounia0yeza340exi1ks")
API_URL = "https://api.gpugeek.com/predictions"

COVER_IMAGE_PROMPT = r"""
# Paper Cover Illustrator

## Role
You are an expert at creating simple, striking cover images for scientific papers.

## Task
Create a single focused illustration representing the paper's ONE core idea.

---
## Visual Style (Required)
Hand-sketched aesthetic:
- Aspect ratio: 16:9
- Wobbly marker-style black outlines
- Hand-written casual font (minimal text)
- Soft pastel highlights (yellow, blue, green, pink)
- White paper background
- Simple sketched icons (gears, arrows, stick figures, boxes)
- Avoid using brain imagery as a generic symbol for "AI" or "intelligence" — only use if the paper is specifically about neuroscience or cognitive science

---
## Cover Design Principles

**This is a COVER, not an infographic:**

| Principle | Requirement |
|-----------|-------------|
| Focus | ONE central visual element, large and prominent |
| Text | Maximum 3-5 words (core concept only) |
| White space | 60%+ of canvas empty |
| Complexity | No detailed explanations, labels, or annotations |
| Mindset | Think "book cover" not "textbook diagram" |

---
## Element Selection

**Identify the ONE most iconic visual from the paper:**

| If the paper introduces... | Draw this |
|----------------------------|-----------|
| A pipeline or process | Single key transformation (input to output) |
| An architecture | One distinctive component, enlarged |
| A comparison | Simple symbol of contrast (A vs B) |
| A mechanism | The mechanism as one clear metaphor |
| A concept | An object or icon embodying the idea |

---
## Instructions

1. Read the paper
2. Ask: "If I had to represent this paper with ONE simple drawing, what would it be?"
3. State your choice:
```json
{{
  "core_concept": "[describe in 3-5 words]",
  "visual_element": "[the single thing you will draw]"
}}
```
4. Generate a minimal, centered cover image with generous white space

---
## Paper Content
{summary_text}
"""

BODY_IMAGE_PROMPT = r"""Create a technical infographic in hand-drawn whiteboard sketch style (Excalidraw aesthetic).
3-column layout separated by wobbly hand-sketched vertical lines.
Wobbly marker-style black outlines, casual handwritten font, pastel color highlights (muted yellow, blue, green) on white background.
Simple stick figures, cubes, arrows, gears as icons. NEVER draw brains.
Left column: Problem/Motivation. Center column: Method/Architecture with flowchart arrows. Right column: Key Results/Impact.
Keep text labels concise (1-3 words). Use visual metaphors, not paragraphs.

Paper content:
{summary_text}
"""


def generate_image(summary_text, prompt_type):
    template = COVER_IMAGE_PROMPT if prompt_type == "cover" else BODY_IMAGE_PROMPT
    prompt = template.format(summary_text=summary_text)

    headers = {
        "Authorization": "Bearer " + GPUGEEK_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "model": "Vendor2/Gemini-3-Pro-Image",
        "input": {
            "aspectRatio": "16:9",
            "imageSize": "1K",
            "images": [],
            "prompt": prompt,
        },
    }

    resp = requests.post(API_URL, headers=headers, json=data, timeout=180)
    result = resp.json()

    if result.get("status") in ("starting", "processing") and result.get("id"):
        pred_id = result["id"]
        print("    Polling async prediction...", flush=True)
        for _ in range(60):
            time.sleep(5)
            poll = requests.get(
                API_URL + "/" + pred_id,
                headers={"Authorization": "Bearer " + GPUGEEK_API_KEY},
                timeout=30,
            ).json()
            if poll.get("status") == "succeeded":
                return poll.get("output")
            if poll.get("status") == "failed":
                return None
        return None

    return result.get("output")


def decode_and_save(image_data, output_path):
    if not image_data:
        return False
    if isinstance(image_data, list):
        if not image_data:
            return False
        image_data = image_data[0]
    if isinstance(image_data, str) and "," in image_data and image_data.strip().startswith("data:"):
        image_data = image_data.split(",", 1)[1]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(image_data))
    return True


def get_field(index_path, field):
    with open(index_path, "r") as f:
        for line in f:
            if line.strip().startswith(field + ":"):
                m = re.search(r'"([^"]*)"', line)
                return m.group(1) if m else ""
    return None


def needs_cover(index_path):
    val = get_field(index_path, "image")
    return val is not None and val.strip() == ""


def needs_body(index_path):
    with open(index_path, "r") as f:
        content = f.read()
    return "](body_image_url)" in content


def find_blogs(blog_dir):
    """Find blog folders. Handles both single folder and parent directory."""
    index = os.path.join(blog_dir, "index.md")
    if os.path.isfile(index):
        return [blog_dir]
    folders = []
    for name in sorted(os.listdir(blog_dir)):
        idx = os.path.join(blog_dir, name, "index.md")
        if os.path.isfile(idx):
            folders.append(os.path.join(blog_dir, name))
    return folders


def main():
    parser = argparse.ArgumentParser(description="Generate blog cover/body images")
    parser.add_argument("blog_dir", help="Blog directory or parent directory")
    parser.add_argument("--cover-only", action="store_true")
    parser.add_argument("--body-only", action="store_true")
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    blog_dir = os.path.abspath(args.blog_dir)
    folders = find_blogs(blog_dir)
    if not folders:
        print("No blog folders with index.md found.")
        sys.exit(1)

    output_dir = args.output_dir or os.path.join(blog_dir, "generated_images")
    os.makedirs(output_dir, exist_ok=True)

    tasks = []
    for folder in folders:
        index_path = os.path.join(folder, "index.md")
        slug = get_field(index_path, "url_slug")
        if not slug:
            continue

        if not args.body_only and needs_cover(index_path):
            tasks.append((folder, index_path, slug, "cover"))
        if not args.cover_only and needs_body(index_path):
            tasks.append((folder, index_path, slug, "body"))

    if not tasks:
        print("All images present. Nothing to generate.")
        return

    print("Found %d images to generate:" % len(tasks))
    for _, _, slug, ptype in tasks:
        print("  %s: %s" % (ptype.upper(), slug))
    print()

    ok = 0
    for i, (folder, index_path, slug, ptype) in enumerate(tasks, 1):
        filename = "-%s-%s-image.png" % (slug, ptype)
        filepath = os.path.join(output_dir, filename)

        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            kb = os.path.getsize(filepath) / 1024
            print("[%d/%d] SKIP %s (%.0f KB exists)" % (i, len(tasks), filename, kb), flush=True)
            ok += 1
            continue

        print("[%d/%d] %s | %s" % (i, len(tasks), ptype.upper(), slug), flush=True)

        with open(index_path, "r") as f:
            content = f.read()
        if len(content) > 2000:
            content = content[:2000]

        try:
            time.sleep(3)
            output = generate_image(content, ptype)
            if decode_and_save(output, filepath):
                kb = os.path.getsize(filepath) / 1024
                print("  OK %s (%.0f KB)" % (filename, kb), flush=True)
                ok += 1
            else:
                print("  FAIL empty API response", flush=True)
        except Exception as e:
            print("  FAIL %s" % e, flush=True)

    print("\nDone: %d/%d succeeded. Output: %s" % (ok, len(tasks), output_dir))


if __name__ == "__main__":
    main()
