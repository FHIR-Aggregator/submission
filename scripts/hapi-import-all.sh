# load all the TCGA data into the FHIR server HAPI

curl -vvvv $AUTH   --header "X-Upsert-Extistence-Check: disabled"   --header "Content-Type: application/fhir+json"   --header "Prefer: respond-async"   -X POST $FHIR_BASE'/$import'   --data @scripts/bulk-import-request-TCGA-LUAD.json
curl -vvvv $AUTH   --header "X-Upsert-Extistence-Check: disabled"   --header "Content-Type: application/fhir+json"   --header "Prefer: respond-async"   -X POST $FHIR_BASE'/$import'   --data @scripts/bulk-import-request-TCGA-KIRC.json
curl -vvvv $AUTH   --header "X-Upsert-Extistence-Check: disabled"   --header "Content-Type: application/fhir+json"   --header "Prefer: respond-async"   -X POST $FHIR_BASE'/$import'   --data @scripts/bulk-import-request-TCGA-HNSC.json
curl -vvvv $AUTH   --header "X-Upsert-Extistence-Check: disabled"   --header "Content-Type: application/fhir+json"   --header "Prefer: respond-async"   -X POST $FHIR_BASE'/$import'   --data @scripts/bulk-import-request-TCGA-BRCA.json
curl -vvvv $AUTH   --header "X-Upsert-Extistence-Check: disabled"   --header "Content-Type: application/fhir+json"   --header "Prefer: respond-async"   -X POST $FHIR_BASE'/$import'   --data @scripts/bulk-import-request-TCGA-LUSC.json
