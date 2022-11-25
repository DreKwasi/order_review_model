import streamlit as st
import pandas as pd
import numpy as np
import vaex as vx
import plotly_express as px
import plotly.graph_objects as go
import datetime as dt
import pyarrow as pa
from geopy.geocoders import Nominatim
import pickle
from operator import and_
from functools import reduce
from pages.helper.data_import import parse_data

df = parse_data()

if not vx.cache.is_on():
    vx.cache.on()
df = df._future()

st.sidebar.header('User Input Features')


def save(data):
    with open("regions_lot.txt", "wb") as f:
        pickle.dump(data, f)


def load():
    with open("pages/regions_lot.txt", "rb") as f:
        data = pickle.load(f)
        return data


def filter_data(filter_dict, date_range):
    filters = [df[key].isin(values)
               for key, values in filter_dict.items() if values != []]
    filtered_df = reduce(and_, filters, True)

    date_min = np.datetime64(date_range[0])
    date_max = np.datetime64(date_range[1])

    df_max = df['Sale_Date'].values.max()
    df_min = df['Sale_Date'].values.min()

    if date_min is not df_min:
        filtered_df = filtered_df & (df.Sale_Date >= date_min)
    if date_max is not df_max:
        filtered_df = filtered_df & (df.Sale_Date <= date_max)

    return filtered_df


def parameter_outputs(param_dict):
    x = ''
    for key in param_dict.keys():
        if param_dict[key] != []:
            x += f' - {key}: {param_dict[key]} \n'
    return x


def compute_filter(filter, binner_resolution):
    # extract data from filter
    dff = df.filter(filter)

    # get regional data
    region = dff['LOCATION'].unique()
    avg_sales = vx.agg.mean(dff['Sum_of_Quantity_In_Packs'])
    regional_sales = df[df['LOCATION'].isin(region)]

    # get category data
    category = dff['VDL_Sub_Category'].unique()
    if len(category) == 1:
        category_ranks = regional_sales.groupby(
            by=['VDL_Sub_Category'], agg={"Sum_of_Quantity_In_Packs": "sum"}).sort(by="Sum_of_Quantity_In_Packs", ascending=False)
        category_rank = f"{category_ranks['VDL_Sub_Category'].tolist().index(category[0]) + 1} / {len(category_ranks)}"

    else:
        category_rank = None

    # get facility data
    facility = dff['Sale_Facility'].unique()
    if len(facility) == 1:
        facility_ranks = regional_sales.groupby(
            by=['Sale_Facility'], agg={"Sum_of_Quantity_In_Packs": "sum"}).sort(by="Sum_of_Quantity_In_Packs", ascending=False)
        facility_rank = f"{facility_ranks['Sale_Facility'].tolist().index(facility[0]) + 1} / {len(facility_ranks)}"
    else:
        facility_rank = None

    dff = dff.extract()
    dff["Sale_Date"] = np.datetime_as_string(
        dff["Sale_Date"].values, unit=binner_resolution[0])
    gdf = dff.groupby(by=["Sale_Date", "VDL_Sub_Category", "Sale_Facility",
                          "LOCATION"], agg={"Sum_of_Quantity_In_Packs": "sum"}).sort(by="Sale_Date", ascending=True)

    avg_monthly_sales = gdf.sum(
        gdf['Sum_of_Quantity_In_Packs']) / gdf.count(gdf['Sum_of_Quantity_In_Packs'])
    facility_total = dff.sum(dff['Sum_of_Quantity_In_Packs'])
    g_region_sales = regional_sales[regional_sales['VDL_Sub_Category'].isin(
        category)]
    regional_total = g_region_sales.sum(g_region_sales['Sum_of_Quantity_In_Packs'])

    return facility_total, regional_total, avg_monthly_sales, category_rank, facility_rank, gdf


def human_format(num):
    '''Better formatting of large numbers
    Kudos to:
    '''
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def line_plot(data, facility, location):
    if len(facility) > 1:
        fig = px.line(data, x="Sale_Date", y="Sum_of_Quantity_In_Packs",
                      color="VDL_Sub_Category", facet_col='Sale_Facility')
    elif len(location) > 1 & len(facility) == 0:
        fig = px.line(data, x="Sale_Date", y="Sum_of_Quantity_In_Packs",
                      color="VDL_Sub_Category", facet_col='LOCATION')
    elif len(facility) == 1:
        fig = px.line(data, x="Sale_Date", y="Sum_of_Quantity_In_Packs",
                      color="VDL_Sub_Category", facet_col='Sale_Facility')

    st.plotly_chart(fig)


def get_locators(location):

    try:
        loc_dict = load()
        return loc_dict
    except FileNotFoundError:
        loc_dict = {}
        if location != []:
            for i in location:
                geolocator = Nominatim(user_agent="id_explorer")
                if i == "BRONG AHAFO":
                    i = "Ahafo"
                loc = geolocator.geocode(i + " Ghana")
                loc_dict[i] = [loc.latitude, loc.longitude, ]

        save(loc_dict)
        return loc_dict


# Info

date_range = st.sidebar.slider(
    label='Date Range',
    min_value=dt.date(2018, 1, 1),
    max_value=dt.date(2022, 10, 20),
    value=(dt.date(2018, 1, 1), dt.date(2022, 10, 20)),
    step=dt.timedelta(days=1),
    help='Select a date range.')

binner_resolution = st.sidebar.selectbox(label='Time Resolution', options=[
                                            'Week', 'Month', 'Year'], index=1)

facility = st.sidebar.multiselect(
    "Select Facility:", df['Sale_Facility'].unique(), default='Lifedoor Pharmacy, Dansoman')

if facility == []:
    location = st.sidebar.multiselect(
        "Select Location:", options=df['LOCATION'].unique())
    if location == []:
        st.error("Select Facility or Location")
        st.stop()
else:
    location = df[df['Sale_Facility'].isin(facility)]['LOCATION'].unique()
    st.sidebar.multiselect(
        "Select Location:", options=df['LOCATION'].unique(), default=location)

product = st.sidebar.multiselect(
    "Select Product:", options=df["Product_Description"].unique())
if product == []:
    category = st.sidebar.multiselect(
        "Select Category:", options=df['VDL_Sub_Category'].unique(), default="Analgesics")
else:
    category = df[df['Product_Description'].isin(
        product)]['VDL_Sub_Category'].unique()
    st.sidebar.multiselect(
        "Select Location:", options=df['VDL_Sub_Category'].unique(), default=category)

filter_dict = {
    "VDL_Sub_Category": category,
    "Sale_Facility": facility,
    "LOCATION": location,
    "Product_Description": product
}

filtered_df = filter_data(filter_dict, date_range)

param_dict = {'Location': location,
                'Facility Name': facility, 'Product Sub Category': category}
st.subheader("Parameters Selected")
st.markdown(parameter_outputs(param_dict))

st.subheader("Summary Statistics")
facility_total, regional_total, avg_monthly_sales, category_rank, facility_rank, gdf = compute_filter(
    filtered_df, binner_resolution)

metrics_cols = st.columns(5)

metrics_cols[0].metric(label='Total Sales Per Facility (Packs)',
                        value=human_format(facility_total))
metrics_cols[1].metric(label='Total Sales Per Region (Packs)',
                        value=human_format(regional_total))
metrics_cols[2].metric(label=f'Average {binner_resolution}ly Sales Per Facility (Packs)',
                        value=human_format(np.round(avg_monthly_sales, 2)))
metrics_cols[3].metric(
    label='Category Regional Rank ', value=category_rank)
metrics_cols[4].metric(
    label='Facility Regional Rank ', value=facility_rank)

st.subheader("DataFrame")
if gdf.shape[0] > 1_000:
    df_selection = gdf.head(1000).to_pandas_df()
    st.warning(
        'Maximum Number of Rows Exceeded (1000)')
else:
    df_selection = gdf.to_pandas_df()

st.dataframe(df_selection)

# visualize
st.subheader("Time Series Visualization")
line_plot(gdf.to_pandas_df(), facility, location)

locators = get_locators(location)
geo_data = r"ghana_regions.json"

gdf = gdf.groupby(by="LOCATION", agg={"Sum_of_Quantity_In_Packs": "sum"})
pd_gdf = gdf.to_pandas_df()

pd_gdf['Sum_of_Quantity_In_Packs'] = pd_gdf['Sum_of_Quantity_In_Packs'].round(decimals=0)

if len(pd_gdf['LOCATION'].unique()) > 1:
    X_std = (pd_gdf['Sum_of_Quantity_In_Packs'] - pd_gdf['Sum_of_Quantity_In_Packs'].min()) / \
        (pd_gdf['Sum_of_Quantity_In_Packs'].max() - pd_gdf['Sum_of_Quantity_In_Packs'].min())
    pd_gdf['Threshold'] = X_std * (10 - 2) + 2
else:
    pd_gdf['Threshold'] = pd_gdf['Sum_of_Quantity_In_Packs']

latitudes = []
longitudes = []
for index, rows in pd_gdf.iterrows():
    latitudes.append(locators[rows['LOCATION']][0])
    longitudes.append(locators[rows['LOCATION']][1])

pd_gdf = pd.concat([pd_gdf, pd.Series(latitudes, name="Latitude"), pd.Series(
    longitudes, name="Longitude")], axis=1)
pd_gdf['LOCATION'] = pd_gdf['LOCATION'].astype(str)

# st.dataframe(pd_gdf)

fig = px.scatter_mapbox(
    pd_gdf,
    lat="Latitude",
    lon="Longitude",
    hover_data=["Sum_of_Quantity_In_Packs"],
    color='Threshold',
    color_continuous_scale='viridis_r',
    mapbox_style="carto-positron",
    opacity=0.9,
    zoom=5,
    size='Threshold'
)

with fig.batch_update():
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(width=1000)
    fig.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=0),)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(geo=go.layout.Geo(
        projection=go.layout.geo.Projection(type='natural earth')))
    fig.update_layout(coloraxis_showscale=False)

st.plotly_chart(fig)

# map_sby = fl.Map(location=[8.0300284, -1.0800271], zoom_start=7)

# fl.Choropleth(
# data = pd_gdf,
# geo_data=geo_data,
# columns=['LOCATION','Sum_of_Quantity_In_Packs'],
# bins=threshold_scale,
# fill_color="YlOrRd",
# fill_opacity=0.7,
# line_opacity=0.2,
# legend_name='Sum_of_Quantity_In_Packs',
# reset=True).add_to(map_sby)

# for location in locators.keys():
#     label = '{}'.format(location)
#     label = fl.Popup(label, parse_html=True)
#     fl.CircleMarker(
#         [locators[location][0], locators[location][1]],
#         radius=5,
#         popup=label,
#         color='green',
#         fill_color='#3186cc',
#         parse_html=False).add_to(map_sby)

# folium_static(map_sby)
