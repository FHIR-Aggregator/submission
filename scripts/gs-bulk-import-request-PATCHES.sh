#!/bin/bash
# Bucket: fhir-aggregator-public
# Project: FHIRIZED-HTAN
# Generation date: 2025-03-11T08:48:15.868727
set -euo pipefail
: "${FHIR_STORE_ID:?Need to set FHIR_STORE_ID}"
: "${DATASET_ID:?Need to set DATASET_ID}"
: "${LOCATION:?Need to set LOCATION}"
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/PATCHES/META/Observation-vocabulary.ndjson
