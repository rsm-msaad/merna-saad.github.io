# Merna Saad Portfolio: Design System

This file is the single source of truth for all visual styling on merna.org. Claude Code should read this file before making any design, color, or styling decisions on any page or project.

## Color Palette

### Primary Colors
- **Deep Navy (primary, headings, buttons):** `#2c3e50`
- **Navy Light (hover states):** `#3d5166`
- **Antique Brass (accent, underlines, highlights):** `#b8945a`
- **Brass Light (secondary accent):** `#d4b483`
- **Brass Subtle (light backgrounds):** `#f5efe6`

### Neutrals
- **Cream (page background):** `#f5f2ed`
- **Cream Light (card backgrounds, navbar):** `#faf8f5`
- **Charcoal (primary text):** `#2a2a2a`
- **Text Secondary:** `#5a5a5a`
- **Text Muted:** `#8a8a8a`

### Code Blocks
- **Code background:** `#1e2430`
- **Code text:** `#e8edf3`
- **Code left border:** `#b8945a`

## Typography

### Fonts
- **Headings:** Playfair Display (serif), fallback: Georgia, serif
- **Body text:** Inter (sans-serif), fallback: Helvetica Neue, sans-serif
- **Code:** System monospace

### Font Sizes (keep compact)
- **h1 / page title:** 1.6rem
- **h2:** 1.2rem
- **h3:** 1.05rem
- **Body text / paragraphs:** 0.88rem
- **Navbar links:** 0.85rem
- **Card text:** 0.82rem
- **About link buttons:** 0.82rem

### Google Fonts Import
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Chart and Plot Colors

When creating matplotlib, seaborn, plotly, or any other charts in Python or R, use these colors:

```python
# Primary chart color (lines, bars, main data)
NAVY = '#2c3e50'

# Secondary chart color (reference lines, secondary data)
BRASS = '#b8945a'

# Additional chart colors if needed
NAVY_LIGHT = '#3d5166'
BRASS_LIGHT = '#d4b483'
CHARCOAL = '#2a2a2a'

# Plot background
plt.rcParams.update({
    'figure.facecolor': '#faf8f5',
    'axes.facecolor': '#faf8f5',
    'axes.edgecolor': '#888888',
    'axes.labelcolor': '#2a2a2a',
    'text.color': '#2a2a2a',
    'xtick.color': '#5a5a5a',
    'ytick.color': '#5a5a5a',
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
```

## Writing Style Rules

- **NEVER use em dashes or en dashes.** No `---` or `--` anywhere in prose. Use commas, periods, semicolons, parentheses, or rewording instead.
- Keep prose clean and professional.
- Sentence case for all headings.

## Animation Guidelines

The site uses CSS animations. Key patterns:
- **fadeInUp:** Elements slide up and fade in on page load
- **fadeInLeft / fadeInRight:** Used for the homepage two-column split
- **Staggered delays:** Sequential elements appear one after another (0.1s increments)
- **Hover effects:** Cards lift with shadow, buttons fill with navy, navbar links get brass underline
- Keep animations subtle and professional (0.3s to 0.8s duration, ease-out timing)

## Component Styles

### Project Cards
- Background: `#faf8f5`
- Border: `rgba(44, 62, 80, 0.1)`
- Border radius: 10px
- Hover: lift 3px, brass border, shadow

### Buttons / About Links
- Border: 1.5px solid `#2c3e50`
- Border radius: 20px (pill shape)
- Hover: fill with `#2c3e50`, cream text

### Tables
- Header background: `#2c3e50` with white text
- Striped rows: `#f5efe6`

### Horizontal Rules
- Gradient from transparent to `#b8945a` to transparent

## File Structure

- `styles.css` holds all custom CSS
- `styles_backup_original.css` is the pre-redesign backup (restore if needed)
- `DESIGN_SYSTEM.md` is this file (read before any design work)
- `_quarto.yml` references styles.css and Google Fonts
- Each project folder (e.g., `projects/ab-testing/`) contains its own `index.qmd` file

## Project Cover Images

All project blog posts use a consistent hand-drawn illustration style for their cover images, inspired by a data scientist's field notebook aesthetic.

### Visual Style

- **Medium:** Hand-drawn pencil sketch with watercolor accents
- **Paper:** Cream background (#faf8f5), warm and tactile
- **Colors:** Deep navy (#2c3e50) and antique gold / brass (#b8945a) for watercolor washes and ink
- **Feel:** Loose, artistic, imperfect. Like a page from a working notebook. Not polished or corporate.
- **Aspect ratio:** Square (1:1). 1024x1024 pixels minimum.

### Content Requirements

Every cover image must include:

1. **Project title** in loose handwritten pencil lettering across the top (e.g., "A/B Testing", "Churn Prediction", "Recommender Systems")
2. **Short description** (2-3 lines) in smaller but legible handwritten script below the title, explaining what the project is about
3. **A relevant sketched visual** that represents the topic (bar charts for A/B testing, a branching tree for classification, network nodes for recommenders, etc.)

### Gemini Prompt Template

Use this prompt with Gemini (or similar image generator) to create new covers:

> Hand-drawn sketch on cream paper, square 1:1 aspect ratio. Pencil lines with subtle navy blue and antique gold watercolor accents around the edges. Top of the image has "[PROJECT TITLE]" written in loose handwritten pencil calligraphy. Below the title, in smaller handwritten pencil script on 2-3 lines: "[PROJECT DESCRIPTION]". In the main area, [DESCRIBE THE SKETCHED VISUAL]. Minimalist, artistic, looks like a page from a data scientist's field notebook. No digital or polished elements.

### File Naming and Placement

- Save each cover image in the `/assets/` folder
- Name it `projectN.png` where N is the project number (project1.png, project2.png, etc.)
- In the project's index.qmd frontmatter, reference it as:

```yaml
image: ../../assets/projectN.png
image-alt: "[Short descriptive alt text for accessibility]"
```

### CSS Treatment

Project cover images display as square cards on the Projects listing page. The styling is defined in styles.css under `.quarto-post` rules:

- Square aspect ratio (1:1)
- `object-fit: contain` so the full image shows without cropping
- Soft shadow on hover with a subtle lift effect
- No title or description text overlay (the image contains all the text)
