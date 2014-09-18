try:
    import models
except ImportError:
    print "execute the contents of this file in your interactive console:"
    print "http://localhost:8000/console"
    raise SystemExit

data_point = models.MyModel(property1="hello", property2="world")
data_point.put()
print "you should now see this data in the response at:"
print "http://localhost:8080/api/mymodel"
