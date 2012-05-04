import os
os.environ['PYTHONPATH'] = '/webroot/djangolasso/lasso'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.utils import timezone
from links.models import Link,Tag
from linkbot.models import LinkCollection
from linkbot.models import Link as LinkbotLink

class LinkData(object):
    
    def __init__(self):
        pass

    def recent(self, count=5):
        links = Link.objects.all()[:count]
        collection = LinkCollection() 

        for item in links:
            link = LinkbotLink()
            link.url = item.url
            collection.add_link(link)

        return collection

    def get_links_with_tag(self, tag):
        tags = Tag.objects.filter(value=tagStr)
        collection = LinkCollection()  
        
        for item in tags:
            link = LinkbotLink()
            link.url = item.link.url
            collection.add_link(link)

        return collection

    def add_link(self, url, description, tags):
        l = Link(url=url,pub_date=timezone.now())
        l.save()
        linkId = l.id

        for tag in tags:
            t = Tag(value=tag,link=l)
            t.save()

    def get_tags(self):
        raise NotImplemented()
