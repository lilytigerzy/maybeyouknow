import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pivottablejs import pivot_ui
from PIL import Image

img = Image.open('crime.jpeg')
st.set_page_config(layout="wide", page_title='Boston Crime Cases Statistics in the First Half of 2021', page_icon=img)

t1, t2 = st.columns([0.09, 1])

with t1:
    st.image('chart_icon.png')
with t2:
    st.title("Boston Crime Cases Statistics in the First Half of 2021")
    st.markdown(
        " **tel:** 01392 451192 **|  website:** https://www.data.boston.gov **|  email:** mediarelations@pd.boston.gov")


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


month = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6}
month_list=['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
week_list = ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

hour_list = ['All', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

result = df['OFFENSE_DESCRIPTION'].drop_duplicates().tolist()
offense_list = ['All'] + result
print(offense_list)
st.header(' ')
offense_selected = st.multiselect('Choose the item you are interested in:', offense_list)
st.session_state['offense_map'] = offense_selected


col1, col2, col3 = st.columns(3)
with col1:
    Month_selected = st.multiselect('Choose the month you are interested in:', month_list)
    if 'All' in Month_selected:
        month_selected = ['All']
    elif 'All' not in Month_selected:
        month_selected = [month[i] for i in Month_selected]
    st.session_state['month_map'] = month_selected

with col2:
    day_selected = st.multiselect('Choose the day you are interested in:', week_list)
    st.session_state['day_map'] = day_selected

with col3:
    hour_selected = st.multiselect('Choose the hour you are interested in:', hour_list)
    st.session_state['hour_map'] = hour_selected

chart_df = filterdata(df, offense_selected, month_selected, day_selected, hour_selected)
st.table(chart_df.head(20))



chart_df_2 = chart_df[['INCIDENT_NUMBER', 'OFFENSE_DESCRIPTION', 'DISTRICT', 'MONTH', 'DAY_OF_WEEK', 'HOUR']]
print(chart_df_2)


t = pivot_ui(chart_df_2)
with open(t.src) as t:
    components.html(t.read(), width=1000, height=1000, scrolling=True)
