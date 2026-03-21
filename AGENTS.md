# AGENTS.md — Winery File Format

This document defines the standard format for winery entries in this repository.

## File Location

Wineries are organized by county/region:

```
regions/
  el-dorado/
    boeger-winery.md
    lava-cap-winery.md
  amador/
    sobon-estate.md
    terre-rouge.md
  calaveras/
    ironstone-vineyards.md
```

## File Naming

- Lowercase, hyphenated: `winery-name.md`
- Use the winery's common name, not corporate entity
- Examples: `boeger-winery.md`, `terre-rouge.md`, `jeff-runquist-wines.md`

## Winery File Template

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

Highlight 2-3 standout bottles.

## Vineyards

Estate vineyard details, soil types, exposures, notable blocks.

## History

Brief history of the winery.

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

## Required Fields

At minimum, every winery file should have:

1. **Name** (H1 header)
2. **Location** (city, county)
3. **Contact** (at least website or phone)
4. **Wines** (at least a partial list)

## Optional Sections

- Vineyards (for estate wineries)
- History (for historically significant wineries)
- Notes (personal observations)
- Rating (subjective, can omit)

## Tags / Metadata

For future searchability, consider including in the Overview table:

- **Style:** Old World / New World / Natural / etc.
- **Focus:** Zinfandel specialist / Rhône / Italian / etc.
- **Price Range:** $ / $$ / $$$ / $$$$
- **Tasting Fee:** $X (waived with purchase?)

## Region Files

Each region folder should have an `_index.md` with:

- Brief region overview
- AVA information (if applicable)
- Map or geographic notes
- List of wineries in the region

Example: `regions/el-dorado/_index.md`

## Conventions

- Use **bold** for wine names in lists
- Use standard varietal spellings (Zinfandel, not zin)
- Include vintage years when known
- Note if a winery is closed, sold, or defunct
- Update "Last updated" when making changes
