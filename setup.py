from setuptools import setup, find_packages


def parse_requirements(filename: str) -> list[str]:
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]


setup(
    name="fhir_aggregator_submission",
    version="0.1.0",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "fa_submit=fhir_aggregator_submission:prep.cli",
        ],
    },
)
