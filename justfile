@a_default:
    just --list


@dev:
    # uv run fastapi dev ./app/main.py
    uv run uvicorn app.main:app --reload --log-config log_conf.yaml

@prod:
    uv run uvicorn app.main:app --log-config log_conf.prod.yaml

@format:
    uv run ruff format

@lint:
    uv run ruff check --fix