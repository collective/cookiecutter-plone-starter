# DevOps Operations using GitLab CI/CD 🚀

## Introduction

Welcome to the DevOps operations guide for deploying your project using GitHub Actions! This README provides step-by-step instructions on setting up your GitLab repository and initiating manual deployment workflows. Ensure to follow each step carefully to configure your environment and secrets correctly.

## Repository Setup 🛠️

### Step 1: Add the deployment environment variables

1. Visit [GitLab](https://gitlab.com/) and log in with your credentials.
2. Go to your repository at [{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}](https://github.com/{{ cookiecutter.github_organization }}/{{ cookiecutter.project_slug }}).
3. Click on `Settings` at the left menu and select `CI/CD`.
4. Expand the `Variables`.
5. Add all variables and its corresponding values, copying them from the `.env` file. This file is not commited into the repository, and that's why we need to add them here.

### Step 2: Add deployment's host SSH key as a known hosts

1. Run `ssh-keyscan -t rsa DEPLOY_HOST` in a terminal (substitute DEPLOY_HOST with the address of the host as in the `.env` file).
2. Copy the prompted value, and add it as a `Variable` like in the previous step. Name the variable `SSH_KNOWN_HOSTS`.

### Step 3: Add a SSH deployment key

1. Create a new ssh-key that will be used by GitLab CI/CD to connect to your host. You can create it in your terminal using `ssh-keygen -t rsa`.
2. Copy the public key to the DEPLOY_HOST's user's `~/.ssh/authorized_keys` file. Check your DEPLOY_HOST and DEPLOY_USER in the `.env` file.
3. Copy the private key as a `Variable` like in the previous step. Name the variable `DEPLOY_SSH_PRIVATE_KEY`

## Automatic Deployment 🚀

The deployment is executed automatically on each commit on `main` branch.

You may want to adapt your development workflow to that, and use a `develop` branch to develop and create Merge Requests to do the deployments.

## Manual Deployment 🚀

If you want to do manual deployments, you can enable the `when: manual` option of the `.gitlab-ci.yml` file (by default it is commented).

## Deployment with an auxiliary docker image

The provided configuration tries to mimic the `Makefile` deployment flow. Using the same commands as you would use when deploying from your computer.

If you want, you can use [an auxiliary docker image](https://github.com/kitconcept/docker-stack-deploy/) which does the deployment for you instead of using the `Makefile`. This is the docker image that is used if you configure the deployments in GitHub.

In such case please check the commented section of the `.gitlab-ci.yml` file where you can find an example.
