"""Tests for the cleaning module"""

import zipfile
import json
from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region

FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Fixtures loading functions

def eu_life_expectancy_raw_fixture():
    """Load raw TSV sample fixture as DataFrame."""
    path = FIXTURES_DIR / "eu_life_expectancy_raw.tsv"
    return pd.read_csv(path, sep="\t")

def eu_life_expectancy_raw_zip_fixture():
    """Load raw zipped JSON sample fixture as DataFrame."""
    zip_path = FIXTURES_DIR / "eurostat_life_expect.zip"
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        filename = zip_file.namelist()[0]
        with zip_file.open(filename) as f:
            data = json.load(f)
    return pd.DataFrame(data)

def pt_life_expectancy_expected_fixture():
    """Load expected cleaned DataFrame."""
    path = FIXTURES_DIR / "eu_life_expectancy_expected.csv"
    return pd.read_csv(path)

def pt_life_expectancy_expected_zip_fixture():
    """Load expected cleaned DataFrame from ZIP fixture."""
    path = FIXTURES_DIR / "eurostat_life_expect_expected.csv"
    return pd.read_csv(path)


# Tests

def test_clean_data_tsv():
    """Test clean_data function with raw TSV data."""
    df_raw = eu_life_expectancy_raw_fixture()
    df_cleaned = clean_data(df_raw, region=Region.PT)

    expected = pt_life_expectancy_expected_fixture()

    try:
        pd.testing.assert_frame_equal(
            df_cleaned.reset_index(drop=True),
            expected.reset_index(drop=True)
        )
    except AssertionError:
        print("Differences in cleaned dataset:")
        print(df_cleaned[~df_cleaned.isin(expected)].dropna())
        print("Differences in expected dataset:")
        print(expected[~expected.isin(df_cleaned)].dropna())
        raise

def test_clean_data_zip():
    """Test clean_data function with raw zipped JSON data."""
    df_raw = eu_life_expectancy_raw_zip_fixture()
    df_cleaned = clean_data(df_raw, region=Region.PT)

    expected = pt_life_expectancy_expected_zip_fixture()

    try:
        pd.testing.assert_frame_equal(
            df_cleaned.reset_index(drop=True),
            expected.reset_index(drop=True)
        )
    except AssertionError:
        print("Differences in cleaned dataset:")
        print(df_cleaned[~df_cleaned.isin(expected)].dropna())
        print("Differences in expected dataset:")
        print(expected[~expected.isin(df_cleaned)].dropna())
        raise
