#!/usr/bin/env python3
"""
Quick start script - demonstrates the complete workflow with sample data.
This is useful for understanding how the pipeline works before using real datasheets.
"""
import os
import subprocess
import sys

def print_step(step_num, description):
    """Print a formatted step header."""
    print("\n" + "="*70)
    print(f"STEP {step_num}: {description}")
    print("="*70 + "\n")

def run_command(script, description):
    """Run a Python script and display output."""
    print(f"Running: {description}")
    print(f"Script: {script}\n")
    result = subprocess.run([sys.executable, script])
    return result.returncode == 0

def main():
    """Run the quick start demo."""
    print("="*70)
    print("PELTIER DATASHEET ANALYSIS - QUICK START DEMO")
    print("="*70)
    print("\nThis demo will:")
    print("1. Create sample data (simulating manual digitization)")
    print("2. Generate Qc vs COP graphs from the sample data")
    print("3. Show you where to find the results")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled.")
        return 1
    
    # Step 1: Create sample data
    print_step(1, "Creating Sample Data")
    print("In a real scenario, you would:")
    print("  a) Download PDFs using step1_download_datasheets.py")
    print("  b) Extract graphs using step2_extract_graphs.py")
    print("  c) Manually digitize graphs using WebPlotDigitizer")
    print("\nFor this demo, we'll create sample data automatically:\n")
    
    if not run_command("create_sample_data.py", "Create sample data"):
        print("✗ Failed to create sample data")
        return 1
    
    # Step 2: Generate graphs
    print_step(2, "Generating Qc vs COP Graphs")
    print("Now we'll generate the final graphs from the sample data:\n")
    
    if not run_command("step4_generate_graphs.py", "Generate graphs"):
        print("✗ Failed to generate graphs")
        return 1
    
    # Step 3: Show results
    print_step(3, "Results")
    print("✓ Demo completed successfully!\n")
    print("You can find:")
    print("  • Sample data files in: extracted_data/")
    print("  • Generated graphs in: generated_graphs/\n")
    print("Next steps:")
    print("  1. View the generated graphs in the 'generated_graphs/' directory")
    print("  2. Review the sample data format in 'extracted_data/'")
    print("  3. When ready to process real datasheets:")
    print("     - Run: python step1_download_datasheets.py")
    print("     - Run: python step2_extract_graphs.py")
    print("     - Manually digitize graphs (see extracted_data/README.md)")
    print("     - Run: python step4_generate_graphs.py")
    print("\nOr use the pipeline script:")
    print("     python run_pipeline.py --all")
    
    print("\n" + "="*70)
    print("DEMO COMPLETED")
    print("="*70)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
