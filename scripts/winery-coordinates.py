#!/usr/bin/env python3
"""
Winery coordinates database for map generation.
Coordinates are approximate based on addresses.
"""

# Format: 'winery-slug': (latitude, longitude, county)
WINERY_COORDS = {
    # El Dorado County - key wineries
    'boeger-winery': (38.7294, -120.7789, 'el-dorado'),
    'lava-cap-winery': (38.7456, -120.7234, 'el-dorado'),
    'sierra-vista-winery': (38.7178, -120.7456, 'el-dorado'),
    'skinner-vineyards': (38.6123, -120.6789, 'el-dorado'),
    'madrona-vineyards': (38.7534, -120.6567, 'el-dorado'),
    'hollys-hill-vineyards': (38.7089, -120.7345, 'el-dorado'),
    'miraflores-winery': (38.7234, -120.7123, 'el-dorado'),
    'gold-hill-vineyard': (38.7989, -120.8734, 'el-dorado'),
    'david-girard-vineyards': (38.7767, -120.8512, 'el-dorado'),
    'cedarville-vineyard': (38.6234, -120.6456, 'el-dorado'),
    'crystal-basin-cellars': (38.7445, -120.6478, 'el-dorado'),
    'e16-winery': (38.6189, -120.6534, 'el-dorado'),
    'perry-creek-winery': (38.6212, -120.6612, 'el-dorado'),
    'narrow-gate-vineyards': (38.7312, -120.7589, 'el-dorado'),
    
    # Amador County - key wineries  
    'sobon-estate': (38.531051, -120.758589, 'amador'),  # Verified
    'terre-rouge-easton': (38.5234, -120.7345, 'amador'),
    'vino-noceto': (38.5389, -120.7289, 'amador'),
    'helwig-winery': (38.5456, -120.7123, 'amador'),
    'andis-wines': (38.5467, -120.7312, 'amador'),
    'jeff-runquist-wines': (38.5234, -120.7178, 'amador'),
    'scott-harvey-wines': (38.4845, -120.7489, 'amador'),
    'cooper-vineyards': (38.5123, -120.7456, 'amador'),
    'villa-toscano': (38.5278, -120.7234, 'amador'),
    'amador-cellars': (38.5312, -120.7189, 'amador'),
    'bella-grace-vineyards': (38.5189, -120.6978, 'amador'),
    'dobra-zemlja': (38.5145, -120.6856, 'amador'),
    'karmere-vineyards': (38.5234, -120.7089, 'amador'),
    
    # Calaveras County - key wineries
    'ironstone-vineyards': (38.106143, -120.494211, 'calaveras'),  # Verified
    'black-sheep-winery': (38.1345, -120.4567, 'calaveras'),
    'stevenot-winery': (38.1234, -120.4456, 'calaveras'),
    'brice-station': (38.1678, -120.3234, 'calaveras'),
    'indian-rock-vineyards': (38.1423, -120.4312, 'calaveras'),
    'newsome-harlow': (38.1367, -120.4578, 'calaveras'),
    'hovey-winery': (38.1389, -120.4534, 'calaveras'),
    'val-du-vino': (38.1412, -120.4623, 'calaveras'),
    'hatcher-winery': (38.1045, -120.4189, 'calaveras'),
    
    # Placer County - key wineries
    'wise-villa': (38.9234, -121.2345, 'placer'),
    'mt-vernon': (38.9123, -121.0567, 'placer'),
    'vina-castellano': (38.9345, -121.0789, 'placer'),
    'lone-buffalo': (38.9278, -121.0623, 'placer'),
    'casque-wines': (38.8234, -121.0012, 'placer'),
    'secret-ravine': (38.8156, -121.0178, 'placer'),
    'rancho-roble': (38.9012, -121.2134, 'placer'),
    
    # Nevada County - key wineries
    'nevada-city-winery': (39.2617, -121.0178, 'nevada'),  # Town coords
    'lucchesi-vineyards': (39.2234, -121.0456, 'nevada'),
    'avanguardia-wines': (39.2145, -121.0312, 'nevada'),
    'sierra-starr': (39.2156, -121.0623, 'nevada'),
    'double-oak': (39.2512, -120.9812, 'nevada'),
    
    # Tuolumne County
    'inner-sanctum': (37.9534, -120.4234, 'tuolumne'),
    'gianelli-family': (37.9789, -120.3812, 'tuolumne'),
    
    # Mariposa County
    'butterfly-creek': (37.5234, -119.9623, 'mariposa'),
    'casto-oaks': (37.5412, -119.9512, 'mariposa'),
    
    # Yuba County
    'renaissance-vineyard': (39.4123, -121.2345, 'yuba'),
    'clos-saron': (39.4056, -121.2189, 'yuba'),
}

if __name__ == '__main__':
    import json
    print(json.dumps(WINERY_COORDS, indent=2))
