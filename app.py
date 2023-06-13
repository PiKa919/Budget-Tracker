import calendar
from datetime import datetime
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly


#-------------Settings----------------
income = ['Salary', 'Business', 'Rental', 'Other']
expenses = ['Food', 'Clothing', 'Transportation', 'Education', 'Healthcare', 'Entertainment', 'Other']

currency = "₹INR"
page_title = "Budget Tracker"
page_icon = "💵"
layout = 'centered'

#-------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout) # Page Config
st.title(page_title+" "+page_icon) # Title4

#Dropdown menu for selecting the items
# year = st.selectbox("Select Year", list(range(2020, 2030)), key='year')
# month = st.selectbox("Select Month", list(range(1, 13)), key='month')
# https://youtu.be/ub9wksI-M2M

years = [datetime.today() . year, datetime . today() . year + 1] # Year list
months = list(calendar.month_name[1:])


#Imput and Save periods
st.header(f"Data Entry in(currency)")
with st.form("entry_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    col1.selectbox("Select Month:", months, key='month')
    col2.selectbox("Select Year:", years, key='year')
