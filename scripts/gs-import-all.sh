set -euo pipefail
scripts/gs-bulk-import-request-IG.sh 
scripts/gs-bulk-import-request-FHIRIZED-CELLOSAURUS.sh
scripts/gs-bulk-import-request-FHIRIZED-GDC.sh
scripts/gs-bulk-import-request-FHIRIZED-HTAN.sh
scripts/gs-bulk-import-request-FHIRIZED-1KGENOMES.sh
scripts/gs-bulk-import-request-PATCHES.sh
while true; do
  result=$(gcloud healthcare operations list --dataset=$DATASET_ID --location=$LOCATION --filter 'done!=true' --format json)
  if [ "$result" == "[]" ]; then
    echo "No pending operations found."
    break
  fi
  echo "Waiting for imports to complete.  Checking again in 15 seconds..."
  sleep 15
done

echo "Import complete, indexing data"
scripts/gs-configure-search.sh

while true; do
  result=$(gcloud healthcare operations list --dataset=$DATASET_ID --location=$LOCATION --filter 'done!=true' --format json)
  if [ "$result" == "[]" ]; then
    echo "No pending operations found."
    break
  fi
  echo "Waiting for re-indexing to complete.  Checking again in 15 seconds..."
  sleep 15
done

