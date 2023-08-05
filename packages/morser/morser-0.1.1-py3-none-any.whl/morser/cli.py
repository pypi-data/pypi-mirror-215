from functools import wraps
from typing import Optional

import typer
from typing_extensions import Annotated

import morser

app = typer.Typer(name='Morser', no_args_is_help=True)

__version__ = '0.1.1'


def show_version(value: bool):
    if value:
        print(app.info.name, __version__)
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        typer.Option(
            '--version',
            callback=show_version,
            help='Show the CLI app version.',
        ),
    ] = None
):
    ...


def on_stdout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func(*args, **kwargs))

    return wrapper


app.command(name='encode', no_args_is_help=True)(
    on_stdout(morser.encode_text_to_morse_code)
)
app.command(
    name='decode',
    no_args_is_help=True,
    help=(
        'Decode morse code to plain text. '
        'If morse code starts with a \'-\', use: decode -- "your string".'
    ),
)(on_stdout(morser.decode_morse_code))
