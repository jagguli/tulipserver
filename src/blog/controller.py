from aioweb.controller import Controller
from datetime import datetime


class HomeController(Controller):
    def __init__(self, db, post_source='post', comment_source='comment', 
                 **kwargs):
        super(HomeController, self).__init__(db, **kwargs)
        self.blog_source = post_source
        self.comment_source = comment_source

    def store_query(self, query):
        query['datetime'] = datetime.now()
        return query

    def new_post(self, model):
        assert 'title' in model.data
        assert 'date' in model.data
        assert 'body' in model.data
        r = yield from self.db.put(model.data)
        return r.ok == True
