
# DocumentReference Paths


## Assay 

> Use case: Need to link 0..* Specimen or Patient resources to DocumentReference resources.

Solution: Create `Assay` resources, propose using [ServiceRequest](https://hl7.org/fhir/R4B/ServiceRequest.html)

### Constraints:

#### DocumentReference

* R4B: Primarily limited to Patient as the subject Reference(Patient | Practitioner | Group | Device). See https://hl7.org/fhir/R4B/documentreference-definitions.html#DocumentReference.subject
* R5: Allows for a potentially broader range of subject types beyond Patient, Reference(Any) See https://www.hl7.org/fhir/documentreference-definitions.html#DocumentReference.subject

Other:
* R4: Specimen not allowed as subject of DocumentReference


#### Group

* R4B: 
  * Group.type: code type mismatch: "specimen" is not a GroupTypeCode See https://hl7.org/fhir/R4B/valueset-group-type.html
  * Group.member[1].entity: invalid reference to a Specimen resource, want Patient, Practitioner, PractitionerRole, Device, Medication, Substance, Group  See https://hl7.org/fhir/R4B/group-definitions.html#Group.member.entity

* R5:
  * Group.type: Specimen added GroupTypeCode: https://www.hl7.org/fhir/group-definitions.html#Group.type 
  * Group.member.entity: Specimen added Reference(CareTeam | Device | Group | HealthcareService | Location | Organization | Patient | Practitioner | PractitionerRole | RelatedPerson | Specimen)  See https://www.hl7.org/fhir/group-definitions.html#Group.member.entity

Other:
* R5: This allows for more complex group definitions and relationships between group members.

