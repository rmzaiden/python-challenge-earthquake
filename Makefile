.PHONY: help

help:
	@echo "\033[0;33mPlease use \`make <target>' where <target> is one of\033[0m"
	@printf "  %-30s to setup the project \n" "setup"
	@printf "  %-30s to clean the project \n" "clean"
	@printf "  %-30s to install git hooks \n" "githook"
	@printf "  %-30s to lint the project \n" "lint"
	@printf "  %-30s to fix linting issues \n" "lint-fix"
	@printf "  %-30s to test the project \n" "test"
	@printf "  %-30s to test the project with coverage \n" "test-coverage"
	@printf "  %-30s to generate pydoc \n" "pydoc"
	@printf "  %-30s to activate virtualenv \n" "activate"

setup:
	# install virtualenv if not exists
	which virtualenv || pip install virtualenv && \
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install -r requirements-dev.txt

clean:
	find . -type f -name '*.py[co]' -delete && \
    find . -type d -name __pycache__ -delete && \
    find . -type d -name 'UNKNOWN.egg-info' -exec rm -r {} + && \
    find . -type d -name '.tox' -exec rm -r {} + && \
    find . -type d -name '.venv' -exec rm -r {} +

githook:
	pre-commit install -t pre-commit -t pre-push -t commit-msg

.PHONY: test
test:
	. .venv/bin/activate && \
	python -m tox

test-coverage:
	. .venv/bin/activate && \
	python -m coverage run -m pytest tests --disable-warnings && \
	coverage html

lint:
	pylint src/ tests/ && \
	isort --check-only src/ tests/

lint-fix:
	black -l 100 -t py311 . --config pyproject.toml && \
	isort src/ tests/

pydoc:
	. .venv/bin/activate && \
	python -m pydoc -b

activate:
	. .venv/bin/activate