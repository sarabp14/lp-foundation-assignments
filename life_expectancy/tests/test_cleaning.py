"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import load_data, clean_data

def test_clean_data(pt_life_expectancy_expected):
    """Testa a função de limpeza de dados para a região PT"""
    df_raw = load_data()
    df_cleaned = clean_data(df_raw, region="PT")

    # Compara com o DataFrame esperado
    pd.testing.assert_frame_equal(df_cleaned.reset_index(drop=True), pt_life_expectancy_expected)
