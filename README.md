## About

This script was designed to help students enrolled in the Introduction to Data Science graduate level course access publicly available stock information through the SEC Api
 to build a small predictive model. It creates a CSV file given a ticker symbol and date range in the hw_filings directory.

### Dependencies
In addition to Python and its standard libraries Pandas, Requests, and Sec_api are all required for the script to run.
`pip install pandas`
`pip install requests`
`pip install sec_api`

You will also need to visit https://sec-api.io/signup/free and sign up for a free trial api key, which allows you 100 requests (which is more than enough).
#### You must paste your API key into the sec_api_key.txt file for the query to work



### Usage
For the final output needed for the homework assignment you will need to run two commands per ticker.

The first looks like this:
`python sec_query.py MSFT 2022-10-01`

This will return all the urls for associated 10-Q and 10-K forms and pass them into a function which writes the entirety of those filings as json files to the whole_filings directory.
There is no output to console.

The second command looks like this:
`python hw_data_maker.py MSFT`

This will access all json files associated with the ticker symbol and merge the relevant information (Revenue, Earnings, Dividends paid) into a single csv file that will be output to your hw_filings directory.
Repeat this for each symbol as you wish.

You will only accumulate pull requests via the first command. There is a delay timer to prevent exceeding the frequency in which you are allowed to make requests. Furthermore,
there is one request to pull all the documents, then 1 request per document, you are allotted 100 requests as part of your free trial.

There is an optional argument you can pass to the sec_query.py script for the end date (because you wouldn't want to always pull to the most recent filing, especially if you already have it saved). The command looks like this:

`python sec_query.py MSFT 2022-10-01 -e 2023-10-01`

### Possible Errors
This script was tested on the symbols requested in the HW assignment. Companies use different names of categories to store values, it is very possible to get an error when converting from a json to a csv if used on a company other than AAPL, GOOG, GE, IBM, META, MSFT, PG.

Furthermore, a 10-K filing is a form that is filled out yearly, and includes values for the entire year (meaning that it needs to be processed relative to the previous 3 values of that year to get a value for the final quarter of the year).
This effects the dividends paid out in a way that does not reflect the real world comparison. Sometimes the dividends become negative, however this cannot be, as shareholders do not directly pay the company for any given quarter.
