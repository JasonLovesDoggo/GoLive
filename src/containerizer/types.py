import dataclasses
from typing import List, Optional
from .defaults import *
from .constants import *
from .utils import convert_list


@dataclasses.dataclass
class Options:
    language: LANGUAGES
    framework: FRAMEWORKS
    version: str
    project_dir: str
    port: Optional[int] = (
        8000  # which port the user wants to run the app on (if they care)
    )
    build_commands: Optional[List[str]] = None
    install_command: Optional[str] = None
    run_command: Optional[str] = None
    app_dir: Optional[str] = "Jamhacks8"  # todo
    app_file: Optional[str] = "app.py"  # todo
    app_name: Optional[str] = "app"  # todo // for flask
    ssh_pub_key: Optional[str] = None
    ip: Optional[str] = "" # generated post creation

    def __post_init__(self):  # Fill in the blanks
        if self.install_command is None:
            self.install_command = INSTALL_COMMANDS[self.language]
        if self.run_command is None:
            self.run_command = convert_list(
                OPTIONS[self.framework][COMMAND_TYPES.RUN_CMD]
            )
        if self.build_commands is None:
            self.build_commands = OPTIONS[self.framework][COMMAND_TYPES.BUILD]

        assert self.language in LANGUAGES, f"Language {self.language} not supported"
        assert (
            self.version in VERSIONS[self.language]
        ), f"Version {self.version} not supported for {self.language}"
        if self.ssh_pub_key is None:
            import subprocess
            import pathlib
            import os

            # get full path of build dir
            build_dir = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'build')
            if os.path.exists(build_dir + "/id_ed25519"):
                os.remove(build_dir + "/id_ed25519")
            if os.path.exists(build_dir + "/id_ed25519.pub"):
                os.remove(build_dir + "/id_ed25519.pub")
            subprocess.run(
                ["ssh-keygen", "-t", "ed25519", "-f", f'{build_dir}/id_ed25519', "-q", "-N", ""]
            )
            with open(f'{build_dir}/id_ed25519.pub', 'r') as f:
                self.ssh_pub_key = f.read().strip()


