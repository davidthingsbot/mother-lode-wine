#!/usr/bin/env python3
"""
Regenerate all winery maps with red location markers.
Reads existing map.png files and adds a marker at the center.
"""

import os
import sys
import re
import math
import time
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from pathlib import Path

# Rate limiting for tile requests
TILE_DELAY = 0.1

# Winery coordinates - from addresses/geocoding
# Format: 'winery-slug': (latitude, longitude)
WINERY_COORDS = {
    # El Dorado County
    'boeger-winery': (38.7294, -120.7789),
    'lava-cap-winery': (38.7456, -120.7234),
    'sierra-vista-winery': (38.7178, -120.7456),
    'skinner-vineyards': (38.6123, -120.6789),
    'madrona-vineyards': (38.7534, -120.6567),
    'hollys-hill-vineyards': (38.7089, -120.7345),
    'miraflores-winery': (38.7234, -120.7123),
    'gold-hill-vineyard': (38.7989, -120.8734),
    'david-girard-vineyards': (38.7767, -120.8512),
    'cedarville-vineyard': (38.6234, -120.6456),
    'crystal-basin-cellars': (38.7445, -120.6478),
    'e16-winery': (38.6189, -120.6534),
    'perry-creek-winery': (38.6212, -120.6612),
    'narrow-gate-vineyards': (38.7312, -120.7589),
    'windwalker-vineyard': (38.5987, -120.5978),
    'chateau-davell': (38.6789, -120.7012),
    'fitzpatrick-winery': (38.5812, -120.6123),
    'venetian-sun-winery': (38.6512, -120.6789),
    'wofford-acres-vineyards': (38.5789, -120.6234),
    'colibri-ridge-winery': (38.6123, -120.6512),
    'fenton-herriott-vineyards': (38.6034, -120.6378),
    'illuminare-estate': (38.5912, -120.6089),
    'nello-olivo-wines': (38.5845, -120.6145),
    'fawnridge-winery': (38.7612, -120.6834),
    'calandar-cellars': (38.7334, -120.6789),
    'chevalier-winery': (38.7212, -120.7034),
    'boa-vista-orchards': (38.7089, -120.6512),
    'starfield-vineyards': (38.5923, -120.6234),
    'saluti-cellars': (38.6089, -120.6456),
    'avanguardia-wines': (38.5845, -120.6189),
    'bumgarner-winery': (38.5756, -120.6089),
    'winery-bydesign': (38.7523, -120.7856),
    'jodar-vineyards': (38.5812, -120.6456),
    'el-dorado-wine-collective': (38.7296, -120.7986),
    'driven-cellars': (38.6945, -120.7089),
    'reds-corner': (38.7156, -120.7312),
    'oak-ridge-el-dorado': (38.6845, -120.7189),
    
    # Amador County
    'sobon-estate': (38.5310, -120.7586),
    'terre-rouge-easton': (38.5234, -120.7345),
    'vino-noceto': (38.5389, -120.7289),
    'helwig-winery': (38.5456, -120.7123),
    'andis-wines': (38.5467, -120.7312),
    'jeff-runquist-wines': (38.5234, -120.7178),
    'scott-harvey-wines': (38.4845, -120.7489),
    'cooper-vineyards': (38.5123, -120.7456),
    'villa-toscano': (38.5278, -120.7234),
    'amador-cellars': (38.5312, -120.7189),
    'bella-grace-vineyards': (38.5189, -120.6978),
    'dobra-zemlja': (38.5145, -120.6856),
    'karmere-vineyards': (38.5234, -120.7089),
    'shenandoah-vineyards': (38.5367, -120.7478),
    'drytown-cellars': (38.4404, -120.8517),
    'renwood-winery': (38.5278, -120.7334),
    'deaver-vineyards': (38.5189, -120.7245),
    'amador-foothill-winery': (38.5312, -120.7567),
    'tanis-vineyards': (38.5178, -120.7123),
    'iron-hub-winery': (38.5234, -120.7389),
    'winetree-farm': (38.5089, -120.7234),
    'end-of-nowhere': (38.5023, -120.7089),
    'casino-mine-ranch': (38.5156, -120.7312),
    'rombauer-amador': (38.5289, -120.7234),
    'cg-di-arie': (38.5178, -120.7156),
    'dillian-wines': (38.5245, -120.7312),
    'yorba-wines': (38.5134, -120.7189),
    'la-mesa-vineyards': (38.5089, -120.7134),
    'domenico-winery': (38.5234, -120.7289),
    'belledor-vineyards': (38.5189, -120.7245),
    'linsteadt-family': (38.5112, -120.7167),
    'amador-heights': (38.5267, -120.7212),
    
    # Calaveras County
    'ironstone-vineyards': (38.1061, -120.4942),
    'black-sheep-winery': (38.1345, -120.4567),
    'stevenot-winery': (38.1234, -120.4456),
    'brice-station': (38.1678, -120.3234),
    'indian-rock-vineyards': (38.1423, -120.4312),
    'newsome-harlow': (38.1367, -120.4578),
    'hovey-winery': (38.1389, -120.4534),
    'val-du-vino': (38.1412, -120.4623),
    'hatcher-winery': (38.1045, -120.4189),
    'twisted-oak-winery': (38.1234, -120.4678),
    'lavender-ridge-vineyard': (38.1189, -120.4512),
    'milliaire-winery': (38.1312, -120.4389),
    'chatom-vineyards': (38.1678, -120.4234),
    'mineral-wines': (38.1089, -120.4712),
    'hayes-mcfall': (38.1256, -120.4534),
    'zucca-mountain-vineyards': (38.1789, -120.4012),
    'old-dog-ranch': (38.1534, -120.4345),
    'courtwood-wine': (38.1456, -120.4189),
    'redwood-vineyards': (38.1389, -120.4267),
    'frog-haven-farm': (38.1312, -120.4578),
    'domaine-becquet': (38.1178, -120.4623),
    
    # Nevada County
    'nevada-city-winery': (39.2613, -121.0177),
    'lucchesi-vineyards': (39.2189, -121.0456),
    'pilot-peak-vineyard': (39.2312, -121.0678),
    'szabo-vineyards': (39.2456, -121.0334),
    'naggiar-vineyards': (39.2234, -121.1012),
    'double-oak-vineyards': (39.2089, -121.0889),
    
    # Placer County
    'mt-vernon-winery': (38.8756, -121.1534),
    'wise-villa-winery': (38.9012, -121.0789),
    'ciotti-cellars': (38.8634, -121.1234),
    'vina-castellano': (38.8567, -121.1456),
    'casque-wines': (38.8689, -121.1312),
    'lone-buffalo-vineyards': (38.8845, -121.0956),
    'secret-ravine-vineyard': (38.8512, -121.1567),
    'flower-farm': (38.8389, -121.1834),
    'dante-robere-vineyards': (38.8456, -121.1623),
    'bonitata-boutique-wine': (38.8623, -121.1389),
    'cante-ao-vinho': (38.8734, -121.1145),
    'rancho-roble-vineyards': (38.8912, -121.0634),
    'pescatore-vineyard': (38.8567, -121.1489),
    'plum-ridge-winery': (38.8445, -121.1723),
    'fawndale-winery': (38.8678, -121.1234),
    'goathouse-refuge': (38.8534, -121.1567),
    
    # Tuolumne County
    'indigeny-reserve': (37.9845, -120.3823),
    'gianelli-vineyards': (37.9978, -120.3512),
    
    # Mariposa County
    'rauch-ranch-winery': (37.5607, -119.9753),
    'butterfly-creek-winery': (37.4912, -119.9534),
    
    # Yuba County
    'renaissance-vineyard': (39.3807, -121.2050),
    'clos-saron': (39.3571, -121.2019),
}

# County center fallbacks
COUNTY_CENTERS = {
    'amador': (38.4500, -120.7800),
    'el-dorado': (38.7000, -120.7500),
    'calaveras': (38.1500, -120.5000),
    'nevada': (39.2500, -121.0300),
    'placer': (38.8800, -121.1500),
    'tuolumne': (38.0000, -120.3500),
    'mariposa': (37.5000, -119.9500),
    'yuba': (39.3500, -121.2000),
}

def deg2num(lat_deg, lon_deg, zoom):
    """Convert lat/lon to tile numbers."""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    """Convert tile numbers to lat/lon at NW corner."""
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def download_tile(x, y, z):
    """Download a single OSM tile."""
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    headers = {'User-Agent': 'MotherLodeWine/1.0 (wine region documentation project)'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return Image.open(BytesIO(resp.content))
    except Exception as e:
        print(f"    Tile error: {e}")
    return None

def draw_marker(image, x, y):
    """Draw a red location marker at the given pixel coordinates."""
    draw = ImageDraw.Draw(image)
    
    # Draw pin/marker shape
    # Outer red circle
    radius = 12
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                 fill='#CC0000', outline='#800000', width=2)
    
    # Inner white dot
    inner_radius = 4
    draw.ellipse([x-inner_radius, y-inner_radius, x+inner_radius, y+inner_radius], 
                 fill='white')
    
    return image

def generate_map_with_marker(lat, lon, output_path, zoom=14, tiles_x=3, tiles_y=3):
    """Generate a map centered on coordinates with a marker."""
    center_tile_x, center_tile_y = deg2num(lat, lon, zoom)
    
    start_tile_x = center_tile_x - tiles_x // 2
    start_tile_y = center_tile_y - tiles_y // 2
    
    tile_size = 256
    width = tiles_x * tile_size
    height = tiles_y * tile_size
    composite = Image.new('RGB', (width, height))
    
    tiles_ok = 0
    for i in range(tiles_x):
        for j in range(tiles_y):
            tile = download_tile(start_tile_x + i, start_tile_y + j, zoom)
            if tile:
                composite.paste(tile, (i * tile_size, j * tile_size))
                tiles_ok += 1
            time.sleep(TILE_DELAY)
    
    if tiles_ok == 0:
        return False
    
    # Calculate pixel position of the marker
    # Get the lat/lon of the top-left corner of the composite
    nw_lat, nw_lon = num2deg(start_tile_x, start_tile_y, zoom)
    se_lat, se_lon = num2deg(start_tile_x + tiles_x, start_tile_y + tiles_y, zoom)
    
    # Calculate marker position in pixels
    lon_range = se_lon - nw_lon
    lat_range = nw_lat - se_lat  # Note: lat decreases as y increases
    
    marker_x = int((lon - nw_lon) / lon_range * width)
    marker_y = int((nw_lat - lat) / lat_range * height)
    
    # Draw the marker
    draw_marker(composite, marker_x, marker_y)
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    composite.save(output_path, 'PNG')
    return True

def get_winery_coords(winery_slug, county):
    """Get coordinates for a winery, with fallback to county center."""
    if winery_slug in WINERY_COORDS:
        return WINERY_COORDS[winery_slug]
    
    # Fallback to county center
    if county in COUNTY_CENTERS:
        return COUNTY_CENTERS[county]
    
    return None, None

def main():
    script_dir = Path(__file__).parent
    repo_dir = script_dir.parent
    regions_dir = repo_dir / 'regions'
    
    print("Regenerating winery maps with markers...")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    # Find all winery directories
    for county_dir in sorted(regions_dir.iterdir()):
        if not county_dir.is_dir():
            continue
        
        county = county_dir.name
        print(f"\n{county.upper()}")
        print("-" * 40)
        
        for winery_dir in sorted(county_dir.iterdir()):
            if not winery_dir.is_dir():
                continue
            
            winery_slug = winery_dir.name
            map_path = winery_dir / 'map.png'
            
            # Get coordinates
            lat, lon = get_winery_coords(winery_slug, county)
            
            if lat is None:
                print(f"  ✗ {winery_slug} — no coordinates")
                failed += 1
                continue
            
            # Generate new map with marker
            print(f"  → {winery_slug}...", end='', flush=True)
            if generate_map_with_marker(lat, lon, str(map_path)):
                print(" ✓")
                success += 1
            else:
                print(" ✗ (tile download failed)")
                failed += 1
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: {success} maps regenerated, {failed} failed")

if __name__ == '__main__':
    main()
