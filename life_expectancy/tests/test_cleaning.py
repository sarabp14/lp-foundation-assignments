"""Tests for the cleaning module"""
import sys
import os
import pandas as pd

from life_expectancy.cleaning import clean_data

def test_clean_data(eu_life_expectancy_raw_fixture, pt_life_expectancy_expected_fixture):
    df_cleaned = clean_data(eu_life_expectancy_raw_fixture, region="PT")

    pd.testing.assert_frame_equal(
        df_cleaned.reset_index(drop=True),
        pt_life_expectancy_expected_fixture.reset_index(drop=True)
    )