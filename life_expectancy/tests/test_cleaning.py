"""Tests for the cleaning module"""

import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region

def test_clean_data_tsv(eu_life_expectancy_raw_fixture, pt_life_expectancy_expected_fixture):
    """Test cleaning of TSV data for Portugal."""
    df_raw = eu_life_expectancy_raw_fixture
    df_cleaned = clean_data(df_raw, region=Region.PT)

    expected = pt_life_expectancy_expected_fixture

    pd.testing.assert_frame_equal(
        df_cleaned.reset_index(drop=True),
        expected.reset_index(drop=True)
    )

def test_clean_data_zip(eu_life_expectancy_raw_zip_fixture,
                        pt_life_expectancy_expected_zip_fixture):
    """Test cleaning of zipped JSON data for Portugal."""
    df_raw = eu_life_expectancy_raw_zip_fixture
    df_cleaned = clean_data(df_raw, region=Region.PT)

    expected = pt_life_expectancy_expected_zip_fixture

    pd.testing.assert_frame_equal(
        df_cleaned.reset_index(drop=True),
        expected.reset_index(drop=True)
    )
