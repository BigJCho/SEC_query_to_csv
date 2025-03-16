import requests
import json

#We define a method to intended to be used sequentially
#This means several API calls, each creating its own JSON file
def fetch_and_save(url, ticker, date):
    
    filing_url = url
    xbrl_converter_api_endpoint = "https://api.sec-api.io/xbrl-to-json"

    #Reads the api key saved in the txt file
    with open('sec_api_key.txt', 'r') as file:
        key = file.read().strip()

    #Forms the appropriate url to request from
    final_url = xbrl_converter_api_endpoint + "?htm-url=" + filing_url + "&token=" + key

    #Saves the response and converts it into a json file
    response = requests.get(final_url)
    xbrl_json = json.loads(response.text)

    #We define a unique name to save the entirety of the api call into a file we can work with
    #Because it's my free trial, and dang it I'm going to use the entirety of the data if I please
    output_file = f"whole_filings/{ticker}_whole_filing_{date}.json"
    with open(output_file, 'w') as json_file:
        json.dump(xbrl_json, json_file, indent=4)


        