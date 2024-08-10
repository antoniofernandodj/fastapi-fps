t:
	poetry run pytest tests -vv

dev:
	poetry run uvicorn --reload --host 0.0.0.0 asgi:app