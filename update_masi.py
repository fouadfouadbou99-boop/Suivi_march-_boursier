import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://www.casablanca-bourse.com/live-market/indices/cours?symbol=MASI"


def test_connexion():

    try:

        response = requests.get(
            URL,
            verify=False,
            timeout=30
        )

        print(
            f"Statut HTTP : {response.status_code}"
        )

        print(
            response.text[:3000]
        )

    except Exception as e:

        print(
            f"Erreur : {e}"
        )


if __name__ == "__main__":

    test_connexion()
