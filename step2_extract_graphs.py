#!/usr/bin/env python3
"""
Step 2: Extract graph images from PDF datasheets
Extracts relevant graphs (Qc/V and COP/V vs delta T) from the PDFs and saves them as images.
"""
import os
import fitz  # PyMuPDF
from pathlib import Path
from PIL import Image
import io

def extract_graphs_from_pdf(pdf_path, output_dir):
    """Extract images from a PDF file."""
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    pdf_output_dir = os.path.join(output_dir, pdf_name)
    Path(pdf_output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"\nProcessing {pdf_name}...")
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    image_count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract images from the page
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            
            # Extract the image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Convert to PIL Image to check if it's substantial (likely a graph)
            pil_image = Image.open(io.BytesIO(image_bytes))
            width, height = pil_image.size
            
            # Filter out small images (likely not graphs)
            if width > 200 and height > 200:
                image_count += 1
                output_path = os.path.join(pdf_output_dir, f"page{page_num + 1}_img{img_index + 1}.png")
                pil_image.save(output_path, "PNG")
                print(f"  Saved: page{page_num + 1}_img{img_index + 1}.png ({width}x{height})")
    
    doc.close()
    print(f"  Total images extracted: {image_count}")
    return image_count

def extract_all_graphs(datasheets_dir='datasheets', output_dir='extracted_graphs'):
    """Extract graphs from all PDF datasheets."""
    Path(output_dir).mkdir(exist_ok=True)
    
    pdf_files = sorted(Path(datasheets_dir).glob('*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in '{datasheets_dir}' directory")
        return
    
    total_images = 0
    for pdf_file in pdf_files:
        count = extract_graphs_from_pdf(str(pdf_file), output_dir)
        total_images += count
    
    print(f"\n✓ Total images extracted: {total_images}")
    print(f"✓ Images saved to '{output_dir}' directory")

if __name__ == '__main__':
    extract_all_graphs()
