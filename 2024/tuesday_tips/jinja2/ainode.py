import json
from typing import Any, Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape
from openai import OpenAI

# Models
GPT3_TURBO = "gpt-3.5-turbo-1106"
GPT4 = "gpt-4"
GPT4_TURBO = "gpt-4-1106-preview"

type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None

type NodeFn = Callable[[JSON], JSON]


def jinja_template(template_file: str) -> NodeFn:
    jinja_env = Environment(
        loader=FileSystemLoader(searchpath="./"), autoescape=select_autoescape()
    )
    template = jinja_env.get_template(template_file)
    return lambda data: template.render(**data)


def chat(openai_key: str, model: str = GPT4_TURBO) -> NodeFn:
    client = OpenAI(api_key=openai_key)

    def send_request(query: JSON) -> JSON:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": query},
            ],
        )
        content = response.choices[0].message.content
        if content:
            return content
        else:
            return ""

    return send_request


def extract(label: str) -> NodeFn:
    def node(data: JSON) -> JSON:
        if isinstance(data, dict):
            return data[label]
        else:
            raise ValueError(f"Expected a dictionary but got {data}.")

    return node


def embed(label: str) -> NodeFn:
    def node(data: JSON) -> JSON:
        return {label: data}

    return node


def merge(new_data: dict[str, JSON]) -> NodeFn:
    def node(data: JSON) -> JSON:
        if isinstance(data, dict):
            data.update(new_data)
            return data
        else:
            raise ValueError(f"Expected a dictionary but got {data}.")

    return node


def parse_json(data: JSON) -> JSON:
    if isinstance(data, str):
        print(f"Data: #####{data}#####")
        return json.loads(data)
    else:
        return data


def compose(*nodes: NodeFn) -> NodeFn:
    def node(data: JSON) -> JSON:
        for n in nodes:
            data = n(data)
        return data

    return node


def debug(data: JSON) -> JSON:
    print(data)
    return data
