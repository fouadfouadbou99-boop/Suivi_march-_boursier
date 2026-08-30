import pandas as pd
from io import BytesIO


def generate_excel_report(df, metrics):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # KPI

        pd.DataFrame(
            [metrics]
        ).to_excel(
            writer,
            sheet_name="KPI",
            index=False
        )

        # Historique

        historique = df.copy()

        historique.to_excel(
            writer,
            sheet_name="Historique"
        )

    output.seek(0)

    return output
