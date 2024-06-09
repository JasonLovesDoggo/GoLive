from .defaults import *
from .docker_builder.generator import Options, dockerize
from .constants import *


def generate():
    print("Generating container...")
    opt = Options(
        language=LANGUAGES.PYTHON,
        framework=FRAMEWORKS.FLASK,
        version="3.12",
        project_dir="/home/json/projects/JAMHACKS8/sample_project",
    )
    dockerize(opt)
    print("Container generated successfully!")


if __name__ == "__main__":
    generate()
