## Preparing Data for the FHIR Aggregator

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
4. **Set up environment variables:**

   Ensure you have a .env file in the root directory of the project. You can use the .env-sample file as a template:  
   ```
   cp .env-sample .env
   # Edit the .env file to include your specific environment variables.
   source .env 
   ```

### Usage

1. **Run the preparation script on your data:**

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


### Uploading Data to bucket

- Upload the files to the `public` bucket - see scripts/upload.sh
- Import manifest - see scripts/[hapi|gs]create-bulk-import-request.py
   - Creates scripts/bulk-import-request-PROJECT_NAME.json

### Importing Data
* See [HAPI-import.md](HAPI-import.md) for details on loading data into the FHIR server.
* See [Google-import.md](Google-import.md) for details on loading data into the Google FHIR server.


### Other Scripts

- Inventory the server - see scripts/fhir-inventory.py


* get the counts of data loaded
```bash
python scripts/fhir-inventory.py count-resources 
```

* query resource counts:

```bash
python scripts/fhir-inventory.py count-resources
```

