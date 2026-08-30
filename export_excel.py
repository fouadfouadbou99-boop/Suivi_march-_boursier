from market import load_data,compute_metrics
import pandas as pd
sym='^FCHI'
df=load_data(sym)
metrics=compute_metrics(df)
pd.DataFrame([metrics]).to_excel('rapport.xlsx',index=False)
print('rapport.xlsx généré')
