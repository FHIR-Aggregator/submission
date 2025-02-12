
## Transform data

* R5 to R4
The Google Healthcare API only supports R4, so we need to transform the data from R5 to R4.
[R5 support expected first half of 2025](https://groups.google.com/g/gcp-healthcare-discuss/c/DAua7sqmSl8/m/h1-nnpClBwAJ)

Note: The transformation is based on the differences between R5 and R4 observed in the TCGA data.
See scripts/prep.py `r4` transformer for details.

The individual commands below are captured here: `scripts/gs-import-all.sh`

A script to generate the import commands is available at `fhir_aggregator_submission/gs-create-bulk-import-request.py`

```bash
#  the base URL for the FHIR store
export FHIR_BASE=https://healthcare.googleapis.com/v1beta1/projects/$GOOGLE_PROJECT/locations/$GOOGLE_LOCATION/datasets/$GOOGLE_DATASET/fhirStores/$GOOGLE_DATASTORE

# Issue an import request, using the publicly available data and your google credentials
# Wildcard or individual files can be imported
curl -X POST \
    -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
    -H "Content-Type: application/json; charset=utf-8" \
    --data '{
      "contentStructure": "RESOURCE",
      "gcsSource": {
        "uri": "gs://fhir-aggregator-public/MY-R4-PROJECT/META/*.ndjson"        
      }
    }' "https://healthcare.googleapis.com/v1beta1/projects/$GOOGLE_PROJECT/locations/$GOOGLE_LOCATION/datasets/$GOOGLE_DATASET/fhirStores/$GOOGLE_DATASTORE:import"

```

## Query the data

```bash

curl \
    -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
    $FHIR_BASE'/fhir/Patient?_total=accurate&_count=0'
```
