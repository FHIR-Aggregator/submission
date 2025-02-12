curl -X POST \
    -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data '{
        "canonicalUrls": [
          "http://example.org/fhir/SearchParameter/assay-part-of-study",
          "http://example.org/fhir/SearchParameter/bodystructure-part-of-study",
          "http://example.org/fhir/SearchParameter/condition-part-of-study",
          "http://example.org/fhir/SearchParameter/documentreference-part-of-study",
          "http://example.org/fhir/SearchParameter/encounter-part-of-study",
          "http://example.org/fhir/SearchParameter/group-part-of-study",
          "http://example.org/fhir/SearchParameter/imagingstudy-part-of-study",
          "http://example.org/fhir/SearchParameter/medicationadministration-part-of-study",
          "http://example.org/fhir/SearchParameter/observation-part-of-study",
          "http://example.org/fhir/SearchParameter/patient-part-of-study",
          "http://example.org/fhir/SearchParameter/procedure-part-of-study",
          "http://example.org/fhir/SearchParameter/researchstudy-part-of-study",
          "http://example.org/fhir/SearchParameter/researchsubject-part-of-study",
          "http://example.org/fhir/SearchParameter/specimen-part-of-study"
        ],
    }' \
    "https://healthcare.googleapis.com/v1beta1/projects/$PROJECT_ID/locations/$LOCATION/datasets/$DATASET_ID/fhirStores/$FHIR_STORE_ID:configureSearch"
