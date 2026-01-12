In order to run a MongoDB instance locally, make sure you have docker installed on your machine and run:

```
docker compose up -d
```

Then run the FastAPI app as follows:

```
uv sync
source .venv/bin/activate
uvicorn before:app --reload # to run the before version of the code
```

Here are a few example requests you can use to test the FastAPI app: