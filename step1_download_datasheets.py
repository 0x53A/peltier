#!/usr/bin/env python3
"""
Step 1: Download Peltier element datasheets
Downloads the three PDF datasheets and saves them to the datasheets folder.
"""
import os
import requests
from pathlib import Path

# Define the datasheet URLs
DATASHEETS = {
    'TEC1-12715.pdf': 'https://homotix_it.e-mind.it/upld/catalogo/doc/TEC1-12715.PDF',
    'TEC1-12712S.pdf': 'https://www.thermonamic.com/TEC1-12712S-English%2020220526.pdf',
    'TEC1-12708.pdf': 'https://www.thermonamic.com/TEC1-12708-English%2020220521.pdf'
}

def download_datasheets(output_dir='datasheets'):
    """Download all datasheets to the specified directory."""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    for filename, url in DATASHEETS.items():
        output_path = os.path.join(output_dir, filename)
        
        # Skip if already downloaded
        if os.path.exists(output_path):
            print(f"✓ {filename} already exists, skipping download")
            continue
        
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Successfully downloaded {filename}")
        except Exception as e:
            print(f"✗ Failed to download {filename}: {e}")
    
    print(f"\nAll datasheets downloaded to '{output_dir}' directory")

if __name__ == '__main__':
    download_datasheets()
