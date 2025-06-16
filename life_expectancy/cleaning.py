import pathlib
import argparse
import pandas as pd


def load_data():
    """Carrega o dataset original a partir do ficheiro TSV"""
    path = pathlib.Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    df = pd.read_csv(path, sep="\t")
    return df


def clean_data(df, region="PT"):
    """Limpa os dados e filtra pela região"""
    # Separar a primeira coluna em 4 novas
    df[['unit', 'sex', 'age', 'region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)

    # Remover coluna antiga
    df = df.drop(columns=['unit,sex,age,geo\\time'])

    # Converter anos para formato longo
    df = df.melt(
        id_vars=['unit', 'sex', 'age', 'region'],
        var_name='year',
        value_name='value'
    )

    # Converter ano para inteiro
    df['year'] = df['year'].astype(int)

    # Limpar valores não numéricos e converter para float
    df['value'] = df['value'].str.replace(r'[a-zA-Z]', '', regex=True).str.strip()
    df['value'] = pd.to_numeric(df['value'], errors='coerce').astype(float)
    df = df.dropna(subset=['value'])

    # Filtrar por região
    df = df[df['region'] == region]

    return df


def save_data(df):
    """Guarda os dados limpos num ficheiro CSV"""
    output_path = pathlib.Path(__file__).parent / "data" / "pt_life_expectancy.csv"
    df.to_csv(output_path, index=False)

def main():
    """Função principal para carregar, limpar e guardar os dados"""

    parser = argparse.ArgumentParser(description="Cleans data for life expectancy in Europe")
    parser.add_argument("--region", default="PT", help="Country code (eg: PT, ES, FR)")
    args = parser.parse_args()

    df_raw = load_data()
    df_cleaned = clean_data(df_raw, region=args.region)
    save_data(df_cleaned)


if __name__ == "__main__":  # pragma: no cover
    main()
