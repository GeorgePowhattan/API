import json
import requests
import pandas as pd
from datetime import datetime
from misspellings import Misspellings


def search_term_variations(item):
    search_term = Misspellings().misspelling(item)
    return search_term

def get_url(search_term):
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

def get_response():



if __name__ == "__main__":
    pass




key = 'XXX'
search_term = 'meermin'

### Finding service - using findItemsByKeywords API call
url = ('https://svcs.ebay.com/services/search/FindingService/v1\
?SECURITY-APPNAME=OndejMar-PrvniApl-PRD-6d8cefb65-8ed3ffd7\
&OPERATION-NAME=findItemsByKeywords\
&SERVICE-VERSION=1.13.0\
&RESPONSE-DATA-FORMAT=JSON\
&callback=_cb_findItemsByKeywords\
&REST-PAYLOAD\
&GLOBAL-ID=EBAY-US\
&keywords=' + search_term)

apiResult = requests.get(url)
parsed = apiResult.text[28:-1]  
translated_to_json = json.loads(parsed)

### Parsing response into dataframe
tab = []
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
    tab.append([title,category,location,condition,buying_format,price,currency,shipping,payment,ending])
#values are not stored in lists - don't access via [0]

# Create dataframe
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
