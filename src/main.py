from models import Paste, Db_Connection, Db_Actions, Page
import time
import os

ARCHIVE_URL = 'https://pastebin.com/archive'
MAIN_URL = 'https://pastebin.com'
CONNECTION_STRING = f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@{os.environ['MONGODB_HOSTNAME']}:27017/{os.environ['MONGODB_DATABASE']}"

def main():
    new_db = Db_Connection(CONNECTION_STRING, "pastedb") # in case mongo failed to connect the function return False and process will exit
    pastes_collection_connection = new_db.connect()
    pastes_collection = Db_Actions(pastes_collection_connection)
    if pastes_collection == False:
        return exit()
    print('scrawl in process')
    new_page = Page.fetch_page_html(ARCHIVE_URL)
    links = new_page.fetch_links_from_page()
    new_items = 0
    for link in links:
        internal_page = Page.fetch_page_html(f'{MAIN_URL}{link}')
        new_paste = internal_page.get_page_info()
        status = pastes_collection.insert(new_paste)
        if status == True:
            new_items += 1   
    print(f'scrawl finished - added {new_items} new pastes')
    time.sleep(120) # wait 2 minutes till the next scrawl


if __name__ == '__main__':
    while True:
        main()
