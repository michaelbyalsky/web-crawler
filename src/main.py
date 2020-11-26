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


def fetch_page_html(url):
    results = session.get(url)
    parsed_html = BeautifulSoup(results.text, "html.parser")
    return parsed_html


def fetch_links_from_page(html):
    links = []
    table = html.find('table', class_='maintable')
    rows = table.findAll('tr')
    for row in rows:
        link = row.a
        if link is not None:
            links.append(str(link['href']))
    return links


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


def insert_data_to_db(db_collection, data):
    try:
        db_collection.insert_one(data)
        return "new paste added"
        exit()
    except Exception as e:
        return e


def remove_data_from_db(db_collection):
    try:
        db_collection.delete_many({})
        return "data deleted- ready to replace"
    except Exception as e:
        return e


def main():
    print('scrawl started')
    pastes_collection = connect_to_mongodb()
    remove_msg = remove_data_from_db(pastes_collection)
    print(remove_msg)
    parsed_html = fetch_page_html(ARCHIVE_URL)
    links = fetch_links_from_page(parsed_html)
    for link in links:
        link_html = fetch_page_html(f'{MAIN_URL}{link}')
        obj = get_page_info(link_html)
        insert_msg = insert_data_to_db(pastes_collection, obj)
        print(insert_msg)    
    print(f'scrawl finished- added {str(len(links))} new pastes')
    time.sleep(120)


if __name__ == '__main__':
    while True:
        main()
