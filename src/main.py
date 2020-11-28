import arrow
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from models import Paste
from services import connect_to_mongodb
import dotenv
import time

dotenv.load_dotenv()
session = HTMLSession()

ARCHIVE_URL = 'https://pastebin.com/archive'
MAIN_URL = 'https://pastebin.com'

## get the page html
def fetch_page_html(url):
    try:
        results = session.get(url)
        parsed_html = BeautifulSoup(results.text, "html.parser")
        return parsed_html
    except Exception as e:
        print("error:", e)
        return exit()    

## get the links for the top pastes 
def fetch_links_from_page(html):
    links = []
    table = html.find('table', class_='maintable')
    rows = table.findAll('tr')
    for row in rows:
        link = row.a
        if link is not None:
            links.append(str(link['href']))
    return links

## get paste from specific page
def get_page_info(html):
    title, username, content, date = '', '', '', ''
    title_tag = html.find('div', class_='info-top')
    if title_tag is not None:
        title = title_tag.h1.text
    username_tag = html.find('div', class_='username')
    if username_tag is not None:
        if username_tag.find('a'):
            username = username_tag.a.text
        else:
            username = 'Unknown_Author'
    content_code = html.find('div', class_='source')
    for li in content_code.findAll('li'):
        for span in li.findAll('span'):
            content += span.text.strip()
    date_local = html.find('div', class_='date').span.text
    replace_date = date_local.replace('th,', '')
    date = str(arrow.get(replace_date, 'MMM D YYYY').to('UTC'))
    new_data = Paste(username, title, content, date)
    paste_obj = new_data.create_obj()
    return paste_obj

## insert only new pastes into db
def insert_data_to_db(db_collection, data):
    try:
        count = db_collection.count_documents({
           "Author": data["Author"],
           "Title": data["Title"],
           "Content": data["Content"],
           "Date": data["Date"]   
        })
        if count == 0:
            db_collection.insert_one(data)
            return True
        else:
            return False    
    except Exception as e:
        print("mongo error:",e)
        return exit()

def main():
    pastes_collection = connect_to_mongodb() # in case mongo failed to connect the function return False and process will exit
    if pastes_collection == False:
        return exit()
    print('scrawl in process')
    parsed_html = fetch_page_html(ARCHIVE_URL)
    links = fetch_links_from_page(parsed_html)
    new_items = 0
    for link in links:
        link_html = fetch_page_html(f'{MAIN_URL}{link}')
        obj = get_page_info(link_html)
        status = insert_data_to_db(pastes_collection, obj)
        if status == True:
            new_items += 1   
    print(f'scrawl finished - added {new_items} new pastes')
    time.sleep(120) # wait 2 minutes till the next scrawl


if __name__ == '__main__':
    while True:
        main()
