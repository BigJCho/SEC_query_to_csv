from sec_api import QueryApi
from sec_to_json import fetch_and_save
import argparse

parser = argparse.ArgumentParser("Queries the SEC for a company ticker and date in YYYY-MM-DD format")
parser.add_argument("ticker_name", type = str, help="A single ticker symbol that you would like to be pulled")
parser.add_argument("start_date", type = str, help="Everything after the date (YYYY-MM-DD) entered will be pulled")
parser.add_argument("-e", type = str, default = '*', help="Specify an end date in YYYY-MM-DD to avoid additional api calls")
args = parser.parse_args()

ticker = args.ticker_name.upper()
start = args.start_date
end = args.e
with open('sec_api_key.txt', 'r') as file:
    key = file.read().strip()

query_api = QueryApi(api_key=key)
input_query = f'(formType:\"10-Q\" OR formType:\"10-K\") AND ticker:{ticker} AND filedAt:[{start} TO {end}]'

query = {
    "query": {
        "query_string": {
            "query": input_query
        }
    }
}

query_result = query_api.get_filings(query)

filing_info = []
for filing in query_result['filings']:
    filing_info.append({
        'url' : filing['linkToFilingDetails'],
        'date' : filing['filedAt'][:10]
    })

for entry in filing_info:
    fetch_and_save(entry['url'], ticker, entry['date'])