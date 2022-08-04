import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import pydeck as pdk

img = Image.open('crime.jpeg')
st.set_page_config(layout="wide", page_title='Boston Crime Cases Statistics in the First Half of 2021', page_icon=img)

st.header('Split-panel Map')
st.markdown('**If you have finished the data selection. We can now look at the distribution of this crime data across 12 police districts in Boston. You can also zoom in on the map to see the categories of these crimes. If no crime has occurred in the district (under the conditions you selected), a no-crime image will be displayed.**')

st.header('')

col0, col1, col2, col3 = st.columns(4)
with col0:
    st.write('Crime Type:', st.session_state['offense_map'])
with col1:
    st.write('Month:', st.session_state['month_map'])
with col2:
    st.write('Day:' , st.session_state['day_map'])
with col3:
    st.write('Hour:', st.session_state['hour_map'])

def get_data():
    datafile = "bostoncrime2021_7000_sample.csv"
    df = pd.read_csv(datafile)
    data = df[
        ['INCIDENT_NUMBER', 'OFFENSE_CODE', 'OFFENSE_DESCRIPTION', 'DISTRICT', 'MONTH', 'DAY_OF_WEEK', 'HOUR', 'Lat',
         'Long']]
    crime_data = data[(data != 0).all(1)]
    crime_data.rename(columns={'Lat': 'lat', 'Long': 'lon'}, inplace=True)
    return crime_data


df = get_data()

st.header('')


def filterdata(df, offense_selected, month_selected, day_selected, hour_selected):
    if 'All' in offense_selected:
        d1 = df
    else:
        d1 = df[df['OFFENSE_DESCRIPTION'].isin(offense_selected)]
    if 'All' in month_selected:
        d2 = df
    else:
        d2 = df[df['MONTH'].isin(month_selected)]
    if 'All' in day_selected:
        d3 = df
    else:
        d3 = df[df['DAY_OF_WEEK'].isin(day_selected)]
    if 'All' in hour_selected:
        d4 = df
    else:
        d4 = df[df['HOUR'].isin(hour_selected)]

    merge1 = pd.merge(d1, d2, how='inner')
    merge2 = pd.merge(merge1, d3, how='inner')
    filtereddata = pd.merge(merge2, d4, how='inner')
    filtereddata.reset_index(drop=False)
    return filtereddata



mapdf = filterdata(df, st.session_state['offense_map'], st.session_state['month_map'], st.session_state['day_map'],
                   st.session_state['hour_map'])


# Function for 12 police Districts
def map(data, lat, lon, zoom):
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=50)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=data,
                       get_position='[lon, lat]',
                       get_radius=50,
                       pickable=True,
                       extruded=True,
                       get_color=[255, 0, 0]
                       )
    tool_tip = {
        'html': '<b>Crime type:</b> {OFFENSE_DESCRIPTION}',
        'style': {
            'color': 'white'}}

    map_fig = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip=tool_tip)
    st.pydeck_chart(map_fig)


f2 = open('BostonPoliceDistricts.csv', 'r')

boston_police_districts_dict = {}
first = True
for aline in f2:
    if first:
        first = False
        continue
    alist = aline.strip().split(",")
    boston_police_districts_dict[alist[0]] = alist[1]
f2.close()
print(boston_police_districts_dict)


def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))


fig = Image.open('nocrime.png')

row2_1, row2_2, row2_3, row2_4 = st.columns(4)
with row2_1:
    st.write(boston_police_districts_dict['A1'])
    A1df = mapdf[mapdf['DISTRICT'] == 'A1']
    if A1df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(A1df["lat"], A1df["lon"])
        map(A1df, midpoint[0], midpoint[1], 12)

with row2_2:
    st.write(boston_police_districts_dict['A15'])
    A15df = mapdf[mapdf['DISTRICT'] == 'A15']
    if A15df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(A15df["lat"], A15df["lon"])
        map(A15df, midpoint[0], midpoint[1], 12)

with row2_3:
    st.write(boston_police_districts_dict['A7'])
    A7df = mapdf[mapdf['DISTRICT'] == 'A7']
    if A7df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(A7df["lat"], A7df["lon"])
        map(A7df, midpoint[0], midpoint[1], 12)

with row2_4:
    st.write(boston_police_districts_dict['B2'])
    B2df = mapdf[mapdf['DISTRICT'] == 'B2']
    if B2df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(B2df["lat"], B2df["lon"])
        map(B2df, midpoint[0], midpoint[1], 12)

row3_1, row3_2, row3_3, row3_4 = st.columns(4)
with row3_1:
    st.write(boston_police_districts_dict['B3'])
    B3df = mapdf[mapdf['DISTRICT'] == 'B3']
    if B3df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(B3df["lat"], B3df["lon"])
        map(B3df, midpoint[0], midpoint[1], 12)

with row3_2:
    st.write(boston_police_districts_dict['C6'])
    C6df = mapdf[mapdf['DISTRICT'] == 'C6']
    if C6df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(C6df["lat"], C6df["lon"])
        map(C6df, midpoint[0], midpoint[1], 12)

with row3_3:
    st.write(boston_police_districts_dict['C11'])
    C11df = mapdf[mapdf['DISTRICT'] == 'C11']
    if C11df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(C11df["lat"], C11df["lon"])
        map(C11df, midpoint[0], midpoint[1], 12)

with row3_4:
    st.write(boston_police_districts_dict['D4'])
    D4df = mapdf[mapdf['DISTRICT'] == 'D4']
    if D4df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(D4df["lat"], D4df["lon"])
        map(D4df, midpoint[0], midpoint[1], 12)

row4_1, row4_2, row4_3, row4_4 = st.columns(4)
with row4_1:
    st.write(boston_police_districts_dict['D14'])
    D14df = mapdf[mapdf['DISTRICT'] == 'D14']
    if D14df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(D14df["lat"], D14df["lon"])
        map(D14df, midpoint[0], midpoint[1], 12)

with row4_2:
    st.write(boston_police_districts_dict['E5'])
    E5df = mapdf[mapdf['DISTRICT'] == 'E5']
    if E5df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(E5df["lat"], E5df["lon"])
        map(E5df, midpoint[0], midpoint[1], 12)

with row4_3:
    st.write(boston_police_districts_dict['E13'])
    E13df = mapdf[mapdf['DISTRICT'] == 'E13']
    if E13df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(E13df["lat"], E13df["lon"])
        map(E13df, midpoint[0], midpoint[1], 12)

with row4_4:
    st.write(boston_police_districts_dict['E18'])
    E18df = mapdf[mapdf['DISTRICT'] == 'E18']
    if E18df.empty:
        st.image(fig)
    else:
        midpoint = mpoint(E18df["lat"], E18df["lon"])
        map(E18df, midpoint[0], midpoint[1], 12)
