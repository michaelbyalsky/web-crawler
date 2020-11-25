class Paste:
    def __init__(self, Author='', Title='', Content='', Date=''):
        self.Author = Author
        self.Title = Title
        self.Content = Content
        self.Date = Date

    def create_obj(self):
        return {'Author': self.Author, 'Title': self.Title, 'Content': self.Content, 'Date': self.Date}
