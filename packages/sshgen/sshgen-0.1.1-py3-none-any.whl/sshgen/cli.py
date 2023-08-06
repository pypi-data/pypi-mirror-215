#!/usr/bin/env python
from typing import Optional

import typer
from typing_extensions import Annotated

from sshgen import __app_name__, __version__
from sshgen.utils.app import AppUtils
from sshgen.utils.file import FileUtils

app = typer.Typer(no_args_is_help=True)


@app.command("generate")
def generate_hosts_file(hosts_file: Annotated[str, typer.Option('--hosts-file', '-h')] = './hosts.yml',
                        output: Annotated[str, typer.Option('--output', '-o')] = "./config"):
    """
    Command to generate SSH configuration file.
    By default, it uses hosts.yml file placed in your working directory and outputs to file named as "config"

    Example usage: sshconf generate -o my_ssh_config
    """

    hosts_file = FileUtils.as_file(file_path=hosts_file)
    output_file = FileUtils.as_file(file_path=output)

    AppUtils(hosts_file, output_file).generate_ssh_config()


def _version_callback(value: bool):
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
        raise typer.Exit()


@app.callback()
def callback(
        version: Annotated[Optional[bool],
        typer.Option('-v', '--version', callback=_version_callback, is_eager=True)] = None
):
    """
    sshgen generates SSH configuration file based on an Ansible hosts file.
    """
    return


if __name__ == '__main__':
    app()
