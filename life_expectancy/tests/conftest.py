from pathlib import Path
import zipfile
import json
import pandas as pd
import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
OUTPUT_DIR = Path(__file__).parent / "output"

@pytest.fixture(autouse=True)
def clean_output_file():
    """Fixture to clean the output file before each test."""
    file_path = OUTPUT_DIR / "pt_life_expectancy.csv"
    if file_path.exists():
        file_path.unlink()
    yield
    if file_path.exists():
        file_path.unlink()

@pytest.fixture(scope="session")
def pt_life_expectancy_expected_fixture() -> pd.DataFrame:
    """Load expected cleaned DataFrame for Portugal life expectancy."""
    df = pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")
    df["year"] = df["year"].astype(int)
    return df

@pytest.fixture(scope="session")
def eu_life_expectancy_raw_fixture() -> pd.DataFrame:
    """Load raw TSV life expectancy data for Europe."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")

@pytest.fixture(scope="session")
def eu_life_expectancy_raw_zip_fixture() -> pd.DataFrame:
    """Load raw zipped JSON life expectancy data for Europe."""
    zip_path = FIXTURES_DIR / "eurostat_life_expect.zip"
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        filename = zip_file.namelist()[0]
        with zip_file.open(filename) as f:
            data = json.load(f)
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def pt_life_expectancy_expected_zip_fixture() -> pd.DataFrame:
    """Load expected cleaned DataFrame from zipped fixture."""
    return pd.read_csv(FIXTURES_DIR / "eurostat_life_expect_expected.csv")
