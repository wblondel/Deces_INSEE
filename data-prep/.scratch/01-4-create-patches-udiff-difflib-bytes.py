# This should be the solution for files with inconsistent encoding.
# But... it is... really... too... slow!!!
# After 30 minutes, the first file was still processing...

from difflib import unified_diff
from difflib import diff_bytes
from pathlib import Path

renamed_csv_folder = Path('01-renamed/csv')
corrected_csv_folder = Path('02-corrected/csv')
patches_folder = Path('patches')

renamed_csv_files = renamed_csv_folder.glob('*.csv')

for renamed_csv_file in renamed_csv_files:
    if renamed_csv_file.name != "test.csv":
        continue
    print(renamed_csv_file)
    
    renamed_csv_bytes = []
    corrected_csv_bytes = []
    
    print("storing 1/2")
    with open(renamed_csv_file, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            renamed_csv_bytes.append(byte)
    
    byte = None
    
    print("storing 2/2")
    with open(corrected_csv_folder / renamed_csv_file.name, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            corrected_csv_bytes.append(byte)

    patch_file = patches_folder / (renamed_csv_file.name + '.patch')
     
    results = diff_bytes(unified_diff, renamed_csv_bytes, corrected_csv_bytes, n=0)
    
    print("comparing")
    
    with open(patch_file, 'wb') as f:
        for result in results:
            f.write(result)
    
    