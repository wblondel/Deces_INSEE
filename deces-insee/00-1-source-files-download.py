from pathlib import Path
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi

source_zip_folder = Path("00-source/zip")

base_url = "https://www.insee.fr/fr/statistiques/fichier/"
files_url = ["4190491/Deces_2020_M11.zip", "4190491/Deces_2020_M10.zip", "4190491/Deces_2020_M09.zip", "4190491/Deces_2020_M08.zip", "4190491/Deces_2020_M07.zip", "4190491/Deces_2020_M06.zip", "4190491/Deces_2020_M05.zip", "4190491/Deces_2020_M04.zip", "4190491/Deces_2020_M03.zip", "4190491/Deces_2020_M02.zip", "4190491/Deces_2020_M01.zip", "4190491/Deces_2019.zip", "4769950/deces-2010-2018-csv.zip", "4769950/deces-2000-2009-csv.zip", "4769950/deces-1990-1999-csv.zip", "4769950/deces-1980-1989-csv.zip", "4769950/deces-1970-1979-csv.zip"]

for file_url in files_url:
    url = base_url + file_url
    remotefile = urlopen(url)
    blah = remotefile.info()['Content-Disposition']
    value, params = cgi.parse_header(blah)
    filename = params['filename']
    print(url)
    urlretrieve(url, source_zip_folder / filename)
