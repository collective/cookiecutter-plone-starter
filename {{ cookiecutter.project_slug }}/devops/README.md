# {{ cookiecutter.project_title }} Devops

## Setup

### Environment configuration
#### For Local Deployment (Using Vagrant)

```shell
source .env_dev
```
#### For Production

Create `.env_prod`, if it does not exist, setting all values defined in `.env_dev`, then:

```shell
source .env_prod
```

Also, add a `prod.yml` file to `inventory` folder (with information about the production server), and a `{{ cookiecutter.github_organization }}-prod.yml` to `host_vars` folder.

### Install Ansible

Install Python 3 virtual environment and Ansible

```shell
cd devops
make clean
make setup
```

### Configure SSH key

Edit the `group_vars/users.yml` file and replace the line **public_keys: []** with

```yaml
    public_keys:
      - '<your ssh public key>'

```

## Docker configuration

As the images used in this deployment are public, just make sure you already are logged in with Docker.

After that, we need to create a new docker context, to be stored inside this folder.

```shell
make docker-setup
```

## Deploy

The shortcut is to run all steps at once with:

```shell
make all
```

This command provision a new machine, if running in the local environment, run the playbook and then deploy the stack.
### Provision

Only valid for local deployments using Vagrant. This creates a new Vagrant box with the configuration according to the `Vagrantfile`.

```shell
make provision
```

### Run playbook

Setup the server, by installing base packages, creating `UFW` configuration and adding users

```shell
make run-playbook
```

### Deploy stack to the server

Run `docker stack` to deploy to the server

```shell
make deploy
```

Use this also when there is a new version of any of the images.

## Check Stack Status

```shell
make status
```

## Check Logs

|Tool|Command|
|-|-|
|webserver|`make logs-webserver`|
|frontend|`make logs-frontend`|
|backend|`make logs-backend`|
