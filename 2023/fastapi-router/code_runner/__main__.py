import os
import time

import pulumi
from pulumi_gcp import cloudfunctions, storage

# Disable rule for that module-level exports be ALL_CAPS, for legibility.
# pylint: disable=C0103

# File path to where the Cloud Function's source code is located.
PATH_TO_SOURCE_CODE = "./functions"

# We will store the source code to the Cloud Function in a Google Cloud Storage bucket.
bucket = storage.Bucket("run_code_bucket", location="US", force_destroy=True)

# The Cloud Function source code itself needs to be zipped up into an
# archive, which we create using the pulumi.AssetArchive primitive.
assets = {
    "main.py": pulumi.FileAsset(path="main.py"),
}
# for file in os.listdir(PATH_TO_SOURCE_CODE):
#     location = os.path.join(PATH_TO_SOURCE_CODE, file)
#     asset = pulumi.FileAsset(path=location)
#     assets[file] = asset

archive = pulumi.AssetArchive(assets=assets)

# Create the single Cloud Storage object, which contains all of the function's
# source code. ("main.py" and "requirements.txt".)
source_archive_object = storage.BucketObject(
    "run_code_object",
    name=f"main.py-{time.time()}",
    bucket=bucket.name,
    source=archive,
)

# Create the Cloud Function, deploying the source we just uploaded to Google
# Cloud Storage.
fxn = cloudfunctions.Function(
    "run_code_function",
    entry_point="run_code",
    region="us-central1",
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

# Export the cloud function URL.
pulumi.export("fxn_url", fxn.https_trigger_url)
