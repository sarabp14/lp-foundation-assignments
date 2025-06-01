import pandas as pd
from pathlib import Path
from life_expectancy.cleaning import clean_data  # ajusta conforme o teu módulo

OUTPUT_DIR = Path(__file__).parent.parent / "life_expectancy" / "data"

def test_clean_data(pt_life_expectancy_expected):
    # Executa a função de limpeza (ela já grava o CSV)
    clean_data("PT")

    # Caminho do ficheiro que a função gravou
    output_path = OUTPUT_DIR / "pt_life_expectancy.csv"

    # Lê o ficheiro gravado pela função
    pt_life_expectancy_actual = pd.read_csv(output_path)

    # Compara com o DataFrame esperado
    pd.testing.assert_frame_equal(pt_life_expectancy_actual, pt_life_expectancy_expected)
