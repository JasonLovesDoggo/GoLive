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
    app_file: Optional[str] = "app.py"  # todo
    app_name: Optional[str] = "app"  # todo // for flask

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
