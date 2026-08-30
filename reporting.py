import pandas as pd


def export_excel(metrics):

    with pd.ExcelWriter(
        "reports/Rapport_Marche.xlsx",
        engine="openpyxl"
    ) as writer:

        pd.DataFrame(
            [metrics]
        ).to_excel(
            writer,
            sheet_name="Dashboard",
            index=False
        )
