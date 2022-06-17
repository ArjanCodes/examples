## Intro

If you're developing software for the cloud, you've certainly run into Docker. Docker has a lot of capabilities, but to get the most out of it, you have to make sure that the way you're running the code locally matches up with how it runs in the cloud. If you don't, you're going to run into incompatibility issues, the software might crash in the cloud but work perfectly on your machine, and that makes testing things and fixing those issues a real pain.

So, today I'm going to show you how to go all in on Docker, and avoid all of those problems. And I'll use a simple API server in Python as an illustration. The code for this episode is on GitHub including all the settings, ready-to-go, so you have no excuse to not do this :).

## Explain the example

(only the main.py file is important)

- Talk about FastAPI
- Dataclasses vs Pydantic for the representation of data
- Show how to run the app locally with uvicorn

## About Docker

Docker has completely changed the game for cloud development. It allows us to run applications in a completely separate container running your preferred Linux distribution. Moreover, you can create an image where you can pre-install software, change anything, treat it like a virtual machine. you can run these images locally on your machine, and they also neatly integrate with cloud technologies such as Kubernetes.

Docker makes going from local development to production code really easy. In between these two environments, you might have other environments such as staging, or a testing environment.

Talk about DTAP street.

Because the same Docker image runs in each of these environments, you reduce the chance that locally running code breaks when you run it in the cloud. This is why Docker is so great and has been adopted as the de facto container solution for the cloud. In this video, I won't talk about deployment specifically. If you'd like me to do a separate video about that, let me know in the comments. And when you're there, why don't you hit that like button as well? It really helps me a lot to reach more people.

## Build the Docker image and then run it in a container

The way I ran the code locally before is not ideal. It's running on a Mac and when we deploy this server, it'll run on Linux. The server might break if I try do deploy it due to some incompatibility issue between Linux and macOS, who knows? I also have to make sure that I'm using the right version of Python and that all the dependencies are installed on my machine. If you're a solo developer working on a single project it might not be a big issue. If you work in a bigger team, anything you can do to homogenize things between developers is going to make your life a whole lot easier.

So instead of running this locally, let's try this with Docker.

First, install Docker.

Talk about Docker and the Dockerfile structure. Specifically, explain why the requirements.txt file is copied first: so that dependency installation can be cached by Docker, and you don't have to do that every time you change something minor in the code.

And then, build and run the Docker image locally, as follows:

```
docker build -t channel-api .
docker run -d -p 8080:80 channel-api
```

## Docker compose

When you deploy your code to the cloud, you'll need to build the Docker image just like I did before, and tell Kubernetes or whatever other container orchestration system you're using to update the running image to the next version. This is all part of your continuous deployment pipeline. If you're using GitHub, you can set this up with a GitHub Workflow. If you're using BitBucket, you can use a BitBucket pipeline. Most alternatives will also have some kind of mechanism to start and run a deployment after committing and pushing a code change.

But the way I built and ran the container locally is not ideal. Every time I change something in the code, I have to stop the server manually, rebuild the image, and then run the image.

This is where Docker compose comes in. It has a two important features that make running your code locally in a Docker container really easy: begin able to supply a custom run command that restarts the server, and linking a volume on your machine to a folder inside the running container.

You still need the Dockerfile that I talked about before, but when you use Docker compose, you also need to supply a YAML file that contains the information that docker-compose needs to run.There are a couple of important ingredients in the docker-compose.yaml file:

- If you want docker-compose to build the image before you start the server (which generally, you want to do), you need to provide the build folder
- I also provide a container name so it's easy to find it back in the Docker GUI
- I use a slightly different command: uvicorn with the --reload option enabled so that the app reloads when it detects a code change. The command in the docker compose file overrides the command from the Dockerfile. It's still good to leave the command inside the Dockerfile though, because you'll need it when you deploy the image to the cloud.
- I define a volume that binds the current folder to the folder in the container and syncs their content. This means that if you change your code, the change is synced to the folder inside the container. And because uvicorn has the --reload option, it will then restart the server. Neat!
- The volume defined in the docker compose file overrides the copy command in the Dockerfile. Again, don't delete the copy command from the Dockerfile because you'll need it when you create the Docker image and deploy it to the cloud.
- I map the internal port (80) to 8080. The specific port is kind of random, but this allows you to have multiple Docker containers running and map them to different ports so you can more easily test things locally.

Let's try it:

```
docker-compose up --build
```

Make a minor change in the file, and see how everything is updated and the server is restarted.

## Outro

Hope you enjoyed this video. If you did, give it a like. And if you want to learn more about API development, GraphQL and REST interfaces, watch this video next. Take care, and see you soon!
