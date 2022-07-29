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
