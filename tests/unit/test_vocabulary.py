import json
import sys
from collections import defaultdict

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

    bundle = {"link": [{"url": "http://example.com"}], "entry": [{"resource": observation}, {"resource": research_study}]}
    simplified = vocabulary.vocabulary_simplifier(bundle)
    assert sorted([_['code'] for _ in simplified if _['code'] in ['white', 'asian']]) == ['asian', 'white']
    df = pd.DataFrame(simplified)
    df.to_csv(sys.stdout, sep="\t", index=False)

    rows = df.loc[
        df["extension_url"]
        == "http://hl7.org/fhir/SearchParameter/patient-extensions-Patient-age"
    ]
    row_list = rows.to_dict(orient="records")
    assert len(row_list) == 1
    row_dict = row_list[0]
    print(row_dict)

    assert row_dict["low"] == 55
    assert row_dict["high"] == 63

    rows = df.loc[
        df["extension_url"]
        == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
    ]
    row_list = rows.to_dict(orient="records")
    assert len(row_list) == 2


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
            "white": {"count": 1, "valueString": "white"},
            "asian": {"count": 1, "valueString": "asian"}
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
    assert extension_dict == {
        'DocumentReference.extension~https://nih-ncpi.github.io/ncpi-fhir-ig-2/StructureDefinition/file-size': {
            'range': {'min': 12345, 'max': 56789}}}, "Should return expected values"


def test_vocabulary_document_reference(document_references):
    coding_dict = None
    for resource in document_references:
        coding_dict = extract_coding_values(resource, coding_dict)
    expected_values = ["DocumentReference.category", "DocumentReference.type"]
    assert (
        sorted(coding_dict.keys()) == expected_values
    ), "Should return expected_values"
    assert sorted(coding_dict['DocumentReference.type'].keys()) == ['TSV', 'VCF'], "expected values"


def test_vocabulary_collector_document_references(document_references, research_study):
    collector = VocabularyCollector()
    for document_reference in document_references:
        # print(patient['extension'])
        collector.collect(document_reference)

    observations = collector.to_observations()

    from pprint import pprint
    pprint(observations)

    assert len(observations) == 1
    by_path = defaultdict(list)
    observation = observations[0]
    assert len(observation["component"]) == 10
    for component in observation["component"]:
        for coding in component["code"]["coding"]:
            if coding["system"] == "http://fhir-aggregator.org/fhir/CodeSystem/vocabulary/path":
                by_path[coding["code"]].append(component)
    assert len(by_path['DocumentReference.type']) == 2, ("expected 2 DocumentReference.type", by_path['DocumentReference.type'])

    from fhir_query import vocabulary

    bundle = {"link": [{"url": "http://example.com"}], "entry": [{"resource": observation}, {"resource": research_study}]}
    simplified = vocabulary.vocabulary_simplifier(bundle)
    codes = [_['code'] for _ in simplified if _['code'] in ['VCF', 'TSV']]
    print(codes)
    assert sorted(codes) == ['TSV', 'VCF'], "expected values"
    paths = [_['path'] for _ in simplified if _['code'] in ['VCF', 'TSV']]
    assert paths == ['DocumentReference.type', 'DocumentReference.type'], "expected paths"

