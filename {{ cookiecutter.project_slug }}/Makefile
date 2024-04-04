### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

PLONE_VERSION=$$(cat backend/version.txt)
VOLTO_VERSION = $(shell cat ./frontend/package.json | python -c "import sys, json; print(json.load(sys.stdin)['dependencies']['@plone/volto'])")

PROJECT_NAME={{ cookiecutter.project_slug }}
STACK_NAME={{ cookiecutter.__devops_stack_name }}

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

.PHONY: all
all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install-frontend
install-frontend:  ## Install React Frontend
	$(MAKE) -C "./frontend/" install

.PHONY: build-frontend
build-frontend:  ## Build React Frontend
	$(MAKE) -C "./frontend/" build

.PHONY: start-frontend
start-frontend:  ## Start React Frontend
	$(MAKE) -C "./frontend/" start

.PHONY: install-backend
install-backend:  ## Create virtualenv and install Plone
	$(MAKE) -C "./backend/" build-dev
	$(MAKE) create-site

.PHONY: build-backend
build-backend:  ## Build Backend
	$(MAKE) -C "./backend/" build-dev

.PHONY: create-site
create-site: ## Create a Plone site with default content
	$(MAKE) -C "./backend/" create-site

.PHONY: start-backend
start-backend: ## Start Plone Backend
	$(MAKE) -C "./backend/" start

.PHONY: install
install:  ## Install
	@echo "Install Backend & Frontend"
	$(MAKE) install-backend
	$(MAKE) install-frontend

# TODO production build

.PHONY: build
build:  ## Build in development mode
	@echo "Build"
	$(MAKE) build-backend
	$(MAKE) install-frontend


.PHONY: start
start:  ## Start
	@echo "Starting application"
	$(MAKE) start-backend
	$(MAKE) start-frontend

.PHONY: clean
clean:  ## Clean installation
	@echo "Clean installation"
	$(MAKE) -C "./backend/" clean
	$(MAKE) -C "./frontend/" clean

.PHONY: format
format:  ## Format codebase
	@echo "Format codebase"
	$(MAKE) -C "./backend/" format
	$(MAKE) -C "./frontend/" format

.PHONY: i18n
i18n:  ## Update locales
	@echo "Update locales"
	$(MAKE) -C "./backend/" i18n
	$(MAKE) -C "./frontend/" i18n

.PHONY: test-backend
test-backend:  ## Test backend codebase
	@echo "Test backend"
	$(MAKE) -C "./backend/" test

.PHONY: test-frontend
test-frontend:  ## Test frontend codebase
	@echo "Test frontend"
	$(MAKE) -C "./frontend/" test

.PHONY: test
test:  test-backend test-frontend ## Test codebase

.PHONY: build-images
build-images:  ## Build docker images
	@echo "Build"
	$(MAKE) -C "./backend/" build-image
	$(MAKE) -C "./frontend/" build-image

## Docker stack
.PHONY: stack-start
stack-start:  ## Local Stack: Start Services
	@echo "Start local Docker stack"
	@docker compose -f docker-compose.yml up -d --build
	@echo "Now visit: http://{{ cookiecutter.project_slug }}.localhost"

.PHONY: start-stack
stack-create-site:  ## Local Stack: Create a new site
	@echo "Create a new site in the local Docker stack"
	@docker compose -f docker-compose.yml exec backend ./docker-entrypoint.sh create-site

.PHONY: start-ps
stack-status:  ## Local Stack: Check Status
	@echo "Check the status of the local Docker stack"
	@docker compose -f docker-compose.yml ps

.PHONY: stack-stop
stack-stop:  ##  Local Stack: Stop Services
	@echo "Stop local Docker stack"
	@docker compose -f docker-compose.yml stop

.PHONY: stack-rm
stack-rm:  ## Local Stack: Remove Services and Volumes
	@echo "Remove local Docker stack"
	@docker compose -f docker-compose.yml down
	@echo "Remove local volume data"
	@docker volume rm $(PROJECT_NAME)_vol-site-data

## Acceptance
.PHONY: build-acceptance-servers
build-acceptance-servers: ## Build Acceptance Servers
	@echo "Build acceptance backend"
	@docker build backend --build-arg PLONE_VERSION=${PLONE_VERSION} -t {{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}-backend:acceptance -f backend/Dockerfile.acceptance
	@echo "Build acceptance frontend"
	@docker build frontend --build-arg VOLTO_VERSION=${VOLTO_VERSION} -t {{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}-frontend:acceptance -f frontend/Dockerfile

.PHONY: start-acceptance-servers
start-acceptance-servers: build-acceptance-servers ## Start Acceptance Servers
	@echo "Start acceptance backend"
	@docker run --rm -p 55001:55001 --name {{ cookiecutter.project_slug }}-backend-acceptance -d {{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}-backend:acceptance
	@echo "Start acceptance frontend"
	@docker run --rm -p 3000:3000 --name {{ cookiecutter.project_slug }}-frontend-acceptance --link {{ cookiecutter.project_slug }}-backend-acceptance:backend -e RAZZLE_API_PATH=http://localhost:55001/plone -e RAZZLE_INTERNAL_API_PATH=http://backend:55001/plone -d {{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}-frontend:acceptance

.PHONY: stop-acceptance-servers
stop-acceptance-servers: ## Stop Acceptance Servers
	@echo "Stop acceptance containers"
	@docker stop {{ cookiecutter.project_slug }}-frontend-acceptance
	@docker stop {{ cookiecutter.project_slug }}-backend-acceptance

.PHONY: run-acceptance-tests
run-acceptance-tests: ## Run Acceptance tests
	$(MAKE) start-acceptance-servers
	npx wait-on --httpTimeout 20000 http-get://localhost:55001/plone http://localhost:3000
	$(MAKE) -C "./frontend/" test-acceptance-headless
	$(MAKE) stop-acceptance-servers

## Acceptance Frontend tests in development mode
.PHONY: start-test-acceptance-frontend-dev
start-test-acceptance-frontend-dev: ## Start the Acceptance Frontend Fixture in development mode
	(cd frontend && RAZZLE_API_PATH=http://127.0.0.1:55001/plone yarn start)

.PHONY: start-test-acceptance-server
start-test-acceptance-server: build-acceptance-servers ## Start Backend Acceptance Servers in development mode
	@echo "Starting test acceptance server"
	@docker run --rm -p 55001:55001 --name {{ cookiecutter.project_slug }}-backend-acceptance -d {{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}-backend:acceptance
	@echo "Started test acceptance server"

.PHONY: test-acceptance
test-acceptance: ## Start Cypress (for use it while developing)
	(cd frontend && ./node_modules/.bin/cypress open')

.PHONY: stop-acceptance-server
stop-acceptance-server: ## Stop Backend Acceptance Server in development mode
	@echo "Stopping acceptance server"
	@docker stop {{ cookiecutter.project_slug }}-backend-acceptance
	@echo "Stopped acceptance server"
