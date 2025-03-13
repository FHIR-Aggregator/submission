import pathlib

import pytest

from click.testing import CliRunner
from orjson import orjson

from fhir_aggregator_submission import prep


@pytest.fixture
def tcga_path():
    return "tests/fixtures/TCGA-KIRC/META"


def test_tcga(tcga_path, tmp_path):
    if not pathlib.Path(tcga_path).exists():
        pytest.skip("TCGA data not found")
    else:
        runner = CliRunner()
        args = f"prep {tcga_path} {tmp_path} --transformers part-of,vocabulary,validate --fhir-version R4".split()
        print(args)
        result = runner.invoke(prep.cli, args)
        assert result.exit_code == 0, result.output
        vocabulary_observations = []
        with open(tmp_path / "Observation.ndjson", "r") as f:
            for line in f.readlines():
                observation = orjson.loads(line)
                if observation["code"]["coding"][0]["code"] == "vocabulary":
                    vocabulary_observations.append(observation)
        assert len(vocabulary_observations) == 2
        assert sum([len(_['component']) for _ in vocabulary_observations]) == 232
