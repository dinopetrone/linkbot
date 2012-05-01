class LinkCollection(object):
    
    def __init__(self, data=[]):
        self.data = data

    def add_link(self, link):
        print(link)
        print(self.data)
        self.data.append(link)

    def __iter__(self):
        data = self.data
        for item in data:
            yield item    

class Link(object):
    
    def __init__(self):
        self.url  = None
        self.description = None
        self.tags = []