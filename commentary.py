def generate_commentary(metrics):

    commentaire = (
        f"Le MASI affiche une performance mensuelle (MTD) de "
        f"{metrics['MTD (%)']} %. \n\n"

        f"Depuis le début de l'année, la performance ressort à "
        f"{metrics['YTD (%)']} %. \n\n"

        f"Le cours actuel ressort à "
        f"{metrics['Cours Actuel']} points. \n\n"

        f"La moyenne mobile 20 séances ressort à "
        f"{metrics['MM20']}. \n\n"

        f"La moyenne mobile 52 séances ressort à "
        f"{metrics['MM52']}. \n\n"

        f"Tendance : "
        f"{metrics['Tendance']}. \n\n"

        f"Dynamique : "
        f"{metrics['Dynamique']}. \n\n"

        f"Signal de croisement MM20/MM52 : "
        f"{metrics['Signal']}. \n\n"

        f"La volatilité annualisée s'établit à "
        f"{metrics['Volatilité (%)']} %. \n\n"

        f"Le drawdown maximal atteint "
        f"{metrics['Drawdown Max (%)']} %. \n\n"

        f"L'indice demeure à "
        f"{metrics['Distance Plus Haut (%)']} % "
        f"de son plus haut historique."
    )

    return commentaire
