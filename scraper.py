import argparse
import validators
import requests
import json
from bs4 import BeautifulSoup
import spacy
nlp = spacy.load("en_core_web_md")


def main(urls):
    web = scraper(urls)
    web_json = json.dumps(web)
    extract_entities(web_json)


def extract_entities(web_data):
    web_json = json.loads(web_data)
    for data in web_json:
        stripped = data['body'].replace('"', '')
        doc = nlp(stripped)
        data['people'] = [ent for ent in doc.ents if ent.label_ == 'PERSON']
        data['places'] = [ent for ent in doc.ents if ent.label_ == 'LOC']
        data['organisations'] = [ent for ent in doc.ents if ent.label_ == 'ORG']

        print(f"\nArticle Title: {data['title']}")
        print(f"People identified: {data['people']}")
        print(f"Places identified: {data['places']}")
        print(f"Organisations identified: {data['organisations']}")


def scraper(urls):
    web = []
    for url in urls:
        if validators.url(url):
            web_site = {}
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            web_site['title'] = soup.title.string
            dates = soup.find_all('div', attrs={'class': 'date date--v2'})
            web_site['date'] = dates[0]['data-datetime']
            web_site['body'] = soup.find('div', attrs={'class': 'story-body__inner'}).get_text()
            web.append(web_site)

    return web


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs='+', help="Enter the URL to be scraped")
    args = parser.parse_args()

    main(args.urls)
