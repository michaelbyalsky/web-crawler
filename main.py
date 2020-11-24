from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pymongo import MongoClient
import dotenv
import os


dotenv.load_dotenv()

session = HTMLSession()
ARCHIVE_URL = 'https://pastebin.com/archive'
MAIN_URL = 'https://pastebin.com'

user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
mongo_url = f'mongodb+srv://{user}:{password}@cluster0.d9oxu.mongodb.net/scrawler?retryWrites=true&w=majority'

try:
    client = MongoClient(mongo_url)
    print('sucessfully connected to mongo')
except Exception as e:
    print(e)
    
db = client["scrawler"]
collection = db["pastes"]

class Paste:
    def __init__(self, Author='', Title='', Content='', Date=''):
        self.Author = Author
        self.Title = Title
        self.Content = Content
        self.Date = Date

    def create_obj(self):
        return {'Author': self.Author, 'Title': self.Title, 'Content': self.Content, 'Date': self.Date}

def fetch(url):
    results = session.get(url)
    parsed_html = BeautifulSoup(results.text, "html.parser")
    return parsed_html

def get_pages_data(html):
    # obg_list = []
    links = []
    table = html.find('table', class_='maintable')
    rows = table.findAll('tr')
    for row in rows:
        link = row.a
        if link is not None:
            links.append(str(link['href']))
    for link in links:
        link_html = fetch(f'{MAIN_URL}{link}')
        obj = get_page_info(link_html) 
        # obg_list.append(obj) 
        try:
            insert_data = collection.insert_one(obj) 
        except Exception as e:
            print(e)
    return 'check your db for new data'

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
            content += span.text
        content += '\n'    
    date = html.find('div', class_='date').span.text
    new_data = Paste(username, title, content, date)
    paste_obj = new_data.create_obj() 
    return paste_obj        
        
def main():
    parsed_html = fetch(ARCHIVE_URL)
    objects = get_pages_data(parsed_html)
    print(objects)
    exit()

if __name__ == '__main__':
    main()
    
