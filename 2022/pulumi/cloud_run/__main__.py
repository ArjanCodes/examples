import pulumi
import pulumi_docker
import pulumi_gcp as gcp

# Create a private GCR repository.
registry = gcp.container.Registry("arjancodes-registry")
registry_url = registry.id.apply(
    lambda _: gcp.container.get_registry_repository().repository_url
)

# Get registry info (creds and endpoint).
image_name = registry_url.apply(lambda url: f"{url}/channel-api")

# Build and publish the container image.
image = pulumi_docker.Image(
    "my-image",
    build=pulumi_docker.DockerBuild(
        context="app", extra_options=["--platform=linux/amd64"]
    ),
    image_name=image_name,
    registry=None,  # we're using gcloud for authentication
)

# Create the Cloud Run service
service = gcp.cloudrun.Service(
    "default",
    location="us-central1",
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[
                gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                    image=image.image_name,
                )
            ],
        ),
    ),
    traffics=[
        gcp.cloudrun.ServiceTrafficArgs(
            latest_revision=True,
            percent=100,
        )
    ],
)

noauth_iam_policy = gcp.organizations.get_iam_policy(
    bindings=[
        gcp.organizations.GetIAMPolicyBindingArgs(
            role="roles/run.invoker",
            members=["allUsers"],
        )
    ]
)
noauth_iam_policy = gcp.cloudrun.IamPolicy(
    "noauthIamPolicy",
    location=service.location,
    project=service.project,
    service=service.name,
    policy_data=noauth_iam_policy.policy_data,
)

# Export the base and specific version image name and the service url
pulumi.export("baseImageName", image.base_image_name)
pulumi.export("fullImageName", image.image_name)
pulumi.export("service_url", service.statuses[0].url)
