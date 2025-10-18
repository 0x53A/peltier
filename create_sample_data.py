#!/usr/bin/env python3
"""
Create sample data files for testing the pipeline.
This demonstrates the expected format of data files after manual digitization.
"""
import os
import numpy as np
from pathlib import Path

def create_sample_data_files(output_dir='extracted_data'):
    """Create sample data files that simulate manually digitized graphs."""
    Path(output_dir).mkdir(exist_ok=True)
    
    print("Creating sample data files for testing...")
    
    # Sample data for TEC1-12715
    # Qc data at 12V (example values)
    deltaT = np.array([0, 10, 20, 30, 40, 50, 60])
    qc_12v = np.array([50.0, 45.0, 38.0, 29.0, 18.0, 5.0, 0.0])
    qc_10v = np.array([42.0, 38.0, 32.0, 24.0, 15.0, 4.0, 0.0])
    qc_8v = np.array([34.0, 31.0, 26.0, 20.0, 12.0, 3.0, 0.0])
    
    # COP data at different voltages (example values)
    cop_12v = np.array([0.8, 1.2, 1.4, 1.3, 0.9, 0.3, 0.0])
    cop_10v = np.array([0.9, 1.3, 1.5, 1.4, 1.0, 0.4, 0.0])
    cop_8v = np.array([1.0, 1.4, 1.6, 1.5, 1.1, 0.5, 0.0])
    
    files_created = []
    
    # TEC1-12715
    for voltage, qc_data, cop_data in [(12, qc_12v, cop_12v), 
                                        (10, qc_10v, cop_10v), 
                                        (8, qc_8v, cop_8v)]:
        # Qc file
        qc_filename = f'TEC1-12715_Qc_vs_deltaT_{voltage}V.csv'
        qc_path = os.path.join(output_dir, qc_filename)
        with open(qc_path, 'w') as f:
            f.write('# Cooling power vs temperature difference\n')
            f.write('# deltaT (°C), Qc (W)\n')
            for dt, qc in zip(deltaT, qc_data):
                f.write(f'{dt},{qc}\n')
        files_created.append(qc_filename)
        
        # COP file
        cop_filename = f'TEC1-12715_COP_vs_deltaT_{voltage}V.csv'
        cop_path = os.path.join(output_dir, cop_filename)
        with open(cop_path, 'w') as f:
            f.write('# Coefficient of Performance vs temperature difference\n')
            f.write('# deltaT (°C), COP\n')
            for dt, cop in zip(deltaT, cop_data):
                f.write(f'{dt},{cop}\n')
        files_created.append(cop_filename)
    
    # TEC1-12712S (slightly different performance)
    qc_12v_s = qc_12v * 0.85
    qc_10v_s = qc_10v * 0.85
    cop_12v_s = cop_12v * 1.1
    cop_10v_s = cop_10v * 1.1
    
    for voltage, qc_data, cop_data in [(12, qc_12v_s, cop_12v_s), 
                                        (10, qc_10v_s, cop_10v_s)]:
        # Qc file
        qc_filename = f'TEC1-12712S_Qc_vs_deltaT_{voltage}V.csv'
        qc_path = os.path.join(output_dir, qc_filename)
        with open(qc_path, 'w') as f:
            f.write('# Cooling power vs temperature difference\n')
            f.write('# deltaT (°C), Qc (W)\n')
            for dt, qc in zip(deltaT, qc_data):
                f.write(f'{dt},{qc}\n')
        files_created.append(qc_filename)
        
        # COP file
        cop_filename = f'TEC1-12712S_COP_vs_deltaT_{voltage}V.csv'
        cop_path = os.path.join(output_dir, cop_filename)
        with open(cop_path, 'w') as f:
            f.write('# Coefficient of Performance vs temperature difference\n')
            f.write('# deltaT (°C), COP\n')
            for dt, cop in zip(deltaT, cop_data):
                f.write(f'{dt},{cop}\n')
        files_created.append(cop_filename)
    
    print(f"\n✓ Created {len(files_created)} sample data files:")
    for filename in files_created:
        print(f"  - {filename}")
    
    print(f"\n✓ Sample data saved to '{output_dir}' directory")
    print("\nThese files demonstrate the expected format after manual digitization.")
    print("You can now run step 4 to generate the final graphs.")

if __name__ == '__main__':
    create_sample_data_files()
