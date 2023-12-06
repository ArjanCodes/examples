import pulumi
import pulumi_docker
import pulumi_gcp as gcp

REGISTRY = "arjancodes-registry"
ENDPOINT = "automation-api"
IMAGE_NAME = "backend"


def create_registry(name: str) -> pulumi.Output[str]:
    registry = gcp.container.Registry(name)
    return registry.id.apply(
        lambda _: gcp.container.get_registry_repository().repository_url
    )


def build_image(image_name: pulumi.Input[str], context: str) -> pulumi_docker.Image:
    return pulumi_docker.Image(
        "my-image",
        image_name=image_name,
        registry=None,  # we're using gcloud for authentication
        build=pulumi_docker.DockerBuildArgs(
            platform="linux/amd64",
        ),
    )


def create_cloud_run_service(
    resource_name: str, location: str, image: pulumi_docker.Image
) -> gcp.cloudrun.Service:
    return gcp.cloudrun.Service(
        resource_name=resource_name,
        location=location,
        template=gcp.cloudrun.ServiceTemplateArgs(
            spec=gcp.cloudrun.ServiceTemplateSpecArgs(
                containers=[
                    gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                        image=image.image_name
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


def create_noauth_iam_policy(service: gcp.cloudrun.Service) -> None:
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


def main() -> None:
    # Create a private GCR repository.
    registry_url = create_registry(REGISTRY)

    # Get registry info (creds and endpoint).
    image_name = registry_url.apply(lambda url: f"{url}/{ENDPOINT}")

    image = build_image(image_name, IMAGE_NAME)

    # Create the Cloud Run service
    service = create_cloud_run_service(
        resource_name="default", location="us-central1", image=image
    )

    create_noauth_iam_policy(service)

    # Export the base and specific version image name and the service url
    pulumi.export("baseImageName", image.base_image_name)
    pulumi.export("fullImageName", image.image_name)
    pulumi.export("service_url", service.statuses[0].url)


if __name__ == "__main__":
    main()
