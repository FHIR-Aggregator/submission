import importlib
import click
import json
from pydantic import ValidationError

# Import the R4 classes
FHIR_CLASSES = importlib.import_module('fhir.resources.R4B')


def transform_documentreference(resource):
    """
    Transform a DocumentReference resource from R5 to R4.

    Parameters:
    resource (dict): The DocumentReference resource to transform.

    Returns:
    dict: The transformed DocumentReference resource.
    """
    del resource["version"]
    if "content" in resource:
        for content in resource["content"]:
            if "profile" in content:
                content["format"] = content.pop("profile")[0]["valueCoding"]
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
        resource["reasonReference"] = [ref["reference"] for ref in resource.pop("reference", [])]
    if "class" in resource:
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
    del resource["membership"]
    resource["actual"] = True
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
                series["modality"]["system"] = series["modality"]["system"].replace(" ", "")
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
        resource["effectiveDateTime"] = resource.pop("occurenceDateTime")
        if "category" in resource:
            resource["category"] = resource["category"][0]
    if "medicationCodeableConcept" in resource:
        resource["medicationCodeableConcept"]["coding"][0]["system"] = resource["medicationCodeableConcept"]["coding"][0]["system"].replace("'", "")
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
    return resource


def transform_researchsubject(resource):
    """
    Transform a ResearchSubject resource from R5 to R4.

    Parameters:
    resource (dict): The ResearchSubject resource to transform.

    Returns:
    dict: The transformed ResearchSubject resource.
    """
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
            process["procedure"] = process.pop("method")
    if "collection" in resource:
        if "procedure" in resource["collection"]:
            del resource["collection"]["procedure"]
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
        klass = FHIR_CLASSES.get_fhir_model_class(resource['resourceType'])
        _ = klass.model_validate(resource)
        return True  # If no exceptions, it's valid
    except ValidationError as e:
        for error in e.errors():
            # Ignore the error about attachment.size, R4 has it as an unsignedInt, R5 has it as an integer64
            if '.'.join([str(_) for _ in error['loc']]) == 'content.0.attachment.size':
                return True
        click.echo(f"Validation error: {klass} {e}\n{json.dumps(resource, indent=2)}")
        return False


@click.command()
@click.option('--input-ndjson', required=True, type=click.Path(exists=True), help='Path to the input NDJSON file')
@click.option('--output-ndjson', required=True, type=click.Path(writable=True), help='Path to the output NDJSON file')
@click.option('--validate', is_flag=True, default=True, help='Validate transformed resources for R4 compliance')
@click.option('--stop-on-first-error', is_flag=True, default=False, help='Stop processing on the first error')
def process_ndjson(input_ndjson, output_ndjson, validate, stop_on_first_error):
    """
    Process an NDJSON file to transform R5 resources to R4 equivalents.

    Parameters:
    input_ndjson (str): Path to the input NDJSON file.
    output_ndjson (str): Path to the output NDJSON file.
    validate (bool): Flag to validate transformed resources for R4 compliance.
    stop_on_first_error (bool): Flag to stop processing on the first error.
    """
    with open(input_ndjson, 'r') as infile, open(output_ndjson, 'w') as outfile:
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
                outfile.write(json.dumps(transformed_resource) + '\n')
            except ValueError as e:
                click.echo(f"Error processing resource: {e}")
                if stop_on_first_error:
                    exit(1)


if __name__ == "__main__":
    process_ndjson()