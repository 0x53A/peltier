#!/usr/bin/env python3
"""
Step 3: Extract data points from graph images
Uses image processing to digitize the graph data points and save them to text files.
This is a manual/semi-automated step - the user may need to adjust parameters or
manually digitize complex graphs using tools like WebPlotDigitizer.
"""
import os
import cv2
import numpy as np
from pathlib import Path
import json

def analyze_graph_image(image_path):
    """
    Analyze a graph image and provide information about it.
    For actual data extraction, manual digitization is recommended.
    """
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"  Could not load image: {image_path}")
        return None
    
    height, width = img.shape[:2]
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect edges
    edges = cv2.Canny(gray, 50, 150)
    
    # Count edge pixels (rough estimate of graph complexity)
    edge_count = np.count_nonzero(edges)
    
    return {
        'filename': os.path.basename(image_path),
        'dimensions': f"{width}x{height}",
        'edge_pixels': edge_count,
        'complexity': 'high' if edge_count > 10000 else 'medium' if edge_count > 5000 else 'low'
    }

def create_manual_digitization_guide(graphs_dir='extracted_graphs', output_dir='extracted_data'):
    """
    Create a guide for manual digitization of graphs.
    Since automatic graph digitization is complex and error-prone,
    this creates a template for manual data entry.
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    # Create a README for the data extraction process
    readme_path = os.path.join(output_dir, 'README.md')
    
    readme_content = """# Graph Data Extraction Guide

## Manual Digitization Recommended

For accurate data extraction from the Peltier element datasheets, manual digitization is recommended.

### Tools
- **WebPlotDigitizer** (https://automeris.io/WebPlotDigitizer/) - Free online tool
- **Engauge Digitizer** - Desktop application

### Process
1. Load each graph image from the `extracted_graphs/` directory
2. Define the axes ranges based on the graph labels
3. Click on data points along each curve
4. Export the data in CSV or JSON format
5. Save to this directory with descriptive filenames

### Required Data

For each TEC model, we need to extract:

1. **Qc vs ΔT curves** at different voltages
   - X-axis: ΔT (Temperature difference in °C)
   - Y-axis: Qc (Cooling power in Watts)
   - Multiple curves for different voltages

2. **COP vs ΔT curves** at different voltages
   - X-axis: ΔT (Temperature difference in °C)
   - Y-axis: COP (Coefficient of Performance)
   - Multiple curves for different voltages

### File Naming Convention
- `{model}_Qc_vs_deltaT_{voltage}V.csv`
- `{model}_COP_vs_deltaT_{voltage}V.csv`

Example: `TEC1-12715_Qc_vs_deltaT_12V.csv`

### CSV Format
```
deltaT,value
0,50.5
10,45.2
20,38.7
...
```
"""
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Created digitization guide: {readme_path}")
    
    # Analyze all extracted images
    print("\n" + "="*60)
    print("GRAPH IMAGE ANALYSIS")
    print("="*60)
    
    graphs_path = Path(graphs_dir)
    image_files = sorted(graphs_path.glob('**/*.png'))
    
    if not image_files:
        print(f"No images found in '{graphs_dir}' directory")
        return
    
    for img_path in image_files:
        analysis = analyze_graph_image(str(img_path))
        if analysis:
            relative_path = img_path.relative_to(graphs_path)
            print(f"\n{relative_path}")
            print(f"  Dimensions: {analysis['dimensions']}")
            print(f"  Complexity: {analysis['complexity']}")
    
    # Create example data template
    example_data_path = os.path.join(output_dir, 'example_data_template.csv')
    example_content = """# Example data file format
# deltaT (°C), value (Qc in W or COP dimensionless)
0,50.0
5,48.5
10,45.0
15,40.0
20,33.5
25,25.0
30,14.5
"""
    
    with open(example_data_path, 'w') as f:
        f.write(example_content)
    
    print(f"\n✓ Created example data template: {example_data_path}")
    print(f"\n{'='*60}")
    print("Next Steps:")
    print("1. Review the extracted images in 'extracted_graphs/' directory")
    print("2. Use WebPlotDigitizer or similar tool to extract data")
    print("3. Save the data files to 'extracted_data/' directory")
    print("4. Run step4_generate_graphs.py to create the final plots")
    print("="*60)

if __name__ == '__main__':
    create_manual_digitization_guide()
