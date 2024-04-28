setup:
	@test -d .venv || python3.9 -m venv .venv
	@. .venv/bin/activate && pip install -r requirements-dev.txt

db-migrate:
	@test -n "$(msg)" || (echo "msg is not set. Use make db-migrate MSG='Your migration message here'"; exit 1)
	cd db_migration && \
	alembic revision --autogenerate --m "$(msg)"

db-upgrade:
	cd db_migration && \
	alembic upgrade head

test:
	pytest tests/

coverage:
	pytest --cov=src --cov-report=term-missing tests/

test-coverage:
	. .venv/bin/activate && \
	python -m coverage run --source=src -m pytest tests --disable-warnings && \
	coverage html	