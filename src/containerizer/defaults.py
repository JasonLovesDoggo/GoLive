import enum
from typing import Dict, List


class COMMAND_TYPES(enum.Enum):
    PRE_INIT = "pre_init"
    POST_INIT = "post_init"
    BUILD = "build"
    POST_BUILD = "post_build"
    PRE_RUN = "pre_run"
    POST_RUN = "post_run"
    RUN_CMD = "run_cmd"


class FRAMEWORKS(enum.Enum):
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"
    RAILS = "rails"
    EXPRESS = "express"
    SPRING = "spring"
    LARAVEL = "larvel"
    GIN = "gin"

OPTIONS: Dict[FRAMEWORKS, Dict[COMMAND_TYPES, List[str]]] = {
    FRAMEWORKS.DJANGO: {
        COMMAND_TYPES.PRE_RUN: [
            #          "python3 manage.py makemigrations --no-input",
            "python3 manage.py migrate --no-input",
            "python3 manage.py collectstatic --no-input",
        ],
        COMMAND_TYPES.RUN_CMD: ["python3 manage.py runserver 0.0.0.0:${PORT}"],
    },
    FRAMEWORKS.FLASK: {
        COMMAND_TYPES.BUILD: ["pip install waitress"],
        COMMAND_TYPES.PRE_RUN: [
            "export FLASK_ENV=production",
            "flask db upgrade",
        ],
        COMMAND_TYPES.RUN_CMD: ["waitress-serve --port=${PORT} ${WGSI}"],
    },
    FRAMEWORKS.FASTAPI: {
        COMMAND_TYPES.RUN_CMD: [
            "python -m fastapi run ${FILE} --host 0.0.0.0 --port ${PORT}"
        ],  # Uvicorn based
    },
    FRAMEWORKS.RAILS: {
        COMMAND_TYPES.PRE_RUN: [
            "rails db:migrate",
            "rails assets:precompile",
        ],
        COMMAND_TYPES.RUN_CMD: ["rails server -b 0.0.0.0 -p ${PORT}"],
    },
    FRAMEWORKS.EXPRESS: {
        COMMAND_TYPES.BUILD: [
            "npm install",
            "npm run build",
        ],
        # Express typically uses PORT environment variable, not a flag
        COMMAND_TYPES.RUN_CMD: ["PORT=${PORT} npm start"],
    },
    FRAMEWORKS.SPRING: {
        COMMAND_TYPES.BUILD: ["./mvnw clean install"],
        COMMAND_TYPES.RUN_CMD: [
            "mvnw spring-boot:run -Dspring-boot.run.arguments=--server.port=${PORT}"
        ],
    },
    FRAMEWORKS.LARAVEL: {
        COMMAND_TYPES.BUILD: [
            "composer install",
        ],
        COMMAND_TYPES.PRE_RUN: [
            "php artisan migrate",
            "php artisan config:cache",
            "php artisan route:cache",
            "php artisan view:cache",
        ],
        COMMAND_TYPES.RUN_CMD: ["php artisan serve --host=0.0.0.0 --port=${PORT}"],
    },
    FRAMEWORKS.GIN: {
        COMMAND_TYPES.BUILD: ["go mod download", "CGO_ENABLED=0 GOOS=linux go build -o ./binary"],
        COMMAND_TYPES.RUN_CMD: ["./$binary"],
    },
}
