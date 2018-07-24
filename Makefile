PACKAGES := tulips tests

.PHONY: all
all: install

.PHONY: install
install: .venv/flag
.venv/flag: pyproject.lock
	@ poetry config settings.virtualenvs.in-project true
	poetry develop
	@ touch $@

pyproject.lock: pyproject.toml
	poetry lock

.PHONY: fmt
fmt: install
	poetry run isort $(PACKAGES) --recursive --apply
	poetry run black $(PACKAGES)

.PHONY: release
release: install
	poetry build
	poetry publish

.PHONY: lint
lint: install
	poetry run isort $(PACKAGES) --recursive --check-only --diff
	poetry run mypy $(PACKAGES)
	poetry run flake8 $(PACKAGES)

.PHONY: test
test: install
	@find . -name "__pycache__" -type d | xargs rm -rf
	poetry run pytest

.PHONY: watch
watch: install
	poetry run rerun "make test format check" -i .coverage -i htmlcov

.PHONY: clean
clean:
	rm -rf .venv
