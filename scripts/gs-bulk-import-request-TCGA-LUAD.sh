#!/bin/bash
# Bucket: fhir-aggregator-public
# Project: TCGA-LUAD
# Generation date: 2025-01-27T13:46:08.902790
set -euo pipefail
: "${FHIR_STORE_ID:?Need to set FHIR_STORE_ID}"
: "${DATASET_ID:?Need to set DATASET_ID}"
: "${LOCATION:?Need to set LOCATION}"
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/BodyStructure.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Condition.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/DocumentReference.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Encounter.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Group.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/ImagingStudy.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Medication.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/MedicationAdministration.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Observation.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Patient.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Procedure.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/ResearchStudy.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/ResearchSubject.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/ServiceRequest.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUAD/META/Specimen.ndjson
