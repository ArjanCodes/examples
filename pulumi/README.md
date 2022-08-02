# Introduction

Have you hear of Infrastructure-as-Code? Today I'm going to talk about what it is and why I think it's going to change the way we do Devops. This video is sponsored by Pulumi. I'll talk more about Pulumi during the video and show you how infrastructure as code work.

I have a lot of thoughts about Infrastructure as Code that I'll share with you today and one, pretty crazy idea.

# GCloud

First, login to gcloud:
gcloud auth login

Then, set the correct project:
gcloud config set project <project_id>

Obtain default application credentials that Pulumi needs to interact with the Google Cloud resources
gcloud auth application-default login

https://medium.com/google-cloud/use-multiple-paths-in-cloud-functions-python-and-flask-fc6780e560d3

Create a new project (I'm using Google Cloud)

Destroy the resources:
pulumi destroy
pulumi stack rm dev

If you need to install extra packages (like the Docker client), make sure that they're also installed in the virtual environment!

```
venv/bin/pip install -r requirements.txt
```

## Idea

If we define what the cloud infrastructure is using Python code, how far can we take this? For example, suppose you have a machine learning algorithm that looks at infrastructure usage data from the past and predicts how many resources you're going to need and then write a Python script that automatically creates or destroys the resources in advance to minimize costs? Is that possible?
