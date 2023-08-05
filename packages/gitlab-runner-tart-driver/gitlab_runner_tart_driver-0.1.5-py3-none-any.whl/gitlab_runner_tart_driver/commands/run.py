import os
import sys

import click

from gitlab_runner_tart_driver.modules.gitlab_custom_command_config import GitLabCustomCommandConfig
from gitlab_runner_tart_driver.modules.tart import Tart


@click.command()
@click.option(
    "--default-ssh-username", default="admin", required=False, type=str, help="username to login to a tart vm"
)
@click.option(
    "--default-ssh-password", default="admin", required=False, type=str, help="password to login to a tart vm"
)
@click.option(
    "-x",
    "--tart-executable",
    required=False,
    default="tart",
    type=str,
    help="Path to the tart executable.",
)
@click.option(
    "--shell",
    required=False,
    default="/bin/zsh",
    type=str,
    help="Path to the shell to be used for commands over ssh.",
)
@click.argument("script")
@click.argument("stage")
def run(default_ssh_username, default_ssh_password, tart_executable, shell, script, stage):
    """Run commands."""
    p = GitLabCustomCommandConfig()

    if not p.tart_ssh_username:
        p.tart_ssh_username = default_ssh_username
    if not p.tart_ssh_password:
        p.tart_ssh_password = default_ssh_password

    ######################################################################
    # Connect to VM
    ######################################################################
    tart = Tart(exec_path=tart_executable)
    tart_vm_name = p.vm_name()
    tart_ip = tart.ip(tart_vm_name, timeout=30)
    click.echo(f"[INFO] Establishing SSH conntection to '{p.tart_ssh_username}@{tart_ip}'")

    ssh_session = tart.ssh_session(name=p.vm_name(), username=p.tart_ssh_username, password=p.tart_ssh_password)

    click.echo("[INFO] Preparing workspace")
    remote_temp_dir = "/opt/temp"

    script_name = os.path.basename(script)
    remote_script_path = os.path.join(remote_temp_dir, stage + "-" + script_name)

    sftp = ssh_session.ssh_client.open_sftp()
    sftp.put(script, remote_script_path)
    sftp.close()

    # ssh_session.exec_ssh_command(f"cd {remote_build_dir}")
    script_exit_code = ssh_session.exec_ssh_command(f"{shell} -l {remote_script_path}", get_pty=True)

    sys.exit(script_exit_code)
