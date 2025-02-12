#!/bin/bash
# Bucket: fhir-aggregator-public
# Project: TCGA-BRCA
# Generation date: 2025-01-27T13:43:37.854032
set -euo pipefail
: "${FHIR_STORE_ID:?Need to set FHIR_STORE_ID}"
: "${DATASET_ID:?Need to set DATASET_ID}"
: "${LOCATION:?Need to set LOCATION}"
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/IG/META/part-of-search-parameter.ndjson

