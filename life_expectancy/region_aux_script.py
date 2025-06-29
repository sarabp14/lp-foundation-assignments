from cleaning import load_data, split_metadata_column, drop_metadata_column, reshape_to_long_format, clean_year_column, clean_value_column

# Carregar e limpar os dados
df = load_data()
df = split_metadata_column(df)
df = drop_metadata_column(df)
df = reshape_to_long_format(df)
df = clean_year_column(df)
df = clean_value_column(df)

# Agora podes extrair as regiões únicas
regions = df['region'].unique()

for region in regions:
    enum_name = region.upper().replace(" ", "_").replace("-", "_")
    print(f'{enum_name} = "{region}"')
