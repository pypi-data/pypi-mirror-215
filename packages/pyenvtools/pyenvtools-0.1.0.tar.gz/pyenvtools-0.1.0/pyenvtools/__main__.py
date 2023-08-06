import os
from pathlib import Path
from typing import Annotated

import dotenv
import rich
from typer import Argument, Typer

app = Typer()


@app.command()
def dump(file: Annotated[Path, Argument()] = None):
    if file:
        with open(file, "w") as fs:
            fs.write("\n".join([f"{key}='{value}'" for key, value in os.environ.items()]))
        return
    rich.print("\n".join([f"[yellow]{key}[/]=[green]{value}[/]" for key, value in os.environ.items()]))


@app.command()
def join(file: Annotated[Path, Argument()]):
    envs = dotenv.dotenv_values(file)
    string = ";".join([f"{key}={value}" for key, value in envs.items()])
    print(string)


@app.command()
def script(file: Annotated[Path, Argument()]):
    envs = dotenv.dotenv_values(file)
    rich.print("!#/bin/bash")
    for key, value in envs.items():
        rich.print(f"export {key}='{value}'")


if __name__ == "__main__":
    app()
