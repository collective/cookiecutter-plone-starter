### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

ifndef DEPLOY_ENV
$(error DEPLOY_ENV is not set)
endif

ifndef DEPLOY_USER
$(error DEPLOY_USER is not set)
endif

ifndef DEPLOY_SCALES
	DEPLOY_SCALES=2
endif

ifeq ($(DEPLOY_ENV), dev)
	CONTEXT=dev
	CONTEXT_HOST=ssh://$(DEPLOY_USER)@$(DEPLOY_HOST):$(DEPLOY_PORT)
else ifeq ($(DEPLOY_ENV), prod)
	CONTEXT=prod
	CONTEXT_HOST=ssh://$(DEPLOY_USER)@$(DEPLOY_HOST):$(DEPLOY_PORT)
else
$(error DEPLOY_ENV is not supported)
endif

DOCKER=docker
DOCKER_CONTEXT=${DOCKER} --context ${CONTEXT}

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## remove all build, test, coverage and Python artifacts
	rm -Rf bin lib lib64 include pyvenv.cfg .docker

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -U pip

bin/ansible: bin/pip
	@echo "$(GREEN)==> Setup Ansible $(RESET)"
	bin/pip install -r requirements/python.txt --upgrade
	bin/ansible-galaxy install -r requirements/ansible.yml --force

.PHONY: setup
setup: bin/ansible ## Create VirtualEnv and install Ansible via Pip

.PHONY: docker-login
docker-login: .docker/config.json  ## Login with Docker
	@echo "$(GREEN)==> Docker login $(RESET)"
	${DOCKER} login

.PHONY: docker-setup
docker-setup:  ## Setup docker context
	${DOCKER} context create ${CONTEXT} --description "{{ cookiecutter.project_title }} deployment" --docker "host=${CONTEXT_HOST}"

.PHONY: destroy
destroy: ## Destroy Vagrant box
	if [ "$(DEPLOY_ENV)" = "dev" ]; then \
		echo "$(GREEN)==> Destroy Vagrant box $(RESET)"; \
		sudo vagrant destroy; \
		sudo rm -Rf .vagrant_private_key .vagrant; \
		ssh-keygen -f ~/.ssh/known_hosts -R "[127.0.0.1]:2222"; \
	fi

.PHONY: provision
provision: bin/ansible ## Provision Vagrant box
	if [ "$(DEPLOY_ENV)" = "dev" ]; then \
		echo "$(GREEN)==> Provision Vagrant box $(RESET)"; \
		sudo vagrant up; \
		sudo cp .vagrant/machines/default/virtualbox/private_key .vagrant_private_key; \
		USER=`whoami` sudo chown ${USER}: .vagrant_private_key; \
		ssh-keyscan -p 2222 -H 127.0.0.1 >> ~/.ssh/known_hosts; \
	fi

.PHONY: run-playbook
run-playbook: bin/ansible ## Run playbook
	@echo "$(GREEN)==> Apply playbook in $(DEPLOY_ENV) $(RESET)"
	./bin/ansible-playbook playbook-setup.yml --limit ${CONTEXT}

.PHONY: deploy
deploy: ## Deploy stacks: Plone
	@echo "$(GREEN)==> Deploy Stack in $(DEPLOY_ENV) $(RESET)"
	${DOCKER_CONTEXT} stack deploy -c stacks/plone.yml plone

.PHONY: status
status: ## Check status of stack
	@echo "$(GREEN)==> Stack status in $(DEPLOY_ENV) $(RESET)"
	${DOCKER_CONTEXT} stack ps -f "desired-state=running" plone

.PHONY: logs-webserver
logs-webserver: ## Display webserver logs
	@echo "$(GREEN)==> Logs for webserver in $(DEPLOY_ENV) $(RESET)"
	${DOCKER_CONTEXT} service logs plone_traefik

.PHONY: logs-frontend
logs-frontend: ## Display frontend logs
	@echo "$(GREEN)==> Logs for frontend in $(DEPLOY_ENV) $(RESET)"
	${DOCKER_CONTEXT} service logs plone_frontend

.PHONY: logs-backend
logs-backend: ## Display backend logs
	@echo "$(GREEN)==> Logs for backend in $(DEPLOY_ENV) $(RESET)"
	${DOCKER_CONTEXT} service logs plone_backend

.PHONY: scale-services
scale-services: ## Scale services
	@echo "$(GREEN)==> Scaling Frontend and Backend to $(DEPLOY_SCALES) in $(DEPLOY_ENV) $(RESET)"
	${DOCKER_CONTEXT} service scale plone_frontend=$(DEPLOY_SCALES) plone_backend=$(DEPLOY_SCALES)

.PHONY: all
all: ## Create new box, run ansible, deploy stack
	if [ "$(DEPLOY_ENV)" = "dev" ]; then
		$(MAKE) provision
	fi
	$(MAKE) run-playbook
	$(MAKE) deploy
