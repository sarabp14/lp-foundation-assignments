from pathlib import Path
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
    # Clean up after tests
    if file_path.exists():
        file_path.unlink()

def clean_output_file_after_tests():
    """Fixture to clean the output file after all tests."""
    yield
    file_path = OUTPUT_DIR / "pt_life_expectancy.csv"
    if file_path.exists():
        file_path.unlink()

@pytest.fixture(scope="session")
def pt_life_expectancy_expected_fixture() -> pd.DataFrame:
    """Fixture to load the expected output DataFrame for Portugal life expectancy."""
    df = pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")
    df["year"] = df["year"].astype(int)  # Important to avoid type mismatch errors
    return df

@pytest.fixture(scope="session")
def eu_life_expectancy_raw_fixture() -> pd.DataFrame:
    """Fixture to load the raw life expectancy data for Europe."""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep="\t")
