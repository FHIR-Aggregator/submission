import importlib
import json
import pathlib
import sys
from urllib.parse import urlparse
import uuid
import mimetypes
from typing import Generator, Any
from click_default_group import DefaultGroup

import click
from halo import Halo
from nested_lookup import nested_lookup, nested_alter
from pydantic import ValidationError

from transform import dispatch_transformation

DEFAULT_TRANSFORMERS = "assay,part-of,validate"

# Import the R4 classes
FHIR_R4_CLASSES = importlib.import_module("fhir.resources.R4B")
FHIR_R5_CLASSES = importlib.import_module("fhir.resources")


# Add additional mimetypes
mimetypes.add_type("text/x-r", ".R", strict=True)
mimetypes.add_type("text/x-r", ".r", strict=True)
mimetypes.add_type("text/tab-separated-values", ".maf", strict=True)
mimetypes.add_type("text/tab-separated-values", ".bed5", strict=True)
mimetypes.add_type("text/tab-separated-values", ".bed", strict=True)
mimetypes.add_type("text/tab-separated-values+vcf", ".vcf", strict=True)
mimetypes.add_type("text/tab-separated-values", ".sam", strict=True)
mimetypes.add_type("text/yaml", ".yaml", strict=True)
mimetypes.add_type("text/x-markdown", ".md", strict=True)
mimetypes.add_type("text/x-markdown", ".markdown", strict=True)


# Codes used to identify medical devices. Includes concepts from SNOMED CT (http://www.snomed.org/) where concept is-a 49062001 (Device) and is provided as a suggestive example.
# SCTID: 706687001 Software


def apply_part_of(resource, research_study_id, *args, **kwargs):
    """
    Add a part-of extension to the resource.
    :param resource:
    :param research_study_id:
    :return:
    """
    if "ResearchStudy" == resource["resourceType"]:
        return resource

    if "extension" not in resource:
        resource["extension"] = []

    for ext in resource["extension"]:
        if "part-of-study" in ext["url"]:
            return resource

    extension = [
        {
            "url": "http://example.org/fhir/StructureDefinition/part-of-study",
            "valueReference": {"reference": f"ResearchStudy/{research_study_id}"},
        }
    ]

    resource["extension"].extend(extension)
    return resource


@click.group(cls=DefaultGroup, default="prep", default_if_no_args=True)
def cli():
    """Transform R5 FHIR resources for NCPI FHIR Aggregator."""
    pass


class Emitters:
    """Write the resource to the output path."""

    def __init__(self, output_path):
        self._files = {}
        if not isinstance(output_path, pathlib.Path):
            output_path = pathlib.Path(output_path)
        self._output_path = output_path

    def emit(self, resource):
        """Write the resource to the output path."""
        if resource:
            if resource["resourceType"] not in self._files:
                self._files[resource["resourceType"]] = open(
                    self._output_path / f"{resource['resourceType']}.ndjson", "w"
                )
            self._files[resource["resourceType"]].write(json.dumps(resource) + "\n")

    def close(self):
        """Close the open files."""
        for file in self._files.values():
            file.close()
        self._files = {}

    def __del__(self):
        """Ensure all files are closed when the object is destroyed."""
        self.close()


REFERENCES = []
IDS = []


def validate(resource, fhir_version, *args, **kwargs):
    """Validate the resource."""
    klasses = FHIR_R5_CLASSES if fhir_version == "R5" else FHIR_R4_CLASSES
    klass = klasses.get_fhir_model_class(resource["resourceType"])
    try:
        klass.model_validate(resource)
    except (ValidationError, AttributeError) as e:
        ignore = False
        # # ignore the error about attachment.size, R4 has it as an unsignedInt, R5 has it as an integer64
        # if e.errors():
        #     errors = e.errors()
        #     if len(errors) == 1 and 'loc' in e.errors()[0] and e.errors()[0]['loc'] == ('content', 0, 'attachment', 'size'):
        #         ignore = True
        if not ignore:
            click.echo(
                f"Validation error: {fhir_version} {klass} {e}\n{json.dumps(resource, indent=2)}"
            )
            exit(1)

    IDS.append(f"{resource['resourceType']}/{resource['id']}")
    for _ in nested_lookup("reference", resource):
        if isinstance(_, str):
            REFERENCES.append(_)
        elif isinstance(_, dict):
            # https://www.hl7.org/fhir/medicationrequest-definitions.html#MedicationRequest.medication
            # is a reference to a Medication resource https://www.hl7.org/fhir/references.html#CodeableReference
            # so it has a reference.reference form, strip it out
            REFERENCES.append(_["reference"])
        else:
            raise ValueError(f"Invalid reference type: {type(_)}")
    return resource


def reseed(resource, seed, *args, **kwargs):
    """Reseed the resource.  Change all the ids to be based on the seed."""
    resource["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS, resource["id"] + seed))

    def callback(reference):
        if isinstance(reference, dict):
            return reference
        resource_type, resource_id = reference.split("/")
        return (
            f"{resource_type}/{str(uuid.uuid5(uuid.NAMESPACE_DNS, resource_id + seed))}"
        )

    resource = nested_alter(resource, "reference", callback)

    return resource


def validate_references(*args, **kwargs):
    """Validate the references."""
    references = set(REFERENCES)
    ids = set(IDS)
    if not references.issubset(ids):
        _ = Exception(f"references not found {references - ids}")
        click.echo(f"references not found {references - ids}")
        exit(1)


@cli.command(name="prep")
@click.argument("input_path", required=True, type=click.Path(exists=True))
@click.argument("output_path", required=True, type=click.Path())
@click.option(
    "--transformers",
    required=False,
    default=DEFAULT_TRANSFORMERS,
    help=f"CSV Transformation steps.  Known transformations: [assay,part-of,r4,validate,validate_references, reseed], default:{DEFAULT_TRANSFORMERS}",
)
@click.option(
    "--seed",
    required=False,
    default=None,
    help="Reseed all references with the new seed",
)
def prep(input_path, output_path, transformers, seed):
    """Run a set of transformations on the input META directory.

    \b
    INPUT_PATH META directory containing the input NDJSON files
    OUTPUT_PATH the output META directory
    """
    if not pathlib.Path(output_path).exists():
        pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    fhir_version = "R4" if "r4" in transformers.lower() else "R5"  # default to R5

    assert fhir_version in ["R4", "R5"], f"Invalid FHIR version: {fhir_version}"

    # if seed:
    #     # reseed needs to be before validate
    #     transformers = 'assay,part-of,reseed,validate,validate_references'

    transformers = transformers.split(",")
    emitters = Emitters(output_path)

    research_study = pathlib.Path(input_path) / "ResearchStudy.ndjson"
    with open(research_study, "r") as research_study_file:
        research_study = json.loads(research_study_file.readline().strip())
        research_study_id = research_study["id"]

    transformer_map = {
        "part-of": apply_part_of,
        "r4": dispatch_transformation,
        "validate": validate,
        "reseed": reseed,
    }
    known_transformers = set(transformer_map.keys())
    for k in known_transformers:
        if k not in transformers:
            del transformer_map[k]

    if not set(list(transformer_map.keys())) == set(transformers):
        unknown_transformers = set(transformers) - known_transformers
        if unknown_transformers != {"assay"}:
            click.secho(
                f"Unknown transformers: {unknown_transformers}",
                file=sys.stderr,
                fg="red",
            )
            exit(1)
    if "reseed" in transformers and not seed:
        click.secho(
            f"reseed specified, please specify --seed", file=sys.stderr, fg="red"
        )
        exit(1)

    emitted = []
    click.echo(f"Transformers: {transformers}", file=sys.stderr)
    with Halo(
        text="Processing",
        spinner="line",
        placement="right",
        color="white",
        stream=sys.stderr,
    ) as spinner:
        # assay is a special case, it requires a set of resources to work ['DocumentReference', 'Group', 'Specimen']
        last_resource_type = None
        if "assay" in transformers:
            for resource in create_assays(fhir_version, input_path):
                for transformer in transformer_map.values():
                    resource = transformer(
                        resource=resource,
                        research_study_id=research_study_id,
                        fhir_version=fhir_version,
                        seed=seed,
                    )
                if not resource:
                    continue
                emitters.emit(resource)
                if (
                    last_resource_type
                    and last_resource_type != resource["resourceType"]
                ):
                    spinner.succeed(last_resource_type)
                    spinner.start()
                last_resource_type = resource["resourceType"]
                spinner.text = f"Processing {last_resource_type}"
            emitted.extend(["DocumentReference", "Group"])
        for resource in pathlib.Path(input_path).glob("*.ndjson"):
            if resource.stem in emitted:
                continue
            with open(resource, "r") as infile:
                for line in infile:
                    resource = json.loads(line.strip())
                    for transformer in transformer_map.values():
                        resource = transformer(
                            resource=resource,
                            research_study_id=research_study_id,
                            fhir_version=fhir_version,
                            seed=seed,
                        )
                    if not resource:
                        continue
                    emitters.emit(resource)
                    if (
                        last_resource_type
                        and last_resource_type != resource["resourceType"]
                    ):
                        spinner.succeed(last_resource_type)
                        spinner.start()
                    last_resource_type = resource["resourceType"]
                    spinner.text = f"Processing {last_resource_type}"

                    emitted.append(resource["resourceType"])
        spinner.succeed("Processing complete")
        if "validate" in transformers:
            spinner.text = "Validating references"
            validate_references()
            spinner.succeed("Validation complete")
    emitters.close()


def create_assays(fhir_version, input_path) -> Generator[dict, None, None]:
    """Create assays from the input files [DocumentReference, Group, Specimen]."""
    document_reference = pathlib.Path(input_path) / "DocumentReference.ndjson"
    with open(document_reference, "r") as doc_file:
        document_references = [json.loads(line.strip()) for line in doc_file]
    with open(pathlib.Path(input_path) / "Group.ndjson", "r") as group_file:
        groups: list[dict] = [json.loads(line.strip()) for line in group_file]
    specimen = pathlib.Path(input_path) / "Specimen.ndjson"
    with open(specimen, "r") as specimen_file:
        specimens = {
            spec["id"]: spec
            for spec in (json.loads(line.strip()) for line in specimen_file)
        }
    # Index document references by group
    document_references_by_group: dict[str, list[dict]] = {}
    for doc in document_references:
        group_id = doc["subject"]["reference"].split("/")[1]
        if group_id not in document_references_by_group:
            document_references_by_group[group_id] = []
        document_references_by_group[group_id].append(doc)
    assays = []
    # find  documents that are part of a group that has a specimen
    # R4B does not support groups of specimens
    groups_with_specimen = set()
    for group in groups:

        patient_reference = None
        specimen_references = []
        # find the specimen references in the group
        for member in group.get("member", []):
            if "reference" in member["entity"]:
                if member["entity"]["reference"].startswith("Specimen/"):
                    specimen_id = member["entity"]["reference"].split("/")[1]
                    specimen_references.append(member["entity"]["reference"])
                    if specimen_id in specimens:
                        patient_reference = specimens[specimen_id]["subject"][
                            "reference"
                        ]

        # skip if no patient or specimen references
        if not patient_reference or not specimen_references:
            continue

        groups_with_specimen.add(group["id"])

        # get all the docs for the group
        assay_documents = [
            doc for doc in document_references_by_group.get(group["id"], [])
        ]

        # create the assay
        assay_id = group["id"]  # for now, use the group id as the assay id
        assay_dict = create_assay_refactor_docs(
            assay_id,
            patient_reference,
            specimen_references,
            assay_documents,
            fhir_version,
        )
        assay_dict["extension"] = group.get("extension", [])
        assays.append(assay_dict)
    # remove groups with Specimen members
    groups = [group for group in groups if group["id"] not in groups_with_specimen]
    # find documents that have a specimen as subject
    for doc in document_references:
        if doc["subject"]["reference"].startswith("Specimen/"):
            specimen_references = []
            specimen_id = doc["subject"]["reference"].split("/")[1]
            specimen_references.append(doc["subject"]["reference"])
            patient_reference = specimens[specimen_id]["subject"]["reference"]
            assert (
                patient_reference
            ), f"Patient reference not found for specimen {specimen_id}"
            assay_documents = [doc]
            assay_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc["id"] + "-assay"))
            assay_dict = create_assay_refactor_docs(
                assay_id,
                patient_reference,
                specimen_references,
                assay_documents,
                fhir_version,
            )
            assert doc["subject"]["reference"].startswith(
                "Patient/"
            ), f"Document subject is not a patient: {doc['subject']['reference']}"
            assays.append(assay_dict)
    docs_with_non_patient_subject = [
        (doc["id"], doc["subject"]["reference"])
        for doc in document_references
        if not doc["subject"]["reference"].startswith("Patient/")
    ]
    assert len(docs_with_non_patient_subject) == len(
        groups
    ), f"Documents have groups with non-patient subject: {docs_with_non_patient_subject}"

    # write the assays to file
    for _ in assays:
        yield _

    for _ in document_references:
        yield _

    for _ in groups:
        yield _


def update_mime_type(doc: dict) -> dict:
    """Update the mime type of the document to be a valid mime type."""
    attachment = doc["content"][0]["attachment"]
    title = attachment.get("title", None)
    url = attachment.get("url", None)
    # get path from url
    file_name = title
    if url:
        path = urlparse(url).path
        if "." in path:
            file_name = path
    (mimetype, enc) = mimetypes.guess_type(file_name, strict=False)
    if mimetype is None:
        mimetype = "application/octet-stream"
    assert "vcard" not in mimetype, f"Invalid mime type for {file_name}"

    attachment["contentType"] = mimetype
    return doc


def create_assay_refactor_docs(
    assay_id: str,
    patient_reference: str,
    specimen_references: list[str],
    assay_documents: list[dict],
    fhir_version="R4",
) -> dict:
    """
    Create an R4B `Assay`, adjusting the `DocumentReference` to have the patient as the subject and the assay as a related context.

    Parameters:
    assay_id (str): The unique identifier for the assay.
    patient_reference (str): The reference to the patient associated with the assay.
    specimen_references (list[str]): A list of references to the specimens associated with the assay.
    assay_documents (list[dict]): A list of document references to be included in the assay.

    Returns:
    dict: The created assay dictionary.
    """
    assay_dict: dict[str, Any] = {
        "resourceType": "ServiceRequest",
        "id": assay_id,
        "status": "completed",
        "intent": "order",
        # TODO - set category and code based on the document type
        "category": [
            {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "108252007",
                        "display": "Laboratory procedure",
                    }
                ]
            }
        ],
        "code": {
            # 15220000 | "Laboratory test"
            # 405824009 | "Genetic test"
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "15220000",
                    "display": "Laboratory test",
                }
            ]
        },
        "subject": {"reference": patient_reference},
        #  "performer": [{"reference": "Practitioner/ETL"}],  # IT personnel merging or unmerging patient records
        "text": {
            "status": "generated",
            "div": '<div xmlns="http://www.w3.org/1999/xhtml">Autogenerated Assay. Packages references to Subject, Specimen and DocumentReference</div>',
        },
        "specimen": [{"reference": _} for _ in specimen_references],
    }

    if fhir_version == "R5":
        assay_dict["code"]["concept"] = {}
        assay_dict["code"]["concept"]["coding"] = assay_dict["code"]["coding"]
        del assay_dict["code"]["coding"]

    # TODO - move this to its own function
    # now modify the document.subject to the patient and add the assay to the context.related
    for doc in assay_documents:
        doc["subject"] = {"reference": patient_reference}

        if fhir_version != "R4":
            if "basedOn" not in doc:
                doc["basedOn"] = []
            # set reference to the Assay in basedOn
            based_on = doc["basedOn"]
            based_on.append(
                {"reference": f"{assay_dict['resourceType']}/{assay_dict['id']}"}
            )

            # set size to a string
            attachment = doc["content"][0]["attachment"]
            if not isinstance(attachment["size"], str):
                attachment["size"] = str(attachment["size"])
        else:
            # make it a R4B document
            # these fields don't exist in R4B
            del doc["version"]
            del doc["content"][0]["profile"]

            # set reference to Assay in context.related
            if "context" not in doc:
                doc["context"] = {}
            context = doc["context"]
            if "related" not in context:
                context["related"] = []
            # TODO R5 does not use related as a list of References(Any) remove it from here
            context["related"].append(
                {"reference": f"{assay_dict['resourceType']}/{assay_dict['id']}"}
            )
            context["related"].extend([{"reference": _} for _ in specimen_references])

        # ensure mime type is set correctly
        update_mime_type(doc)

    return assay_dict


if __name__ == "__main__":
    cli()
