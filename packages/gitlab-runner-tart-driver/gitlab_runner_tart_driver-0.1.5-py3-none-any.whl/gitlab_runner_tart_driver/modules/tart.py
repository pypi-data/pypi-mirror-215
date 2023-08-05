import os
import re
import subprocess
import tempfile

import click
from jinja2 import Environment
from jinja2 import FileSystemLoader
from paramiko import MissingHostKeyPolicy
from paramiko import SSHClient
from pydantic import BaseModel
from pydantic import Field
from tabulate import tabulate


class TartImage(BaseModel):
    source: str = Field()
    name: str = Field()
    size: int = Field()
    running: bool = Field()


class TartVmSpec(BaseModel):
    cpu_count: int
    memory: int
    disk: int
    display: str
    running: bool
    ip_address: str


class TartVolume(BaseModel):
    name: str
    source: str
    dest: str
    ro: bool = Field(default=False)

    @classmethod
    def from_string(cls, value):
        components = value.split(":")
        if len(components) < 2:
            raise ValueError(f"'{value}' is not a valid volume mount definition")

        source = os.path.abspath(os.path.expanduser(components[0])).rstrip("/")
        dest = components[1].rstrip("/")
        name = dest.strip("/").replace("/", "__")
        ro = False
        if len(components) > 2:
            if "ro" == components[2]:
                ro = True
            else:
                raise ValueError(f"'{components[2]}' flag unknown")

        return cls(name=name, source=source, dest=dest, ro=ro)


class TartSshSession:
    def __init__(self, username, password, ip):
        self.user = username
        self.ip = ip
        self.password = password
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(MissingHostKeyPolicy())
        self.ssh_client.connect(ip, username=username, password=password)

    def exec_ssh_command(self, command, get_pty=True):
        """Executes an ssh command and prints it's output continously to stdout/stderr"""
        _, stdout, stderr = self.ssh_client.exec_command(command, get_pty=get_pty)
        for line in iter(stdout.readline, ""):
            click.echo(line, nl=False)
        for line in iter(stderr.readline, ""):
            click.echo(line, nl=False, err=True)
        return stdout.channel.recv_exit_status()


class Tart(object):
    def __init__(self, exec_path="tart"):
        self.tart_executable = exec_path

    def version(self) -> str:
        """Returns the tart version"""
        return self.exec(["--version"]).strip()

    def login(self, username: str, password: str, host: str) -> None:
        """Authenticates against a private OCI registry"""
        p = subprocess.Popen(
            [self.tart_executable, "login", host, "--username", username, "--password-stdin"],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        p.communicate(input=password.encode())
        ret = p.wait()
        if ret != 0:
            raise ValueError("Could not login to OCI registry")

    def pull(self, image) -> None:
        """pulls a new tart VM from a OCI registry. Make sure to use 'login' for private registries"""
        self.exec(["pull", image])

    def clone(self, source_name, new_name) -> None:
        """clones a tart VM"""
        self.exec(["clone", source_name, new_name])

    def delete(self, name) -> None:
        """deletes a tart VM"""
        self.exec(["delete", name])

    def set(self, name, cpu: int = None, memory: int = None, display: str = "") -> None:
        """sets the virtualization parameters like cpu, memory and display for a given tart VM"""
        args = ["set", name]
        if cpu:
            args.extend(["--cpu", str(cpu)])
        if memory:
            args.extend(["--memory", str(memory)])
        if display:
            args.extend(["--display", display])
        self.exec(args)

    def get(self, name) -> TartVmSpec:
        specs = self.exec(["get", name])

        # 'spec' will look like this:
        #
        #    CPU Memory Disk Display  Running
        #    4   8192   46   1024x768 true
        spec = specs.split("\n")[1]
        m = re.match(r"([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9x]+)\s+(\w+)", spec)
        if m:
            spec = TartVmSpec(
                cpu_count=int(m.group(1)),
                memory=int(m.group(2)),
                disk=int(m.group(3)),
                display=m.group(4),
                running=True if m.group(5).lower() == "true" else False,
                ip_address="n/a",
            )
            if spec.running:
                spec.ip_address = self.ip(name)

            return spec
        else:
            raise ValueError("cloud not determine vm specs")

    def print_spec(self, name, tablefmt="fancy_grid"):
        spec = self.get(name)
        data = [
            (str(spec.cpu_count), str(spec.memory), str(spec.disk), spec.display, str(spec.running), spec.ip_address)
        ]
        print(tabulate(data, headers=["CPU", "Memory", "Disk", "Display", "Running", "IP Address"], tablefmt=tablefmt))

    def stop(self, name) -> None:
        """stops a given tart VM"""
        self.exec(["stop", name])

    def run(self, name: str, volumes: list[TartVolume] = [], no_graphics=True) -> None:
        """starts a given tart VM"""
        args = ["run", name]
        if no_graphics:
            args.append("--no-graphics")

        if volumes:
            for d in volumes:
                source_path = os.path.abspath(os.path.expanduser(d.source))
                if d.ro:
                    source_path = f"{source_path}:ro"
                args.extend(["--dir", f"{d.name}:{source_path}"])
        try:
            self.spawn_exec(args)
        except Exception as e:
            print(f"Error when running VM {name}")
            raise e

    def ip(self, name, timeout=30, resolver="dhcp") -> str:
        """return the IP adress of a given tart VM"""
        ip = ""
        ret = self.exec(["ip", name, "--wait", str(timeout), "--resolver", resolver])
        for line in ret.split("\n"):
            m = re.match(r"^((?:[0-9]{1,3}\.){3}[0-9]{1,3})$", line)
            if m:
                ip = m.group(1)
                break
        return ip

    def list(self) -> list[TartImage]:
        """lists all available tart images and VMs"""
        tart_images = []

        resources = self.exec(["list"])
        resource_items = resources.split("\n")

        # remove header if present
        if resource_items:
            resource_items = resource_items[1:]

        for i in resource_items:
            m = re.match(r"^(\w+)\s+([a-zA-Z0-9./:@\-]+)\s+([0-9]+)\s+(\w+)\s+$", i)
            if m:
                tart_images.append(
                    TartImage(source=m.group(1), name=m.group(2), size=int(m.group(3)), running=(m.group(4) == "true"))
                )
        return tart_images

    def exec(self, cmd) -> str:
        """Executes a given command using subprocess and returns decoded string"""
        exec_cmd = [self.tart_executable]
        if cmd:
            exec_cmd.extend(cmd)
        return subprocess.check_output(exec_cmd).decode("utf-8")

    def spawn_exec(self, cmd):
        """Spawns a new main process using 'nohup'"""
        exec_cmd = ["nohup", self.tart_executable]
        if cmd:
            exec_cmd.extend(cmd)
        subprocess.Popen(exec_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def ssh_session(self, name, username, password) -> TartSshSession:
        ip = self.ip(name=name)
        if not ip:
            raise ValueError("Could not retrievew IP")

        return TartSshSession(ip=ip, username=username, password=password)

    def install_gitlab_runner(self, name, username, password, force=False, version="latest"):
        file_loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), os.path.pardir, "scripts"))
        env = Environment(loader=file_loader)
        template = env.get_template("install-gitlab-runner.sh.j2")

        data = {"gitlab_runner_force_install": "true" if force else "false", "gitlab_runner_version": version}

        temp = tempfile.NamedTemporaryFile()
        with open(temp.name, "w") as f:
            f.write(template.render(**data))
        f.close()

        remote_temp_dir = "/tmp"
        remote_script_path = os.path.join(remote_temp_dir, "install-gitlab-runner.sh")

        ssh_session = self.ssh_session(name=name, username=username, password=password)
        sftp = ssh_session.ssh_client.open_sftp()
        sftp.put(temp.name, remote_script_path)
        sftp.close()

        # ssh_session.exec_ssh_command(f"cd {remote_build_dir}")
        script_exit_code = ssh_session.exec_ssh_command(f"bash -l {remote_script_path}", get_pty=True)

        if script_exit_code != 0:
            raise ValueError("Error when installing GitLab Runner")
