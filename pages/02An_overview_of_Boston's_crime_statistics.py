import pandas as pd
import numpy as np
import pylab as pl
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open('crime.jpeg')
st.set_page_config(layout="wide", page_title='Boston Crime Cases Statistics in the First Half of 2021', page_icon=img)

st.header("Statistics on Boston Crime Cases in the First Half of 2021 ")

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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Top 20 Crimes", "Number of Crimes in Different Months", "Number of Crimes in Different Days",
     'Number of Crimes in Different Hours', 'Number of Crimes in 12 Police Districts'])

with tab1:
    result = (df['OFFENSE_DESCRIPTION'].value_counts()[0:20]).to_dict()
    print(result)
    fig, ax = plt.subplots(figsize=(4, 3))
    crime_type = result.keys()
    y_pos = np.arange(len(crime_type))
    number = result.values()
    hbars = ax.barh(y_pos, number, align='center')
    ax.set_yticks(y_pos, labels=crime_type)
    ax.set_xlim(right=600)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.bar_label(hbars)
    ax.set_xlabel('Number')
    ax.set_title('Top 20 Crimes in the First Half of 2021')
    plt.yticks(fontsize=6)
    plt.show()
    st.pyplot(fig)

with tab2:
    result = (df['MONTH'].value_counts()).to_dict()
    print(result)
    fig, ax = plt.subplots(figsize=(5, 2.5))
    month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun'}
    month_number = [result[i] for i in month.keys()]
    print(month_number)
    explode = (0, 0.1, 0, 0, 0, 0)
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(month.keys())))


    def func(pct, allvals):
        absolute = int(np.round(pct / 100. * np.sum(allvals)))
        return "{:.1f}%\n({:d})".format(pct, absolute)


    wedges, texts, autotexts = ax.pie(month_number, colors=colors, explode=explode, labels=month.values(),
                                      autopct=lambda pct: func(pct, month_number), textprops=dict(color='w'),
                                      startangle=60)
    ax.axis('equal')
    plt.setp(autotexts, size=5, weight="bold")
    ax.legend(wedges, month.values(),
              title="Months",
              loc="center left",
              bbox_to_anchor=(0.8, 0, 0.2, 1), fontsize=7)
    ax.set_title("Number of Crimes in the First Six Months", fontsize=8)
    plt.show()
    st.pyplot(fig)
with tab3:
    result = (df['DAY_OF_WEEK'].value_counts()).to_dict()
    print(result)
    week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    week_number = [result[i] for i in week]
    print(week_number)
    fig, ax = plt.subplots(figsize=(6, 2.7))
    ax.plot(week, week_number)
    ax.scatter(week, week_number, s=9, c='red')
    ax.set_title("Number of Crimes in Seven Days")
    ax.set_ylim(top=1000)
    for a, b in zip(week, week_number):
        ax.text(a, b, b, ha='left', va='top', fontsize=8)
    plt.show()
    st.pyplot(fig)

with tab4:
    result = (df['HOUR'].value_counts()).to_dict()
    result[24] = 0
    print(result)
    hour = range(1, 25)
    hour_number = [result[i] for i in hour]
    fig, ax = plt.subplots(figsize=(6, 2.7))
    ax.plot(hour, hour_number)
    ax.scatter(hour, hour_number, s=9, c='red')
    ax.set_title("Number of Crimes in 24 Hours")
    ax.set_ylim(top=500)
    hour_chosen = [12, 16, 24]
    hour_number_chosen = [440, 440, 0]
    for a, b in zip(hour_chosen, hour_number_chosen):
        ax.text(a, b, (a, b), ha='right', va='bottom', fontsize=5)
    for a, b in zip([17], [445]):
        ax.text(a, b, (a, b), ha='left', va='bottom', fontsize=5)
    plt.show()
    st.pyplot(fig)

with tab5:
    result12 = (df['DISTRICT'].value_counts()[0:12]).to_dict()
    result = (df['DISTRICT'].value_counts()).to_dict()
    print(result)
    district_number = result.values()
    print(district_number)
    district12 = [boston_police_districts_dict[i] for i in result12.keys()]
    district = np.arange(len(result.keys()))
    district_name = district12 + ['External']
    print(district_name)
    fig, ax = plt.subplots(figsize=(4, 1.8))
    ax.bar(district, district_number, width=0.9, edgecolor="white", linewidth=0.5)
    ax.set_title("Number of Crimes in 12 Police Districts", fontsize=7)
    ax.set_xticks(district, labels=district_name)
    ax.set_ylim(top=900)
    pl.xticks(rotation=45)
    plt.tick_params(labelsize=5)
    for a, b in zip(district, district_number):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=4)
    plt.show()
    st.pyplot(fig)
