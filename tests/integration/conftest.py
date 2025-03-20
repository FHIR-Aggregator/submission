import pytest


@pytest.fixture
def fhir_base_urls():
    """Return a list of FHIR base URLs."""
    return [
        "https://google-fhir.test-fhir-aggregator.org",
        "https://google-fhir.fhir-aggregator.org"
    ]


@pytest.fixture
def expected_part_of_study_search_parameters():
    """Return a list of expected part-of-study search parameters."""
    return ['BodyStructure.part-of-study', 'Condition.part-of-study', 'DocumentReference.part-of-study',
            'Encounter.part-of-study', 'Group.part-of-study', 'ImagingStudy.part-of-study', 'Medication.part-of-study',
            'MedicationAdministration.part-of-study', 'Observation.part-of-study', 'Patient.part-of-study',
            'Procedure.part-of-study', 'ResearchStudy.part-of-study', 'ResearchSubject.part-of-study',
            'ServiceRequest.part-of-study', 'Specimen.part-of-study']


@pytest.fixture
def expected_search_definition_urls():
    return """
http://hl7.org/fhir/SearchParameter/patient-extensions-Patient-age
http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex
http://hl7.org/fhir/us/core/SearchParameter/us-core-ethnicity
http://hl7.org/fhir/us/core/SearchParameter/us-core-race
http://fhir-aggregator.org/fhir/SearchParameter/bodystructure-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/condition-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/documentreference-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/encounter-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/group-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/imagingstudy-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/medication-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/medicationadministration-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/observation-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/patient-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/procedure-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/researchstudy-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/researchsubject-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/servicerequest-part-of-study
http://fhir-aggregator.org/fhir/SearchParameter/specimen-part-of-study
    """.split()