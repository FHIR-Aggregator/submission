# see https://cloud.google.com/healthcare-api/docs/reference/rest/v1beta1/projects.locations.datasets.fhirStores/configureSearch
set -euo pipefail
: "${FHIR_STORE_ID:?Need to set FHIR_STORE_ID}"
: "${DATASET_ID:?Need to set DATASET_ID}"
: "${LOCATION:?Need to set LOCATION}"

# Note: The configureSearch call operates as a 'last-one-wins'
# operation.  This means that if you call it multiple times with
# different canonicalUrls values, the last call will be the one that is used.
# This is why we include all of the canonicalUrls in a single call.


curl -X POST     -H "Authorization: Bearer $(gcloud auth application-default print-access-token)"     -H "Content-Type: application/json; charset=utf-8"     --data '{
        "canonicalUrls": [
          "http://fhir-aggregator.org/fhir/SearchParameter/bodystructure-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/condition-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/documentreference-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/encounter-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/group-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/imagingstudy-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/medication-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/medicationadministration-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/observation-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/patient-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/procedure-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/researchstudy-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/researchsubject-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/servicerequest-part-of-study",
          "http://fhir-aggregator.org/fhir/SearchParameter/specimen-part-of-study",
          "http://hl7.org/fhir/us/core/SearchParameter/us-core-ethnicity",
          "http://hl7.org/fhir/SearchParameter/patient-extensions-Patient-age",
          "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
          "http://hl7.org/fhir/us/core/SearchParameter/us-core-race"

        ],
    }'     "https://healthcare.googleapis.com/v1beta1/projects/$PROJECT_ID/locations/$LOCATION/datasets/$DATASET_ID/fhirStores/$FHIR_STORE_ID:configureSearch"

