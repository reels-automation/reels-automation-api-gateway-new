create-env:
	@echo "Creating Python virtual environment in ./env using python3 -m venv..."
	@python3 -m venv env

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black .

ruff:
	ruff check . --fix

lint: 
	pylint auth blueprints kafka models services utils

python-run:
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEVELOPMENT' >> .env
	bash -c 'source env/bin/activate && fastapi dev main.py --port 7080'

run-postgres:
	docker compose up