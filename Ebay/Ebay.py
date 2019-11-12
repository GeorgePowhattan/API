import json
import requests
from datetime import datetime
import pandas as pd

from misspellings import Misspellings

# EbayAPI will fetch data about your desired item including possible misspellings to find potentially attractive deals.
# EbayAPI will output the found items and data into a pandas dataframe.

# url='https://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME=OndejMar-PrvniApl-PRD-6d8cefb65-8ed3ffd7&OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT=JSON&callback=_cb_findItemsByKeywords&REST-PAYLOAD&keywords=iPhone&paginationInput.entriesPerPage=6&GLOBAL-ID=EBAY-US&siteid=0'

def construct_url(search_term, country):
    
    # Look-up country ID e.g. EBAY-US
    df_country_code = pd.read_csv('EbayGlobalID.csv',delimiter=';')
    country_map = dict(zip(df_country_code['Site Name'], df_country_code['Global ID']))
    if country in country_map.values:
        country_code = country
    else:
        country_code = 'EBAY-DE'
    
    url = ('https://svcs.ebay.com/services/search/FindingService/v1?SECURITY-APPNAME=OndejMar-PrvniApl-PRD-6d8cefb65-8ed3ffd7\
    &OPERATION-NAME=findItemsByKeywords\
    &SERVICE-VERSION=1.13.0\
    &RESPONSE-DATA-FORMAT=JSON\
    &callback=_cb_findItemsByKeywords\
    &REST-PAYLOAD\
    &GLOBAL-ID=' + country_code + '\
    &keywords=' + search_term )
    
    return url
    
def parse_response(translated_to_json):
    table = []
    for item in (translated_to_json["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]):
        title = item["title"][0]
        category = item["primaryCategory"][0]['categoryName'][0]
        payment = item["paymentMethod"][0]
        try:
            condition = item['condition'][0]['conditionDisplayName'][0]
        except:
            condition = 'not available'
        price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']
        currency = item['sellingStatus'][0]["convertedCurrentPrice"][0]['@currencyId']
        location = item['location'][0]
        buying_format = item['listingInfo'][0]['listingType'][0] 
        ending = item['listingInfo'][0]['endTime'][0]
        try:
            shipping = item["shippingInfo"][0]['shippingServiceCost'][0]['__value__']
        except:
            shipping = "not available"
        table.append([title,category,location,condition,buying_format,price,currency,shipping,payment,ending])
    return table


if __name__ == "__main__":
    
    
    print("\n"+ "*"*15)
    print("Welcome to Ebay finder & misspellings checker!")
    print("*"*15 + "\n")
    print("Please enter the item you wish to buy.")
    desired_item = input()
    
    print("Please enter the Ebay country code to search. If omitted, Germany will be selected by default")
    print('\
    EBAY-AT	:	eBay Austria\
    EBAY-AU	:	eBay Australia\
    EBAY-CH	:	eBay Switzerland\
    EBAY-DE	:	eBay Germany\
    EBAY-ENCA	:	eBay Canada (English)\
    EBAY-ES	:	eBay Spain\
    EBAY-FR	:	eBay France\
    EBAY-FRBE	:	eBay Belgium (French)\
    EBAY-FRCA	:	eBay Canada (French)\
    EBAY-GB	:	eBay UK\
    EBAY-HK	:	eBay Hong Kong\
    EBAY-IE	:	eBay Ireland\
    EBAY-IN	:	eBay India\
    EBAY-IT	:	eBay Italy\
    EBAY-MOTOR	:	eBay Motors\
    EBAY-MY	:	eBay Malaysia\
    EBAY-NL	:	eBay Netherlands\
    EBAY-NLBE	:	eBay Belgium (Dutch)\
    EBAY-PH	:	eBay Philippines\
    EBAY-PL	:	eBay Poland\
    EBAY-SG	:	eBay Singapore\
    EBAY-US	:	eBay United States')

    country = input()
    
    print("Please enter the buying format:")
    print("a = auction only")
    print("b = auction and direct purchase")
    buying_format = input()
    
    
    key = '0e3601c9-4b61-48f8-9851-641301c57c26'
    
    # Include misspellings and other variations of the search term
    search_term = Misspellings().misspelling(desired_item)
    
    # Construct the url - using findItemsByKeywords API call
    url = construct_url(search_term, country)
    
    # Get a response from Ebay API
    apiResult = requests.get(url)
    
    # Prepare the response for parsing
    response_to_parse = apiResult.text[28:-1] 
    translated_to_json = json.loads(response_to_parse)

    # parameters of the item we want to get
    # parameters = [title,category,location,condition,buying_format,price,currency,shipping,payment,ending]

    # Parsing the response
    parsed = parse_response(translated_to_json)
    


    # Create a dataframe
    df = pd.DataFrame(data=parse_response,columns=['title','category','location','condition','buying_format','price','currency','shipping','payment','ending'])

    ### CONVERTING data formats
    df['price'] = pd.to_numeric(df['price'])
    df['ending'] = pd.to_datetime(df['ending'])
    df['ending'] = df['ending'].dt.tz_convert(None)  # different timezones cause trouble in "time remaining" subtraction
    df['today'] = pd.to_datetime(datetime.now())
    df['time_remaining'] = df['ending'] - df['today']

    ### FILTERING results
    # Filtering location ex-USA
    df[df['location'].apply(lambda x: "USA" not in x)]

    ### SORTING
    # Enter the column to sort the dataframe by
    sorting_var = ['ending']
    df.sort_values(by=sorting_var,kind='quicksort')

    print(df)
    df.to_excel("Ebay.xlsx")
