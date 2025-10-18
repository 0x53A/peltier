#!/usr/bin/env python3
"""
Main script to run all steps of the Peltier datasheet analysis pipeline.
"""
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Peltier Datasheet Analysis Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py --all          # Run all steps
  python run_pipeline.py --step 1       # Run only step 1
  python run_pipeline.py --step 1 2     # Run steps 1 and 2
        """
    )
    
    parser.add_argument('--all', action='store_true',
                        help='Run all steps of the pipeline')
    parser.add_argument('--step', type=int, nargs='+', choices=[1, 2, 3, 4],
                        help='Run specific step(s) (1-4)')
    
    args = parser.parse_args()
    
    if not args.all and not args.step:
        parser.print_help()
        return
    
    steps_to_run = []
    if args.all:
        steps_to_run = [1, 2, 3, 4]
    elif args.step:
        steps_to_run = sorted(args.step)
    
    print("="*70)
    print("PELTIER DATASHEET ANALYSIS PIPELINE")
    print("="*70)
    
    for step in steps_to_run:
        print(f"\n{'='*70}")
        print(f"STEP {step}")
        print("="*70)
        
        if step == 1:
            print("Downloading datasheets...")
            import step1_download_datasheets
            step1_download_datasheets.download_datasheets()
            
        elif step == 2:
            print("Extracting graphs from PDFs...")
            import step2_extract_graphs
            step2_extract_graphs.extract_all_graphs()
            
        elif step == 3:
            print("Creating data extraction guide...")
            import step3_extract_data
            step3_extract_data.create_manual_digitization_guide()
            print("\n⚠ MANUAL STEP REQUIRED:")
            print("Please digitize the graphs manually using WebPlotDigitizer")
            print("or similar tool. See extracted_data/README.md for details.")
            
        elif step == 4:
            print("Generating final graphs...")
            import step4_generate_graphs
            step4_generate_graphs.generate_qc_vs_cop_plots()
    
    print(f"\n{'='*70}")
    print("Pipeline execution completed!")
    print("="*70)

if __name__ == '__main__':
    main()
