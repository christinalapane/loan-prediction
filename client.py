import numpy as np
import pandas as pd
import names

from app import app

df = pd.read_csv('train.csv')

# client information
df_banking = pd.DataFrame().assign(Loan_ID=df['Loan_ID'], Income=df['ApplicantIncome'],
                                   Co_Income=df['CoapplicantIncome'], Loan_Amount=df['LoanAmount'],
                                   Term_Length=df['Loan_Amount_Term'], Property=df['Property_Area'],
                                   Loan_Status=df['Loan_Status'])

# adding names to clients for the dashboard
loan_id_list = list(df_banking.Loan_ID.unique())
names_list = []
for i in range(614):
    names_list.append(names.get_full_name())

df_banking.insert(1, 'Clients', names_list)

# for property information
df_property = pd.DataFrame().assign(Property_Type=df['Property_Area'], Loan_Status=df['Loan_Status'])

print(df_banking['Loan_Status'].value_counts())


property_table = pd.DataFrame({
    'Property': ['Semi-urban', 'Urban', 'Rural'],
    'Sold': [179, 133, 110],
    'On_Market': [69, 69, 54]
}
)

market_df = pd.read_csv('static/address.csv')








def property_info():
    property_type = property_table.Property
    sold = property_table.Sold
    for_sale = property_table.On_Market
