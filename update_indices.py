import pandas as pd

nouveau = pd.read_excel(
    "source/MASI_Jour.xlsx"
)

historique = pd.read_excel(
    "data/MASI.xlsx"
)

df = pd.concat(
    [
        historique,
        nouveau
    ]
)

df = df.drop_duplicates()

df.to_excel(
    "data/MASI.xlsx",
    index=False
)

print(
    "MASI mis à jour"
)
