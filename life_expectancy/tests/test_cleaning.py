"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import clean_data

def test_clean_data(eu_life_expectancy_raw_fixture, eu_life_expectancy_expected_fixture):
    """Test the cleaning function for region PT using fixtures"""
    
    df_cleaned = clean_data(eu_life_expectancy_raw_fixture, region="PT")

    pd.testing.assert_frame_equal(df_cleaned.reset_index(drop=True), 
                                  eu_life_expectancy_expected_fixture.reset_index(drop=True))