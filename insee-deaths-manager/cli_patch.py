import click
from pathlib import Path
import subprocess


@click.group(name='patch')
def cli_patch():
    """Data patch related commands"""
    pass


@cli_patch.command(name='apply', help='Apply patches to unmodified files')
@click.argument(
    'csv_dir',
    type=click.Path(exists=True, resolve_path=False, file_okay=False, dir_okay=True, writable=True, readable=True)
)
@click.argument(
    'patch_dir',
    type=click.Path(exists=True, resolve_path=False, file_okay=False, dir_okay=True, writable=True, readable=True)
)
def patch_apply(csv_dir, patch_dir):
    click.echo("Applying patches...")

    for patch_file in Path(patch_dir).glob('*.patch'):
        patched_csv_file = Path(csv_dir) / patch_file.stem

        click.echo(f"Applying patch {patch_file} TO {patched_csv_file} ...")
        subprocess.run(
            f"patch {str(patched_csv_file)} < {str(patch_file)}",
            shell=True
        )
        click.echo(f"Patch applied.")

    click.echo("Finished applying patches.")


@cli_patch.command(name='create', help='Create patches from modified files')
@click.argument(
    'source_csv_dir',
    type=click.Path(exists=True, resolve_path=False, file_okay=False, dir_okay=True, writable=True, readable=True)
)
@click.argument(
    'modified_csv_dir',
    type=click.Path(exists=True, resolve_path=False, file_okay=False, dir_okay=True, writable=True, readable=True)
)
@click.argument(
    'patch_dir',
    type=click.Path(exists=True, resolve_path=False, file_okay=False, dir_okay=True, writable=True, readable=True)
)
def patch_create(source_csv_dir, modified_csv_dir, patch_dir):
    click.echo("Creating patches...")

    for source_csv_file in Path(source_csv_dir).glob('*.csv'):
        modified_csv_file = Path(modified_csv_dir) / source_csv_file.name
        patch_file = Path(patch_dir) / (source_csv_file.name + '.patch')

        click.echo(f"Creating patch {patch_file} FROM {source_csv_file} TO {modified_csv_file} ...")
        subprocess.run(
            f"diff -Nar -U 0 {str(source_csv_file)} {str(modified_csv_file)} > {str(patch_file)}",
            shell=True
        )
        click.echo("Patch created.")

    click.echo("Finished creating patches.")
