import pandas as pd
2
import numpy as np
3
import yfinance as yf
4
 
5
 
6
def load_yahoo_data(symbol):
7
 
8
return yf.download(
9
symbol,
10
start="2020-01-01",
11
auto_adjust=True,
12
progress=False
13
)
14
 
15
 
16
def load_maroc_index(filepath):
17
 
18
df = pd.read_excel(filepath)
19
 
20
df["Date"] = pd.to_datetime(df["Date"])
21
 
22
df.set_index(
23
"Date",
24
inplace=True
25
)
26
 
27
return df
28
 
29
 
30
def compute_metrics(df):
31
 
32
close = df["Close"]
33
 
34
if isinstance(close, pd.DataFrame):
35
close = close.iloc[:, 0]
36
 
37
close = close.dropna()
38
 
39
current_year = close.index[-1].year
40
 
41
ytd = close[
42
close.index.year == current_year
43
]
44
 
45
perf_ytd = (
46
close.iloc[-1]
47
/
48
ytd.iloc[0]
49
-
50
1
51
) * 100
52
 
53
returns = close.pct_change().dropna()
54
 
55
volatility = (
56
returns.std()
57
*
58
np.sqrt(252)
59
*
60
100
61
)
62
 
63
return {
64
"Performance YTD": round(perf_ytd, 2),
65
"Volatilite": round(volatility, 2)
66
}
