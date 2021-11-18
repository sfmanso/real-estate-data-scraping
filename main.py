#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#create an empty list
aptlist = []

#function to extract data from
def extract(page):
    
    #headers
    request_headers = {
        'accept': 'text/html, application/xhtml+xml, application/xml;q=0.9,image/webp, image/apng,*/*: q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US, en; q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    
    #start session
    with requests.Session() as session:
        url = f'https://www.apartments.com/nj/{page}'
        response = session.get(url, headers=request_headers)
        response_out = str(response).strip('>]<').replace('[','').split()
    
    #create and return soup
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

#function to transform data from page
def transform(soup):
    
    #store soup in variable called apartments
    apartments = soup.find_all('article', class_ = 'placard placard-option-diamond has-header js-diamond')
    
    #iterate apartments for specific data
    for apartment in apartments:
        title = apartment.find('span').text.strip()
        address = apartment.find('div', class_ = 'property-address').text.strip()
        zipcode = address.split(' ')[-1]
        price = apartment.find('p', class_ = 'property-pricing').text.strip()
        bed = apartment.find('p', class_ = 'property-beds').text.strip()
        
        #save to dictionary
        apt = {
            'title': title,
            'addtess': address,
            'zipcode': zipcode,
            'price': price,
            'bed': bed
        }
        
        #add to list
        aptlist.append(apt)
    return

#function to execute transform and load
def run(pages):
    
    #determine number of web-pages to iterate
    if pages == 1:
        print (f'extracting for {pages} pages')
        c = extract(1)
        transform(c)
    elif pages > 1:
        npages = pages+1
        print (f'extracting for {pages} pages')
        for i in range(1,npages):
            c = extract(i)
            transform(c)
            print(f'page {i} completed with no errors')
    
    #save list to dataframe
    df = pd.DataFrame(aptlist)
    
    #save dataframe to csv
    print('writing to csv...')
    df.to_csv('apartments.csv', index=False)
    print('process complete!')
    return

#execute code
run(100)