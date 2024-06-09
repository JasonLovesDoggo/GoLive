from string import Template
import os
from ..defaults import *
from ..constants import *
from ..types import Options
from ..utils import convert_to_list_args, process_build_args
import pathlib

def process(dockerfile: str, options: Options):
    # get all variables in the dockerfile dynamically and replace them with the values

    def convert(data):
        return Template(data).substitute(
            VERSION=options.version,
            LANGUAGE=options.language.value,
            PORT=options.port,
            FILE=options.app_file,
        )

    def convert_to_run(options: Options):
        if options.framework == FRAMEWORKS.FLASK:
            assert options.run_command is not None, "Run command not provided"
            options.run_command = options.run_command.replace(
                "${WGSI}", f"{str(options.app_file).split('.')[0]}:{options.app_name}"
            )
        return repr(convert_to_list_args(convert(options.run_command))).replace(
            "'", '"'
        )

    BUILD_COMMANDS = process_build_args(options, convert)
    return Template(dockerfile).substitute(
        VERSION=options.version,
        INSTALL_COMMAND=convert(options.install_command),
        RUN_COMMAND=convert_to_run(options),
        BUILD_COMMANDS=BUILD_COMMANDS,
        LANGUAGE=options.language.value,
        FILE=options.app_file,
    )


def dockerize(options: Options):

    template_path = os.path.join(
        os.path.dirname(__file__), "templates", "basic.template"
    )
    build_dir = os.path.join(pathlib.Path(__file__).parent.parent.parent.parent, "build/Dockerfile")
    with open(template_path, "r") as raw_dockerfile:
        dockerfile = raw_dockerfile.read()
        dockerfile = process(dockerfile, options)
    with open(build_dir, "w") as f:
        f.write(dockerfile)

    # Dockerize the language and version
