```Python
### Template for custom verb
@app.api_route("/", methods=["CUSTOM_VERB"])
def custom_verb() -> dict[str, str]:
    return {"CUSTOM_VERB": "This is a custom verb"}
```