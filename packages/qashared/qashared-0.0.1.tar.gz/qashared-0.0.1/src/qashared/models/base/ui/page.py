class Page(object):
    def __init__(self, page, base_url):
        self.base_url = base_url
        self.page = page

    def navigate(self):
        self.page.goto(self.base_url)
