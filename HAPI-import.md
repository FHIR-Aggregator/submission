# HAPI

* Start a job to load from a `public` bucket

```bash

curl -vvvv $AUTH --header "X-Upsert-Extistence-Check: disabled" --header "Content-Type: application/fhir+json" --header "Prefer: respond-async"  -X POST $FHIR_BASE'/$import' --data @scripts/bulk-import-request-PROJECT_NAME.json 

```
*Note:*
> The first time this command is run after restarting the server, it may take a few ( well more than a few ) minutes  to respond. Subsequent runs will be faster.
> See https://groups.google.com/g/hapi-fhir/c/V87IZHvlDyM/m/JIOvBvgwAQAJ

* reindex the data
```bash
curl -X POST $AUTH $FHIR_BASE'/$reindex'
# monitor server for progress
```

* To delete all data on the server
```bash
curl -X 'POST' \
  $AUTH \
  $FHIR_BASE'/$expunge' \
  -H 'accept: application/fhir+json' \
  -H 'Content-Type: application/fhir+json' \
  -d '{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "expungeEverything",
      "valueBoolean": true
    }
  ]
}'
```

## Monitoring Jobs
There are two ways to monitor the jobs:

* Query the db 

    ```bash
    docker compose exec -it postgres /bin/bash
    
    psql -U XXXX -d XXXX
    
    
    hapi=# SELECT x.start_time, x.id, x.error_count, x.definition_id, x.progress_pct,  x.stat  FROM public.bt2_job_instance x  order by x.start_time desc ;
           start_time        |                  id                  | error_count |  definition_id   |    progress_pct     |    stat
    -------------------------+--------------------------------------+-------------+------------------+---------------------+-------------
     2025-01-23 11:46:13.726 | 83fb8066-63ce-426f-a431-b39232ba4a44 |           0 | REINDEX          | 0.10927835051546392 | IN_PROGRESS
     2025-01-23 00:18:41.164 | ccc248f4-e67d-400b-8384-a2398bbdb55b |           0 | BULK_IMPORT_PULL |                   1 | COMPLETED
     2025-01-23 00:18:13.74  | 7cabb43a-568e-4a6d-95c3-e810559e903d |           0 | BULK_IMPORT_PULL |                   1 | COMPLETED
     2025-01-23 00:18:13.725 | ece310b7-cf7f-45d7-98ef-fc5860fa196a |           0 | BULK_IMPORT_PULL |                   1 | COMPLETED
     2025-01-23 00:18:13.706 | e4a659ba-f1b1-4735-807a-506c4e03bb9e |           0 | BULK_IMPORT_PULL |                   1 | COMPLETED
     2025-01-23 00:18:13.693 | 6acdb100-d745-4044-a816-aa6474d66975 |           0 | BULK_IMPORT_PULL |                   1 | COMPLETED
    (6 rows)
    ```

* Monitor the logs
    
    ```bash
    docker compose logs hapi --tail 10 -f
    ```