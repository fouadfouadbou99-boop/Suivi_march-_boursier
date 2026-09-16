def generate_commentary(
    nom,
    cours,
    mm20,
    mm52,
    ytd,
    vol,
    drawdown,
    distance_plus_haut
):

    # Détermination de la tendance

    if cours > mm20 and cours > mm52:
        tendance = "Haussière"

    elif cours < mm20 and cours < mm52:
        tendance = "Baissière"

    else:
        tendance = "Neutre"

    return f"""
L'indice {nom} affiche une performance YTD de {ytd:.2f} %.

Le niveau actuel ressort à {cours:,.2f} points.

La moyenne mobile 20 séances ressort à {mm20:,.2f} points.

La moyenne mobile 52 séances ressort à {mm52:,.2f} points.

Tendance technique : {tendance}.

La volatilité annualisée s'établit à {vol:.2f} %.

Le drawdown maximum atteint {drawdown:.2f} %.

L'indice demeure à {distance_plus_haut:.2f} % de son plus haut historique.
"""
