from pathlib import Path
from zipfile import ZipFile

source_zip_folder = Path('00-source/zip')
source_csv_folder = Path('00-source/csv')

source_zip_files = source_zip_folder.glob('*.zip')

for source_zip_file in source_zip_files:
    with ZipFile(source_zip_file, 'r') as zip:        
        zipinfos = zip.infolist()
        for zipinfo in zipinfos:
            if zipinfo.filename.endswith('.csv'):
                original_name = zipinfo.filename
                zipinfo.filename = zipinfo.filename.lower().replace("-", "_")
                
                print(f"Extracting {original_name} to {zipinfo.filename} ...")
                
                zip.extract(zipinfo, source_csv_folder)
