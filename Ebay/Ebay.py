import json
import requests
import pandas as pd
from datetime import datetime
from misspellings import Misspellings

# EbayAPI will fetch you data about your desired item including a misspellings class to find out potentially attractive deals.
# EbayAPI will output the found items and data into a pandas dataframe.

def get_global_ID():
    

def construct_url(search_term):
    url = 'https://svcs.ebay.com/services/search/FindingService/v1\
    ?SECURITY-APPNAME=OndejMar-PrvniApl-PRD-6d8cefb65-8ed3ffd7\
    &OPERATION-NAME=findItemsByKeywords\
    &SERVICE-VERSION=1.13.0\
    &RESPONSE-DATA-FORMAT=JSON\
    &callback=_cb_findItemsByKeywords\
    &REST-PAYLOAD\
    &GLOBAL-ID=EBAY-US\
    &keywords=' + search_term
    return url

# parameters of the item we want to get
parameters = [title,category,location,condition,buying_format,price,currency,shipping,payment,ending]  
    
def parse_response():
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
    
    key = 'XXX'
    # Item to search for on Ebay
    
    desired_item = input()
    # Include misspellings and other variations of the search term
    
    search_term = Misspellings().misspelling(desired_item)
    
    # Construct the url - using findItemsByKeywords API call
    url = get_url(search_term)
    
    # Get a response from Ebay API
    apiResult = requests.get(url)
    
    # Prepare the response for parsing
    response_to_parse = apiResult.text[28:-1] 
    translated_to_json = json.loads(response_to_parse)

    ### Parsing the response
    parsed = parse_response(translated_to_json)
    
    


    # Create a dataframe
    df = pd.DataFrame(data=tab,columns=['title','category','location','condition','buying_format','price','currency','shipping','payment','ending'])

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
