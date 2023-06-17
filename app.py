import calendar
from datetime import datetime
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly
from streamlit_option_menu import option_menu # pip install streamlit_option_menu

import database as db #local import

#Import the database functions



#-------------Settings----------------
incomes = ['Salary', 'Business', 'Rental', 'Other']
expenses = ['Food', 'Clothing', 'Transportation', 'Education', 'Healthcare', 'Entertainment', 'Others']

currency = "₹INR"
page_title = "Budget Tracker"
page_icon = "💵"
layout = 'centered'

#-------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout) # Page Config
st.title(page_title+" "+page_icon) # Title4



#--Nevigation Menu--#
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization", "About"],
    icons=["📝", "📊", "📄"], #https://bootstrap-vue.org/docs/icons
    orientation = "horizontal",
)

#Dropdown menu for selecting the items
# year = st.selectbox("Select Year", list(range(2020, 2030)), key='year')
# month = st.selectbox("Select Month", list(range(1, 13)), key='month')

years = [datetime.today() . year, datetime . today() . year + 1] # Year list
months = list(calendar.month_name[1:])

#----Database Interface----#
def get_all_periods():
    """Return all the periods in the database"""
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods



#---HIDE STREAMLIT STYLE---#
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)


#Imput and Save periods
if selected == "Data Entry":
    st.header(f"Data Entry in(currency)")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:", months, key='month')
        col2.selectbox("Select Year:", years, key='year')
        
        "---"
        "__Incomes__"
        with st.expander("Add Income"):
            for income in incomes:
                col1, col2 = st.columns(2)
                col1.text(income)
                col2.number_input("Enter Amount", key=income, step=10, min_value=0)
        "__Expenses__"
        with st.expander("Add Expense"):
            for expense in expenses:
                col1, col2 = st.columns(2)
                col1.text(expense)
                col2.number_input("Enter Amount", key=expense, step=10, min_value=0)
        "__Comments__"
        # with st.expander("Add Comments"):
        comment = st.text_area("", placeholder="Enter your comments here...")
        
        "---"
        submitted = st.form_submit_button("Submit")
        if submitted:
            period = str(st.session_state["year"])+"-"+str(st.session_state["month"])
            # income = [st.session_state["Salary"], st.session_state["Business"], st.session_state["Rental"], st.session_state["Other"]]
            income = {income: st.session_state[income] for income in incomes} 
            expense = {expense: st.session_state[expense] for expense in expenses}   
            db.insert_period(period, income, expense, comment)
            # st.write(f"income: {income}")
            # st.write(f"expense: {expense}")
            st.success(f"Data saved for {period}")
            
            
        
        
#---PLOT PERIODS---#
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"): #get the periods from database
        period = st.selectbox("Select Period:",get_all_periods())
        submitted = st.form_submit_button("Plot")
        if submitted:
            period_data = db.get_period(period)
            comment = period_data["comment"]
            expenses = period_data["expenses"]
            incomes = period_data["incomes"]
            
            # comment = "This is a comment"
            # incomes = {'Salary':1500, 'Business':100, 'Rental':500, 'Other':100}
            # expenses = {'Food':100, 'Clothing':500, 'Transportation':50, 'Education':50, 'Healthcare':50, 'Entertainment':150, 'Others':50}    
            
    #Create Metrics
    total_income = sum(incomes.values())
    total_expense = sum(expenses.values())
    remaining = total_income - total_expense
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Income", f"{currency} {total_income}")
    col2.metric("Total Expense", f"{currency} {total_expense}")
    col3.metric("Remaining", f"{currency} {remaining}")
    st.text(f"Comments: {comment}")
        
            
    #SANKEY CHART
    label =   list(incomes.keys()) + ["Total Income"] + list(expenses.keys()) 
    source = list(range(len(incomes))) + [len(incomes)] * (len(expenses) +1)
    target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
    value = list(incomes.values()) + list(expenses.values())   
    # value = list(incomes.values()) + [sum(incomes.values())] + list(expenses.values())

    #Data to dictionary, dict to sankey
    link = dict(source = source, target = target, value = value)
    node = dict(label = label, pad=50, thickness=3, color="blue")
    data = go.Sankey(link = link, node=node)

    #plot it
    fig = go.Figure(data)
    fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
    st.plotly_chart(fig, use_container_width=True)