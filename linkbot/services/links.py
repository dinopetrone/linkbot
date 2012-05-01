class LinkService(object):
    
    def __init__(self, dao):
        self.dao = dao

    def recent(self, count=5):
        """
        Fetch the N most recent links
        """
        return self.dao.recent(count)

    def get_tags(self):
        """
        Fetch all of the tags with how many times 
        it has been used
        """
        return self.dao.get_tags()

    def get_links_with_tag(self, tag=None):
        """
        Fetch links containing tags
        """
        return self.dao.get_links_with_tag(tag)

    def add_link(self, url, tags=None):
        """
        Save link with tags
        """
        self.dao.add_link(url, tags)