from google.appengine.ext import ndb
from sys import modules
from inspect import getmembers, isclass


class MyModel(ndb.Model):
    property1 = ndb.StringProperty()
    property2 = ndb.StringProperty()
    owner = ndb.KeyProperty(kind='User')

    class RESTMeta:
        # When a new instance is created, this property will be set to the logged-in user
        user_owner_property = 'owner'


def list_models():
    models = []
    for name, obj in getmembers(modules[__name__]):
        if isclass(obj):
            models.append(name)
    return models
