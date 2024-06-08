from .defaults import *
from .docker_builder.generator import Options, dockerize
from .docker_builder.constants import LANGUAGES


def generate():
    print("Generating container...")
    opt = Options(language=LANGUAGES.PYTHON, framework=FRAMEWORKS.FLASK, version="3.12")
    command = dockerize(opt)
    with open("build/Dockerfile", "w") as f:
        f.write(command)
    print(command)
    print("Container generated successfully!")
    return command


if __name__ == "__main__":
    generate()
