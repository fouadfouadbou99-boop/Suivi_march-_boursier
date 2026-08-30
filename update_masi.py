import pandas as pd

URL = "https://www.casablanca-bourse.com/live-market/indices/cours?symbol=MASI"

FICHIER_MASI = "Data_masi.xlsx"


def update_masi():

    print("Connexion au site Casablanca Bourse...")

    try:

        tables = pd.read_html(URL)

        print(f"{len(tables)} table(s) trouvée(s).")

        for i, table in enumerate(tables):

            print("\n====================")
            print(f"TABLE {i}")
            print("====================")

            print(table.head())

    except Exception as e:

        print(f"Erreur : {e}")


if __name__ == "__main__":

    update_masi()
