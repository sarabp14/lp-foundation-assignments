import pandas as pd
import pathlib

def clean_data(region):
    """Carregar o dataset e limpar os dados"""
    path = pathlib.Path(__file__).parent / "data" / "eu_life_expectancy_raw.tsv"
    df = pd.read_csv(path, sep="\t")
    
    #Separar a primeira coluna em 4 colunas novas
    df[['unit', 'sex', 'age', 'region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)

    #Remover a coluna antiga
    df = df.drop(columns=['unit,sex,age,geo\\time'])

    #Converter os anos para formato longo
    df = df.melt(
        id_vars=['unit', 'sex', 'age', 'region'],
        var_name='year',
        value_name='value'
    )

    #Converter ano para inteiro
    df['year'] = df['year'].astype(int)

    #Filtrar apenas as linhas com valores numéricos válidos
    df['value'] = df['value'].str.replace(r'[a-zA-Z]', '', regex=True).str.strip()
    df['value'] = pd.to_numeric(df['value'], errors='coerce').astype(float)
    df = df.dropna(subset=['value'])

    # Filtrar apenas os dados de Portugal
    df = df[df['region'] == 'PT']
    return df



if __name__ == "__main__": # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Limpa dados de esperança de vida da UE.")
    parser.add_argument("--region", default="PT", help="Código do país (ex: PT, ES, FR)")
    args = parser.parse_args()

    df_cleaned = clean_data(region=args.region)

    df_cleaned.to_csv(
    "/Users/sarapaisana/assignments/life_expectancy/data/pt_life_expectancy.csv", index=False)
