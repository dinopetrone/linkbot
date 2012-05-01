import json
from linkbot.lib import pinboard
from linkbot.models import LinkCollection
from linkbot.models import Link

pinboard_cfg = None

try:
    with open("pinboard.cfg") as cfg:
        pinboard_cfg = json.loads(cfg.read())
except IOError:
    print("Unable to load pinboard.cfg")


class LinkData(object):
    def __init__(self):
        username = pinboard_cfg['username']
        password = pinboard_cfg['password']

        self.pinboard = pinboard.open(username, password)

    def recent(self, count=5):
        posts = self.pinboard.posts(count=count)
        collection = LinkCollection()

        for post in posts:
            link = Link()
            link.url = post['href']
            link.description = post['description']
            link.tags = post['tags']
            collection.add_link(link)
        
        return collection

    def get_links_with_tag(self, tag):
        posts = self.pinboard.posts(tag=tag)
        collection = LinkCollection()

        for post in posts:
            link = Link()
            link.url = post['href']
            link.description = post['description']
            link.tags = post['tags']
            collection.add_link(link)

        return collection

    def add_link(self, url, tags):
        self.pinboard.add(url=url, description="", tags=tags)
