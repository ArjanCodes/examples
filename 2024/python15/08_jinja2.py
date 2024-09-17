from jinja2 import Template


def main():
    prompt_template = Template(
        "Write a Python script that does {{ task }} using {{ technology }}."
    )

    prompt = prompt_template.render(task="web scraping", technology="BeautifulSoup")
    print(prompt)


if __name__ == "__main__":
    main()
