from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region

FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Original raw data path
input_path = Path(__file__).parent.parent / "data" / "eu_life_expectancy_raw.tsv"
df = pd.read_csv(input_path, sep="\t")

# Create sample
sample_df = df.sample(n=150, random_state=42)


# Save raw sample fixture
fixture_raw_path = FIXTURES_DIR / "eu_life_expectancy_raw.tsv"
sample_df.to_csv(fixture_raw_path, sep="\t", index=False)

# Clean sample
cleaned_df = clean_data(sample_df, region=Region.PT)

# Save expected output fixture (com nome corrigido)
fixture_expected_path = FIXTURES_DIR / "eu_life_expectancy_expected.csv"
cleaned_df.to_csv(fixture_expected_path, index=False)

print("Fixtures successfully created!")