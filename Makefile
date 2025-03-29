install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

python-run:
	sed -i '/^ENVIRONMENT/d' .env
	echo 'ENVIRONMENT=DEVELOPMENT' >> .env
	bash -c 'source env/bin/activate && fastapi dev main.py --port 7080'

run-postgres:
	docker compose up