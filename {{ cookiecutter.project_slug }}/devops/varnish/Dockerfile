# syntax=docker/dockerfile:1
FROM varnish:{{ cookiecutter.__devops_varnish_version }}

LABEL maintainer="{{ cookiecutter.author }} <{{ cookiecutter.email }}>" \
      org.label-schema.name="{{ cookiecutter.project_slug }}-varnish" \
      org.label-schema.description="{{ cookiecutter.project_title }} Varnish image." \
      org.label-schema.vendor="{{ cookiecutter.author }}"

COPY etc/varnish.vcl /etc/varnish/default.vcl
