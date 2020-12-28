from pathlib import Path
import shutil

source_csv_folder = Path('00-source/csv')
corrected_csv_folder = Path('01-corrected/csv')

source_csv_files = source_csv_folder.glob('*.csv')

for source_csv_file in source_csv_files:
    corrected_csv_file = corrected_csv_folder / (source_csv_file.name)

    print(f"Copying {source_csv_file} to {corrected_csv_file} ...")
    
    shutil.copy2(source_csv_file, corrected_csv_file)
