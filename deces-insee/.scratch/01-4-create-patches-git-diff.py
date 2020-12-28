from pathlib import Path
import subprocess

source_csv_folder = Path('00-source/csv')
corrected_csv_folder = Path('01-corrected/csv')
patches_folder = Path('patches')

source_csv_files = source_csv_folder.glob('*.csv')

for source_csv_file in source_csv_files:
    corrected_csv_file = corrected_csv_folder / source_csv_file.name
    patch_file = patches_folder / (source_csv_file.name + '.patch')
    
    print(f"Creating patch FROM {source_csv_file} TO {corrected_csv_file} ...")
    
    #subprocess.run(['git', 'diff', '--unified=0', '--raw', '--word-diff', '--word-diff-regex=.', '--no-index', '--text', '--output='+str(patch_file), str(renamed_csv_file), str(corrected_csv_file)])
    subprocess.run(['git', 'diff', '--unified=0', '--no-index', '--text', '--no-prefix', '--output='+str(patch_file), str(source_csv_file), str(corrected_csv_file)])
