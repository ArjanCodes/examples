import os
import time

import pulumi
from pulumi_gcp import cloudfunctions, storage

# File path to where the Cloud Function's source code is located.
PATH_TO_SOURCE_CODE = "./functions"

# We will store the source code to the Cloud Function in a Google Cloud Storage bucket.
bucket = storage.Bucket("channel_api_bucket", location="US", force_destroy=True)

# Create the single Cloud Storage object, which contains all of the function's
# source code. ("main.py" and "requirements.txt".)
source_archive_object = storage.BucketObject(
    "channel_api",
    bucket=bucket.name,
    source=pulumi.asset.FileArchive(PATH_TO_SOURCE_CODE),
)

# Create the Cloud Function, deploying the source we just uploaded to Google
# Cloud Storage.
fxn = cloudfunctions.Function(
    "channel_api",
    entry_point="channel_api",
    runtime="python310",
    source_archive_bucket=bucket.name,
    source_archive_object=source_archive_object.name,
    trigger_http=True,
)

invoker = cloudfunctions.FunctionIamMember(
    "invoker",
    project=fxn.project,
    region=fxn.region,
    cloud_function=fxn.name,
    role="roles/cloudfunctions.invoker",
    member="allUsers",
)

# Export the DNS name of the bucket and the cloud function URL.
pulumi.export("bucket_name", bucket.url)
pulumi.export("fxn_url", fxn.https_trigger_url)
