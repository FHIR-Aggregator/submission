import datetime
import subprocess

import click


@click.command()
@click.argument("bucket_path")
def bulk_import(bucket_path):
    """
    Create manifest for loading FHIR data from bucket.

    \b
    Arguments:\n
    bucket_path (str): gs:// path to the FHIR ndjson files in the bucket.
    """

    if not bucket_path.startswith("gs://"):
        raise ValueError(f"{bucket_path} is not a valid gs:// path")

    # get the bucket name
    path_parts = bucket_path.split("/")
    # retrieve the bucket name and project name from the bucket path given structure gs://<bucket-name>/R4/<project-name>
    assert path_parts[0] == "gs:", path_parts
    assert path_parts[1] == "", path_parts
    assert path_parts[3] == 'R4', path_parts
    bucket_name = path_parts[2]
    project_name = path_parts[4]


    assert bucket_name, bucket_path.split("/")
    assert project_name, bucket_path.split("/")

    # list the bucket by calling the gsutil command
    result = subprocess.run(
        ["gsutil", "ls", "-r", bucket_path], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"gsutil command failed: {result.stderr}")

    # process the output
    ndjson_files = [
        line for line in result.stdout.splitlines() if line.endswith(".ndjson")
    ]

    # Write the load commands to a shell script
    output_file = f"scripts/gs-bulk-import-request-{project_name}.sh"
    with open(output_file, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"# Bucket: {bucket_name}\n")
        f.write(f"# Project: {project_name}\n")
        f.write(f"# Generation date: {datetime.datetime.now().isoformat()}\n")
        f.write("set -euo pipefail\n")
        # see .env-sample file
        f.write(': "${FHIR_STORE_ID:?Need to set FHIR_STORE_ID}"\n')
        f.write(': "${DATASET_ID:?Need to set DATASET_ID}"\n')
        f.write(': "${LOCATION:?Need to set CLUSTER_NAME}"\n')

        for _ in ndjson_files:
            f.write(f"gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri={_}\n")

    print(f"Manifest written to {output_file}")


if __name__ == "__main__":
    bulk_import()
