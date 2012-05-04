import json
from linkbot.lib import pinboard
from linkbot.models import LinkCollection
from linkbot.models import Link
from linkbot.models import Tag

pinboard_cfg = None

try:
    with open("pinboard.cfg") as cfg:
        pinboard_cfg = json.loads(cfg.read())
except IOError:
    print("Unable to load pinboard.cfg")


class LinkData(object):
    def __init__(self):
        
        try:
            username = pinboard_cfg['username']
            password = pinboard_cfg['password']
            self.pinboard = pinboard.open(username, password)
        except:
            print("Unable to continue. No pinboard.cfg found")


    def recent(self, count=5):
        posts = self.pinboard.posts(count=count)
        collection = []

        for post in posts:
            link = Link()
            link.url = post['href']
            link.description = post['description']
            link.tags = post['tags']
            collection.append(link)
        
        return collection

    def get_links_with_tag(self, tag):
        posts = self.pinboard.posts(tag=tag)
        collection = []

        for post in posts:
            link = Link()
            link.url = post['href']
            link.description = post['description']
            link.tags = post['tags']
            collection.append(link)

        return collection

    def add_link(self, url, description, tags):
        self.pinboard.add(url=url, description=description, tags=tags)

    def get_tags(self):
        tags = self.pinboard.tags()
        collection = []
        
        for item in tags:
            tag = Tag()
            tag.name = item['name']
            tag.count = item['count']
            collection.append(tag)

        return collection

