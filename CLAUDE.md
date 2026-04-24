# CLAUDE.md - Instructions for Claude Code

This file contains standing conventions for the merna.org portfolio site. Read it at the start of every session and follow these rules unless explicitly overridden by the user.

## About this project

Portfolio site for Merna Saad, MSBA at UCSD Rady (2026). Built with Quarto, deployed to GitHub Pages via the rsm-msaad/merna-saad.github.io repo. Custom domain on Porkbun. Aesthetic is editorial and warm, not corporate tech.

## NON-NEGOTIABLE RULES

### 1. No em dashes or en dashes, ever

Never use em dashes or en dashes in content, code comments, commit messages, file names, or any output whatsoever. Use commas, periods, semicolons, parentheses, or rewording instead. If unsure, rewrite the sentence.

Verify after any content change by running grep for em and en dashes on the rendered HTML. The result should always be 0.

### 2. Never add Claude as a co-author on commits

Do NOT add Co-Authored-By lines with Claude, Claude's email, or any robot emoji to commit messages. Do NOT add "Generated with Claude Code" or similar attribution. Commit messages should be short and written in the user's voice.

If a prompt ever says "commit and push", do exactly that with no attribution.

### 3. Never break live posts to try new things

The live posts at /projects/ab-testing/, /projects/charitable-giving/, and /about-me/ are all working. If asked to apply a change, verify the existing behavior stays intact after the change. Check the rendered page after any CSS or markup changes.

## Project architecture

### File structure

- /_quarto.yml (site config)
- /index.qmd (homepage)
- /about-me/index.qmd (animated illustrated story theater, 13 scenes)
- /projects/index.qmd (manual HTML cards, NOT Quarto listings)
- /projects/PROJECT_NAME/index.qmd (individual posts)
- /projects/PROJECT_NAME/data/ (data files, per-project)
- /styles.css (shared stylesheet for all pages)
- /assets/ (all images and SVGs in ONE shared folder, never per-page subfolders)
- /CNAME (custom domain)

### Tech stack

- Quarto 1.9+ for static site generation
- GSAP 3.12.5 from Cloudflare CDN for animations
- Python (pandas, statsmodels, pyreadstat) for data analysis posts
- Fonts: Playfair Display (headings), Source Sans 3 (body), Kalam (handwritten notes)

### Color palette (strict, do not deviate)

- Navy #2c3e50 (primary dark, line work, titles)
- Antique brass #b8945a (accent, highlights, badges)
- Cream paper #faf6ef (ALL backgrounds, never pure white)

Extended palette for the About Me travel panel and coastal themes:
- Baby blue #b8dce8, turquoise #7cc4c2, sage #9fb8a1, terracotta #c27c5a, rose #e2a69c

Chart colors for the charitable-giving post red/blue states:
- Blue states control #6a8eb8, blue match #2c3e50
- Red states control #c27c5a, red match #7a3a3a
- Plus 60% accent in brass #b8945a

### Fonts

- Playfair Display for headings and titles
- Source Sans 3 for body text
- Kalam for handwritten notes in speech bubbles

## GSAP theater pattern

Three pages use this same architecture. Reuse it exactly when building new theaters.

### Critical gotchas

1. Scripts MUST be wrapped in raw HTML blocks using Quarto's raw content syntax. Quarto strips unwrapped script tags.

2. Use the savedDefine pattern for GSAP loading to avoid AMD conflict. Save window.define to a temp variable, set window.define to undefined, load GSAP, then restore window.define in the onload handler.

3. Never use the wildcard selector with gsap.killTweensOf because it kills theater fade-ins. Scope to specific elements like screen.querySelectorAll.

4. Scenes must be an array of functions that swap innerHTML on a single #gs-screen container. Do NOT render all scenes into the DOM simultaneously.

5. IntersectionObserver for scroll-triggered animations should use threshold 0.1 (not 0.5) so animations fire before the element is fully in view.

### Scene structure

Scenes are an ordered array of functions. A showScene(i) function calls scenes[i](). Previous and Next buttons adjust currentIndex and call showScene. A counter displays "N / total", a timeline bar fills proportionally. Keyboard arrows navigate. A Restart link returns to the first scene.

### Speech bubble styling (.gs-bubble class)

- Background #faf6ef with subtle gradient
- 1px border at 15% navy opacity
- Navy text, Kalam font, 1.5rem size on desktop, scaling down on mobile
- Rotation of negative 1.5 degrees
- No tail (display none on .gs-bubble-tail)
- Soft shadow

### Character positioning

Both persona SVGs (persona-guide, persona-analyst) face right by default. Position character on LEFT of scene, bubble on RIGHT. Use display inline-flex on .gs-char-scene plus text-align center on parent to center the pair as a tight unit. Character width 320px, max-height 480px, gap 2rem.

## Deployment workflow

After any change:

1. Run quarto render

2. Verify animation scripts survived (for pages with theaters):
   grep -c "gsap.min.js" _site/path/to/page.html
   Result should be at least 1. If 0, scripts were stripped.

3. Verify no em or en dashes:
   grep -cE em-dash-character-here or en-dash-character-here in _site/path/to/page.html
   Result MUST be 0.

4. If the change is ready, commit and push:
   git add .
   git commit -m "short descriptive message"
   git push

Commit message format: short, lowercase, descriptive. Examples:
- fix mobile layout for about me theater
- update scene 6 narrative text
- add sticky note for gpa

NEVER include co-author attribution or Claude branding.

## Common request patterns

When the user says "fix X" or "X is broken":
1. Reproduce the issue first (view the relevant file, check rendered HTML)
2. Diagnose the root cause
3. Apply the fix
4. Verify with grep or file checks
5. Deploy

When the user says "add X to Y page":
1. Check how similar elements are implemented on other pages
2. Match the existing pattern, don't invent new architecture
3. Add to shared styles.css if the style should be reusable
4. Verify the change rendered correctly

When the user says "update content on page X":
1. Open the file
2. Apply the text change
3. Run quarto render
4. Verify the new content appears in _site/path/to/page.html
5. Deploy

### When to ask for clarification

Ask the user before:
- Making changes that affect multiple pages (confirm scope)
- Restructuring folders or renaming files
- Deleting content
- Any change that could break a live post

Do NOT ask for confirmation before:
- Small CSS tweaks within a single page
- Typo fixes
- Running quarto render
- Running grep verifications
- Routine git add / commit / push

## Known issues and past fixes (don't re-introduce these)

- Quarto strips script tags outside raw HTML blocks
- Wildcard gsap.killTweensOf kills theater fade-ins
- All theater scenes rendering in DOM simultaneously (must use innerHTML swapping)
- IntersectionObserver threshold 0.5 is too conservative, use 0.1
- Characters facing wrong direction on scenes (fixed by using persona-guide and persona-analyst SVGs that both face right, placing bubble on opposite side)
- Flex containers stretching children to edges (fixed with display inline-flex + text-align center on parent)

## Content voice

Merna's writing voice is warm, reflective, editorial. Not corporate. Signature phrases she uses:
- "Visca Barça", "Més que un club"
- "The analyst bakes bread"
- "Let us build something great together"

When writing or editing content on the site, match this register. Write paragraphs, not bullet points. She prefers "let us" over "let's" in some narrative contexts.

## End of file

If you have read this, you're ready to help with this project. Execute requested tasks efficiently. Verify after every change. Never violate the NON-NEGOTIABLE RULES. Keep commits clean and attribution-free.
