"""Tests for the cleaning module"""
import sys
import os
import pandas as pd

import life_expectancy
from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region



def test_clean_data(eu_life_expectancy_raw_fixture, pt_life_expectancy_expected_fixture):
    df_cleaned = clean_data(eu_life_expectancy_raw_fixture, region=Region.PT)

    print("Regiões no df_cleaned:", df_cleaned['region'].unique())
    print("Regiões na fixture esperada:", pt_life_expectancy_expected_fixture['region'].unique())
    print("Linhas df_cleaned:", len(df_cleaned))
    print("Linhas esperado:", len(pt_life_expectancy_expected_fixture))

    try:
        pd.testing.assert_frame_equal(
            df_cleaned.reset_index(drop=True),
            pt_life_expectancy_expected_fixture.reset_index(drop=True)
        )
    except AssertionError:
        print("Diferenças no dataframe limpo:")
        print(df_cleaned[~df_cleaned.isin(pt_life_expectancy_expected_fixture)].dropna())
        print("Diferenças no dataframe esperado:")
        print(pt_life_expectancy_expected_fixture[~pt_life_expectancy_expected_fixture.isin(df_cleaned)].dropna())
        raise
