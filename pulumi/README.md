# Introduction

Have you heard of Infrastructure-as-Code? Today I'm going to talk about what it is and give you a few examples of how to use it. Will infrastructure-as-code change Devops forever? I have some thoughts about that. And a pretty crazy idea as well.

I'm going to use Pulumi, which is an infrastructure-as-code platform, to create a cloud application. They're also the sponsor of this video, I'll talk more about them in a minute. But first, let's take a look at the example.

# Example

I'm going to use an example I've shown in a previous video. This is a simple API for retrieving information about YouTube channels. There's a Docker file that you can use to build and run this locally.

# Different ways to deploy to the cloud

There are different ways to deploy services to the cloud. It's mostly trying to find a balance between simplicity and flexibility.

The simplest way to deploy something to the cloud is by directy letting your cloud provider run your code and attach that to a URL. If you're using Google Cloud, this is called Google Cloud Functions. If you're using AWS, it's called Lambda. With this approach, you have very little control over how your code is run in terms of infrastructure, but it's also really easy to setup. You don't use a Dockerfile in this case. You simply deploy your code and the cloud provider will setup a service that provides the application context.

If you want more control over how your code is run, you can also opt for running a container (built with Docker). Within Google Cloud, this is called Cloud Run. AWS has something similar called Fargate (which I don't have personal experience with). Microsoft Azure has Container Instances. This allows for more flexibility in how you want to run your code, but it's also a bit more complicated to setup since you need to create a Docker file, build an image, etc.

If you need even more flexibility than this, you can also create your own Kubernetes cluster and have full control over how to deal with services, containers, scaling, load balancing, and so on. Unless you know exactly what you're doing and you have a good reason for needing this, I recommend avoiding this option. One of the two previous options is way simpler to setup. I won't cover Kubernetes in this video but I'll show you a few examples of using Cloud Functions and Cloud Run.

Before we can start creating cloud applications, we need to setup Google Cloud.

# GCloud

First, login to gcloud:
gcloud auth login

Then, set the correct project:
gcloud config set project <project_id>

# Pulumi and Infrastructure-as-code

I'm going to use Pulumi to create the cloud resources. Pulumi is a so-called infrastructure-as-code platform. What is that?

If you have any experience creating and running cloud infrastructures, you probably know that it can become quite complicated and that there are many different kinds of settings to deal with. You may use YAML files to define resources, change settings directly with a CLI, or do it in a web-based interface. Pulumi provides an environment where you do all of this in code, using your favorite programming language. So instead of deal with YAML files, CLIs and web-based consoles, you write everything in code and Pulumi takes care of updating your cloud infrastructure to match your code. I definitely think you should give this a try. You can get started for free with Pulumi using this link [add pulumi.com link to the video] - you can also find it in the description of this video.

To get started, we need to obtain default application credentials that Pulumi needs to interact with the Google Cloud resources:

```
gcloud auth application-default login
```

# Basic project

Show the basic_project example to deploy a very simple piece of code to the cloud using Pulumi.

# Cloud function

Show how to use cloud functions to create a simple channel API

# Cloud run

Next, show how to setup an application that relies on cloud run.

## Final tidbits

How to destroy the resources:

```
pulumi destroy
pulumi stack rm dev
```

Also, if you need to install extra packages (like the Docker client), make sure that they're also installed in the virtual environment!

```
venv/bin/pip install -r requirements.txt
```

## Final thoughts

I think Infrastructure-as-code is very interesting technology. In my opinion, this is the direction that Devops will go into.

So where will this technology take us? I think a great next step would be to have a generic layer that allows us to define cloud resources independent of whether they're running on AWS, Google Cloud, Azure or any other type of cloud provider. I totally understand that this isn't there yet though. This is very new technology, and cloud providers are still figuring out what cloud infrastructure actually is. I mean, it's not that long ago that Kubernetes support was added to AWS. With infrastructure as code, defining a generic layer seems feasible. In my opinion, this is definitely going to come.

If we define what the cloud infrastructure is using Python code, how far can we take this? Here's a crazy idea. Suppose you have a machine learning algorithm that looks at infrastructure usage data from the past and predicts how many resources you're going to need and then write a Python application that automatically creates or destroys the resources in advance to minimize costs? Is that possible? Would that make sense? I'm curious to hear your thoughts about this, so let me know in the comments.

Anyway, I hope you enjoyed this video. Thanks again to Pulumi for sponsoring this video. Check them out via the link in the description. Thanks for watching, take care, and see you soon.
