import json
import zipfile
from abc import ABC, abstractmethod
import pandas as pd

class DataLoaderStrategy(ABC):
    """Abstract base class for data loading strategies."""
    @abstractmethod
    def load(self, file_path: str) -> pd.DataFrame:
        pass

class TSVLoader(DataLoaderStrategy):
    """Loader for TSV files."""
    def load(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, sep="\t")

class ZippedJSONLoader(DataLoaderStrategy):
    """Loader for JSON files within a ZIP archive."""
    def load(self, file_path: str) -> pd.DataFrame:
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            filename = zip_file.namelist()[0]
            with zip_file.open(filename) as f:
                data = json.load(f)
        return pd.DataFrame(data)
