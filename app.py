import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


@st.cache
def load_data():
    df = pd.read_csv("states.csv")
    return df

df = load_data()
df_ts=pd.read_csv("case_time_series.csv")

st.title('Covid-19 India Cases Total Confirmed')
fig = px.line(df_ts,x='Date',y=df_ts['TotalConfirmed'])
st.plotly_chart(fig)
st.title('Covid-19 India Cases State Wise')
st.write("State Wise ***Coronavirus Cases*** in India")
st.title("Total Recovered Cases Among states")

st.sidebar.title("Please Select")
image = Image.open("corona.jpg")
st.image(image,use_column_width=True)
st.markdown('<style>body{background-color: yellow;}</style>',unsafe_allow_html=True)



visualization = st.sidebar.selectbox('Select a Chart type',('Bar Chart','Pie Chart','Line Chart'))
state_select = st.sidebar.selectbox('Select a state',df['State'].unique())
status_select = st.sidebar.radio('Covid-19 patient status',('Confirmed','Tested','Recovered','Deceased'))
#select = st.sidebar.selectbox('Covid-19 patient status',('Confirmed','Tested','Recovered','Deceased'))
selected_state = df[df['State']==state_select]
st.markdown("## **State level analysis**")

def get_total_dataframe(df):
    total_dataframe = pd.DataFrame({
    'Status':['Confirmed', 'Recovered', 'Deceased','Tested'],
    'Number of cases':(df.iloc[0]['Confirmed'],
    df.iloc[0]['Recovered'], 
    df.iloc[0]['Deceased'],df.iloc[0]['Tested'])})
    return total_dataframe
state_total = get_total_dataframe(selected_state)
if visualization=='Bar Chart':
    state_total_graph = px.bar(state_total, x='Status',y='Number of cases',
                               labels={'Number of cases':'Number of cases in %s' % (state_select)},color='Status')
    st.plotly_chart(state_total_graph)
elif visualization=='Pie Chart':
    if status_select=='Confirmed':
        st.title("Total Confirmed Cases ")
        fig = px.pie(df, values=df['Confirmed'], names=df['State'])
        st.plotly_chart(fig)
    elif status_select=='Tested':
        st.title("Total Tested Cases ")
        fig = px.pie(df, values=df['Tested'], names=df['State'])
        st.plotly_chart(fig)
    elif status_select=='Deceased':
        st.title("Total Death Cases ")
        fig = px.pie(df, values=df['Deceased'], names=df['State'])
        st.plotly_chart(fig)
    else:
        st.title("Total Recovered Cases ")
        fig = px.pie(df, values=df['Recovered'], names=df['State'])
        st.plotly_chart(fig)
elif visualization =='Line Chart':
    if status_select == 'Deceased':
        st.title("Total Death Cases Among states")
        fig = px.line(df,x='State',y=df['Deceased'])
        st.plotly_chart(fig)
    elif status_select =='Confirmed':
        st.title("Total Confirmed Cases Among states")
        fig = px.line(df,x='State',y=df['Confirmed'])
        st.plotly_chart(fig)
    elif status_select =='Recovered':
        st.title("Total Recovered Cases Among states")
        fig = px.line(df,x='State',y=df['Recovered'])
        st.plotly_chart(fig)
    else:
        st.title("Total Tested Among states")
        fig = px.line(df,x='State',y=df['Tested'])
        st.plotly_chart(fig)
        
def get_table():
    datatable = df[['State', 'Confirmed', 'Recovered', 'Deceased','Tested']].sort_values(by=['Confirmed'],ascending =False)
    return datatable

datatable = get_table()
st.dataframe(datatable)

