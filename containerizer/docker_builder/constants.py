import enum
from re import L
from typing import Dict, List


class LANGUAGES(enum.Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    RUBY = "ruby"
    GO = "go"
    DART = "dart"
    SWIFT = "swift"
    CPP = "cpp"
    C = "c"
    CSHARP = "csharp"
    KOTLIN = "kotlin"
    SCALA = "scala"
    RUST = "rust"
    PHP = "php"
    


INSTALL_COMMANDS: Dict[LANGUAGES, str] = {
    LANGUAGES.PYTHON: "pip install -r requirements.txt",
    LANGUAGES.JAVASCRIPT: "npm install",
    LANGUAGES.RUBY: "bundle install",
    LANGUAGES.GO: "go mod download",
    LANGUAGES.DART: "flutter pub get",
    LANGUAGES.SWIFT: "swift package resolve",
    LANGUAGES.CPP: "make",
    LANGUAGES.C: "make",
    LANGUAGES.CSHARP: "dotnet restore",
    LANGUAGES.KOTLIN: "gradle build",
    LANGUAGES.SCALA: "sbt compile",
    LANGUAGES.RUST: "cargo build",
    LANGUAGES.PHP: "composer install",
}


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
