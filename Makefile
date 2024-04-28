venv:
	cd src && \
	python3.9 --version && python3.9 -m venv .venv && \
	python3.9 -m pip install --upgrade pip

install:
	cd src && \
	pip install -r requirements-dev.txt

db-migrate:
	cd db_migration && \
	alembic revision --autogenerate --m "Evolving database schema"	

db-upgrade:
	cd db_migration && \
	alembic upgrade head