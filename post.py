import datetime


class Post:
    def __init__(self, title, date, content):
        self.title = title
        self.date = date
        self.content = content

    def formatted_date(self):
        return datetime.datetime.date(self.date).strftime("%B %d")
