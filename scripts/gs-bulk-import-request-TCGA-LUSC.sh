#!/bin/bash
# Bucket: fhir-aggregator-public
# Project: TCGA-LUSC
# Generation date: 2025-01-27T13:46:13.306546
set -euo pipefail
: "${FHIR_STORE_ID:?Need to set FHIR_STORE_ID}"
: "${DATASET_ID:?Need to set DATASET_ID}"
: "${LOCATION:?Need to set CLUSTER_NAME}"
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/BodyStructure.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Condition.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/DocumentReference.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Encounter.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Group.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/ImagingStudy.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Medication.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/MedicationAdministration.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Observation.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Patient.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Procedure.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/ResearchStudy.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/ResearchSubject.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/ServiceRequest.ndjson
gcloud healthcare fhir-stores import gcs $FHIR_STORE_ID --dataset=$DATASET_ID --location=$LOCATION --content-structure=resource --async --gcs-uri=gs://fhir-aggregator-public/R4/TCGA-LUSC/META/Specimen.ndjson
