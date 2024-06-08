import enum
from typing import Dict, List


class LANGUAGES(enum.Enum):
    PYTHON = "python"


VERSIONS: Dict[LANGUAGES, List[str]] = {
    LANGUAGES.PYTHON: [
        "3.8.19",
        "3.9.19",
        "3.10.14",
        "3.11.9",
        "3.12.4",
        "3" "3.12",
        "3.13.0b2",
    ]
    
}
