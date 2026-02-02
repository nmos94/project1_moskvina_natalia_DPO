install:
	poetry install

run:
	poetry run python labyrinth_game/main.py

lint:
	poetry run ruff check treasure_maze/