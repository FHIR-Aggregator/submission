from pytest import fixture


@fixture
def research_study_id():
    return "test-research-study-id"


@fixture
def research_study(research_study_id):
    return {
        "resourceType": "ResearchStudy",
        "id": research_study_id,
        "identifier": [
            {
                "system": "https://gdc.cancer.gov/study_id",
                "value": "TEST-STUDY",
            }
        ],
    }


@fixture
def patients(research_study_id):
    return [
        {
            "resourceType": "Patient",
            "id": "0368f85d-9028-5810-bda6-ec6ced4c0544",
            "extension": [
                {
                    "url": "http://fhir-aggregator.org/fhir/StructureDefinition/part-of-study",
                    "valueReference": {
                        "reference": f"ResearchStudy/{research_study_id}"
                    },
                },
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                    "valueCode": "M",
                },
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                    "valueString": "white",
                },
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                    "valueString": "not hispanic or latino",
                },
                {
                    "url": "http://hl7.org/fhir/SearchParameter/patient-extensions-Patient-age",
                    "valueQuantity": {"value": 63},
                },
                {
                    "url": "http://example.org/fhir/StructureDefinition/part-of-study",
                    "valueReference": {
                        "reference": "ResearchStudy/ed0d94e6-51c3-5833-9a20-8ff1c5efc286"
                    },
                },
            ],
            "gender": "male",
        },
        {
            "resourceType": "Patient",
            "id": "bd185005-11c2-55e7-a148-506d57abfce6",
            "meta": {
                "versionId": "1",
                "lastUpdated": "2025-01-23T00:18:41.574+00:00",
            },
            "extension": [
                {
                    "url": "http://fhir-aggregator.org/fhir/StructureDefinition/part-of-study",
                    "valueReference": {
                        "reference": f"ResearchStudy/{research_study_id}"
                    },
                },
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                    "valueCode": "F",
                },
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                    "valueString": "white",
                },
                {
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                    "valueString": "not reported",
                },
                {
                    "url": "http://hl7.org/fhir/SearchParameter/patient-extensions-Patient-age",
                    "valueQuantity": {"value": 55},
                },
                {
                    "url": "http://example.org/fhir/StructureDefinition/part-of-study",
                    "valueReference": {
                        "reference": "ResearchStudy/ed0d94e6-51c3-5833-9a20-8ff1c5efc286"
                    },
                },
            ],
            "gender": "female",
        },
    ]


@fixture
def conditions():
    return [
        {
            "bodySite": [
                {
                    "coding": [
                        {
                            "code": "110736001",
                            "display": "Bronchus and lung",
                            "system": "http://snomed.info/sct",
                        }
                    ]
                }
            ],
            "category": [
                {
                    "coding": [
                        {
                            "code": "encounter-diagnosis",
                            "display": "Encounter Diagnosis",
                            "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                        },
                        {
                            "code": "439401001",
                            "display": "Diagnosis",
                            "system": "http://snomed.info/sct",
                        },
                    ]
                }
            ],
            "clinicalStatus": {
                "coding": [
                    {
                        "code": "unknown",
                        "display": "unknown",
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    }
                ]
            },
            "code": {
                "coding": [
                    {
                        "code": "Squamous cell carcinoma, NOS",
                        "display": "Squamous cell carcinoma, NOS",
                        "system": "https://gdc.cancer.gov/primary_diagnosis",
                    }
                ]
            },
            "encounter": {
                "reference": "Encounter/ae0ed86b-7945-5de0-ab41-4b26ab2f84a1"
            },
            "extension": [
                {
                    "url": "http://example.org/fhir/StructureDefinition/part-of-study",
                    "valueReference": {
                        "reference": "ResearchStudy/687eece2-87f6-5ebd-94db-e97497b57498"
                    },
                }
            ],
            "id": "8003bd68-c75d-52b0-8856-ed17f406835f",
            "identifier": [
                {
                    "system": "https://gdc.cancer.gov/submitter_diagnosis_id",
                    "use": "official",
                    "value": "TCGA-37-3789_diagnosis",
                }
            ],
            "meta": {"lastUpdated": "2025-01-28T01:05:18.283307+00:00"},
            "onsetAge": {
                "code": "d",
                "system": "http://unitsofmeasure.org",
                "unit": "days",
                "value": 23782,
            },
            "resourceType": "Condition",
            "stage": [
                {
                    "assessment": [
                        {
                            "reference": "Observation/a23b319b-9adf-5b86-b1f2-e63bb4050bd1"
                        },
                        {
                            "reference": "Observation/d69bf598-3e71-5648-a998-4dd283e0eeff"
                        },
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "C48705",
                                "display": "N0",
                                "system": "https://ncit.nci.nih.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "3203106",
                                "display": "N0",
                                "system": "https://cadsr.cancer.gov/",
                            },
                            {
                                "code": "1222590007",
                                "display": "N0",
                                "system": "http://snomed.info/sct",
                            },
                        ]
                    },
                },
                {
                    "assessment": [
                        {
                            "reference": "Observation/f2eaa600-5584-59d3-a2e9-b1d93e08f5f6"
                        },
                        {
                            "reference": "Observation/d69bf598-3e71-5648-a998-4dd283e0eeff"
                        },
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "C27976",
                                "display": "Stage IB",
                                "system": "https://ncit.nci.nih.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "3203222",
                                "display": "Stage IB",
                                "system": "https://cadsr.cancer.gov/",
                            },
                            {
                                "code": "1222593009",
                                "display": "Stage IB",
                                "system": "http://snomed.info/sct",
                            },
                        ]
                    },
                },
                {
                    "assessment": [
                        {
                            "reference": "Observation/57730708-cf4b-5ab3-b773-3c1a5eb7c83f"
                        },
                        {
                            "reference": "Observation/d69bf598-3e71-5648-a998-4dd283e0eeff"
                        },
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "C48724",
                                "display": "T2",
                                "system": "https://ncit.nci.nih.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "3045435",
                                "display": "T2",
                                "system": "https://cadsr.cancer.gov/",
                            },
                            {
                                "code": "1222589003",
                                "display": "T2",
                                "system": "http://snomed.info/sct",
                            },
                        ]
                    },
                },
                {
                    "assessment": [
                        {
                            "reference": "Observation/d69bf598-3e71-5648-a998-4dd283e0eeff"
                        }
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "2785839",
                                "display": "Not Reported",
                                "system": "https://cadsr.cancer.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "2785839",
                                "display": "neoplasm_histologic_grade",
                                "system": "https://cadsr.cancer.gov",
                            }
                        ]
                    },
                },
            ],
            "subject": {"reference": "Patient/d93548fb-8c38-5223-9927-ef38b3ee76f1"},
        },
        {
            "bodySite": [
                {
                    "coding": [
                        {
                            "code": "110736001",
                            "display": "Bronchus and lung",
                            "system": "http://snomed.info/sct",
                        }
                    ]
                }
            ],
            "category": [
                {
                    "coding": [
                        {
                            "code": "encounter-diagnosis",
                            "display": "Encounter Diagnosis",
                            "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                        },
                        {
                            "code": "439401001",
                            "display": "Diagnosis",
                            "system": "http://snomed.info/sct",
                        },
                    ]
                }
            ],
            "clinicalStatus": {
                "coding": [
                    {
                        "code": "unknown",
                        "display": "unknown",
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    }
                ]
            },
            "code": {
                "coding": [
                    {
                        "code": "Basaloid squamous cell carcinoma",
                        "display": "Basaloid squamous cell carcinoma",
                        "system": "https://gdc.cancer.gov/primary_diagnosis",
                    }
                ]
            },
            "encounter": {
                "reference": "Encounter/2102b2f4-10fb-5ff0-aa91-bfc53ae8e2b7"
            },
            "extension": [
                {
                    "url": "http://example.org/fhir/StructureDefinition/part-of-study",
                    "valueReference": {
                        "reference": "ResearchStudy/687eece2-87f6-5ebd-94db-e97497b57498"
                    },
                }
            ],
            "id": "24eb37d8-2e4a-536a-9a67-31675e54db53",
            "identifier": [
                {
                    "system": "https://gdc.cancer.gov/submitter_diagnosis_id",
                    "use": "official",
                    "value": "TCGA-58-A46N_diagnosis",
                }
            ],
            "meta": {"lastUpdated": "2025-01-28T01:05:18.281939+00:00"},
            "onsetAge": {
                "code": "d",
                "system": "http://unitsofmeasure.org",
                "unit": "days",
                "value": 19050,
            },
            "resourceType": "Condition",
            "stage": [
                {
                    "assessment": [
                        {
                            "reference": "Observation/6e96d655-9754-526d-9d68-7f14a8186899"
                        },
                        {
                            "reference": "Observation/28d02378-18de-5659-8d6c-482955c6250b"
                        },
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "C48699",
                                "display": "M0",
                                "system": "https://ncit.nci.nih.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "3045439",
                                "display": "M0",
                                "system": "https://cadsr.cancer.gov/",
                            },
                            {
                                "code": "1222587001",
                                "display": "M0",
                                "system": "http://snomed.info/sct",
                            },
                        ]
                    },
                },
                {
                    "assessment": [
                        {
                            "reference": "Observation/bdf967ae-65a9-55c6-9262-6fe2f890b8f2"
                        },
                        {
                            "reference": "Observation/28d02378-18de-5659-8d6c-482955c6250b"
                        },
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "C48705",
                                "display": "N0",
                                "system": "https://ncit.nci.nih.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "3203106",
                                "display": "N0",
                                "system": "https://cadsr.cancer.gov/",
                            },
                            {
                                "code": "1222590007",
                                "display": "N0",
                                "system": "http://snomed.info/sct",
                            },
                        ]
                    },
                },
                {
                    "assessment": [
                        {
                            "reference": "Observation/2f4e12c0-34cb-5991-bd86-ced3fa2c5cbf"
                        },
                        {
                            "reference": "Observation/28d02378-18de-5659-8d6c-482955c6250b"
                        },
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "C27976",
                                "display": "Stage IB",
                                "system": "https://ncit.nci.nih.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "3203222",
                                "display": "Stage IB",
                                "system": "https://cadsr.cancer.gov/",
                            },
                            {
                                "code": "1222593009",
                                "display": "Stage IB",
                                "system": "http://snomed.info/sct",
                            },
                        ]
                    },
                },
                {
                    "assessment": [
                        {
                            "reference": "Observation/4fb2da9c-1202-54ea-ab39-11fad590fa47"
                        },
                        {
                            "reference": "Observation/28d02378-18de-5659-8d6c-482955c6250b"
                        },
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "C48725",
                                "display": "T2a",
                                "system": "https://ncit.nci.nih.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "3045435",
                                "display": "T2a",
                                "system": "https://cadsr.cancer.gov/",
                            },
                            {
                                "code": "1222589003",
                                "display": "T2a",
                                "system": "http://snomed.info/sct",
                            },
                        ]
                    },
                },
                {
                    "assessment": [
                        {
                            "reference": "Observation/28d02378-18de-5659-8d6c-482955c6250b"
                        }
                    ],
                    "summary": {
                        "coding": [
                            {
                                "code": "2785839",
                                "display": "Not Reported",
                                "system": "https://cadsr.cancer.gov",
                            }
                        ]
                    },
                    "type": {
                        "coding": [
                            {
                                "code": "2785839",
                                "display": "neoplasm_histologic_grade",
                                "system": "https://cadsr.cancer.gov",
                            }
                        ]
                    },
                },
            ],
            "subject": {"reference": "Patient/f0a00da8-94a0-52c9-aacc-2998308aa6bb"},
        },
    ]


@fixture
def document_references():
    return [
        {
            "resourceType": "DocumentReference",
            "id": "ec8b85b7-7965-5d0e-a106-e9b1e94f53c2",
            "identifier": [
                {
                    "use": "official",
                    "system": "https://gdc.cancer.gov/file_id",
                    "value": "eb8d5bd9-2b78-4798-97f9-6940ed8a2f78",
                },
                {
                    "use": "secondary",
                    "system": "https://gdc.cancer.gov/submitter_id",
                    "value": "fdeff875-8210-41d3-83ca-d21b42d00f01",
                },
            ],
            "version": "2",
            "status": "current",
            "type": {
                "coding": [
                    {
                        "system": "https://gdc.cancer.gov/data_format",
                        "code": "VCF",
                        "display": "VCF",
                    }
                ]
            },
            "category": [
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/data_category",
                            "code": "Simple Nucleotide Variation",
                            "display": "Simple Nucleotide Variation",
                        }
                    ]
                },
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/platform",
                            "code": "Illumina",
                            "display": "Illumina",
                        }
                    ]
                },
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/experimental_strategy",
                            "code": "WXS",
                            "display": "WXS",
                        }
                    ]
                },
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/data_type",
                            "code": "Annotated Somatic Mutation",
                            "display": "Annotated Somatic Mutation",
                        }
                    ]
                },
            ],
            "subject": {"reference": "Group/0472b446-ffca-5fdc-9dd7-18e49ac9b1e2"},
            "date": "2022-02-03T21:38:30.819180-06:00",
            "content": [
                {
                    "attachment": {
                        "contentType": "VCF",
                        "url": "https://api.gdc.cancer.gov/data/eb8d5bd9-2b78-4798-97f9-6940ed8a2f78",
                        "size": 121056,
                        "hash": "fbe08cfa1a64a55fa8fec330f42482fc",
                        "title": "TCGA_LUAD.4e1a2500-98ba-417b-a58a-973f98852496.wxs.VarScan2.somatic_annotation.vcf.gz",
                    },
                    "profile": [
                        {
                            "valueCoding": {
                                "system": "https://gdc.cancer.gov/data_format",
                                "code": "VCF",
                                "display": "VCF",
                            }
                        }
                    ],
                }
            ],
        },
        {
            "resourceType": "DocumentReference",
            "id": "23dff4b1-f3c2-52b2-ad65-37a035e00662",
            "identifier": [
                {
                    "use": "official",
                    "system": "https://gdc.cancer.gov/file_id",
                    "value": "c568fdc8-6942-44ff-a9d9-3f7a03fdc62a",
                },
                {
                    "use": "secondary",
                    "system": "https://gdc.cancer.gov/submitter_id",
                    "value": "0aabc766-606f-4944-9aa9-ac9ce2f9a963",
                },
            ],
            "version": "1",
            "status": "current",
            "type": {
                "coding": [
                    {
                        "system": "https://gdc.cancer.gov/data_format",
                        "code": "TSV",
                        "display": "TSV",
                    }
                ]
            },
            "category": [
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/data_category",
                            "code": "Transcriptome Profiling",
                            "display": "Transcriptome Profiling",
                        }
                    ]
                },
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/platform",
                            "code": "Illumina",
                            "display": "Illumina",
                        }
                    ]
                },
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/experimental_strategy",
                            "code": "RNA-Seq",
                            "display": "RNA-Seq",
                        }
                    ]
                },
                {
                    "coding": [
                        {
                            "system": "https://gdc.cancer.gov/data_type",
                            "code": "Gene Expression Quantification",
                            "display": "Gene Expression Quantification",
                        }
                    ]
                },
            ],
            "subject": {"reference": "Specimen/62fd09c2-0615-5083-be89-5022807da126"},
            "date": "2021-12-13T19:41:57.249715-06:00",
            "content": [
                {
                    "attachment": {
                        "contentType": "TSV",
                        "url": "https://api.gdc.cancer.gov/data/c568fdc8-6942-44ff-a9d9-3f7a03fdc62a",
                        "size": 4226419,
                        "hash": "a352405548831c550b90884f50402acc",
                        "title": "367864dd-ccd2-473e-9661-6ff4342a4e64.rna_seq.augmented_star_gene_counts.tsv",
                    },
                    "profile": [
                        {
                            "valueCoding": {
                                "system": "https://gdc.cancer.gov/data_format",
                                "code": "TSV",
                                "display": "TSV",
                            }
                        }
                    ],
                }
            ],
        },
    ]
