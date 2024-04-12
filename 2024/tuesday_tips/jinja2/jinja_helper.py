from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


def process_template(template_file: str, data: dict[str, Any]) -> str:
    jinja_env = Environment(
        loader=FileSystemLoader(searchpath="./"), autoescape=select_autoescape()
    )
    template = jinja_env.get_template(template_file)
    return template.render(**data)
