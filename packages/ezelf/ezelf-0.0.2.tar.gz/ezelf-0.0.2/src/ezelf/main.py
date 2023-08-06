import typer
from .simple import add_one

app = typer.Typer()


@app.callback()
def callback():
    """
    Ez-elf is a convenient script for ezpie.

    Provide:
    - package code and save to ezpie.
    """


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def main(num: int):
    """Entry point for the application script"""
    print("Call your main application code here")
    print(add_one(num))
