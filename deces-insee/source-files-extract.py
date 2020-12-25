import glob
from zipfile import ZipFile

source_zip_folder = '00-source/zip'
source_csv_folder = '00-source/csv'

all_files = glob.glob(source_zip_folder + '/*.zip')

for filename in all_files:
    with ZipFile(filename, 'r') as zip:
        zip.printdir()
        zip.extractall(source_csv_folder)
