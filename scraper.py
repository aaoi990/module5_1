import argparse
import validators
import requests
from bs4 import BeautifulSoup


def main(urls):
    scraper(urls)


def scraper(urls):
    web_data = []
    for url in urls:       
        if(validators.url(url)):
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            site_title = soup.title.string
            dates = soup.find_all('div', attrs={'class': 'date date--v2'})    
            site_date = dates[0]['data-datetime']
            site_body = soup.find('div', attrs={'class': 'story-body__inner'}).get_text()    
            web_data.append({ 'url': url, 'title': site_title, 'date':site_date, 'site_body': site_body })

    print(web_data)        
    
def tag_visible(element):
    print(element.child.name, 'elemet')
    if element in ['style', 'script', 'head', 'title', 'meta', '[document]', 'li']:
        return False
    if isinstance(element, Comment):
        return False
    return True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs='+', help="Enter the URL to be scraped")
    args = parser.parse_args()

    main(args.urls)