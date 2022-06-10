## Intro

## Build the Docker image and then run it in a container

```
docker build -t simple-python-server .
docker run -d -p 8080:80 simple-python-server
```

## Docker compose

Docker compose is a great solution if you want to run a Docker container locally, and be able to restart it when the code changes.

```
docker-compose up --build
```

You use a YAML file to provide the information that docker-compose needs to run. There are a couple of important ingredients in the docker-compose.yaml file:

- If you want docker-compose to build the image before you start the server (which generally, you want to do), you need to provide the build folder
- I also provide a container name so it's easy to find it back in the Docker GUI
- I use a slightly different command: uvicorn with the --reload option enabled so that the app reloads when it detects a code change
- I define a volume that binds the current folder to the folder in the container and syncs their content.
- I map the internal port (80) to 8080. The specific port is kind of random, but this allows you to have multiple Docker containers running and map them to different ports so you can more easily test things locally.

The result is that when you change the main file, it's synced to the Docker container, and then Uvicorn restarts the server. And it's really fast too!

## Outro
