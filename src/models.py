from bs4 import BeautifulSoup
from pymongo import MongoClient
import arrow
from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()


class Page:

    ## get the page html
    def fetch_page_html(url):
        try:
            result = session.get(url)
        except Exception as e:
            print("error:", e)
            return exit()
        parsed_html = BeautifulSoup(result.text, "html.parser")
        return Page(parsed_html)
    
    def __init__(self, parsed_page):
        self.parsed_page = parsed_page

    ## get the links for the top pastes 
    def fetch_links_from_page(self):
        links = []
        table = self.parsed_page.find('table', class_='maintable')
        rows = table.findAll('tr')
        for row in rows:
            link = row.a
            if link is not None:
                links.append(str(link['href']))
        return links

    ## get paste from specific page
    def get_page_info(self):
        title, username, content, date = '', '', '', ''
        title_tag = self.parsed_page.find('div', class_='info-top')
        if title_tag is not None:
            title = title_tag.h1.text
        username_tag = self.parsed_page.find('div', class_='username')
        if username_tag is not None:
            if username_tag.find('a'):
                username = username_tag.a.text
            else:
                username = 'Unknown_Author'
        content_code = self.parsed_page.find('div', class_='source')
        for li in content_code.findAll('li'):
            for span in li.findAll('span'):
                content += span.text.strip()
        date_local = self.parsed_page.find('div', class_='date').span.text
        replace_date = date_local.replace('th,', '')
        date = str(arrow.get(replace_date, 'MMM D YYYY').to('UTC'))
        new_paste = Paste(username, title, content, date)
        return new_paste.create_object()
               


class Paste:
    
    def __init__(self, Author='', Title='', Content='', Date=''):
        self.Author = Author
        self.Title = Title
        self.Content = Content
        self.Date = Date  

    def create_object(self):
        return {"Author": self.Author,
            "Title": self.Title,
            "Content": self.Content,
            "Date": self.Date}

    
class Db_Connection:

    def __init__(self, connction_string, collection):
        self.connction_string = connction_string
        self.collection = collection

    def connect(self):
        try:
            client = MongoClient(self.connction_string)
            db = client.db
            collection = db[self.collection]
            print('sucessfully connected to mongo')
            return collection
        except Exception as e:
            print("exeption:", e)
            return False

class Db_Actions:

    def __init__(self, collection):
        self.collection = collection

    # insert only new pastes
    def insert(self, data):
        try:
            count = self.collection.count_documents(data)
            if count == 0:
                self.collection.insert_one(data)
                return True
            else:
                return False    
        except Exception as e:
            print("mongo error:",e)
            return exit()   



