import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

print(data["project"]["name"])