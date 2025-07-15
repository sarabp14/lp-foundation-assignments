from pathlib import Path
import zipfile
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region
from life_expectancy.data_loader import ZippedJSONLoader

FIXTURES_DIR = Path(__file__).parent / "fixtures"
DATA_DIR = Path(__file__).parent.parent / "data"

# ===== TSV Fixture =====
# Load the original TSV file
tsv_path = DATA_DIR / "eu_life_expectancy_raw.tsv"
df_tsv = pd.read_csv(tsv_path, sep="\t")

# Create a 150-row sample
sample_tsv = df_tsv.sample(n=150, random_state=42)

# Save raw sample fixture
fixture_raw_tsv_path = FIXTURES_DIR / "eu_life_expectancy_raw.tsv"
sample_tsv.to_csv(fixture_raw_tsv_path, sep="\t", index=False)

# Clean sample
cleaned_tsv = clean_data(sample_tsv, region=Region.PT)

# Save expected output fixture
fixture_expected_tsv_path = FIXTURES_DIR / "eu_life_expectancy_expected.csv"
cleaned_tsv.to_csv(fixture_expected_tsv_path, index=False)

# ===== ZIP/JSON Fixture =====
# Load the original ZIP file containing JSON
zip_path = DATA_DIR / "eurostat_life_expect.zip"
loader = ZippedJSONLoader()
df_zip = loader.load(str(zip_path))

# Create a 150-row sample
df_zip_pt = df_zip[df_zip["country"] == "PT"]
sample_zip = df_zip_pt.sample(n=150, random_state=42)

# Save sample JSON to a temporary file
json_sample_path = FIXTURES_DIR / "eurostat_life_expect.json"
sample_zip.to_json(json_sample_path, orient="records", indent=2)

# Create a ZIP file with the JSON sample
fixture_zip_path = FIXTURES_DIR / "eurostat_life_expect.zip"
with zipfile.ZipFile(fixture_zip_path, 'w') as zipf:
    zipf.write(json_sample_path, arcname="eurostat_life_expect.json")

# Clean sample
cleaned_zip = clean_data(sample_zip, region=Region.PT)

# Save expected output fixture
fixture_expected_zip_path = FIXTURES_DIR / "eurostat_life_expect_expected.csv"
cleaned_zip.to_csv(fixture_expected_zip_path, index=False)

print("Fixtures for TSV and ZIP formats successfully created!")
print("TSV sample PT count:", sample_tsv[
    sample_tsv['unit,sex,age,geo\\time'].str.contains('PT')].shape[0])
print("ZIP sample PT count:", sample_zip[sample_zip['country'] == 'PT'].shape[0])
