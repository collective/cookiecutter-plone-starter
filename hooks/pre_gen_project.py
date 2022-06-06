"""Pre generation hook."""
from pathlib import Path
from textwrap import dedent

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

output_path = Path().resolve()

msg = dedent(
    f"""
    ===============================================================================
    Starting "{{ cookiecutter.project_title }}" generation
       Plone version: {{ cookiecutter.plone_version }}
       Volto version: {{ cookiecutter.volto_version }}
       Output folder: {output_path}
    ===============================================================================
"""
)

print(msg)
