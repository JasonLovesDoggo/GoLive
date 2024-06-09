import string
import os
import urllib.parse
from ..containerizer.types import Options
from ..containerizer.constants import LANGUAGES
from ..containerizer.defaults import FRAMEWORKS


def create(options: Options):
    template_path = os.path.join(os.path.dirname(__file__), "main.tftemplate")
    with open(template_path, "r") as f:
        template = f.read()

    with open("build/main.tf", "w") as main:
        template = string.Template(template).substitute(
            NAME=urllib.parse.quote(str(options.app_dir).split("/")[-1]).casefold(),
            PORT=options.port,
            PROJECT_ID="new-proj-425823",
        )
        main.write(template)

    print("Terraform file created successfully")


if __name__ == "__main__":
    opt = Options(
        language=LANGUAGES.PYTHON,
        framework=FRAMEWORKS.FLASK,
        version="3.12",
        project_dir="/home/json/projects/JAMHACKS8/sample_project",
    )
    create(opt)