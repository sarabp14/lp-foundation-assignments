"""Tests for the cleaning module"""
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region


def test_clean_data(eu_life_expectancy_raw_fixture, pt_life_expectancy_expected_fixture):
    """Test the clean_data function with the raw data fixture and expected output fixture."""
    df_cleaned = clean_data(eu_life_expectancy_raw_fixture, region=Region.PT)
    print(df_cleaned.shape)
    try:
        pd.testing.assert_frame_equal(
            df_cleaned.reset_index(drop=True),
            pt_life_expectancy_expected_fixture.reset_index(drop=True)
        )
    except AssertionError:
        print("Differences in clean dataset:")
        print(df_cleaned[~df_cleaned.isin(pt_life_expectancy_expected_fixture)].dropna())
        print("Differences in expected dataset :")
        print(pt_life_expectancy_expected_fixture
              [~pt_life_expectancy_expected_fixture.isin(df_cleaned)].dropna())
        raise
     