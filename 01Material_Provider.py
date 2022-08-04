import pandas as pd
import streamlit as st
from PIL import Image

img = Image.open('crime.jpeg')
st.set_page_config(layout="wide", page_title='Boston Crime Cases Statistics in the First Half of 2021', page_icon=img)

myphoto = Image.open('YuZhou.jpeg')
st.header(' ')
st.header(' ')
col1, col2 = st.columns([1, 2], gap='medium')
with col1:
    st.image(myphoto)

with col2:
    st.header(' ')
    st.subheader('Hello!')
    st.subheader('I am Yu Zhou.')
    st.write(
        "Currently, I'm studying at Bentley University for my Masters in Business Analytics. Cute animals are my favorite, and I enjoy communicating with everyone. I am very happy to be here to introduce my final program.")
    st.header(' ')
    st.header(' ')
    with st.expander("🦌 Deer"):
        video_file_1 = open('Deers.mp4', 'rb')
        video_bytes = video_file_1.read()
        st.video(video_bytes)
    with st.expander("🐈 Cat"):
        video_file_1 = open('Cat.mp4', 'rb')
        video_bytes = video_file_1.read()
        st.video(video_bytes)

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


# print(boston_police_districts_dict)
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

# st.title("2021 Boston Crime Statistics Analysis")


# option_1 = st.selectbox('View Option: ', ('OFFENSE_TYPE', 'DISTRICT', 'MONTH', 'DAY_OF_WEEK', 'HOUR', 'STREET'))


print('-------------------------------------------------------------------')


# FILTER DATA FOR A SPECIFIC HOUR, CACHE



#
# offense_selected = input('1:')
# month_selected = input('2:')
# day_selected = input('3:')
# hour_selected = input('4:')


