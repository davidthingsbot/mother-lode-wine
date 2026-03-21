# AGENTS.md — Repository Format Specification

This document defines the standard formats for region overviews and winery entries.

---

## Repository Structure

```
regions/
  el-dorado/
    README.md           # Region overview
    boeger-winery.md    # Individual winery
    lava-cap-winery.md
  amador/
    README.md
    sobon-estate.md
    terre-rouge.md
  ...
```

---

## Region Overview Format

Each region folder contains a `README.md` with the following structure:

### Region Template

```markdown
# [County/Region Name]

> *[One-line tagline capturing the region's identity]*

## Overview

Brief 2-3 paragraph introduction covering:
- Geographic location within the Mother Lode
- Wine industry significance
- What makes the region distinctive

| Field | Value |
|-------|-------|
| **AVA(s)** | Sub-AVA names or "Sierra Foothills (no sub-AVA)" |
| **Wineries** | Approximate count |
| **Elevation** | Range in feet |
| **Key Towns** | Main towns/tasting destinations |

## AVAs

### [AVA Name]
- **Established:** Year
- **Area:** Geographic description
- **Elevation:** Range
- **Characteristics:** Soil, terrain, microclimate

*Repeat for each sub-AVA in the region. Omit section if no sub-AVAs.*

## Climate

- **Days:** Temperature description (Region II, III, etc.)
- **Nights:** Cooling factors
- **Diurnal swing:** Temperature range (°F)
- **Growing season:** Days
- **Rainfall:** Annual inches

## Signature Varietals

List the 4-6 most important grape varieties for the region:

- **Zinfandel** — Brief note (e.g., "old-vine heritage")
- **Syrah** — Brief note
- ...

## Notable Wineries

*See individual files for details*

- Winery Name
- Winery Name
- ...

## History

2-4 paragraphs covering:
- Gold Rush era origins
- Peak/decline period
- Modern revival
- Notable milestones

## Resources

- [Regional Association](https://...)
- Other relevant links

---

*Last updated: YYYY-MM-DD*
```

### Required Region Fields

1. **Name** (H1 header)
2. **Overview** (paragraph + table)
3. **Climate** (basic viticulture context)
4. **Signature Varietals** (what grows here)
5. **Notable Wineries** (quick reference list)

### Optional Region Sections

- **AVAs** — Include only if region has sub-AVAs
- **History** — Include for historically significant regions
- **Resources** — Include if useful associations/links exist

---

## Winery File Format

### File Location & Naming

- Location: `regions/<county>/<winery-name>.md`
- Naming: Lowercase, hyphenated (e.g., `boeger-winery.md`, `terre-rouge.md`)
- Use common name, not corporate entity

### Winery Template

```markdown
# [Winery Name]

> *[Optional tagline or brief description]*

## Overview

| Field | Value |
|-------|-------|
| **Location** | City, County |
| **AVA** | Sub-AVA name (if applicable) |
| **Founded** | Year |
| **Owners** | Names |
| **Winemaker** | Name |
| **Acres** | Vineyard acreage (if estate) |
| **Elevation** | Feet above sea level |
| **Annual Production** | Cases per year |

## Contact

- **Address:** Street, City, CA ZIP
- **Phone:** (xxx) xxx-xxxx
- **Website:** https://...
- **Tasting Room:** Hours, appointment required?

## Wines

### Reds
- **[Wine Name]** — Varietal, vintage notes
- ...

### Whites
- **[Wine Name]** — Varietal, vintage notes
- ...

### Rosé / Other
- ...

## Signature Wines

Highlight 2-3 standout bottles with brief tasting notes.

## Vineyards

Estate vineyard details: soil types, exposures, notable blocks, old-vine designations.

## History

Brief history of the winery — founding story, notable events, ownership changes.

## Notes

Personal tasting notes, visit experiences, recommendations.

## Visited

- [ ] Have not visited
- [x] Visited: YYYY-MM-DD

## Rating

⭐⭐⭐⭐⭐ (0-5 stars, subjective)

---

*Last updated: YYYY-MM-DD*
```

### Required Winery Fields

1. **Name** (H1 header)
2. **Location** (city, county)
3. **Contact** (at least website or phone)
4. **Wines** (at least a partial list)

### Optional Winery Sections

- **Vineyards** — For estate wineries
- **History** — For historically significant wineries
- **Notes** — Personal observations
- **Rating** — Subjective, can omit

### Metadata Tags

For future searchability, consider including in the Overview table:

| Tag | Values |
|-----|--------|
| **Style** | Old World / New World / Natural / Minimal Intervention |
| **Focus** | Zinfandel specialist / Rhône / Italian / Bordeaux / etc. |
| **Price Range** | $ / $$ / $$$ / $$$$ |
| **Tasting Fee** | $X (waived with purchase?) |
| **Dog Friendly** | Yes / No |
| **Picnic Area** | Yes / No |

---

## Conventions

### Formatting
- Use **bold** for wine names in lists
- Use standard varietal spellings (Zinfandel, not zin; Cabernet Sauvignon, not cab)
- Include vintage years when known
- Use proper case for AVA names

### Status Notes
- Note if a winery is closed, sold, or defunct
- Note temporary closures or special conditions
- Update "Last updated" when making changes

### Links
- Prefer HTTPS URLs
- Link to official winery websites, not aggregators
- Include social media only if particularly active/useful

---

## Images

### Folder Structure

```
images/
  regions/
    sierra-foothills-map.png    # Full region overview map
    sierra-foothills-ava-map.pdf # Official TTB AVA boundaries
    hero-vineyard.jpg           # Hero image for the region
    el-dorado/
      map.png                   # County map (OpenStreetMap)
      vineyard.jpg              # Representative photo
    amador/
      map.png
      vineyard.jpg
    ...
  wineries/
    <winery-name>/
      exterior.jpg              # Winery building/entrance
      tasting-room.jpg          # Interior
      vineyard.jpg              # Estate vineyard
      wines.jpg                 # Wine bottles/lineup
      ...
  IMAGE_SOURCES.md              # Licensing & attribution
```

### Image Naming

**Regions:**
- `map.png` — OpenStreetMap-derived map
- `vineyard.jpg` — Representative vineyard photo
- `landscape.jpg` — Scenic view of the region

**Wineries:**
- `exterior.jpg` — Building/entrance
- `tasting-room.jpg` — Interior
- `vineyard.jpg` — Estate vineyard
- `wines.jpg` — Wine bottles
- `logo.png` — Winery logo (if available)
- `visit-YYYY-MM-DD.jpg` — Photos from specific visits

### Image Sources

**Acceptable sources:**
1. Personal photos from visits (preferred)
2. OpenStreetMap tiles for maps (CC-BY-SA)
3. Unsplash photos (free license)
4. Wikimedia Commons (check individual licenses)
5. TTB official maps (public domain)
6. Press images from wineries (with permission)

**Do NOT use:**
- Google Images / Google Maps screenshots
- Social media photos without permission
- Copyrighted marketing materials

### Attribution

All image sources must be documented in `images/IMAGE_SOURCES.md`.

### Map Generation

Run `scripts/generate-maps.py` to regenerate all region maps from OpenStreetMap tiles:

```bash
python3 scripts/generate-maps.py
```

Maps are 768×768 pixels (3×3 tiles at 256px each).
