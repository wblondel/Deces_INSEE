from pathlib import Path
import gzip
import shutil

corrected_csv_folder = Path('01-corrected/csv')
corrected_gz_folder = Path('01-corrected/gz')

corrected_csv_files = corrected_csv_folder.glob('*.csv')

for corrected_csv_file in corrected_csv_files:
    with open(corrected_csv_file, 'rb') as f_in:
        corrected_gz_file = corrected_gz_folder / (corrected_csv_file.name + '.gz')
        
        print(f"Compressing {corrected_csv_file} to {corrected_gz_file} ...")
        
        with gzip.open(corrected_gz_file, 'wb', compresslevel=6) as f_out:
            shutil.copyfileobj(f_in, f_out)
