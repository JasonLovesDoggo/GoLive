from constants import LANGUAGES, VERSIONS
from containerizer.defaults import FRAMEWORKS
def dockerize(language: LANGUAGES, framework:FRAMEWORKS , version: str):
    assert language in LANGUAGES, f"Language {language} not supported"
    assert version in VERSIONS[language], f"Version {version} not supported for {language}"

    with open(f"./templates/{language}/{framework}") as raw_dockerfile:
        dockerfile = raw_dockerfile.read()


    # Dockerize the language and version
    pass

