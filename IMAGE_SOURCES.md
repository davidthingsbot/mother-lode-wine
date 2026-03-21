# Image Sources

This file documents the sources and licensing for images used in this project.

## Winery Location Maps

All winery location maps in `images/wineries/*/map.png` are generated from OpenStreetMap tiles.

- **Source:** OpenStreetMap (https://www.openstreetmap.org)
- **License:** CC BY-SA 2.0 (Creative Commons Attribution-ShareAlike 2.0)
- **Attribution:** © OpenStreetMap contributors
- **Tile Server:** https://tile.openstreetmap.org
- **Generated:** March 2026

### Generation Details

Maps are 768×768 pixels (3×3 grid of 256px tiles) at zoom level 14, centered on winery coordinates.

Generated using `scripts/generate-winery-maps.py` and `scripts/batch-generate-maps.py`.

### Map Coverage

| County | Wineries with Maps |
|--------|-------------------|
| Amador | 35 |
| Calaveras | 20 |
| El Dorado | 36 |
| Mariposa | 2 |
| Nevada | 6 |
| Placer | 16 |
| Tuolumne | 2 |
| Yuba | 2 |
| **Total** | **121** |

## Winery Photos

All winery photos in `images/wineries/*/photo.jpg` are sourced from:

### Unsplash
- **Source:** https://unsplash.com
- **License:** Unsplash License (free for commercial and non-commercial use)
- **Photos Used:** Vineyard rows, wine grapes, wine barrels, winery buildings, hillside vineyards
- **Generated:** March 2026

### Lorem Picsum (Fallback)
- **Source:** https://picsum.photos
- **License:** Unsplash License (images sourced from Unsplash)
- **Usage:** Fallback for wineries where direct Unsplash URLs failed
- **Generated:** March 2026

### Photo Coverage

All 121 wineries now have photos in `images/wineries/*/photo.jpg`.

## Other Images

### wine-barrels.jpg
- **Location:** `images/wineries/wine-barrels.jpg`
- **Source:** Stock photo (placeholder)
- **Usage:** General decoration

---

*When adding new images, document their source and license here.*
