#!/usr/bin/env python3
"""
Batch generate winery maps by extracting addresses from .md files,
geocoding them, and creating OSM tile maps.
"""

import os
import sys
import re
import math
import time
import json
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

# Rate limiting for APIs
GEOCODE_DELAY = 1.1  # Nominatim requires 1 request per second
TILE_DELAY = 0.15

def extract_address(md_path):
    """Extract address from winery .md file."""
    with open(md_path, 'r') as f:
        content = f.read()
    
    # Look for Address line
    match = re.search(r'\*\*Address:\*\*\s*(.+?)(?:\n|$)', content)
    if match:
        return match.group(1).strip()
    
    # Try alternative formats
    match = re.search(r'Address:\s*(.+?)(?:\n|$)', content)
    if match:
        return match.group(1).strip()
    
    return None

def extract_location(md_path):
    """Extract location (city, county) from winery .md file."""
    with open(md_path, 'r') as f:
        content = f.read()
    
    # Look for Location in overview table
    match = re.search(r'\*\*Location\*\*\s*\|\s*(.+?)(?:\n|$)', content)
    if match:
        return match.group(1).strip()
    
    return None

def geocode_address(address):
    """Geocode an address using Nominatim (OSM)."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'MotherLodeWine/1.0 (wine region documentation project)'}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"    Geocoding error: {e}")
    
    return None, None

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
        print(f"    Tile error: {e}")
    return None

def generate_map(winery_name, lat, lon, output_dir, zoom=14, tiles_x=3, tiles_y=3):
    """Generate a map centered on coordinates."""
    center_x, center_y = deg2num(lat, lon, zoom)
    
    start_x = center_x - tiles_x // 2
    start_y = center_y - tiles_y // 2
    
    tile_size = 256
    width = tiles_x * tile_size
    height = tiles_y * tile_size
    composite = Image.new('RGB', (width, height))
    
    tiles_ok = 0
    for i in range(tiles_x):
        for j in range(tiles_y):
            tile = download_tile(start_x + i, start_y + j, zoom)
            if tile:
                composite.paste(tile, (i * tile_size, j * tile_size))
                tiles_ok += 1
            time.sleep(TILE_DELAY)
    
    if tiles_ok == 0:
        return None
    
    winery_dir = os.path.join(output_dir, winery_name)
    os.makedirs(winery_dir, exist_ok=True)
    
    out_path = os.path.join(winery_dir, 'map.png')
    composite.save(out_path, 'PNG')
    return out_path

# Town center coordinates for fallback
TOWN_CENTERS = {
    'plymouth': (38.4806, -120.8462),
    'amador city': (38.4187, -120.8244),
    'sutter creek': (38.3929, -120.8026),
    'jackson': (38.3486, -120.7744),
    'ione': (38.3529, -120.9328),
    'drytown': (38.4404, -120.8517),
    'fiddletown': (38.4994, -120.7547),
    'placerville': (38.7296, -120.7986),
    'camino': (38.7357, -120.6714),
    'fair play': (38.5987, -120.6088),
    'somerset': (38.6176, -120.6396),
    'shingle springs': (38.6650, -120.9276),
    'el dorado': (38.6840, -120.8415),
    'diamond springs': (38.6935, -120.8362),
    'coloma': (38.8004, -120.8892),
    'murphy': (38.1374, -120.4539),
    'murphys': (38.1374, -120.4539),
    'angels camp': (38.0682, -120.5396),
    'san andreas': (38.1960, -120.6808),
    'vallecito': (38.0909, -120.4766),
    'copperopolis': (37.9811, -120.6414),
    'mokelumne hill': (38.3001, -120.7126),
    'arnold': (38.2548, -120.3521),
    'grass valley': (39.2191, -121.0610),
    'nevada city': (39.2613, -121.0177),
    'penn valley': (39.2188, -121.1769),
    'auburn': (38.8966, -121.0769),
    'lincoln': (38.8913, -121.2930),
    'loomis': (38.8218, -121.1930),
    'newcastle': (38.8759, -121.1324),
    'penryn': (38.8596, -121.1596),
    'rocklin': (38.7907, -121.2357),
    'roseville': (38.7521, -121.2880),
    'lotus': (38.8296, -120.8996),
    'coloma lotus': (38.8004, -120.8892),
    'sonora': (37.9842, -120.3823),
    'jamestown': (37.9529, -120.4226),
    'columbia': (38.0363, -120.4015),
    'marysville': (39.1457, -121.5911),
    'dobbins': (39.3807, -121.2050),
    'oregon house': (39.3571, -121.2019),
    'north san juan': (39.3696, -121.0988),
    'midpines': (37.5607, -119.9753),
    'mariposa': (37.4849, -119.9665),
    'bear valley': (38.4520, -120.0410),
    'mokelumne hill': (38.3001, -120.7126),
}

def get_fallback_coords(winery_name, location_str, county):
    """Get fallback coordinates from town or county center."""
    if location_str:
        # Extract town name from location
        town = location_str.split(',')[0].strip().lower()
        if town in TOWN_CENTERS:
            return TOWN_CENTERS[town]
    
    # County centers
    county_centers = {
        'amador': (38.4500, -120.7800),
        'el-dorado': (38.7000, -120.7500),
        'calaveras': (38.1500, -120.5000),
        'nevada': (39.2500, -121.0300),
        'placer': (38.8800, -121.1500),
        'tuolumne': (38.0000, -120.3500),
        'mariposa': (37.5000, -119.9500),
        'yuba': (39.3500, -121.2000),
    }
    
    if county in county_centers:
        return county_centers[county]
    
    return None, None

def find_wineries_by_county(regions_dir):
    """Find all winery .md files organized by county."""
    wineries = {}
    
    for county_dir in sorted(Path(regions_dir).iterdir()):
        if not county_dir.is_dir():
            continue
        
        county = county_dir.name
        wineries[county] = []
        
        for md_file in sorted(county_dir.glob('*.md')):
            if md_file.name == 'README.md':
                continue
            
            winery_name = md_file.stem
            wineries[county].append({
                'name': winery_name,
                'path': str(md_file),
                'county': county
            })
    
    return wineries

def main():
    script_dir = Path(__file__).parent
    repo_dir = script_dir.parent
    regions_dir = repo_dir / 'regions'
    images_dir = repo_dir / 'images' / 'wineries'
    
    # Get existing maps
    existing_maps = set()
    for map_file in images_dir.glob('*/map.png'):
        existing_maps.add(map_file.parent.name)
    
    print(f"Found {len(existing_maps)} existing maps")
    
    # Find all wineries
    wineries = find_wineries_by_county(regions_dir)
    
    # Track results
    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }
    
    for county, winery_list in wineries.items():
        print(f"\n{'='*60}")
        print(f"COUNTY: {county.upper()}")
        print(f"{'='*60}")
        
        for winery in winery_list:
            name = winery['name']
            
            if name in existing_maps:
                print(f"  ✓ {name} — already has map")
                results['skipped'].append(name)
                continue
            
            print(f"\n  Processing: {name}")
            
            # Extract address
            address = extract_address(winery['path'])
            location = extract_location(winery['path'])
            
            lat, lon = None, None
            
            if address:
                print(f"    Address: {address}")
                time.sleep(GEOCODE_DELAY)
                lat, lon = geocode_address(address)
                if lat:
                    print(f"    Geocoded: {lat:.4f}, {lon:.4f}")
            
            if not lat:
                # Try fallback
                lat, lon = get_fallback_coords(name, location, county)
                if lat:
                    print(f"    Fallback coords: {lat:.4f}, {lon:.4f}")
            
            if not lat:
                print(f"    ✗ Could not get coordinates")
                results['failed'].append(name)
                continue
            
            # Generate map
            out_path = generate_map(name, lat, lon, str(images_dir))
            if out_path:
                print(f"    ✓ Created: {out_path}")
                results['success'].append({'name': name, 'lat': lat, 'lon': lon})
            else:
                print(f"    ✗ Failed to generate map")
                results['failed'].append(name)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Success: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"Skipped (existing): {len(results['skipped'])}")
    
    if results['failed']:
        print(f"\nFailed wineries:")
        for name in results['failed']:
            print(f"  - {name}")
    
    # Save results for IMAGE_SOURCES update
    with open(repo_dir / 'map-generation-results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
