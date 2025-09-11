from string.templatelib import Template
from typing import Literal


from html import escape
from string.templatelib import Template, Interpolation

def convert(value: object, conversion: Literal["a", "r", "s"] | None) -> object:
    if conversion == "a":
        return ascii(value)
    elif conversion == "r":
        return repr(value)
    elif conversion == "s":
        return str(value)
    return value

def f(template: Template, sanitize: bool = False) -> str:
    parts: list[str] = []
    for item in template:
        match item:
            case str() as s:
                parts.append(s)
            case Interpolation(value, _, conversion, format_spec):
                value = convert(value, conversion)
                value = format(value, format_spec)
                if sanitize:
                    value = escape(str(value))
                parts.append(value)
    return "".join(parts)

def to_html(template: Template) -> str:
    return f(template, sanitize=True)

def main() -> None:
    evil = "<script>alert('evil')</script>"
    template = t"<p>{evil}</p>"

    print(f(template))
    print(to_html(template))

if __name__ == "__main__":
    main()
