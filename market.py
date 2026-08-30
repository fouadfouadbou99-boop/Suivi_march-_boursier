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
        (close.index.year == prev_year) &
        (close.index.month == prev_month)
    ]

    perf_mtd = (
        (last_value / prev_month_data.iloc[-1] - 1) * 100
        if len(prev_month_data) > 0
        else 0
    )

    # YTD

    prev_year_data = close[
        close.index.year == (last_date.year - 1)
    ]

    perf_ytd = (
        (last_value / prev_year_data.iloc[-1] - 1) * 100
        if len(prev_year_data) > 0
        else 0
    )

    # 1 an glissant

    if len(close) >= 52:

        perf_1an = (
            last_value /
            close.iloc[-53]
            - 1
        ) * 100

    else:

        perf_1an = None

    # 3 ans annualisé

    if len(close) >= 156:

        ratio = (
            last_value /
            close.iloc[-157]
        )

        perf_3ans = (
            ratio ** (1/3) - 1
        ) * 100

    else:

        perf_3ans = None

    # Volatilité

    returns = close.pct_change().dropna()

    volatility = (
        returns.std()
        * np.sqrt(52)
        * 100
    )

    # Drawdown

    rolling_max = close.cummax()

    drawdown = (
        close - rolling_max
    ) / rolling_max

    max_drawdown = (
        drawdown.min()
        * 100
    )

    return {

        "MTD (%)": round(perf_mtd, 2),

        "YTD (%)": round(perf_ytd, 2),

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
        round(max_drawdown, 2)
    }


def generate_commentary(metrics):

    tendance = (
        "positive"
        if metrics["YTD (%)"] > 0
        else "négative"
    )

    texte = f"""
Le MASI affiche une performance mensuelle (MTD) de {metrics['MTD (%)']} %.

Depuis le début de l'année, la performance ressort à {metrics['YTD (%)']} %.

La volatilité annualisée s'établit à {metrics['Volatilité (%)']} %.

Le drawdown maximal observé atteint {metrics['Drawdown Max (%)']} %.

L'évolution globale de l'indice demeure {tendance}.
"""

    if metrics["1 An (%)"] is not None:

        texte += f"""

Performance sur 1 an : {metrics['1 An (%)']} %.
"""

    if metrics["3 Ans Ann. (%)"] is not None:

        texte += f"""

Performance annualisée sur 3 ans : {metrics['3 Ans Ann. (%)']} %.
"""

    return texte
