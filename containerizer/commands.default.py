import enum
from typing import Dict, List


class COMMAND_TYPES(enum.Enum):
    PRE_INIT = "pre_init"
    POST_INIT = "post_init"
    PRE_BUILD = "pre_build"
    POST_BUILD = "post_build"
    PRE_RUN = "pre_run"
    POST_RUN = "post_run"


FRAMEWORKS: Dict[str, Dict[str, List[str]]] = {
    "django": {
        "PRE_RUN": [
            "python3 manage.py makemigrations --no-input",
            "python3 manage.py migrate --no-input",
            "python3 manage.py collectstatic --no-input",
        ]
    }
}
