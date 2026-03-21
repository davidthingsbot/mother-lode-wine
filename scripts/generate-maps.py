#!/usr/bin/env python3
"""
Generate region maps from OpenStreetMap tiles.
Maps are CC-BY-SA 2.0 licensed (OpenStreetMap contributors).
"""

import os
import math
import requests
from PIL import Image
from io import BytesIO

# Region definitions: name, center_lat, center_lon, zoom
REGIONS = {
    'sierra-foothills': (38.45, -120.45, 8),   # Full region overview
    'el-dorado': (38.75, -120.55, 10),
    'amador': (38.42, -120.65, 10),
    'calaveras': (38.15, -120.55, 10),
    'placer': (38.95, -121.05, 10),
    'nevada': (39.25, -121.00, 10),
    'yuba': (39.35, -121.20, 10),
    'tuolumne': (37.95, -120.20, 10),
    'mariposa': (37.55, -119.95, 10),
}

def deg2num(lat_deg, lon_deg, zoom):
    """Convert lat/lon to tile numbers."""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_tile(x, y, z):
    """Download a single OSM tile."""
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    headers = {'User-Agent': 'MotherLodeWine/1.0 (wine region documentation project)'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return Image.open(BytesIO(resp.content))
    except Exception as e:
        print(f"  Error downloading tile {x},{y}: {e}")
    return None

def generate_map(name, lat, lon, zoom, tiles_x=3, tiles_y=3, output_dir='images/regions'):
    """Generate a composite map for a region."""
    print(f"Generating map for {name}...")
    
    # Get center tile
    center_x, center_y = deg2num(lat, lon, zoom)
    
    # Calculate tile range
    start_x = center_x - tiles_x // 2
    start_y = center_y - tiles_y // 2
    
    # Create composite image
    tile_size = 256
    width = tiles_x * tile_size
    height = tiles_y * tile_size
    composite = Image.new('RGB', (width, height))
    
    # Download and stitch tiles
    for i in range(tiles_x):
        for j in range(tiles_y):
            tile = download_tile(start_x + i, start_y + j, zoom)
            if tile:
                composite.paste(tile, (i * tile_size, j * tile_size))
    
    # Determine output path
    if name == 'sierra-foothills':
        out_path = os.path.join(output_dir, f'{name}-map.png')
    else:
        out_path = os.path.join(output_dir, name, 'map.png')
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    composite.save(out_path, 'PNG')
    print(f"  Saved: {out_path}")
    return out_path

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(repo_dir, 'images', 'regions')
    
    print("Mother Lode Wine Region Map Generator")
    print("=" * 40)
    print("Maps © OpenStreetMap contributors (CC-BY-SA 2.0)")
    print()
    
    for name, (lat, lon, zoom) in REGIONS.items():
        generate_map(name, lat, lon, zoom, output_dir=output_dir)
    
    print()
    print("Done! All maps generated.")

if __name__ == '__main__':
    main()
