@a_default:
    just --list


@dev:
    uv run fastapi dev ./app/main.py

@format:
    uv run ruff format

@lint:
    uv run ruff check --fix