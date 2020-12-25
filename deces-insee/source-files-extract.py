import glob
from zipfile import ZipFile

data_zip_folder = '00-source/zip'
data_csv_folder = '00-source/csv'

all_files = glob.glob(data_zip_folder + '/*.zip')

for filename in all_files:
    with ZipFile(filename, 'r') as zip:
        zip.printdir()
        zip.extractall(data_csv_folder)
