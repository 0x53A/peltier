#!/usr/bin/env python3
"""
Test script to verify the pipeline works correctly.
"""
import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import step1_download_datasheets
        import step2_extract_graphs
        import step3_extract_data
        import step4_generate_graphs
        import create_sample_data
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_sample_data_generation():
    """Test sample data generation."""
    print("\nTesting sample data generation...")
    import create_sample_data
    
    # Clean up previous test data
    test_dir = '/tmp/test_extracted_data'
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)
    
    create_sample_data.create_sample_data_files(test_dir)
    
    # Check that files were created
    expected_files = 10  # 5 models × 2 file types
    csv_files = list(Path(test_dir).glob('*.csv'))
    
    if len(csv_files) >= expected_files:
        print(f"✓ Generated {len(csv_files)} data files")
        return True
    else:
        print(f"✗ Expected at least {expected_files} files, got {len(csv_files)}")
        return False

def test_graph_generation():
    """Test graph generation from sample data."""
    print("\nTesting graph generation...")
    import step4_generate_graphs
    
    # Use the test data
    test_input_dir = '/tmp/test_extracted_data'
    test_output_dir = '/tmp/test_generated_graphs'
    
    if os.path.exists(test_output_dir):
        import shutil
        shutil.rmtree(test_output_dir)
    
    step4_generate_graphs.generate_qc_vs_cop_plots(test_input_dir, test_output_dir)
    
    # Check that graphs were created
    png_files = list(Path(test_output_dir).glob('*.png'))
    
    if len(png_files) >= 2:  # At least 2 models
        print(f"✓ Generated {len(png_files)} graph files")
        return True
    else:
        print(f"✗ Expected at least 2 graphs, got {len(png_files)}")
        return False

def test_pipeline_script():
    """Test that the main pipeline script can be executed."""
    print("\nTesting pipeline script...")
    import run_pipeline
    print("✓ Pipeline script imported successfully")
    return True

def main():
    """Run all tests."""
    print("="*60)
    print("PELTIER PIPELINE TEST SUITE")
    print("="*60)
    
    tests = [
        test_imports,
        test_sample_data_generation,
        test_graph_generation,
        test_pipeline_script,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {sum(results)}/{len(results)} passed")
    print("="*60)
    
    if all(results):
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
