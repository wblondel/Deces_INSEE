import click
from pathlib import Path
import csv


@click.group(name='check')
def cli_check():
    """Data check related commands"""
    pass


@cli_check.command(name='duplicates')
@click.argument(
    'csv_dir',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, writable=True, readable=True)
)
def check_duplicates(csv_dir):
    """Check for duplicates"""

    def _find_duplicates(hashes: dict):
        rev_multidict = {}
        for key, value in hashes.items():
            rev_multidict.setdefault(value, set()).add(key)

        nb_duplicated_entries = 0
        lines_to_remove = 0
        duplicates = []
        for key, values in rev_multidict.items():
            if len(values) > 1:
                nb_duplicated_entries += 1
                lines_to_remove += len(values) - 1
                duplicates.extend(sorted(list(values))[1:])

        return {
            "nb_dup_entries": nb_duplicated_entries,
            "lines_to_rm": lines_to_remove,
            "duplicates": duplicates
        }

    def _show_duplicates(data: dict, filename: str):
        if data['nb_dup_entries'] > 0:
            click.echo(f"{data['nb_dup_entries']} entrées sont AU MINIMUM en double dans le fichier {filename}.")
            click.echo(
                f"{data['lines_to_rm']} lignes peuvent être supprimées car elles sont des doublons de ces entrées.")
            click.echo(list(find_ranges(sorted(data['duplicates']))))

    click.echo("Checking for duplicates...")

    csv_dir = Path(csv_dir)
    if csv_dir.is_dir():
        csv_files = Path(csv_dir).glob('*.csv')
    else:
        csv_files = [csv_dir]

    import hashlib
    from utils import find_ranges

    for csv_file in csv_files:
        click.echo(f"Opening {csv_file}")
        with csv_file.open('r', encoding='utf-8', errors='strict') as csvfile:
            deathreader = csv.reader(csvfile, delimiter=';')
            header = next(deathreader)  # skip header

            lines_hashes = {}

            for row in deathreader:
                lines_hashes[deathreader.line_num] = hashlib.sha256(str(row).encode()).hexdigest()

        _show_duplicates(_find_duplicates(lines_hashes), csv_file)

        click.echo(f"Closing {csv_file}")


@cli_check.command(name='fields')
@click.argument(
    'csv_dir',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, writable=True, readable=True)
)
@click.option(
    '-f', '--full-name', is_flag=True, default=False, show_default=True,
    help='Enable checks on full name field.'
)
@click.option(
    '-g', '--gender', is_flag=True, default=False, show_default=True,
    help='Enable checks on gender field.'
)
@click.option(
    '-d', '--date', is_flag=True, default=False, show_default=True,
    help='Enable checks on date fields.'
)
@click.option(
    '-p', '--postcode', is_flag=True, default=False, show_default=True,
    help='Enable checks on postcode field.'
)
@click.option(
    '-c', '--city', is_flag=True, default=False, show_default=True,
    help='Enable checks on city fields.'
)
def check_fields(csv_dir, full_name, gender, date, postcode, city):
    """Check fields"""

    import data_tests as tests

    click.echo("Checking fields values...")

    csv_dir = Path(csv_dir)
    if csv_dir.is_dir():
        csv_files = Path(csv_dir).glob('*.csv')
    else:
        csv_files = [csv_dir]

    for csv_file in csv_files:
        click.echo(f"Opening {csv_file}")
        with csv_file.open('r', encoding='utf-8', errors='strict') as csvfile:
            deathreader = csv.reader(csvfile, delimiter=';')
            header = next(deathreader)  # skip header

            for row in deathreader:
                errors = []

                if full_name:
                    if not tests.fullname_is_complete(row):
                        errors.append("Le nom complet est incomplet.")

                if gender:
                    if not tests.gender_value(row):
                        errors.append("Valeur incorrecte pour le genre.")

                if date:
                    if tests.dates_are_int(row):
                        if not tests.dates_birth_is_before_death(row):
                            errors.append("La naissance est après le décès.")
                    else:
                        errors.append("Une des dates n'est pas un entier.")

                if postcode:
                    if not tests.postcodes_are_int(row):
                        errors.append("Un des codes lieu n'est pas valide.")

                if city:
                    if not tests.city_empty_when_postcode_990(row):
                        errors.append("Valeur du champ commune de naissance inutile. "
                                      "Le code lieu indique déjà que la commune est inconnue.")

                    if tests.city_not_known(row):
                        errors.append("Valeur du champ commune inutile.")

                    if not tests.city_correctly_formated_when_arrondissement(row):
                        errors.append("Format requis: VILLE (X)X")

                if errors:
                    print(f"{deathreader.line_num} {row} {errors}")

        click.echo(f"Closing {csv_file}")
