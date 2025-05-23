from pulumi import asset, export
from pulumi_gcp import cloudfunctionsv2, cloudrunv2, storage

bucket = storage.Bucket("bucket", location="europe-west1")

py_bucket_object = storage.BucketObject(
    "python-zip",
    bucket=bucket.name,
    source=asset.AssetArchive({".": asset.FileArchive("./function")}),
)

py_function = cloudfunctionsv2.Function(
    "channels-api",
    name="channels-api",
    location="europe-west1",
    build_config={
        "runtime": "python313",
        "entry_point": "channels_handler",
        "source": {
            "storage_source": {
                "bucket": bucket.name,
                "object": py_bucket_object.name,
            },
        },
    },
    service_config={
        "max_instance_count": 1,
        "available_memory": "256M",
        "timeout_seconds": 60,
    },
)

py_invoker = cloudrunv2.ServiceIamMember(
    "py-invoker",
    project=py_function.project,
    location=py_function.location,
    name=py_function.name,
    # role="roles/cloudfunctions.invoker",
    role="roles/run.invoker",
    member="allUsers",
)

export("python_endpoint", py_function.url)
