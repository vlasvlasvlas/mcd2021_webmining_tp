import os, sys
import pandas as pd
import numpy as np
import datetime as dt
import pandas as pd
import pandas_datareader.data as web

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# dataframe con analisis 30 dias
filecsv = "analisis_30dias.csv"

# get mervals

# dataframe
df = pd.read_csv(os.path.join(ROOT_DIR, filecsv))
df = df.sort_values(["fecha", "puntaje"], ascending=[True, True])
df["fecha"]

# df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
# df = df.rename_axis("fecha").query("fecha.dt.dayofweek < 5")

fechamin = df.fecha.min()
fechamax = df.fecha.max()
print(fechamin)
print(fechamax)

stocks_close = pd.DataFrame(
    web.DataReader(["^MERV"], "yahoo", fechamin, fechamax)["Close"]
)
stocks_close.reset_index(inplace=True)

print(stocks_close.head(1))
print(stocks_close.shape)

stocks_close.to_csv('stocks.csv')