import argparse
from datetime import datetime
import json
import os
import pandas as pd
from read_sec_json import get_income_statement

# Take a ticker name in for turning into a single csv file
parser = argparse.ArgumentParser("This will read the files created from querying the sec api and parse them for your hw assignment")
parser.add_argument("ticker_name", type = str, help="A ticker for the company you would like to parse")
args = parser.parse_args()
ticker= args.ticker_name.upper()

# Iterate through all files in the whole_filings directory and select the ones matching the ticker for processing
filing_dir = 'whole_filings'
files = os.listdir(filing_dir)
matching_files = [file for file in files if ticker in file]
matching_files.sort(key=lambda file: datetime.strptime(file.split('_')[3].split('.')[0], "%Y-%m-%d"))
all_statements = []

# Iterate through each file in our whole_filings directory that has been built with the previous scripts
for file in matching_files:
    file_path = os.path.join(filing_dir, file)

    with open(file_path, 'r') as f:
        xbrl_json = json.load(f)

    # Define the values that will be held in the output
    income_statement, is_10k = get_income_statement(xbrl_json)
    # IBM stores its revenue under 'Revenues', thus we now need a conditional to avoid a key type error
    if 'RevenueFromContractWithCustomerExcludingAssessedTax' in income_statement.index:
        revenue = income_statement.loc['RevenueFromContractWithCustomerExcludingAssessedTax'].iloc[-1]
    elif 'Revenues' in income_statement.index: 
        revenue = income_statement.loc['Revenues'].iloc[-1]
    net_income = income_statement.loc['NetIncomeLoss'].iloc[-1]
    dividends = income_statement.loc['PaymentsOfDividendsCommonStock'].iloc[-1]

    # Define the columns we care about
    data = {
        'Revenue' : [revenue],
        'Earnings' : [net_income],
        'Dividends' : [dividends],
        '10-K' : [is_10k]
    }
    all_statements.append(pd.DataFrame(data))
    
# Combine each single row into a single table
combined_statement = pd.concat(all_statements, ignore_index=True)

# Iterate through each row in the datadrame
for index in range(len(combined_statement)):
    if combined_statement['10-K'].iloc[index]:
        # Avoid going out of bounds by checking we have enough values, warn the user if there are not enough
        if index < 3:
            print("Warning: There are less than 3 values for the first given 10-K form")
            print("Please run the sec_query one more time with an expanded date range")
            print("Or consider deleting this filing from whole_filings and any dated earlier if you have enough data")
            print(f"File index:{index}")
            continue
        else:
            # Modify revenue
            rev_val = int(combined_statement.loc[index, 'Revenue'])
            rev_sub = (int(combined_statement.loc[index-1, 'Revenue'])+
                       int(combined_statement.loc[index-2, 'Revenue'])+
                       int(combined_statement.loc[index-3, 'Revenue']))
            combined_statement.loc[index, 'Revenue'] = rev_val - rev_sub
            # Modify earnings
            ear_val = int(combined_statement.loc[index, 'Earnings'])
            ear_sub = (int(combined_statement.loc[index-1, 'Earnings'])+
                       int(combined_statement.loc[index-2, 'Earnings'])+
                       int(combined_statement.loc[index-3, 'Earnings']))
            combined_statement.loc[index, 'Earnings'] = ear_val - ear_sub
            # Modify dividends
            div_val = int(combined_statement.loc[index, 'Dividends'])
            div_sub = (int(combined_statement.loc[index-1, 'Dividends'])+
                       int(combined_statement.loc[index-2, 'Dividends'])+
                       int(combined_statement.loc[index-3, 'Dividends']))
            combined_statement.loc[index, 'Dividends'] = div_val - div_sub
            # Set 10-K to false to indicated that it has been processed
            combined_statement.loc[index, '10-K'] = False

# Output the dataframe to a csv file in the directory for the homework
output_dir = f'hw_filings/{ticker}_income_statements.csv'
combined_statement.to_csv(output_dir, index = True, mode = 'w')
    


