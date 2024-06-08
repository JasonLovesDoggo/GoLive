from typing import Optional
from constants import *
from containerizer.defaults import FRAMEWORKS
from string import Template


def dockerize(language: LANGUAGES, framework:FRAMEWORKS , version: str, install_command: Optional[str] = None):
    assert language in LANGUAGES, f"Language {language} not supported"
    assert version in VERSIONS[language], f"Version {version} not supported for {language}"
    if install_command is None:
        install_command = INSTALL_COMMANDS[language]

    with open(f"./templates/{language}/{framework}", "r") as raw_dockerfile:
        dockerfile = raw_dockerfile.read()
        dockerfile = process(dockerfile, language, framework, version, install_command)


    # Dockerize the language and version
    pass


def process(dockerfile: str, language: LANGUAGES, framework: FRAMEWORKS, version: str, install_command: str):
    # get all variables in the dockerfile dynamically and replace them with the values
    processed = Template(dockerfile).substitute(
        VERSION=version,
        INSTALL_COMMAND=install_command
    )








def test_dockerize():
    command = dockerize(LANGUAGES.PYTHON, FRAMEWORKS.FLASK, "3.7")
    DOCKERFILE = """
    FROM python:3.7-alpine
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt
    CMD ["python", "app.py"]
    """
    assert command == DOCKERFILE
