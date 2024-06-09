from ..constants import *
from .generator import *
from ..defaults import *
from ..utils import convert_list


def test_dockerize():
    opt = Options(
        language=LANGUAGES.PYTHON,
        framework=FRAMEWORKS.FLASK,
        version="3.12",
        project_dir="/home/json/projects/JAMHACKS8/sample_site",
    )
    command = dockerize(opt)
    DOCKERFILE = """FROM LANGUAGES.PYTHON:3.12-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN pip install waitress
CMD ['waitress-serve', '--call', 'app.py', '--port=8000']
"""
    print("test dockerizer\n\n")
    assert command == DOCKERFILE


def test_convert_list():
    print("test convert_list\n\n")
    command = convert_list(
        ["python3 manage.py runserver", "python3 manage.py migrate --no-input"]
    )
    print(command)
    assert (
        command == "python3 manage.py runserver && python3 manage.py migrate --no-input"
    )


test_convert_list()
test_dockerize()

print("ALL TESTS PASSED! (if u didnt see a big error)")
