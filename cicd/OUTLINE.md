## Introduction

- We’ve all heard about CI/CD, but what does it actually stand for?
- I’ll talk about CI/CD today and show you how it works
- I’m going to be using GitHub actions in this video, and I’ll also use Pulumi - who is the sponsor of this video. I’m going to talk more about them later on.

## Pulumi Sponsored insert

- Cloud infrastructure can become quite complicated and there are many different settings to deal with.
- You may use YAML files to define resources, change settings directly with a CLI, or do it from the web interface of your cloud provider.
- Pulumi provides a way to define resources in code, using your favorite programming languages, IDEs, and package managers.
- So instead of dealing with YAML configurations or manual workflows, you write everything in code and Pulumi takes care of provisioning resources to achieve the desired state of your infrastructure.
- It supports over 80 clouds and cloud native technologies like Kubernetes.
- You can get started for free with Pulumi using this link [add [pulumi.com](http://pulumi.com/) link to the video] - you can also find it in the description of this video.
- Show how to use a template to get started quickly with Pulumi.
- Mention Pulumi Deployment ([https://www.pulumi.com/product/pulumi-deployments/](https://www.pulumi.com/product/pulumi-deployments/))

## Explain the example

- Simple API for retrieving YouTube channel information from a database

## What is CI/CD?

- CI = Continuous Integration
  - DevOps best practice: regularly merge changes into a repository and then run builds and tests automatically.
- CD = either Continuous Delivery or Continuous Deployment
- Continuous Delivery
  - produce software in short, frequent cycles
  - You can release the software at any time
  - Process of deployment is simple and repeatable (though still manual)
- Continuous Deployment
  - Goes one step further than Cont. Delivery
  - Every change that passes all stages of production is released automatically to the customers.
  - You can release faster and releases are less risky because the changes are smaller
  - But…
  - You need a great testing culture in your company
  - You’ll need a mechanism for feature flags and possibly phased rollouts to control availability of new features

## CI

- For the CI part you need a way to automatically build and test your code.
- In case of Python, build is not needed. But might need other things: copy assets, generate configuration files
- And of course, we want to test our code before shipping it.
- Add a test with a mock database to verify that the operations are working.
- Define a GitHub workflow that runs the tests when you push to the main branch.

## Deploying to Google Cloud with a GitHub Action and Pulumi

- Talk through the workflow file (interesting note: there’s no cloud infrastructure settings here - everything is defined in Python using Pulumi)
- Caveat: python -B to make sure that pytest doesn’t create cache files (Pulumi then wants to archive those and it can’t).
- Other caveat: the tests currently run in a separate environment from the virtual environment.
- Storing API keys in GitHub secrets (do not store them in the repository!)

## Final thoughts

- You’ve now seen a complete setup of a simple API with tests that’s automatically deployed to the cloud whenever you push a change.
- Code is available on GitHub as usual.
- If you want more control over the environment that your code is running in, you’ll want to use Docker. Watch this video next to learn more about how Docker works and how to set that up.
