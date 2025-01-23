## Preparation Script

This document provides instructions on how to use the `scripts/prep.py` utility to prepare your data for the FHIR Aggregator project.

### Overview

The `scripts/prep.py` script is designed to finalize and validate the preparation of your data. 
This includes setting up environment variables, creating necessary directories, and performing initial data transformations.

### Prerequisites

Before running the `scripts/prep.py` script, ensure you have the following installed:

- Python 3.12 or later
- `pip` (Python package installer)

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/FHIR-Aggregator/submission.git
    cd submission
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install the required Python packages:**

    ```bash
    pip install -r scripts/requirements.txt
    ```

### Usage

1. **Run the preparation script:**

    ```bash
    python scripts/prep.py prep --help
      Usage: prep.py prep [OPTIONS] INPUT_PATH OUTPUT_PATH
      
        Run a set of transformations on the input META directory.
      
        INPUT_PATH META directory containing the input NDJSON files
        OUTPUT_PATH the output META directory
      
      Options:
        --transformers TEXT  CSV Transformation steps.  Known transformations:
                             [assay,part-of,r4,validate,validate_references,
                             reseed], default:assay,part-of,validate
        --seed TEXT          Reseed all references with the new seed
        --help               Show this message and exit.
   
    ```

    The current set of transformation steps are:
    - `assay`: Creates a ServiceRequest "Assay" type to focus Group, Specimen and DocumentReference types.  Used by the TCGA projects.
    - `part-of`: Adds a "part-of" relationship between the all resources and the ResearchStudy
    - `r4`: Converts the input files to FHIR R4 format.  All input files are assumed to be in R5 format.
    - `validate`: Validates the transformed files
      - `validate_references`: Validates the references in the transformed files
    - `reseed`: Reseeds all resource.id and references to a new UUID based on the seed value
      - `seed`: The seed value to use for the reseed operation.

### Other Scripts

- Upload the files to the bucket - see scripts/upload.sh
- Create a import manifest - see scripts/[hapi|gs]create-bulk-import-request.py
- Inventory the server - see scripts/fhir-inventory.py

