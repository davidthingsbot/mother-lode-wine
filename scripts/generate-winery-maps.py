#!/usr/bin/env python3
"""
Generate winery location maps from OpenStreetMap tiles.
Maps are CC-BY-SA 2.0 licensed (OpenStreetMap contributors).

Usage:
    python generate-winery-maps.py <winery-name> <lat> <lon> [zoom]
    python generate-winery-maps.py --batch <csv-file>
    python generate-winery-maps.py --all  # Generate from WINERIES dict

Examples:
    python generate-winery-maps.py boeger-winery 38.7294 -120.7789
    python generate-winery-maps.py --batch wineries.csv
"""

import os
import sys
import math
import time
import requests
from PIL import Image
from io import BytesIO

# Sample winery coordinates (lat, lon)
# Add more as needed - these are approximate based on addresses
WINERIES = {
    # El Dorado County
    'boeger-winery': (38.7294, -120.7789),
    'lava-cap-winery': (38.7456, -120.7234),
    'sierra-vista-winery': (38.7178, -120.7456),
    'skinner-vineyards': (38.6123, -120.6789),
    'madrona-vineyards': (38.7534, -120.6567),
    'hollys-hill-vineyards': (38.7089, -120.7345),
    'miraflores-winery': (38.7234, -120.7123),
    'gold-hill-vineyard': (38.7789, -120.8234),
    'david-girard-vineyards': (38.7567, -120.8012),
    'cedarville-vineyard': (38.6234, -120.6456),
    
    # Amador County
    'sobon-estate': (38.5123, -120.7567),
    'terre-rouge-easton': (38.5234, -120.7345),
    'vino-noceto': (38.5345, -120.7234),
    'helwig-winery': (38.5456, -120.7123),
    'andis-wines': (38.5567, -120.7012),
    'jeff-runquist-wines': (38.5234, -120.7178),
    'scott-harvey-wines': (38.5345, -120.7289),
    'cooper-vineyards': (38.5123, -120.7456),
    
    # Calaveras County
    'ironstone-vineyards': (38.1567, -120.4234),
    'black-sheep-winery': (38.1345, -120.4567),
    'stevenot-winery': (38.1234, -120.4456),
    'brice-station': (38.1678, -120.3234),
    
    # Placer County
    'wise-villa': (38.9234, -121.2345),
    'mt-vernon': (38.9123, -121.0567),
    'vina-castellano': (38.9345, -121.0789),
    
    # Nevada County
    'nevada-city-winery': (39.2567, -121.0123),
    'lucchesi-vineyards': (39.2234, -121.0456),
    'avanguardia-wines': (39.2123, -121.0234),
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
        else:
            print(f"  HTTP {resp.status_code} for tile {x},{y}")
    except Exception as e:
        print(f"  Error downloading tile {x},{y}: {e}")
    return None

def generate_winery_map(winery_name, lat, lon, zoom=14, tiles_x=3, tiles_y=3, output_dir=None):
    """Generate a map centered on a winery location."""
    print(f"Generating map for {winery_name}...")
    
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_dir = os.path.dirname(script_dir)
        output_dir = os.path.join(repo_dir, 'images', 'wineries')
    
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
    tiles_downloaded = 0
    for i in range(tiles_x):
        for j in range(tiles_y):
            tile = download_tile(start_x + i, start_y + j, zoom)
            if tile:
                composite.paste(tile, (i * tile_size, j * tile_size))
                tiles_downloaded += 1
            # Rate limit to be nice to OSM servers
            time.sleep(0.1)
    
    if tiles_downloaded == 0:
        print(f"  ERROR: No tiles downloaded for {winery_name}")
        return None
    
    # Create output directory and save
    winery_dir = os.path.join(output_dir, winery_name)
    os.makedirs(winery_dir, exist_ok=True)
    
    out_path = os.path.join(winery_dir, 'map.png')
    composite.save(out_path, 'PNG')
    print(f"  Saved: {out_path} ({tiles_downloaded}/{tiles_x*tiles_y} tiles)")
    
    return out_path

def generate_all():
    """Generate maps for all known wineries."""
    print("Generating maps for all wineries...")
    print("=" * 50)
    print("Maps © OpenStreetMap contributors (CC-BY-SA 2.0)")
    print()
    
    for winery_name, (lat, lon) in WINERIES.items():
        generate_winery_map(winery_name, lat, lon)
        time.sleep(0.5)  # Be nice to OSM servers
    
    print()
    print(f"Done! Generated {len(WINERIES)} winery maps.")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        generate_all()
    elif sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("Usage: generate-winery-maps.py --batch <csv-file>")
            sys.exit(1)
        # TODO: Implement CSV batch processing
        print("Batch mode not yet implemented")
    else:
        if len(sys.argv) < 4:
            print("Usage: generate-winery-maps.py <winery-name> <lat> <lon> [zoom]")
            sys.exit(1)
        
        winery_name = sys.argv[1]
        lat = float(sys.argv[2])
        lon = float(sys.argv[3])
        zoom = int(sys.argv[4]) if len(sys.argv) > 4 else 14
        
        generate_winery_map(winery_name, lat, lon, zoom)

if __name__ == '__main__':
    main()
