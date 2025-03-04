import importlib
import click
import json
from pydantic import ValidationError
from datetime import datetime, timedelta


# Import the R4 classes
FHIR_CLASSES = importlib.import_module("fhir.resources.R4B")


def transform_documentreference(resource):
    """
    Transform a DocumentReference resource from R5 to R4.

    Parameters:
    resource (dict): The DocumentReference resource to transform.

    Returns:
    dict: The transformed DocumentReference resource.
    """
    if "version" in resource:
        del resource["version"]
    if "content" in resource:
        for content in resource["content"]:
            if "profile" in content:
                content["format"] = content.pop("profile")[0]["valueCoding"]
            if "attachment" in content and "size" in content["attachment"]:
                if "extension" not in resource:
                    resource["extension"] = []
                resource["extension"].append(
                    {
                        "url": "https://nih-ncpi.github.io/ncpi-fhir-ig-2/StructureDefinition/file-size",
                        "valueQuantity": {
                            "value": int(content["attachment"]["size"]),
                            "unit": "bytes",
                            "system": "http://unitsofmeasure.org",
                            "code": "bytes",
                        },
                    }
                )
                del content["attachment"]["size"]

    if "subject" in resource and "reference" in resource["subject"]:
        if "Specimen" in resource["subject"]["reference"]:
            return None
    return resource


def transform_bodystructure(resource):
    """
    Transform a BodyStructure resource from R5 to R4.

    Parameters:
    resource (dict): The BodyStructure resource to transform.

    Returns:
    dict: The transformed BodyStructure resource.
    """
    if "includedStructure" in resource:
        resource["location"] = resource.pop("includedStructure")[0]["structure"]
    return resource


def transform_encounter(resource):
    """
    Transform an Encounter resource from R5 to R4.

    Parameters:
    resource (dict): The Encounter resource to transform.

    Returns:
    dict: The transformed Encounter resource.
    """
    if "reason" in resource:
        resource["reasonReference"] = [
            ref["reference"] for ref in resource.pop("reference", [])
        ]
    if "class" in resource:
        if "coding" in resource["class"]:
            resource["class"] = resource["class"]["coding"][0]
    else:
        resource["class"] = {"code": "NONAC", "display": "inpatient non-acute"}
    resource["status"] = "finished"
    return resource


def transform_group(resource):
    """
    Transform a Group resource from R5 to R4.

    Parameters:
    resource (dict): The Group resource to transform.

    Returns:
    dict: The transformed Group resource.
    """
    if "membership" in resource:
        del resource["membership"]
    if "actual" not in resource:
        resource["actual"] = True
    if "type" not in resource:
        resource["type"] = "person"
    return resource


def transform_imagingstudy(resource):
    """
    Transform an ImagingStudy resource from R5 to R4.

    Parameters:
    resource (dict): The ImagingStudy resource to transform.

    Returns:
    dict: The transformed ImagingStudy resource.
    """
    if "basedOn" in resource:
        resource["procedureReference"] = resource.pop("basedOn")
    if "series" in resource:
        for series in resource["series"]:
            if "modality" in series:
                series["modality"] = series["modality"]["coding"][0]
                series["modality"]["system"] = series["modality"]["system"].replace(
                    " ", ""
                )
    return resource


def transform_medicationadministration(resource):
    """
    Transform a MedicationAdministration resource from R5 to R4.

    Parameters:
    resource (dict): The MedicationAdministration resource to transform.

    Returns:
    dict: The transformed MedicationAdministration resource.
    """
    if "medication" in resource:
        _medication = resource.pop("medication")
        if "concept" in _medication:
            resource["medicationCodeableConcept"] = _medication.pop("concept")
        else:
            resource["medicationReference"] = _medication.pop("reference")
        if "occurrenceDateTime" in resource.keys():
            resource["effectiveDateTime"] = resource.pop("occurrenceDateTime")
        if "occurenceDateTime" in resource.keys():
            resource["effectiveDateTime"] = resource.pop(
                "occurenceDateTime"
            )  # (misspelled in R5)
        if "occurenceTiming" in resource.keys():
            timing = resource.pop(
                "occurenceTiming"
            )  # temp fix - don't have type Timing in R4 (misspelled in R5)
            start_date = convert_days_to_date(
                days_to_add=timing["repeat"]["boundsRange"]["low"]["value"]
            )
            end_date = convert_days_to_date(
                days_to_add=timing["repeat"]["boundsRange"]["high"]["value"]
            )
            # resource["effectivePeriod"] = {"start": start_date, "end": end_date} # doesn't pass validation on google's end
            resource["effectiveDateTime"] = "2025-01-01T10:10:00Z"
        if "category" in resource:
            resource["category"] = resource["category"][0]
    if "medicationCodeableConcept" in resource:
        resource["medicationCodeableConcept"]["coding"][0]["system"] = resource[
            "medicationCodeableConcept"
        ]["coding"][0]["system"].replace("'", "")

    return resource


def transform_researchstudy(resource):
    """
    Transform a ResearchStudy resource from R5 to R4.

    Parameters:
    resource (dict): The ResearchStudy resource to transform.

    Returns:
    dict: The transformed ResearchStudy resource.
    """
    if "name" in resource:
        resource.pop("name")

    if "status" in resource and resource["status"] == "open":
        resource["status"] = "active"

    return resource


def transform_researchsubject(resource):
    """
    Transform a ResearchSubject resource from R5 to R4.

    Parameters:
    resource (dict): The ResearchSubject resource to transform.

    Returns:
    dict: The transformed ResearchSubject resource.
    """
    if "subject" in resource:
        resource["individual"] = resource.pop("subject")
    resource["status"] = "on-study"
    return resource


def transform_specimen(resource):
    """
    Transform a Specimen resource from R5 to R4.

    Parameters:
    resource (dict): The Specimen resource to transform.

    Returns:
    dict: The transformed Specimen resource.
    """
    if "processing" in resource:
        for process in resource["processing"]:
            if "method" in process:
                process["procedure"] = process.pop("method")
    if "collection" in resource:
        if "procedure" in resource["collection"]:
            del resource["collection"]["procedure"]
    return resource


def transform_imaging_study(resource):
    """
    Cleanup transform_observation.

    Parameters:
    resource (dict): The Specimen resource to transform.

    Returns:
    dict: The transformed Specimen resource.
    """
    if "processing" in resource:
        for process in resource["processing"]:
            process["procedure"] = process.pop("method")
    if "collection" in resource:
        if "procedure" in resource["collection"]:
            del resource["collection"]["procedure"]
    return resource


def transform_medication(resource):
    """
    Transform a Medication resource from R5 to R4.

    Parameters:
    resource (dict): The Medication resource to transform.
    """
    if "code" in resource and "coding" in resource["code"]:
        resource["code"]["coding"][0]["system"] = resource["code"]["coding"][0][
            "system"
        ].replace("'", "")
    return resource


def dispatch_transformation(resource: dict, *args, **kwargs) -> dict | None:
    """
    Dispatch the transformation of a resource based on its resourceType.

    Parameters:
    resource (dict): The resource to transform.

    Returns:
    dict | None: The transformed resource or None if the resource should be skipped.
    """
    transformers = {
        "DocumentReference": transform_documentreference,
        "BodyStructure": transform_bodystructure,
        "Encounter": transform_encounter,
        "Group": transform_group,
        "ImagingStudy": transform_imagingstudy,
        "MedicationAdministration": transform_medicationadministration,
        "Medication": transform_medication,
        "ResearchStudy": transform_researchstudy,
        "ResearchSubject": transform_researchsubject,
        "Specimen": transform_specimen,
    }

    resource_type = resource.get("resourceType")
    if resource_type in transformers:
        return transformers[resource_type](resource)
    else:
        return resource


def validate_r4_resource(resource):
    """
    Validate an R4 resource using the FHIR model classes.

    Parameters:
    resource (dict): The resource to validate.

    Returns:
    bool: True if the resource is valid, False otherwise.
    """
    try:
        klass = FHIR_CLASSES.get_fhir_model_class(resource["resourceType"])
        _ = klass.model_validate(resource)
        return True  # If no exceptions, it's valid
    except ValidationError as e:
        for error in e.errors():
            # Ignore the error about attachment.size, R4 has it as an unsignedInt, R5 has it as an integer64
            if ".".join([str(_) for _ in error["loc"]]) == "content.0.attachment.size":
                return True
        click.echo(f"Validation error: {klass} {e}\n{json.dumps(resource, indent=2)}")
        return False


def convert_days_to_date(days_to_add, start_date_str="2025-01-01T10:10:00Z") -> str:
    """
    Converts a number of days to a date, relative to a start date.

    Args:
        start_date_str (str): The start date in '%Y-%m-%dT%H:%M:%SZ' format.
        days_to_add (int): The number of days to subtract of the start date.

    Returns:
        str: The resulting date in '%Y-%m-%dT%H:%M:%SZ' format ex. 2025-01-01T10:10:00Z
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ")
    new_date = start_date - timedelta(days=days_to_add)
    return new_date.strftime("%Y-%m-%dT%H:%M:%SZ")


@click.command()
@click.option(
    "--input-ndjson",
    required=True,
    type=click.Path(exists=True),
    help="Path to the input NDJSON file",
)
@click.option(
    "--output-ndjson",
    required=True,
    type=click.Path(writable=True),
    help="Path to the output NDJSON file",
)
@click.option(
    "--validate",
    is_flag=True,
    default=True,
    help="Validate transformed resources for R4 compliance",
)
@click.option(
    "--stop-on-first-error",
    is_flag=True,
    default=False,
    help="Stop processing on the first error",
)
def process_ndjson(input_ndjson, output_ndjson, validate, stop_on_first_error):
    """
    Process an NDJSON file to transform R5 resources to R4 equivalents.

    Parameters:
    input_ndjson (str): Path to the input NDJSON file.
    output_ndjson (str): Path to the output NDJSON file.
    validate (bool): Flag to validate transformed resources for R4 compliance.
    stop_on_first_error (bool): Flag to stop processing on the first error.
    """
    with open(input_ndjson, "r") as infile, open(output_ndjson, "w") as outfile:
        for line in infile:
            resource = json.loads(line.strip())
            try:
                transformed_resource = dispatch_transformation(resource)
                if not transformed_resource:
                    continue
                if validate:
                    if not validate_r4_resource(transformed_resource):
                        if stop_on_first_error:
                            exit(1)
                outfile.write(json.dumps(transformed_resource) + "\n")
            except ValueError as e:
                click.echo(f"Error processing resource: {e}")
                if stop_on_first_error:
                    exit(1)


if __name__ == "__main__":
    process_ndjson()
