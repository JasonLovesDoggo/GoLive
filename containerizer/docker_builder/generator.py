from typing import Optional
from .constants import *
from string import Template
import os
from ..defaults import *
import dataclasses


@dataclasses.dataclass
class Options:
    language: LANGUAGES
    framework: FRAMEWORKS
    version: str
    port: Optional[int] = None
    install_command: Optional[str] = None
    run_command: Optional[str] = None
    app_file: Optional[str] = "app.py"  # todo

    def __post_init__(self):  # Fill in the blanks
        if self.port is None:
            self.port = 8000
        if self.install_command is None:
            self.install_command = INSTALL_COMMANDS[self.language]
        if self.run_command is None:
            self.run_command = convert_list(
                OPTIONS[self.framework][COMMAND_TYPES.RUN_CMD]
            )
        assert self.language in LANGUAGES, f"Language {self.language} not supported"

        assert (
            self.version in VERSIONS[self.language]
        ), f"Version {self.version} not supported for {self.language}"


def process(dockerfile: str, options: Options):
    # get all variables in the dockerfile dynamically and replace them with the values
    convert_to_list_args = lambda x: x.split(" ") if x else []

    def convert(data):
        return Template(data).substitute(
            VERSION=options.version,
            LANGUAGE=options.language.value,
            PORT=options.port,
            FILE=options.app_file,
        )

    return Template(dockerfile).substitute(
        VERSION=options.version,
        INSTALL_COMMAND=convert(options.install_command),
        RUN_COMMAND=repr(convert_to_list_args(convert(options.run_command))).replace("'", '"'),
        LANGUAGE=options.language.value,
        FILE=options.app_file,
    )


def convert_list(list_cmds: List):
    return " && ".join(list_cmds)


def convert_to_run(command: str):
    command = '"," '.join(command.split(" "))
    return f" [{command}]"


def dockerize(options: Options):

    template_path = os.path.join(
        os.path.dirname(__file__), "templates", "basic.template"
    )
    with open(template_path, "r") as raw_dockerfile:
        dockerfile = raw_dockerfile.read()
        dockerfile = process(dockerfile, options)

    # Dockerize the language and version
    return dockerfile
