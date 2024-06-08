import enum
from typing import Dict, List


class COMMAND_TYPES(enum.Enum):
    PRE_INIT = "pre_init"
    POST_INIT = "post_init"
    PRE_BUILD = "pre_build"
    POST_BUILD = "post_build"
    PRE_RUN = "pre_run"
    POST_RUN = "post_run"

class FRAMEWORKS(enum.Enum):
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"
    RAILS = "rails"
    EXPRESS = "express"
    SPRING = "spring"
    LARAVEL = "larvel"



OPTIONS: Dict[FRAMEWORKS, Dict[COMMAND_TYPES, List[str]]] = {
    FRAMEWORKS.DJANGO: {
        COMMAND_TYPES.PRE_RUN: [
            "python3 {mainFile} makemigrations --no-input",
            "python3 {mainFile} migrate --no-input",
            "python3 {mainFile} collectstatic --no-input",
        ]
    },
    FRAMEWORKS.FLASK: {
        COMMAND_TYPES.PRE_RUN: [
            "export FLASK_APP={mainFile}",
            "export FLASK_ENV={env}",
            "flask db upgrade",
        ]
    },
    FRAMEWORKS.RAILS: {
        COMMAND_TYPES.PRE_RUN: [
            "bundle install",
            "rails db:migrate",
            "rails assets:precompile",
        ]
    },
    FRAMEWORKS.EXPRESS: {
        COMMAND_TYPES.PRE_RUN: [
            "npm install",
            "npm run build",
        ]
    },
    FRAMEWORKS.LARAVEL: {
        COMMAND_TYPES.PRE_RUN: [
            "composer install",
            "php artisan migrate",
            "php artisan config:cache",
            "php artisan route:cache",
            "php artisan view:cache",
        ]
    },
    FRAMEWORKS.SPRING: {
        COMMAND_TYPES.PRE_RUN: [
            "./mvnw clean install",
            "./mvnw spring-boot:run",
        ]
    }
}
