import json
import sys

import pandas as pd

from fhir_aggregator_submission.vocabulary import (
    extract_coding_values,
    extract_extension_values,
    VocabularyCollector,
)


def test_vocabulary_collector(patients, research_study):
    collector = VocabularyCollector()
    for patient in patients:
        # print(patient['extension'])
        collector.collect(patient)

    observations = collector.to_observations()
    print([_["extension"] for _ in observations])
    assert len(observations) == 1
    observation = observations[0]
    assert observation["resourceType"] == "Observation"
    assert observation["code"]["coding"][0]["code"] == "vocabulary"

    from fhir_query import vocabulary

    bundle = {"entry": [{"resource": observation}, {"resource": research_study}]}
    simplified = vocabulary.vocabulary_simplifier(bundle)
    df = pd.DataFrame(simplified)
    df.to_csv(sys.stdout, sep="\t", index=False)

    row = df.loc[
        df["extension_url"]
        == "http://hl7.org/fhir/SearchParameter/patient-extensions-Patient-age"
    ]
    row_dict = row.to_dict(orient="records")[0]
    print(row_dict)

    assert row_dict["low"] == 55
    assert row_dict["high"] == 63


def test_vocabulary_patient(patients):
    coding_dict = None
    for resource in patients:
        coding_dict = extract_coding_values(resource, coding_dict)
    assert coding_dict == {}, "Should return empty dict if no coding values found"


def test_vocabulary_patient_extension(patients):
    extension_dict = None
    for resource in patients:
        extension_dict = extract_extension_values(resource, extension_dict)
    print(json.dumps(extension_dict))
    expected_values = {
        "Patient.extension~http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex": {
            "M": {"count": 1, "valueCode": "M"},
            "F": {"count": 1, "valueCode": "F"},
        },
        "Patient.extension~http://hl7.org/fhir/us/core/StructureDefinition/us-core-race": {
            "white": {"count": 2, "valueString": "white"}
        },
        "Patient.extension~http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity": {
            "not hispanic or latino": {
                "count": 1,
                "valueString": "not hispanic or latino",
            },
            "not reported": {"count": 1, "valueString": "not reported"},
        },
        "Patient.extension~http://hl7.org/fhir/SearchParameter/patient-extensions-Patient-age": {
            "range": {
                "min": 55,
                "max": 63,
            }
        },
    }

    assert extension_dict == expected_values, "Should return expected_values"


def test_vocabulary_condition(conditions):
    coding_dict = None
    for resource in conditions:
        coding_dict = extract_coding_values(resource, coding_dict)
    expected_values = [
        "Condition.bodySite",
        "Condition.category",
        "Condition.clinicalStatus",
        "Condition.code",
        "Condition.stage",
    ]
    assert (
        sorted(coding_dict.keys()) == expected_values
    ), "Should return expected_values"


def test_vocabulary_document_reference_extension(document_references):
    extension_dict = None
    for resource in document_references:
        extension_dict = extract_extension_values(resource, extension_dict)
    assert extension_dict == {}, "Should return empty dict if no coding values found"


def test_vocabulary_document_reference(document_references):
    coding_dict = None
    for resource in document_references:
        coding_dict = extract_coding_values(resource, coding_dict)
    expected_values = ["DocumentReference.category", "DocumentReference.type"]
    assert (
        sorted(coding_dict.keys()) == expected_values
    ), "Should return expected_values"
