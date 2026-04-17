# Merna Saad Portfolio: Design System

This file is the single source of truth for all visual styling on merna.org. Claude Code should read this file before making any design, color, styling, or content decisions on any page or project.

## Color Palette

### Primary Colors
- **Deep Navy (primary):** `#2c3e50`
- **Navy Light (hover states):** `#3d5166`
- **Antique Brass (accent):** `#b8945a`
- **Brass Light (secondary accent):** `#d4b483`
- **Brass Subtle (backgrounds):** `#f5efe6`

### Neutrals
- **Cream (page background):** `#f5f2ed`
- **Cream Light (card/navbar bg):** `#faf8f5`
- **Charcoal (headings, primary text):** `#2a2a2a`
- **Text Secondary:** `#5a5a5a`
- **Text Muted:** `#8a8a8a`

### CSS Variables
```css
:root {
  --navy: #2c3e50;
  --navy-light: #3d5166;
  --brass: #b8945a;
  --brass-light: #d4b483;
  --brass-subtle: #f5efe6;
  --cream: #f5f2ed;
  --cream-light: #faf8f5;
  --charcoal: #2a2a2a;
  --text-primary: #2a2a2a;
  --text-secondary: #5a5a5a;
  --text-muted: #8a8a8a;
}
```

## Typography

### Fonts
- **Headings:** Playfair Display (serif), fallback: Georgia, serif
- **Body text:** Inter (sans-serif), fallback: Helvetica Neue, sans-serif
- **Code:** System monospace

### Google Fonts Import
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Chart and Plot Colors

When creating matplotlib, seaborn, plotly, or any other charts in Python or R, use these colors:

```python
NAVY = '#2c3e50'
BRASS = '#b8945a'
CREAM = '#faf8f5'

plt.rcParams.update({
    'figure.facecolor': '#faf8f5',
    'axes.facecolor': '#faf8f5',
    'axes.edgecolor': '#888888',
    'axes.labelcolor': '#333333',
    'text.color': '#333333',
    'xtick.color': '#555555',
    'ytick.color': '#555555',
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
```

## Writing Style Rules

- **NEVER use em dashes or en dashes.** No `---` or `--` anywhere. Use commas, periods, semicolons, parentheses, or rewording instead.
- Keep prose clean and professional.
- Sentence case for all headings.

## Characters and Illustrations

### Character SVG Files
Three character illustrations are stored in `/assets/`:
- **c1.svg**: Professional woman at desk with glasses. Use as the primary guide/presenter.
- **c2.svg**: Character at computer workstation. Use for data analysis/working scenes.
- **c3.svg**: Third character for additional variety.

### Character Usage
- Characters appear at the top of each blog post as a "tour guide"
- The character greets the reader with a speech bubble, then slides off screen while animations play, then slides back in to comment
- Use GSAP for character entrance (back.out easing), gentle floating (sine.inOut yoyo), and exit (power2.in) animations
- Characters alternate between scenes: c1.svg for introductions and commentary, c2.svg for results and conclusions
- Character size: 200px x 200px in the hero section, 110px x 110px in subtopic section intros

### Character Speech Bubbles
- Background: `#2c3e50` (navy)
- Text color: `#faf8f5` (cream)
- Font: Playfair Display, italic
- Border radius: 14px
- Include a CSS triangle tail pointing toward the character
- Use GSAP typewriter effect for text appearing letter by letter

## Animation System

### GSAP (GreenSock)
All animations use GSAP loaded from CDN:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

### Blog Post Hero Animation Structure
Each blog post has a guided-story at the top with this pattern:
1. Character scene (character + speech bubble greeting the reader)
2. Act scene (visualization/animation explaining a concept)
3. Character scene (character comments on what just happened)
4. Act scene (next visualization)
5. Repeat until conclusion

Controls: Previous/Next buttons, step dots for navigation.

### Subtopic Animations
Each major section in a blog post gets:
- A section-intro block (character + speech bubble) that fades in on scroll using ScrollTrigger
- An anim-stage with a scroll-triggered visualization (SVG charts, dot grids, histograms, etc.)

### Scroll Animations for Blog Posts
- Sections fade in as the reader scrolls (IntersectionObserver or ScrollTrigger)
- Code blocks slide in from the left
- Charts scale up slightly when appearing
- Reading progress bar at the top (navy to brass gradient)

### CSS Animation Keyframes Used
- `fadeInUp`: elements slide up and fade in
- `fadeInLeft` / `fadeInRight`: used for homepage two-column split
- Staggered delays: sequential elements appear 0.1s apart
- Hover effects: cards lift with shadow, buttons fill with navy, navbar links get underline

### Animation Timing
- Keep animations subtle and professional (0.3s to 0.8s duration, ease-out timing)
- GSAP easing: `power3.out` for entrances, `power2.in` for exits, `back.out(1.4)` for bouncy entrances, `elastic.out(1, 0.5)` for playful reveals, `sine.inOut` for continuous floating

### Important: Quarto Script Handling
ALL `<script>` tags in .qmd files MUST be wrapped in raw HTML blocks:
````
```{=html}
<script>
// your code here
</script>
```
````
Quarto strips bare `<script>` tags. This is the #1 cause of animations not working.

## Project Cover Images

### Visual Style
- Hand-drawn pencil sketch with watercolor accents
- Cream background (#faf8f5)
- Navy (#2c3e50) and brass (#b8945a) watercolor washes
- Looks like a page from a data scientist's field notebook
- Aspect ratio: Square (1:1), 1024x1024 pixels minimum

### Content Requirements
Every cover image must include:
1. Project title in loose handwritten pencil lettering
2. Short description (2-3 lines) in smaller handwritten script
3. A relevant sketched visual representing the topic

### Gemini Prompt Template
```
Hand-drawn sketch on cream paper, square 1:1 aspect ratio. Pencil lines with subtle navy blue and antique gold watercolor accents around the edges. Top of the image has "[PROJECT TITLE]" written in loose handwritten pencil calligraphy. Below the title, in smaller handwritten pencil script on 2-3 lines: "[PROJECT DESCRIPTION]". In the main area, [DESCRIBE THE SKETCHED VISUAL]. Minimalist, artistic, looks like a page from a data scientist's field notebook. No digital or polished elements.
```

### File Naming and Placement
- Save in `/assets/` folder as `projectN.png` (project1.png, project2.png, etc.)
- In the project's index.qmd frontmatter:
```yaml
image: ../../assets/projectN.png
image-alt: "[Descriptive alt text for accessibility]"
```

### Projects Page
The Projects page (projects.qmd) uses manual HTML, NOT Quarto's listing system:
```html
<div class="projects-grid">
  <a href="projects/ab-testing/" class="project-card">
    <img src="assets/project1.png" alt="..." />
  </a>
  <!-- Add more project-card links as new projects are created -->
</div>
```

Card CSS: rounded corners, soft shadow, hover lift effect, max-width 300px per card.

## Component Styles

### Code Blocks
- Background: `#f0ede8` (light cream)
- Text: `#2a2a2a` (dark)
- Left border: 3px solid `#b8945a` (brass)
- Border radius: 8px

### Buttons / About Links
- Border: 1.5px solid `#2c3e50`
- Border radius: 20px (pill shape)
- Hover: fill with `#2c3e50`, cream text, lift 2px

### Tables
- Header background: `#2c3e50` with white text
- Striped rows: `#f5efe6` (brass subtle)

### Horizontal Rules
- Gradient from transparent to `#b8945a` to transparent

### Key Takeaway Callout Boxes
Use Quarto's callout syntax:
```
::: {.callout-tip title="Key Takeaway" appearance="simple"}
Your takeaway text here.
:::
```

### Result Cards (replacing print output)
Styled HTML cards with brass left border instead of raw print() output:
```html
<div style="background: #faf8f5; border: 1px solid rgba(44,62,80,0.1); border-radius: 8px; padding: 16px; margin: 12px 0; border-left: 3px solid #b8945a;">
  <strong style="color: #2c3e50;">Label:</strong> Value
</div>
```

### Summary Card (end of blog post)
Dark navy card summarizing key learnings:
```html
<div style="background: #2c3e50; color: #faf8f5; border-radius: 10px; padding: 24px; margin: 24px 0;">
  <h3 style="color: #b8945a;">What We Learned</h3>
  <!-- Grid of key points -->
</div>
```

## Homepage Elements

### Profile Image
- Circular crop with brass border (2.5px solid #b8945a)
- Shadow on hover

### Typing Tagline
- Text: "Engineering mindset. Strategic vision. Data driven."
- Color: brass, italic
- Blinking cursor animation

### Open to Work Badge
- Green pulsing dot with "Open to Work" text
- Light green background (#f0fdf4), green border (#bbf7d0)

### Skill Pills
Three categories with colored pill badges:
- Languages (navy filled): Python, SQL, Excel VBA, Git
- ML & Stats (brass filled): Regression, Classification, Clustering, XGBoost, NLP, A/B Testing
- Tools (brass outline): Jupyter, Tableau, Plotly, ETL Pipelines

### Footer
- "Merna Saad (c) 2026 | Built with Quarto"
- Cream background, light border top

## File Structure

```
/
├── _quarto.yml
├── index.qmd (homepage, trestles layout)
├── resume.qmd
├── projects.qmd (manual HTML grid)
├── fun.qmd
├── styles.css
├── DESIGN_SYSTEM.md (this file)
├── CNAME (merna.org)
├── assets/
│   ├── Merna.png (profile photo)
│   ├── Resume.pdf
│   ├── project1.png (A/B Testing cover)
│   ├── c1.svg (presenter character)
│   ├── c2.svg (analyst character)
│   └── c3.svg (third character)
├── projects/
│   └── ab-testing/
│       └── index.qmd
├── docs/ (rendered output, pushed to GitHub Pages)
└── _backups/
    └── styles_backup_original.css
```

## Workflow

1. Before any design work, read this file first
2. Generate cover images using the Gemini prompt template above
3. Characters (c1.svg, c2.svg, c3.svg) are reused across all blog posts
4. Always wrap <script> tags in raw HTML blocks for Quarto
5. Test animations locally before pushing
6. Hard refresh (Cmd+Shift+R) after deploying to clear browser cache
