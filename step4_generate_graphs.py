#!/usr/bin/env python3
"""
Step 4: Generate final graphs
Creates Qc vs COP plots at different delta T values based on the extracted data.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
import csv

def load_data_file(filepath):
    """Load data from a CSV file."""
    data = {'deltaT': [], 'value': []}
    
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip empty lines and comments
            if not row or row[0].strip().startswith('#'):
                continue
            
            try:
                deltaT = float(row[0].strip())
                value = float(row[1].strip())
                data['deltaT'].append(deltaT)
                data['value'].append(value)
            except (ValueError, IndexError):
                continue
    
    return np.array(data['deltaT']), np.array(data['value'])

def interpolate_at_deltaT(deltaT_array, value_array, target_deltaT):
    """Interpolate value at a specific delta T."""
    if target_deltaT < deltaT_array.min() or target_deltaT > deltaT_array.max():
        return None
    
    f = interp1d(deltaT_array, value_array, kind='linear')
    return float(f(target_deltaT))

def generate_qc_vs_cop_plots(data_dir='extracted_data', output_dir='generated_graphs'):
    """
    Generate Qc vs COP plots at different delta T values.
    
    This function looks for paired Qc and COP data files at the same voltage
    and creates scatter plots showing the relationship.
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    data_path = Path(data_dir)
    
    # Find all data files
    qc_files = sorted(data_path.glob('*_Qc_*.csv'))
    cop_files = sorted(data_path.glob('*_COP_*.csv'))
    
    if not qc_files or not cop_files:
        print(f"No data files found in '{data_dir}' directory")
        print("Please run step3_extract_data.py and manually digitize the graphs first.")
        return
    
    print(f"Found {len(qc_files)} Qc files and {len(cop_files)} COP files")
    
    # Group files by model
    models = {}
    for qc_file in qc_files:
        # Extract model name from filename (e.g., TEC1-12715)
        name_parts = qc_file.stem.split('_')
        if len(name_parts) >= 1:
            model = name_parts[0]
            if model not in models:
                models[model] = {'qc_files': [], 'cop_files': []}
            models[model]['qc_files'].append(qc_file)
    
    for cop_file in cop_files:
        name_parts = cop_file.stem.split('_')
        if len(name_parts) >= 1:
            model = name_parts[0]
            if model not in models:
                models[model] = {'qc_files': [], 'cop_files': []}
            models[model]['cop_files'].append(cop_file)
    
    # Generate plots for each model
    for model, files in models.items():
        print(f"\nProcessing {model}...")
        
        if not files['qc_files'] or not files['cop_files']:
            print(f"  Skipping {model}: missing Qc or COP data")
            continue
        
        # Create a figure with multiple subplots for different delta T values
        delta_t_values = [0, 10, 20, 30, 40, 50]  # Example delta T values
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'{model}: Cooling Power (Qc) vs COP at Different ΔT', fontsize=16)
        axes = axes.flatten()
        
        # For each voltage, load both Qc and COP data
        plot_created = False
        for qc_file in files['qc_files']:
            # Try to find matching COP file
            qc_basename = qc_file.stem
            voltage_part = None
            
            # Extract voltage from filename
            for part in qc_basename.split('_'):
                if 'V' in part or 'v' in part:
                    voltage_part = part
                    break
            
            if not voltage_part:
                continue
            
            # Find matching COP file
            cop_file = None
            for cf in files['cop_files']:
                if voltage_part in cf.stem:
                    cop_file = cf
                    break
            
            if not cop_file:
                continue
            
            # Load data
            try:
                qc_deltaT, qc_values = load_data_file(qc_file)
                cop_deltaT, cop_values = load_data_file(cop_file)
                
                # For each target delta T, interpolate both Qc and COP
                for idx, target_dt in enumerate(delta_t_values):
                    if idx >= len(axes):
                        break
                    
                    qc_at_dt = interpolate_at_deltaT(qc_deltaT, qc_values, target_dt)
                    cop_at_dt = interpolate_at_deltaT(cop_deltaT, cop_values, target_dt)
                    
                    if qc_at_dt is not None and cop_at_dt is not None:
                        axes[idx].scatter(cop_at_dt, qc_at_dt, label=voltage_part, s=100)
                        plot_created = True
                
            except Exception as e:
                print(f"  Error processing {qc_file.name}: {e}")
                continue
        
        if plot_created:
            # Format subplots
            for idx, target_dt in enumerate(delta_t_values):
                if idx >= len(axes):
                    break
                axes[idx].set_xlabel('COP')
                axes[idx].set_ylabel('Qc (W)')
                axes[idx].set_title(f'ΔT = {target_dt}°C')
                axes[idx].grid(True, alpha=0.3)
                axes[idx].legend()
            
            plt.tight_layout()
            
            output_path = os.path.join(output_dir, f'{model}_Qc_vs_COP.png')
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"  ✓ Saved: {output_path}")
            plt.close()
        else:
            print(f"  No valid data pairs found for {model}")
            plt.close()
    
    print(f"\n✓ Generated graphs saved to '{output_dir}' directory")

if __name__ == '__main__':
    generate_qc_vs_cop_plots()
