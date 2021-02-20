import random
import click
from pathlib import Path


@click.group(name='manage')
def cli_manage():
    """Data managing related commands"""
    pass


@cli_manage.command('download', short_help='download archives')
@click.argument(
    'source_archives_dir',
    type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True, writable=True, readable=True)
)
@click.option(
    '-f', '--force-download',
    default=False,
    show_default=True,
    is_flag=True,
    help='Force download from source if the files already exist locally.'
)
@click.option(
    '-x', '--extract-to',
    'source_csv_dir',
    required=False,
    show_default=True,
    type=click.Path(exists=True, resolve_path=True, file_okay=False, dir_okay=True, writable=True, readable=True),
    help='Folder to which the archives should be extracted.'
)
@click.pass_context
def manage_download(ctx, source_archives_dir, force_download, source_csv_dir):
    """Downloads INSEE deaths archives to SOURCE_ARCHIVES_DIR"""

    from urllib.request import urlopen
    from urllib.request import urlretrieve
    import cgi

    base_url = "https://www.insee.fr/fr/statistiques/fichier/"
    files_url = [
        "4190491/Deces_2021_M01.zip", "4190491/Deces_2020.zip",
        "4190491/Deces_2019.zip", "4769950/deces-2010-2018-csv.zip",
        "4769950/deces-2000-2009-csv.zip", "4769950/deces-1990-1999-csv.zip",
        "4769950/deces-1980-1989-csv.zip", "4769950/deces-1970-1979-csv.zip"
        ]
    
    click.echo("Download started.")

    for file_url in files_url:
        url = base_url + file_url
        remotefile = urlopen(url)
        blah = remotefile.info()['Content-Disposition']
        value, params = cgi.parse_header(blah)
        filename = params['filename']
        click.echo(f'Downloading {url} ...')

        filepath = source_archives_dir / Path(filename)

        if filepath.exists() and not force_download:
            print(filepath)
            click.echo('File already exists, skipping download.')
            continue

        urlretrieve(url, filepath, reporthook=download_progress_hook)
        click.echo()
    
    click.echo('Download finished.')

    if source_csv_dir:
        click.echo()
        ctx.invoke(manage_extract, archives_dir=source_archives_dir, csv_dir=source_csv_dir)


@cli_manage.command('extract', short_help='extract archives')
@click.argument(
    'archives_dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True)
)
@click.argument(
    'csv_dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True)
)
def manage_extract(archives_dir, csv_dir):
    """Extracts archives from ARCHIVES_DIR to CSV_DIR"""

    from zipfile import ZipFile

    click.echo('Extraction started.')

    archives = Path(archives_dir).glob('*.zip')

    for archive in archives:
        with ZipFile(archive, 'r') as zip:        
            zipinfos = zip.infolist()
            for zipinfo in zipinfos:
                if zipinfo.filename.endswith('.csv'):
                    original_name = zipinfo.filename
                    zipinfo.filename = zipinfo.filename.lower().replace("-", "_")
                    
                    print(f"Extracting {zipinfo.filename} ...")
                    
                    zip.extract(zipinfo, csv_dir)
    
    click.echo('Finished extracting.')


@cli_manage.command('compress', short_help='compress csv')
@click.argument(
    'csv_dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True)
)
@click.argument(
    'archives_dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True)
)
def manage_compress(csv_dir, archives_dir):
    """Compresses csv files from CSV_DIR to ARCHIVES_DIR"""

    import gzip
    import shutil

    click.echo('Compression started.')

    csv_files = Path(csv_dir).glob('*.csv')

    for csv_file in csv_files:
        with open(csv_file, 'rb') as f_in:
            archive_file = Path(archives_dir) / (csv_file.name + '.gz')
            
            print(f"Compressing {csv_file} to {archive_file} ...")
            
            with gzip.open(archive_file, 'wb', compresslevel=6) as f_out:
                shutil.copyfileobj(f_in, f_out)
    
    click.echo('Finished compressing.')


@cli_manage.command('copy', short_help='copy csv files to another folder')
@click.argument(
    'from_dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True)
)
@click.argument(
    'to_dir',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True)
)
def manage_copy(from_dir, to_dir):
    """Copies csv files from FROM_DIR to TO_DIR"""

    import shutil

    click.echo('Copy started.')

    for source_file in Path(from_dir).glob('*.csv'):
        destination_file = Path(to_dir) / source_file.name
        print(f"Copying {source_file} to {destination_file} ...")
        shutil.copy2(source_file, destination_file)

    click.echo('Finished copying.')


def download_progress_hook(count: int, block_size: int, total_size: int):
    if random.random() > 0.1:
        return
    click.echo('.', nl=False)
