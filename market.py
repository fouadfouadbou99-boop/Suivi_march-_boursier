import yfinance as yf, numpy as np

def load_data(symbol,start='2020-01-01'):
    df=yf.download(symbol,start=start,auto_adjust=True,progress=False)
    return df

def compute_metrics(df):
    r=df['Close'].pct_change().dropna()
    return {
      'Perf_YTD': float(df['Close'].iloc[-1]/df[df.index.year==df.index[-1].year]['Close'].iloc[0]-1),
      'Volatilite': float(r.std()*np.sqrt(252))
    }

def generate_commentary(name,m):
    return f"{name}: Performance YTD {m['Perf_YTD']:.2%}, volatilité {m['Volatilite']:.2%}."
