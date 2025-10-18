# Peltier Element Analysis

This project analyzes Peltier element datasheets to extract and visualize the relationship between cooling power (Qc) and coefficient of performance (COP) at different temperature differentials (ΔT).

## Overview

The datasheets for Peltier elements typically provide:
- Qc vs ΔT curves at different voltages
- COP vs ΔT curves at different voltages

However, they don't directly show the relationship between Qc and COP. This project extracts data from the datasheets and generates new graphs showing Qc vs COP at various ΔT values, which is useful for element selection when building a cooler.

## Datasheets

The project analyzes three Peltier element models:
- **TEC1-12715**: https://homotix_it.e-mind.it/upld/catalogo/doc/TEC1-12715.PDF
- **TEC1-12712S**: https://www.thermonamic.com/TEC1-12712S-English%2020220526.pdf
- **TEC1-12708**: https://www.thermonamic.com/TEC1-12708-English%2020220521.pdf

## Installation

1. Clone this repository:
```bash
git clone https://github.com/0x53A/peltier.git
cd peltier
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The analysis pipeline consists of 4 steps:

### Quick Start - Run All Steps

```bash
python run_pipeline.py --all
```

### Step-by-Step Execution

#### Step 1: Download Datasheets

Downloads the PDF datasheets from the manufacturers' websites.

```bash
python step1_download_datasheets.py
```

or

```bash
python run_pipeline.py --step 1
```

**Output**: PDF files in `datasheets/` directory

#### Step 2: Extract Graph Images

Extracts graph images from the PDF files.

```bash
python step2_extract_graphs.py
```

or

```bash
python run_pipeline.py --step 2
```

**Output**: PNG images in `extracted_graphs/` directory

#### Step 3: Extract Data Points

This is a **manual/semi-automated step**. The script creates a guide and analyzes the extracted images, but you need to manually digitize the graphs.

```bash
python step3_extract_data.py
```

or

```bash
python run_pipeline.py --step 3
```

**Manual Action Required**:
1. Review the extracted images in `extracted_graphs/`
2. Use [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/) or similar tool to extract data points
3. Save the data as CSV files in `extracted_data/` directory following the naming convention:
   - `{model}_Qc_vs_deltaT_{voltage}V.csv`
   - `{model}_COP_vs_deltaT_{voltage}V.csv`

**CSV Format**:
```csv
deltaT,value
0,50.0
5,48.5
10,45.0
```

See `extracted_data/README.md` for detailed instructions.

#### Step 4: Generate Final Graphs

Creates Qc vs COP plots at different ΔT values.

```bash
python step4_generate_graphs.py
```

or

```bash
python run_pipeline.py --step 4
```

**Output**: Final graphs in `generated_graphs/` directory

## Project Structure

```
peltier/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
├── run_pipeline.py                   # Main pipeline script
├── step1_download_datasheets.py      # Download PDF datasheets
├── step2_extract_graphs.py           # Extract images from PDFs
├── step3_extract_data.py             # Data extraction guide
├── step4_generate_graphs.py          # Generate final plots
├── datasheets/                       # Downloaded PDF files (gitignored)
├── extracted_graphs/                 # Extracted graph images (gitignored)
├── extracted_data/                   # Digitized data CSV files (gitignored)
└── generated_graphs/                 # Final Qc vs COP plots (gitignored)
```

## Dependencies

- `requests` - Download PDF files
- `PyMuPDF` (fitz) - Extract images from PDFs
- `Pillow` - Image processing
- `opencv-python` - Image analysis
- `numpy` - Numerical operations
- `matplotlib` - Graph generation
- `scipy` - Data interpolation

## Workflow

1. **Download** → PDF datasheets downloaded from manufacturer websites
2. **Extract** → Graph images extracted from PDFs
3. **Digitize** → Manual digitization of graphs using WebPlotDigitizer
4. **Generate** → Final Qc vs COP relationship plots created

## Output

The final output is a set of graphs showing the relationship between:
- **X-axis**: COP (Coefficient of Performance)
- **Y-axis**: Qc (Cooling Power in Watts)

With separate plots for different ΔT (temperature differential) values, allowing you to select the optimal Peltier element for your cooler design based on your operating conditions.

## Notes

- Step 3 requires manual digitization because automatic graph digitization from images can be error-prone
- The generated graphs help visualize the trade-off between efficiency (COP) and cooling power (Qc)
- Different ΔT values represent different operating conditions (e.g., 0°C = no temperature difference, 50°C = large temperature difference)

## License

This project is for educational and research purposes. The datasheets are property of their respective manufacturers.
