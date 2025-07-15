import pathlib
import argparse
import pandas as pd
import numpy as np
from life_expectancy.region import Region
from life_expectancy.data_loader import ZippedJSONLoader, TSVLoader

def load_data(file_format: str = "tsv") -> pd.DataFrame:
    """Loads data in different formats based on input."""
    path_dir = pathlib.Path(__file__).parent / "data"
    if file_format == "tsv":
        path = path_dir / "eu_life_expectancy_raw.tsv"
        loader = TSVLoader()
    elif file_format == "zip":
        path = path_dir / "eurostat_life_expect.zip"
        loader = ZippedJSONLoader()
    else:
        raise ValueError("Unsupported format. Use: 'tsv' or 'zip'")
    return loader.load(str(path))


def split_metadata_column(df: pd.DataFrame) -> pd.DataFrame:
    """ Splits the combined 'unit,sex,age,geo\\time' column into separate columns."""
    df[['unit', 'sex', 'age', 'region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    return df


def drop_metadata_column(df: pd.DataFrame) -> pd.DataFrame:
    """Drops the original combined metadata column."""
    return df.drop(columns=['unit,sex,age,geo\\time'])


def reshape_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Converts the DataFrame from wide to long format using melt."""
    df.columns = df.columns.str.strip()
    return df.melt(
        id_vars=['unit', 'sex', 'age', 'region'],
        var_name='year',
        value_name='value'
    )


def clean_year_column(df: pd.DataFrame) -> pd.DataFrame:
    """Converts the 'year' column to integer. """
    df['year'] = df['year'].astype(int)
    return df


def clean_value_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the 'value' column:
    - Replaces ':' with NaN
    - Ensures the column is treated as string for regex operations
    - Removes all non-numeric characters except for the decimal point
    - Converts to float (errors become NaN)
    - Drops NaN values
    """
    df['value'] = df['value'].replace(':', np.nan)
    df['value'] = df['value'].astype(str)
    df['value'] = df['value'].str.replace(r'[^0-9\.]', '', regex=True).str.strip()
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df.dropna(subset=['value'])

def filter_by_region(df: pd.DataFrame, region: Region) -> pd.DataFrame:
    """Filters the DataFrame by a specific region."""
    return df[df['region'] == region.value]

def clean_data(df: pd.DataFrame, region: Region = Region.PT) -> pd.DataFrame:
    