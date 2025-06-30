import pathlib
import argparse
import pandas as pd
from life_expectancy.region import Region


def load_data() -> pd.DataFrame:
    """Loads the oridinal data from a TSV file"""
    path = pathlib.Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    df = pd.read_csv(path, sep="\t")
    return df


def split_metadata_column(df: pd.DataFrame) -> pd.DataFrame:
    """ Splits the combined 'unit,sex,age,geo\\time' column into separate columns."""
    df[['unit', 'sex', 'age', 'region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    return df


def drop_metadata_column(df: pd.DataFrame) -> pd.DataFrame:
    """Drops the original combined metadata column."""
    return df.drop(columns=['unit,sex,age,geo\\time'])


def reshape_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Converts the DataFrame from wide to long format using melt."""
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
    removes non-numeric characters, converts to float and drop NaNs.
    """
    df['value'] = df['value'].str.replace(r'[a-zA-Z]', '', regex=True).str.strip()
    df['value'] = pd.to_numeric(df['value'], errors='coerce').astype(float)
    return df.dropna(subset=['value'])

def filter_by_region(df: pd.DataFrame, region: Region) -> pd.DataFrame:
    """Filters the DataFrame by a specific region."""
    return df[df['region'] == region.value]


def clean_data(df: pd.DataFrame, region: Region = Region.PT) -> pd.DataFrame:
    """
    Cleans and processes the raw life expectancy dataset.

    The cleaning pipeline includes:
    - Splitting the metadata column
    - Dropping the original metadata column
    - Reshaping the data to long format
    - Cleaning and converting 'year' and 'value' columns
    - Filtering by the specified region

    Args:
        df (pd.DataFrame): Raw input DataFrame.
        region (Region, optional): Region to filter by. Defaults to Region.PT.

    Returns:
        pd.DataFrame: Cleaned and filtered DataFrame ready for analysis.
    """
    df = split_metadata_column(df)
    df = drop_metadata_column(df)
    df = reshape_to_long_format(df)
    df = clean_year_column(df)
    df = clean_value_column(df)
    df = filter_by_region(df, region)
    return df


def save_data(df):
    """Saves the cleaned DataFrame to a CSV file."""
    output_path = pathlib.Path(__file__).parent / "data" / "pt_life_expectancy.csv"
    df.to_csv(output_path, index=False)

def main() -> pd.DataFrame:
    """Main function to execute the cleaning process."""

    parser = argparse.ArgumentParser(description="Cleans life expectancy data in Europe.")
    parser.add_argument("--region", default="PT", help="Country code (e.g. PT, ES, FR, etc.)")
    args = parser.parse_args()

    try:
        selected_region = Region(args.region)
    except ValueError as exc:
        raise ValueError(
            f"'{args.region}' is not a valid region. Please choose from: {[r.value for r in Region]}"
        ) from exc
    df_raw = load_data()
    df_cleaned = clean_data(df_raw, region=selected_region)
    save_data(df_cleaned)
    return df_cleaned


if __name__ == "__main__":  # pragma: no cover
    main()
