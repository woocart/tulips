PACKAGES := tulips tests

hash := $(word 1, $(shell grep -i  content-hash poetry.lock | shasum))

.PHONY: all
all: install

.PHONY: install
install: .venv/$(hash)
.venv/$(hash):
	poetry install
	@ touch $@

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

.PHONY: unit
unit:test
.PHONY: test
test: install
	@find . -name "__pycache__" -type d | xargs rm -rf
	poetry run pytest --cov=tulips

.PHONY: watch
watch: install
	poetry run rerun "make test format check" -i .coverage -i htmlcov

.PHONY: clean
clean:
	rm -rf .venv
