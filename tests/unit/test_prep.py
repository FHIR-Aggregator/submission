import pytest

from click.testing import CliRunner
from fhir_aggregator_submission import prep


@pytest.fixture
def tcga_path():
    return "tests/fixtures/TCGA-KIRC/META"


def test_tcga(tcga_path, tmp_path):
    runner = CliRunner()
    args = f"prep {tcga_path} {tmp_path} --transformers part-of,vocabulary,validate --fhir-version R4".split()
    print(args)
    result = runner.invoke(prep.cli, args)
    assert result.exit_code == 0, result.output
