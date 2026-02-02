install:
	poetry install

run:
	poetry run python treasure_maze/main.py

lint:
	poetry run ruff check treasure_maze/