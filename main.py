from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    
def parse_html(url):
    try:
        req = requests.get(url,headers=headers)

    except requests.exceptions.ConnectionError:
        req.status_code = "Connection refused"
  
    parse = BeautifulSoup(req.text,'lxml')
    return parse

def get_link():
    parse = parse_html('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
    movie = parse.find_all('li','ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent')
    links = []
    for m in movie[0:100]:
        link = m.find('a','ipc-title-link-wrapper').get('href')
        links.append(link)
    return links

def loop_data(value):
    data = []
    for i in range(0,len(value)):
        data.append(value[i].text)
    return ",".join(data)


def get_data(link):
    parse = parse_html(link)
    Title = parse.find('span','hero__primary-text').text
    Rating= parse.find('span','sc-bde20123-1').text
    Year=parse.find('div','cFndlt').find_next('a','ipc-link ipc-link--baseAlt ipc-link--inherit-color').text

    Synopsis = parse.find('span','sc-466bb6c-0 hlbAws').text
    Runtime=parse.find('li',attrs={"data-testid": 'title-techspec_runtime'}).find('div','ipc-metadata-list-item__content-container').text
    if parse.find('span',string="Director") :
        Director=parse.find('span',string="Director").parent.find_all('a','ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')
    else:
        Director=parse.find('span',string="Directors").parent.find_all('a','ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')


        
    Directors = loop_data(Director)
    try:
        Filming_location= parse.find('li',attrs={"data-testid": 'title-details-filminglocations'}).find('a','ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text
    except:
        Filming_location = None
    try:
        Budget=parse.find('li',attrs={"data-testid": 'title-boxoffice-budget'}).find('span','ipc-metadata-list-item__list-content-item').text.replace(' (estimated)','')
    except:
        Budget = None
    try:
        Income=parse.find('li',attrs={"data-testid": 'title-boxoffice-cumulativeworldwidegross'}).find('span','ipc-metadata-list-item__list-content-item').text
    except:
        Income = None

    Country_of_origin=parse.find('li',attrs={"data-testid": 'title-details-origin'}).find('a','ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text
    
    genre =parse.find('div','ipc-chip-list--baseAlt ipc-chip-list').find_all('span','ipc-chip__text')
    Genres = loop_data(genre)

   
        
    
    data = {
        'Title' :  Title,
        'Rating' :  Rating,
        'Year' :  Year,
        'Synopsis' :  Synopsis,
        'Runtime' :  Runtime,
        'Directors' :  Directors,
        'Filming_location' :  Filming_location,
        'Budget' :  Budget,
        'Income' :  Income,
        'Country_of_origin' :  Country_of_origin,
        'Genres' :  Genres,
    }
    print(link,'success')
   
    return data

def main():
    baseurl = 'https://www.imdb.com'
    links = get_link()
    data = []
    for l in links:
        movie = get_data(baseurl+l)
        data.append(movie)
    df = pd.DataFrame(data)
    df.to_csv("imdb.csv")




if __name__ == "__main__":  
    main()