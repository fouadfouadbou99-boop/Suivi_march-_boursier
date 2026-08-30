import pandas as pd
from pathlib import Path

FICHIER_MASI = "Data_masi.xlsx"


def update_masi():

    historique = pd.read_excel(FICHIER_MASI)

    historique["Date"] = pd.to_datetime(
        historique["Date"]
    )

    historique = historique.sort_values(
        "Date"
    )

    historique = historique.drop_duplicates(
        subset=["Date"]
    )

    historique.to_excel(
        FICHIER_MASI,
        index=False
    )

    print(
        f"{len(historique)} observations enregistrées."
    )

    print(
        f"Dernière date : "
        f"{historique['Date'].max()}"
    )


if __name__ == "__main__":

    update_masi()
