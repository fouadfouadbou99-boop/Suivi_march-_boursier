import pandas as pd

# historique existant
historique = pd.read_excel(
    "Data_masi.xlsx"
)

# nouvelles données récupérées
nouveau = pd.read_excel(
    "maj_masi.xlsx"
)

df = pd.concat(
    [historique, nouveau]
)

df = df.drop_duplicates()

df.to_excel(
    "Data_masi.xlsx",
    index=False
)

print("MASI mis à jour")
