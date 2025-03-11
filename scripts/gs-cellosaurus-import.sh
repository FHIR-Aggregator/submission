#!/bin/bash

set -euo pipefail

: "${GOOGLE_PROJECT:?Need to set GOOGLE_PROJECT}"
: "${GOOGLE_LOCATION:?Need to set GOOGLE_LOCATION}"
: "${GOOGLE_DATASET:?Need to set GOOGLE_DATASET}"
: "${GOOGLE_DATASTORE:?Need to set GOOGLE_DATASTORE}"

fa_submit prep CELLOSAURUS/META OUTPUT/R4/CELLOSAURUS --transformers r4,vocabulary,validate

scripts/upload.sh OUTPUT/R4/CELLOSAURUS FHIRIZED-CELLOSAURUS

curl -X POST \
    -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data '{
      "contentStructure": "RESOURCE",
      "gcsSource": {
        "uri": "gs://fhir-aggregator-public/FHIRIZED-CELLOSAURUS/META/*.ndjson"
      }
    }' "https://healthcare.googleapis.com/v1beta1/projects/$GOOGLE_PROJECT/locations/$GOOGLE_LOCATION/datasets/$GOOGLE_DATASET/fhirStores/$GOOGLE_DATASTORE:import"
