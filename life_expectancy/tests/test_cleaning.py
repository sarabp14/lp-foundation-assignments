import pandas as pd
from pathlib import Path
from life_expectancy.cleaning import clean_data  # ajusta conforme o teu módulo

OUTPUT_DIR = Path(__file__).parent.parent / "life_expectancy" / "data"

def test_clean_data(pt_life_expectancy_expected):
    # Executa a função de limpeza
    df_cleaned = clean_data("PT")

    # Gera o caminho para salvar o CSV
    output_path = OUTPUT_DIR / "pt_life_expectancy.csv"

    # Salva o DataFrame limpo no CSV (para o teste poder ler)
    df_cleaned.to_csv(output_path, index=False)

    # Agora lê o CSV gerado
    pt_life_expectancy_actual = pd.read_csv(output_path)

    # Compara os DataFrames (podes adaptar conforme os teus critérios)
    pd.testing.assert_frame_equal(pt_life_expectancy_actual, pt_life_expectancy_expected)
