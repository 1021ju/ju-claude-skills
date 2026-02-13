---
name: paper-post-prep
description: "Prepare all assets for a Paper of the Day post (LinkedIn + X). Use when user says 'paper of the day', '每日论文', 'prep paper post', '论文推送', 'prepare paper post', or provides a paper (PDF/arXiv link) for social media posting. This skill orchestrates the full workflow: Bohrium link lookup, image suggestions, author profile finding, and generating both LinkedIn and X post drafts."
---

# Paper Post Prep — Paper of the Day Asset Pipeline

One-stop preparation for Bohrium's Paper of the Day social media posts. Takes a paper and outputs everything needed for posting on both LinkedIn and X.

## Input

User provides one or more of:
- **arXiv link** (e.g., `https://arxiv.org/abs/2401.12345`)
- **Paper PDF** (local file path)
- **Paper title + authors** (manual input)
- **DOI** (e.g., `10.1038/s41586-024-07892`)
- **GitHub repo URL** (if known)

## Workflow

### Step 1: Extract Paper Metadata

From arXiv link or PDF, extract:
- Title, authors, institutions
- Abstract
- DOI (if available)
- GitHub repo link (check abstract, footnotes, "Code available at...")

If user provided an arXiv link:
```
Web search: "{arxiv ID}" site:arxiv.org
```
Read the abstract page. Look for:
- Author list and affiliations
- "Code: github.com/..." links
- Related project pages

### Step 2: Bohrium Link Lookup

Find the paper on bohrium.com using the bundled script:

```bash
# By DOI (preferred — more precise)
python3 scripts/bohrium_lookup.py --doi "10.1234/example.doi"

# By title (fallback)
python3 scripts/bohrium_lookup.py --title "Paper Title Here"

# Both (tries DOI first, falls back to title)
python3 scripts/bohrium_lookup.py --doi "10.1234/example" --title "Paper Title"
```

The script reads credentials from `~/content_writer/blog/.env` automatically.

**Output includes**: Bohrium paper URL, author list, journal, citations, popularity score.

If the paper is found, provide the Bohrium URL to the user — they'll need it for the screenshot.

If NOT found: tell the user. They may need to manually search bohrium.com or skip the Bohrium screenshot.

### Step 3: Image Suggestions

Suggest 4 images for the post (the standard Bohrium Paper of the Day format):

#### Image 1-2: Paper/Repo Figures

Analyze the paper for the best visual assets. Prioritize:

1. **Architecture/pipeline diagrams** (Figure 1 is often the overview) — these explain the method at a glance
2. **Result comparison figures** — before/after, side-by-side, ablation tables with visual impact
3. **GIFs/animations from repo** — if the GitHub repo has demo GIFs in README, these are gold
4. **Teaser figures** — many ML papers have a "teaser" figure showing the key result visually

Output format:
```
### Image Suggestions

📸 Image 1 (recommended): Figure 2 — System architecture diagram (page 3)
   Why: Clean pipeline overview, shows the three-stage approach at a glance

📸 Image 2 (recommended): Figure 5 — Comparison with baselines (page 7)
   Why: Visual results comparison, immediately shows improvement

🎬 Repo GIF alternative: README demo animation showing [description]
   URL: [direct link to the image/gif in the repo]
```

If a GitHub repo exists, search for images:
```
Web search: site:github.com {repo path} readme
```
Look for `.gif`, `.png`, `.mp4` files in the repo root, `assets/`, `docs/`, `figures/` directories.

#### Image 3: Bohrium Screenshot

If Step 2 found the paper on Bohrium, provide the URL:
```
📸 Image 3: Bohrium paper page screenshot
   URL: {bohrium_url}
   → User takes screenshot manually
```

#### Image 4: AI Poster

```
📸 Image 4: AI-generated poster via Bohrium AI Poster
   → User generates this on bohrium.com
```

### Step 4: Find Author Profiles

Use the `author-finder` skill approach (search strategies documented there). For Paper of the Day, focus on:

1. **First author** — usually the PhD student, often most active on social media
2. **Corresponding author** — the PI, often has a larger LinkedIn following
3. **Institution account** — backup tag if personal profiles aren't found

Search in this order:
- GitHub repo → contributor profiles → social links in bios
- arXiv author pages → homepage links
- Web search: `"{author name}" "{institution}" site:linkedin.com`
- Web search: `"{author name}" site:x.com OR site:twitter.com`
- Google Scholar → personal homepage → social links

**Reality check on author tagging:**
- Many authors simply have no findable LinkedIn/X profiles — this is normal
- **Zero taggable authors is OK** if the paper is hot enough. Still post it
- Ideal: at least one person or institution account to tag. But don't block on this
- Don't waste excessive time searching. Run through the 5 layers above; if nothing turns up after that, move on
- Report clearly: "Found 1 of 4 authors" or "No profiles found — recommend posting without @mentions"

### Step 5: Generate LinkedIn Post

Read the LinkedIn style guide: `references/linkedin-style.md`

LinkedIn posts have **2 parts**: a mainpost + 1 reply.

**Mainpost** (1200-1800 characters):
- 🚨 hook → context → author attribution → mechanism → impact → hashtags
- **No links in the mainpost** — all links go in the reply
- Author names written as `@Name (Institution)` format for easy tagging
- `#PaperOfTheDay` always first hashtag
- **Vary the framing** — don't use "milestone study", "breakthrough transforms", "charts a new path" every time. See anti-patterns in the style guide
- **More technical depth than X** — explain the mechanism, include specific numbers/benchmarks
- **One honest caveat** — limitations, caveats, "in mice" disclaimers build credibility
- **Minimize colons** — prefer commas, dashes, or restructuring over colons. One or two per post max

**Reply** (论文 + SP 词条, all in one reply):
- 📄 Bohrium paper link (NOT arXiv — drive traffic to Bohrium)
- 💻 GitHub repo link if available
- 🔬 3 SciencePedia concept names + URLs (name and URL only, no explanations)

**LinkedIn 艾特备注 table**: Provide a separate table mapping each `@Name` in the mainpost to their LinkedIn profile URL, so the user can quickly find and tag them when posting.

### Step 6: Generate X Post

X posts have **2 parts**: a mainpost + 1 thread. Minimal emoji — only 🚨 for the hook line, nothing else.

**Superscript annotations:** Mark 3 key concepts in the mainpost text with superscript numbers ¹ ² ³. Place each superscript right after the first natural mention of the concept. These correspond to numbered SciencePedia entries in the thread.

**Mainpost structure:**

```
🚨 [Hook — tension or surprising claim, one sentence]

#POTD | [One-sentence summary of the core finding/contribution]

@handle1, @handle2, and @handle3 (Institution) [what they did / what they found — 1-2 sentences framing the problem and approach]

[Mechanism paragraph 1: explain the problem in concrete terms — why current approaches fail, what goes wrong. Mark a key concept with ¹ on first mention.]

[Mechanism paragraph 2: explain the solution with specific details. Use numbered lists (1. 2. 3. 4.) for multi-part contributions. Mark concepts with ² ³ where natural.]

[Result paragraph: concrete numbers, key insight in plain language, scale/scope]

Paper and explainers below. [Venue/acceptance info]
```

**Writing guidelines:**
- **No emoji** except 🚨 on the hook line. No 📑📍🔷👇1️⃣ etc.
- **No links in the mainpost** — all links go in the thread
- `#POTD` (Paper of the Day) always on the second line. No other hashtags in X mainpost — `#POTD` is the only one
- @handles woven naturally with (Institution) after the group
- **Closing line** — always "Paper and explainers below." (not "code below" — we don't promote raw repo links in the mainpost)
- **Superscript placement** — attach ¹ ² ³ to key technical terms where they first appear naturally. Don't force all three into one sentence
- **Wording matters** — don't write like a paper abstract. Use tension in the hook ("Right answers, wrong lesson"), explain *why* something fails, not just *that* it fails. Concrete > abstract
- **Minimize colons** — prefer commas, dashes, or restructuring over colons. One or two per post max
- Numbered lists use plain `1. 2. 3.` not emoji numbers

**Thread** (论文 + SP 词条, all in one thread):
- 📄 Bohrium paper link (NOT arXiv — drive traffic to Bohrium)
- 💻 GitHub repo link if available
- ¹ Concept Name + SciencePedia URL (name and URL only, no explanations)
- ² Concept Name + SciencePedia URL
- ³ Concept Name + SciencePedia URL

Look up SciencePedia concepts:
```bash
python3 ~/.claude/skills/sciencepedia/scripts/lookup.py "concept1" "concept2" "concept3"
```

### Step 7: Present Complete Package

Show everything together for user review:

```
## Paper of the Day — {Date}

### 📄 Paper Info
- Title: {title}
- Authors: {author list}
- arXiv: {link}              ← keep arXiv link here for internal reference
- Venue: {conference if applicable}
- Repo: {github link}
- Bohrium: {bohrium URL or "Not found"}

### 👥 Author Profiles
| Author | LinkedIn | X/Twitter | Confidence |
|--------|----------|-----------|------------|
| ... | ... | ... | ... |

### 📸 Image Plan
1. {figure suggestion 1}
2. {figure suggestion 2}
3. Bohrium screenshot: {url}
4. AI Poster: generate on bohrium.com

### LinkedIn Post
**Mainpost:**
{mainpost text — no links}

**Reply (论文 + SP 词条):**
{Bohrium link + repo link + 3 SciencePedia concept names & URLs}

**LinkedIn 艾特备注:**
| 正文中的 @名字 | LinkedIn URL |
|---------------|-------------|
| ... | ... |

### X Post
**Mainpost:**
{mainpost text with ¹ ² ³ superscript annotations — no links}

**Thread (论文 + SP 词条):**
{Bohrium link + repo link + numbered ¹ ² ³ SciencePedia concept names & URLs}
```

Ask the user if they want adjustments to any section.

## Quick-Start (For Returning Users)

If you've used this skill before and just want to run through fast:

```
User: "paper of the day: [arXiv link]"
→ Skill runs Steps 1-7 automatically
→ Presents complete package
→ User reviews, adjusts, posts
```
