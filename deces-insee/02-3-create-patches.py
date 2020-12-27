from pathlib import Path
import subprocess

renamed_csv_folder = Path('01-renamed/csv')
corrected_csv_folder = Path('02-corrected/csv')
patches_folder = Path('patches')

renamed_csv_files = renamed_csv_folder.glob('*.csv')

for renamed_csv_file in renamed_csv_files:
    corrected_csv_file = corrected_csv_folder / renamed_csv_file.name
    patch_file = patches_folder / (renamed_csv_file.name + '.patch')

    subprocess.run(['git', 'diff', '--unified=0', '--word-diff', '--word-diff-regex=.', '--no-index', '--text', '--output='+str(patch_file), str(renamed_csv_file), str(corrected_csv_file)])
