import typer

from .sync import ezpie

app = typer.Typer()


@app.callback()
def callback():
    """
    Ez-elf is a convenient script for ezpie, which provides:

    - package code and save to ezpie.
    """


@app.command()
def save_my_dir(dir_path: str):
    """
    Pack the contents of given directory and save it to ezpie.
    """
    typer.echo(ezpie.ezecho(dir_path))
