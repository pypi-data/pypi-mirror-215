import re

import click

from gitlab_runner_tart_driver.modules.gitlab_custom_command_config import GitLabCustomCommandConfig
from gitlab_runner_tart_driver.modules.tart import Tart


@click.command()
@click.option("-x", "--tart-executable", required=False, default="tart", type=str, help="Path to the tart executable.")
def cleanup(tart_executable):
    """Command to greet a user."""
    p = GitLabCustomCommandConfig()

    tart = Tart(exec_path=tart_executable)
    tart_vm_name = p.vm_name()

    # remove specific VM that we started
    _remove_vm(tart, tart_vm_name)

    # cleanup leftovers from previous runs
    _remove_vm(tart, f"{p.vm_name_prefix}-.*", stopped_only=True)


def _remove_vm(tart, pattern, stopped_only=False):
    tart_images = tart.list()
    tart_vm_map = dict()
    # create map from images
    for i in tart_images:
        tart_vm_map[i.name] = i

    for vm_name, vm in tart_vm_map.items():
        m = re.match(pattern, vm_name)
        if not m:
            break

        try:
            if not vm.running and stopped_only:
                click.echo(f"[INFO] deleting '{vm_name}'")
                tart.delete(vm.name)
            elif vm.running and not stopped_only:
                click.echo(f"[INFO] stopping '{vm_name}'")
                tart.stop(vm.name)
                click.echo(f"[INFO] deleting '{vm_name}'")
                tart.delete(vm.name)
            elif not vm.running:
                click.echo(f"[INFO] deleting '{vm_name}'")
                tart.delete(vm.name)
        except:
            click.secho(f"[ERROR] failed to delete '{vm_name}'", fg="red")
