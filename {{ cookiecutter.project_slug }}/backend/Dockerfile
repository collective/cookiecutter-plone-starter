ARG PLONE_VERSION={{ cookiecutter.plone_version }}
FROM plone/plone-backend:${PLONE_VERSION}

LABEL maintainer="{{ cookiecutter.author }} <{{ cookiecutter.email }}>" \
      org.label-schema.name="{{ cookiecutter.project_slug }}-backend" \
      org.label-schema.description="{{ cookiecutter.project_title }} backend image." \
      org.label-schema.vendor="{{ cookiecutter.author }}"

# Add local code
COPY . .

# Install local requirements and fix permissions
RUN ./bin/pip install mxdev \
    && mv requirements-docker.txt requirements.txt \
    && ./bin/mxdev -c mx.ini \
    && ./bin/pip install -r requirements-mxdev.txt \
    && chown -R plone: /app
