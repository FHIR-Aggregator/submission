import json
from pathlib import Path
import click
import os
import subprocess


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
    bucket_name = bucket_path.split("/")[2]

    # get the project name
    project_name = bucket_path.split("/")[3]

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

    parameters = {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "inputFormat", "valueCode": "application/fhir+ndjson"},
            {
                "name": "inputSource",
                "valueUri": f"https://storage.googleapis.com/{bucket_name}/{project_name}/META",
            },
            {"name": "storageDetail", "part": [{"name": "type", "valueCode": "https"}]},
        ],
    }

    for ndjson_file in ndjson_files:
        path = Path(ndjson_file)
        https_path = ndjson_file.replace("gs://", "https://storage.googleapis.com/")
        _ = {
            "name": "input",
            "part": [
                {"name": "type", "valueCode": path.name.split(".")[0]},
                {"name": "url", "valueUri": https_path},
            ],
        }
        parameters["parameter"].append(_)

    # Write the JSON output to a file
    output_file = f"bulk-import-request-{project_name}.json"
    with open(output_file, "w") as f:
        json.dump(parameters, f, indent=2)
    print(f"Manifest written to {output_file}")


if __name__ == "__main__":
    bulk_import()
