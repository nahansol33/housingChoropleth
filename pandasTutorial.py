import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as doc
import dash_html_components as html
from dash.dependencies import Input, Output


df = pd.read_csv("housingData.csv")
#print top 3 rows (not including headers)
# print(df.iloc[1:3])
# print(df.head(1));

# read headers
# print(df)

#read each column
# print(df["CompBenchmark"])

# read specific row
# print(df.iloc[0:2])

#read spcific location (row and column)
# print(df.iloc[0,1])

#looping through by rows
# for index, row in df.iterrows():
#     print(index, row["calories"])

#read a row that has the name set as Cornstarch
# print(df.loc[df["name"] == "Cornstarch"])

# print(df.sort_values(["CompBenchmark", "CompYoYChange"], ascending=[0,1]))
df["price"] = df["CompBenchmark"]
# axis=1 is for horizontal addition/operation axis=0 is for vertical

df["price"] = df.iloc[:, 1:3].sum(axis=1)
df["percentIncrease"] = df["CompYoYChange"]
df = df.drop(df.iloc[:, 1:16], axis=1)

# Reaaranging columns
cols = list(df.columns)
df = df[[cols[0]] + cols[-2:]]
# print(df)


