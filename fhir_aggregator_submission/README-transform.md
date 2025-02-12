
# Google Healthcare API transformations


## Differences between R5 and R4

* Validation errors &/or schema changes reported by the Google FHIR validator
 
```text
DocumentReference.content[0]: unknown field: "profile"
DocumentReference.subject: invalid reference to a Specimen resource, want Patient, Practitioner, Group, Device
BodyStructure: unknown field: "includedStructure"
Encounter.status: code type mismatch: "completed" is not a EncounterStatusCode
Group: unknown field: "membership" at Group.type: code type mismatch: "specimen" is not a GroupTypeCode
Group.member[1].entity: invalid reference to a Specimen resource, want Patient, Practitioner, PractitionerRole, Device, Medication, Substance, Group"

ImagingStudy.series[0].modality: unknown field: "coding"
MedicationAdministration.category: invalid value (expected a CodeableConcept object):  [{"coding": [{"system": "https://cadsr.cancer.gov
at MedicationAdministration: unknown field: "medication"
at MedicationAdministration: unknown field: "occurenceDateTime""
ResearchStudy: unknown field: "name""
ResearchSubject: unknown field: "subject"
ResearchSubject.status: code type mismatch: "active" is not a ResearchSubjectStatusCode"
Specimen.collection: unknown field: "procedure"

MedicationAdministration.medicationCodeableConcept.coding[0].system: invalid uri "'embedded quotes'"
ResearchSubject.status: code type mismatch: "active" is not a ResearchSubjectStatusCode"

Encounter.status: code type mismatch: "completed" is not a EncounterStatusCode"
ImagingStudy.series[0].modality.system: invalid uri " http:/..."
```

```bash

python scripts/transform.py --input-ndjson $R5_PROJECT/META/Group.ndjson --output-ndjson $R4_PROJECT/META/Group.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/DocumentReference.ndjson --output-ndjson $R4_PROJECT/META/DocumentReference.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/BodyStructure.ndjson --output-ndjson $R4_PROJECT/META/BodyStructure.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/Encounter.ndjson --output-ndjson $R4_PROJECT/META/Encounter.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/Group.ndjson --output-ndjson $R4_PROJECT/META/Group.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/ImagingStudy.ndjson --output-ndjson $R4_PROJECT/META/ImagingStudy.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/MedicationAdministration.ndjson --output-ndjson $R4_PROJECT/META/MedicationAdministration.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/ResearchStudy.ndjson --output-ndjson $R4_PROJECT/META/ResearchStudy.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/ResearchSubject.ndjson --output-ndjson $R4_PROJECT/META/ResearchSubject.ndjson --validate
python scripts/transform.py --input-ndjson $R5_PROJECT/META/Specimen.ndjson --output-ndjson $R4_PROJECT/META/Specimen.ndjson --validate

```

