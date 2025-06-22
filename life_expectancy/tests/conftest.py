import pandas as pd
import pytest

from . import FIXTURES_DIR, OUTPUT_DIR

@pytest.fixture(autouse=True)
def clean_output_file_after_tests():
    """Remove output CSV after tests to avoid clutter."""
    yield
    file_path = OUTPUT_DIR / "pt_life_expectancy.csv"
    file_path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Load expected output of the Portuguese life expectancy cleaning."""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")


@pytest.fixture(scope="session")
def eu_life_expectancy_raw_fixture() -> pd.DataFrame:
    """Load the raw European life expectancy sample fixture."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")


@pytest.fixture(scope="session")
def eu_life_expectancy_expected_fixture() -> pd.DataFrame:
    """Load the expected cleaned European life expectancy fixture."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")
