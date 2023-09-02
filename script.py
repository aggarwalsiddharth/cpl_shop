from playwright.sync_api import Playwright, sync_playwright
from time import sleep
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description ='search in some location')
  
# Adding Argument
parser.add_argument('--search_query', nargs="+")
  
parser.add_argument('--search_location', nargs="+")
  
args = parser.parse_args()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Enable request interception
    page = context.new_page()

    query_entity = ' '.join(args.search_query)
    query_loc = ' '.join(args.search_location)
    query = query_entity + ' in ' + query_loc

    # Navigate to a URL and print all requests
    page.goto(f"https://www.google.com/search?tbm=lcl&q={query}&num=20",wait_until = 'domcontentloaded')
    df = pd.DataFrame()
    # review_container = page.wait_for_selector('#rlfl__tls rl_tls')
    while page.locator('#pnnext').count() > 0:
        for element in page.locator('.rllt__details').all():
            
            try:
                name = element.get_by_role("heading").text_content()
                # print(name)
            except:
                continue
            try:
                address = element.locator('div').nth(2).text_content()
                # print(address)
            except:
                address = 'NOT AVAILABLE'
            
            try:
                phone = element.locator('div').nth(3).text_content()
                phone = (phone.split('·')[1]).replace(" ",'')
                
                if phone.startswith('01'):
                    phone = 'NOT AVAILABLE'

                else:
                    phone = phone.lstrip('0')
                    phone = '+91' + phone

            except:
                phone = 'NOT AVAILABLE'
            # print('-----------')
            # print(text)
            row_item = pd.DataFrame({'name':[name],'address':[address],'phone':[phone]})
            df = pd.concat([df,row_item])
        page.locator('#pnnext').click()
        sleep(2)
    
    
    # sleep(2)
    browser.close()

    if not os.path.exists('result/'+query_loc):
        os.makedirs('result/'+query_loc)
    df.reset_index(drop = True, inplace = True)
    df.to_csv(f'result/{query_loc}/{query_entity}.csv',index = True)
    print('\nFILE SAVED\n')

    # Get all the review elements
    # print(review_container)'tsuid_28'

    
    # Close the browser
    browser.close()

