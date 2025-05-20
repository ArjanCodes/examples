from pulumi import asset, export
from pulumi_gcp import cloudfunctionsv2, storage

bucket = storage.Bucket("bucket", location="europe-west1")

py_bucket_object = storage.BucketObject(
    "python-zip",
    bucket=bucket.name,
    source=asset.AssetArchive({".": asset.FileArchive("./function")}),
)

py_function = cloudfunctionsv2.Function(
    "python-func",
    name="python-func",
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


py_invoker = cloudfunctionsv2.FunctionIamMember(
    "py-invoker",
    project=py_function.project,
    location=py_function.location,
    cloud_function=py_function.name,
    role="roles/cloudfunctions.invoker",
    # role="roles/run.invoker",
    member="allUsers",
)

export("python_endpoint", py_function.url)
