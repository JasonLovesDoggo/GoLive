import string
import os
import urllib.parse
from ..containerizer.types import Options
from ..containerizer.constants import LANGUAGES
from ..containerizer.defaults import FRAMEWORKS
from pathlib import Path
import json
def create(options: Options):
    template_path = os.path.join(os.path.dirname(__file__), "main.tftemplate")
    with open(template_path, "r") as f:
        template = f.read()

    template_path = os.path.join(Path(__file__).parent.parent.parent, "build")
    with open(os.path.join(Path(__file__).parent.parent.parent, "d"), "r") as raw_json:
        raw_json = raw_json.read()
        json_data = json.loads(raw_json)
        PROJECT_ID = json_data["project_id"]



    with open(f"{template_path}/main.tf", "w") as main:
        template = string.Template(template).substitute(
            NAME=urllib.parse.quote(str(options.app_dir).split("/")[-1]).casefold(),
            PORT=options.port,
            PROJECT_ID=PROJECT_ID,
            SSH_PUB_KEY=options.ssh_pub_key,
        )
        main.write(template)

    print("Terraform file created successfully")


if __name__ == "__main__":
    opt = Options(
        language=LANGUAGES.PYTHON,
        framework=FRAMEWORKS.FLASK,
        version="3.12",
        port=328,
        project_dir="/home/json/projects/JAMHACKS8/sample_site",
    )
    create(opt)
