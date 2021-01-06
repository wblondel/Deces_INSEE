# TOO SLOW

from pathlib import Path
import subprocess

patches_folder = Path('patches')
corrected_csv_folder = Path('01-corrected/csv')

patch_files = patches_folder.glob('*.patch')

for patch_file in patch_files:
    corrected_csv_file = corrected_csv_folder / patch_file.stem
    
    print(f"Applying patch {patch_file} TO {corrected_csv_file} ...")
    
    subprocess.run(['git', 'apply', '--unidiff-zero', '--unsafe-paths', '--directory=deces-insee/01-corrected', str(patch_file)])
