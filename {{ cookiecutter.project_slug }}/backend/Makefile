### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

PLONE_VERSION={{ cookiecutter.plone_version }}

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

CODE_QUALITY_VERSION=1.0.1
LINT=docker run --rm -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} check

PACKAGE_NAME={{ cookiecutter.python_package_name }}
PACKAGE_PATH=src/{{ cookiecutter.python_package_name }}/src/
IMAGE_NAME={{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}-backend
IMAGE_TAG=latest
CHECK_PATH=src/{{ cookiecutter.python_package_name }}/setup.py scripts/ $(PACKAGE_PATH)

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean-build clean-pyc clean-test clean-venv clean-instance ## remove all build, test, coverage and Python artifacts

.PHONY: clean-instance
clean-instance: ## remove existing instance
	rm -fr instance etc inituser var

.PHONY: clean-venv
clean-venv: ## remove virtual environment
	rm -fr bin include lib lib64

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -U "pip" "wheel" "cookiecutter"

instance/etc/zope.ini:	bin/pip
	@echo "$(GREEN)==> Install Plone and create instance$(RESET)"
	bin/pip install Plone -c https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt
	bin/cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
	mkdir -p var/{filestorage,blobstorage,cache,log}

bin/black:	bin/pip
	@echo "$(GREEN)==> Install Code Quality tools$(RESET)"
	bin/pip install -r https://raw.githubusercontent.com/plone/code-quality/v$(CODE_QUALITY_VERSION)/requirements.txt

# i18n
bin/i18ndude:	bin/pip
	@echo "$(GREEN)==> Install translation tools$(RESET)"
	bin/pip install i18ndude

.PHONY: i18n
i18n: bin/i18ndude ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	bin/update_locale

.PHONY: build
build: instance/etc/zope.ini ## Create virtualenv and run buildout
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/pip install -r requirements.txt

.PHONY: build
build-dev: instance/etc/zope.ini ## Create virtualenv and run buildout
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/pip install -r requirements/dev.txt

.PHONY: format
format:  bin/black ## Format the codebase according to our standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	bin/isort ${CHECK_PATH}
	bin/black ${CHECK_PATH}
	find "${PACKAGE_PATH}" -name '*.xml' |xargs bin/zpretty -x -i
	find "${PACKAGE_PATH}" -name '*.zcml' |xargs bin/zpretty -z -i

.PHONY: lint
lint: lint-isort lint-black lint-flake8 lint-zpretty ## check code style

.PHONY: lint-black
lint-black: ## validate black formating
	$(LINT) black "$(CHECK_PATH)"

.PHONY: lint-flake8
lint-flake8: ## validate black formating
	$(LINT) flake8 "$(CHECK_PATH)"

.PHONY: lint-isort
lint-isort: ## validate using isort
	$(LINT) isort "$(CHECK_PATH)"

.PHONY: lint-pyroma
lint-pyroma: ## validate using pyroma
	$(LINT) pyroma src/{{ cookiecutter.python_package_name }}/

.PHONY: lint-zpretty
lint-zpretty: ## validate ZCML/XML using zpretty
	$(LINT) zpretty "$(PACKAGE_PATH)"

.PHONY: test
test: ## run tests
	./bin/zope-testrunner --auto-color --auto-progress --test-path src/{{ cookiecutter.python_package_name }}/src/

.PHONY: test_quiet
test_quiet: ## run tests removing deprecation warnings
	PYTHONWARNINGS=ignore ./bin/zope-testrunner --auto-color --auto-progress --test-path src/{{ cookiecutter.python_package_name }}/src/

.PHONY: create-site
create-site: instance/etc/zope.ini ## Create a new site from scratch
	PYTHONWARNINGS=ignore ./bin/zconsole run instance/etc/zope.conf ./scripts/create_site.py

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi instance/etc/zope.ini

.PHONY: build-image
build-image:  ## Build Docker Image
	@docker build . -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile --build-arg PLONE_VERSION=$(PLONE_VERSION)
