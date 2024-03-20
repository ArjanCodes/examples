"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage


def main() -> None:
    # Create a GCP resource (Storage Bucket)
    bucket = storage.Bucket(
        "my-bucket",
        website=storage.BucketWebsiteArgs(main_page_suffix="index.html"),
        uniform_bucket_level_access=True,
        location="US",
        force_destroy=True,
    )

    # Export the DNS name of the bucket
    pulumi.export("bucket_name", bucket.url)

    # Store a file in the bucket
    bucketObject = storage.BucketObject(
        "index.html",
        bucket=bucket.name,
        content_type="text/html",
        source=pulumi.FileAsset("index.html"),
    )

    _ = storage.BucketIAMBinding(
        "my-bucket-IAMBinding",
        bucket=bucket.name,
        role="roles/storage.objectViewer",
        members=["allUsers"],
    )

    pulumi.export(
        "bucket_endpoint",
        pulumi.Output.concat(
            "http://storage.googleapis.com/", bucket.id, "/", bucketObject.name
        ),
    )


if __name__ == "__main__":
    main()
