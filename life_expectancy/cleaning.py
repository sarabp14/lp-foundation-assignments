import pathlib
import argparse
import numpy as np
import pandas as pd
from life_expectancy.region import Region
from life_expectancy.data_loader import TSVLoader, ZippedJSONLoader

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
        raise ValueError(f"Unsupported file format: {file_format}")   
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
    """
    Cleans and processes the life expectancy dataset, for both TSV and JSON formats.

    For TSV:
    - Splits metadata column
    - Drops metadata
    - Reshapes to long format
    - Cleans year and value columns
    - Filters by region

    For JSON:
    - Renames columns to match expected format
    - Filters by region
    - Selects and renames necessary columns
    """
    if 'unit,sex,age,geo\\time' in df.columns:
        # TSV format
        df = split_metadata_column(df)
        df = drop_metadata_column(df)
        df = reshape_to_long_format(df)
        df = clean_year_column(df)
        df = clean_value_column(df)
        df = filter_by_region(df, region)
        return df

    elif {'unit', 'sex', 'age', 'country', 'year', 'life_expectancy'}.issubset(df.columns):
        # JSON format
        df = df.rename(columns={"country": "region", "life_expectancy": "value"})
        df = filter_by_region(df, region)
        df = df[["unit", "sex", "age", "region", "year", "value"]]
        return df

    else:
        raise ValueError("Unrecognized data format: missing expected columns.")


def save_data(df: pd.DataFrame, path: pathlib.Path) -> None:
    """Saves cleaned DataFrame to CSV file."""
    df.to_csv(path, index=False)


def main() -> None:
    """Main function to clean life expectancy data."""
    parser = argparse.ArgumentParser(description="Cleans life expectancy data in Europe.")
    parser.add_argument("--region", default="PT", help="Country code (e.g. PT, ES, FR, etc.)")
    parser.add_argument("--format", default="tsv", help="Data format: tsv or zip")
    args = parser.parse_args()

    region = Region(args.region)
    file_format = args.format

    df_raw = load_data(file_format)
    df_clean = clean_data(df_raw, region=region)

    output_dir = pathlib.Path(__file__).parent / "data"
    filename = f"cleaned_life_expectancy_{region.value}.{file_format}.csv"
    output_path = output_dir / filename
    save_data(df_clean, output_path)
    print(f"Cleaned data saved to {output_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
