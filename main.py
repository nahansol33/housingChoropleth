import pandas as pd
import geopandas as gpd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from housingScrapper import *
from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

#using dash to create online components
app = Dash(__name__)
app.head = [html.Link(rel='stylesheet', href='/assets/styles.css')]
app.layout = html.Div([
    html.H1("Toronto housing Data"),
    html.P("Select data you wish to see"),
    dcc.RadioItems(
        id="choice",
        options=["Avg.Price", "Yearly Change%"],
        # default value to be selected upon page load
        value="Avg.Price",
        inline=True,
        style={"text-align" : "center"}
    ),
    dcc.Graph(id="graph", style={"width": "100%", "height" : "85vh"}, className="legend")
])

@app.callback(
    Output("graph", "figure"),
    Input("choice", "value")
)
def display_map(choice):
    #creating a csv file by using a function made in housingScrapper
    createHousingData()

    gdf = gpd.read_file("toronto_crs84.geojson")
    gdf["color"] = 0
    housing_data =  pd.read_csv("final_housingData2.csv")
    AvgPrices = housing_data["Price"]
    YearlyChanges = housing_data["Yearly Change"]

    gdf["Avg.Price"] = AvgPrices
    gdf["Yearly Change%"] = YearlyChanges

    gdf["Avg.Price"] = gdf["Avg.Price"].str.strip("[]").str.replace("'", "")  # Remove square brackets and single quotes
    # gdf["Avg.Price"].replace('', '0', inplace=True)
    gdf["Avg.Price"] = gdf["Avg.Price"].astype(float)
    gdf["Yearly Change%"] = gdf["Yearly Change%"].str.strip("[]")
    gdf["Yearly Change%"] = gdf["Yearly Change%"].astype(float)

    gdf["text"] = gdf["AREA_NAME"] + "<br>" + \
        "Average Price in Millions CAD: " + "<br>" \
        "Percent annual change in value: " + "<br>"

    if choice == "Avg.Price":
        data_range = (0, 3)
        color_scheme = "blues"
    else:
        data_range = (-20, 100)
        color_scheme = "reds"
    # print(gdf.sort_values("Yearly Change%", ascending=False).head())

    # Create a choropleth map using Plotly Express
    fig = px.choropleth(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,  # You can specify a column from your GeoDataFrame here
        color= choice,  # Specify the column you want to visualize
        color_continuous_scale= color_scheme,
        range_color=data_range,
        title="Choropleth Map of Toronto",
        scope="north america",
        labels= {"Avg.Price" : "Average selling price (Million CAD)"},
        hover_data="Avg.Price",
        hover_name="AREA_NAME",
        basemap_visible = True,
    )

    # Focusing on Toronto using coodinates
    fig.update_geos(center=dict(lon=-79.398866, lat=43.73065), projection_scale=280)
    fig.update_layout(title=dict(font=dict(size=30), x=0.5, xanchor = "center"),margin=dict(b=10, l=20, r=20))
    fig.update_coloraxes(colorbar_orientation="h", colorbar_x=0.5, colorbar_y=-0.5, colorbar_title_side="top")
    return fig


app.run_server()