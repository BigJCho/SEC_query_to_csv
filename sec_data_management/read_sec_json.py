import pandas as pd

# Majority of this code is from the tutorial 'Extracting Financial Statements from SEC Filings - XBRL-To-JSON' on Medium.com
# convert XBRL-JSON of income statement to pandas dataframe
def get_income_statement(xbrl_json):
    income_statement_store = {}
    # iterate over each US GAAP item in the income statement
    for usGaapItem in xbrl_json['StatementsOfIncome']:
        values = []
        indicies = []

        for fact in xbrl_json['StatementsOfIncome'][usGaapItem]:
            # only consider items without segment. not required for our analysis.
            if 'segment' not in fact:
                index = fact['period']['startDate']
                # ensure no index duplicates are created
                if index not in indicies:
                    values.append(fact['value'])
                    indicies.append(index)                    

        
        # This is to select a single value, the value with the latest date
        # Most forms include data from previous years or quarters, we are interested in the most recent date
        if indicies and values:
            latest_index = max(indicies)
            latest_value = values[indicies.index(latest_index)]
            income_statement_store[usGaapItem] = pd.Series([latest_value], index=[latest_index])

    # Dividends paid out are not held in Statements of Income and thus we loop a through a different section
    # Upon testing on other stocks I found there to be many varying names
    # I am adding conditionals to account for this
    # The output will save under the same name each time for consistency among modules
    if xbrl_json.get('StatementsOfCashFlows', {}).get('PaymentsOfDividendsCommonStock'):
        for fact in xbrl_json['StatementsOfCashFlows']['PaymentsOfDividendsCommonStock']:
            if 'value' in fact:
                income_statement_store['PaymentsOfDividendsCommonStock'] = fact['value']
                break
    elif xbrl_json.get('StatementsOfCashFlows', {}).get('PaymentsOfDividends'):
        for fact in xbrl_json['StatementsOfCashFlows']['PaymentsOfDividends']:
            if 'value' in fact:
                income_statement_store['PaymentsOfDividendsCommonStock'] = fact['value']
                break
    elif xbrl_json.get('StatementsOfCashFlows', {}).get('ShareBasedCompensation'):
        for fact in xbrl_json['StatementsOfCashFlows']['ShareBasedCompensation']:
            if 'value' in fact:
                income_statement_store['PaymentsOfDividendsCommonStock'] = fact['value']
                break
    elif xbrl_json.get('StatementsOfCashFlows', {}).get('PaymentsOfOrdinaryDividends'):
        for fact in xbrl_json['StatementsOfCashFlows']['PaymentsOfOrdinaryDividends']:
            if 'value' in fact:
                income_statement_store['PaymentsOfDividendsCommonStock'] = fact['value']
                break
    
    income_statement = pd.DataFrame(income_statement_store).T
    is_10k = xbrl_json['CoverPage']['DocumentType'] == '10-K'
    # 10-K forms require additional processing, thus we need to return a flag if a statement is a 10-K
    return income_statement, is_10k
