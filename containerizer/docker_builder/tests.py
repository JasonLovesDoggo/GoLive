from .constants import *
from .generator import *
from ..defaults import *


def test_dockerize():
    opt = Options(language=LANGUAGES.PYTHON, framework=FRAMEWORKS.FLASK, version="3.12")
    command = dockerize(opt)
    DOCKERFILE = """FROM LANGUAGES.PYTHON:3.12-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
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


def test_run_cmd():
    print("test run_cmd\n\n")
    command = convert_to_run("python3 manage.py runserver")
    print(command)
    assert command == '["python3", "manage.py", "runserver"]'


test_convert_list()
test_dockerize()

print("ALL TESTS PASSED! (if u didnt see a big error)")
