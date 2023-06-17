#key = bC7Mr5sz_FwWuM1c1gHMVYdL28ugW1tKAKUuLr6f3 
from deta import Deta
import os
from dotenv import load_dotenv #For loading the environment variables #pip install python-dotenv

#Loading the environment variables
load_dotenv("key.env")
DETA_Key = os.getenv("DETA_Key")

#Initialize Deta with a product key
deta = Deta(DETA_Key)

#Connecting to Deta Base(Database)
db = deta.Base("Budgeteer")

def insert_period(period, incomes, expenses, comment):
    """Return the report on a succesful creation, otherwise raise an error"""
    return db.insert({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})

def fetch_all_periods():
    """Return all the periods in the database"""
    res = db.fetch()
    return res.items

def get_period(period):
    """Return the period with the given key"""
    return db.get(period)