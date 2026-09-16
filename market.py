import pandas as pd
import numpy as np
import yfinance as yf


def load_yahoo_data(symbol):

    return yf.download(
        symbol,
        start="2020-01-01",
        auto_adjust=True,
        progress=False
    )


def load_maroc_index(filepath):

    df = pd.read_excel(filepath)

    df["Date"] = pd.to_datetime(df["Date"])

    df["Close"] = (
        df["Close"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    df["Close"] = pd.to_numeric(
        df["Close"],
        errors="coerce"
    )

    df = df.dropna(subset=["Close"])

    df = df.sort_values("Date")

    df.set_index("Date", inplace=True)

    return df


def compute_metrics(df):

    close = df["Close"].dropna()

    last_date = close.index[-1]
    last_value = close.iloc[-1]

    # MTD

    prev_month = last_date.month - 1
    prev_year = last_date.year

    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    prev_month_data = close[
        (close.index.year == prev_year)
        &
        (close.index.month == prev_month)
    ]

    perf_mtd = (
        (last_value / prev_month_data.iloc[-1] - 1) * 100
        if len(prev_month_data) > 0
        else 0
    )

    # YTD

    prev_year_data = close[
        close.index.year == last_date.year - 1
    ]

    perf_ytd = (
        (last_value / prev_year_data.iloc[-1] - 1) * 100
        if len(prev_year_data) > 0
        else 0
    )

    # PERFORMANCE 1 AN

    if len(close) >= 252:

        perf_1an = (
            last_value /
            close.iloc[-253]
            - 1
        ) * 100

    else:

        perf_1an = None

    # PERFORMANCE 3 ANS

    nb_annees = (
        (close.index[-1] - close.index[0]).days
    ) / 365.25

    if nb_annees >= 2.75:

        ratio = (
            close.iloc[-1]
            /
            close.iloc[0]
        )

        perf_3ans = (
            ratio ** (1 / nb_annees)
            - 1
        ) * 100

    else:

        perf_3ans = None

    # VOLATILITE

    returns = close.pct_change().dropna()

    volatility = (
        returns.std()
        * np.sqrt(252)
        * 100
    )

    # DRAWDOWN

    rolling_max = close.cummax()

    drawdown = (
        close - rolling_max
    ) / rolling_max

    max_drawdown = (
        drawdown.min() * 100
    )

    # PLUS HAUT / BAS

    plus_haut = close.max()
    plus_bas = close.min()

    distance_plus_haut = (
        last_value / plus_haut - 1
    ) * 100

    # MOYENNES MOBILES

    mm20_series = close.rolling(20).mean()
    mm52_series = close.rolling(52).mean()

    mm20 = mm20_series.iloc[-1]
    mm52 = mm52_series.iloc[-1]

    mm20_prev = mm20_series.iloc[-2]
    mm52_prev = mm52_series.iloc[-2]

    # TENDANCE

    if last_value > mm20 and last_value > mm52:

        tendance = "Haussière"

    elif last_value < mm20 and last_value < mm52:

        tendance = "Baissière"

    else:

        tendance = "Neutre"

    # DYNAMIQUE

    ecart_actuel = mm20 - mm52
    ecart_precedent = mm20_prev - mm52_prev

    if abs(ecart_actuel) > abs(ecart_precedent):

        dynamique = "Accélération"

    else:

        dynamique = "Essoufflement"

    # CROISEMENTS

    if mm20_prev < mm52_prev and mm20 > mm52:

        signal = "Croisement haussier"

    elif mm20_prev > mm52_prev and mm20 < mm52:

        signal = "Croisement baissier"

    else:

        signal = "Aucun croisement"

    return {

        "Cours Actuel":
        round(last_value, 2),

        "MTD (%)":
        round(perf_mtd, 2),

        "YTD (%)":
        round(perf_ytd, 2),

        "1 An (%)":
        round(perf_1an, 2)
        if perf_1an is not None
        else None,

        "3 Ans Ann. (%)":
        round(perf_3ans, 2)
        if perf_3ans is not None
        else None,

        "Volatilité (%)":
        round(volatility, 2),

        "Drawdown Max (%)":
        round(max_drawdown, 2),

        "Plus Haut":
        round(plus_haut, 2),

        "Plus Bas":
        round(plus_bas, 2),

        "Distance Plus Haut (%)":
        round(distance_plus_haut, 2),

        "MM20":
        round(mm20, 2),

        "MM52":
        round(mm52, 2),

        "Tendance":
        tendance,

        "Dynamique":
        dynamique,

        "Signal":
        signal
    }


def generate_commentary(metrics):

    commentaire = (
        f"Le MASI enregistre une performance mensuelle (MTD) de "
        f"{metrics['MTD (%)']} % et une performance depuis le début de l'année (YTD) de "
        f"{metrics['YTD (%)']} %. \n\n"

        f"L'indice clôture à {metrics['Cours Actuel']} points, "
        f"contre une moyenne mobile à 20 séances de {metrics['MM20']} points "
        f"et une moyenne mobile à 52 séances de {metrics['MM52']} points. \n\n"

        f"Le positionnement de l'indice sous ses moyennes mobiles de référence "
        f"traduit actuellement une tendance {metrics['Tendance'].lower()}. \n\n"

        f"La dynamique de marché est qualifiée de "
        f"{metrics['Dynamique'].lower()}, ce qui suggère un rythme de variation "
        f"moins soutenu par rapport aux périodes précédentes. \n\n"

        f"Aucun signal technique majeur de retournement n'est observé à ce stade "
        f"sur les croisements entre les moyennes mobiles "
        f"({metrics['Signal']}). \n\n"

        f"La volatilité annualisée ressort à "
        f"{metrics['Volatilité (%)']} %, reflétant un niveau de risque de marché "
        f"compatible avec les fluctuations récentes observées sur l'indice. \n\n"

        f"Le drawdown maximal constaté atteint "
        f"{metrics['Drawdown Max (%)']} %, traduisant l'amplitude maximale de correction "
        f"enregistrée sur la période analysée. \n\n"

        f"Enfin, le MASI demeure en retrait de "
        f"{abs(metrics['Distance Plus Haut (%)'])} % par rapport à son plus haut historique, "
        f"ce qui indique qu'une partie du potentiel de récupération reste à reconstituer."
    )

    return commentaire
