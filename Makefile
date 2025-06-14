create-env:
	@if [ ! -d ".env" ]; then \
		echo "Creating Python virtual environment in .env using virtualenv..."; \
		virtualenv env; \
	else \
		echo "Virtual environment already exists."; \
	fi

install:
	@. env/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

format:
	black .

python-run:
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEVELOPMENT' >> .env
	bash -c 'source env/bin/activate && fastapi dev main.py --port 7080'

run-postgres:
	docker compose up