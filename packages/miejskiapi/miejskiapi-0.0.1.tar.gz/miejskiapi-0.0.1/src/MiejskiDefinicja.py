import datetime
import json

class Definicja:
    slowo : str = ""
    ocena : int = 0
    definicja : str = ""
    dialog : list[str] = []
    tags : list[str] = []
    author : str = ""
    data : datetime.date = datetime.date.today()
    hour : datetime.time = datetime.time(0, 0, 0)
    url : str = ""
    iddef : int = 0

    def __init__(self, slowo, ocena, definicja, dialog, tags, author, data, hour, url, iddef):
        self.slowo : str = slowo
        self.ocena : int = ocena
        self.definicja : str = definicja
        self.dialog : list[str] = dialog
        self.tags : list[str] = tags
        self.author : str = author
        self.data : datetime.date = data 
        self.hour : datetime.time = hour
        self.url : str = url
        self.iddef : int = iddef

    def toJson(self):
        js = {}
        js["slowo"] = self.slowo
        js["ocena"] = self.ocena
        js["definicja"] = self.definicja
        js["dialog"] = self.dialog
        js["tags"] = self.tags
        js["author"] = self.author
        js["data"] = str(self.data.year) + "." + str(self.data.month) + "." + str(self.data.day)
        js["hour"] = str(self.hour.hour) + ":" + str(self.hour.minute) + ":" + str(self.hour.second)
        js["url"] = str(self.url)
        js["iddef"] = self.iddef
        return js

    def fromJson(self, js):
        self.slowo = js["slowo"]
        self.ocena = js["ocena"]
        self.definicja = js["definicja"]
        self.dialog = js["dialog"]
        self.tags = js["tags"]
        self.author = js["author"]
        self.data = datetime.date(int(js["data"].split(".")[0]), int(js["data"].split(".")[1]), int(js["data"].split(".")[2]))
        try:
            self.hour = datetime.time(int(js["hour"].split(":")[0]), int(js["hour"].split(":")[1]), int(js["hour"].split(":")[2]))
        except:
            self.hour = datetime.time(0, 0, 0)
        self.url = js["url"]
        self.iddef = js["iddef"]

    def __str__(self):
        return json.dumps(self.toJson())
    
    def __repr__(self):
        return json.dumps(self.toJson())
    
    def __eq__(self, other):
        return self.iddef == other.iddef
    
    def __ne__(self, other):
        return self.iddef != other.iddef
    
    def __lt__(self, other):
        return self.iddef < other.iddef
    
    def __gt__(self, other):
        return self.iddef > other.iddef
    
    def __le__(self, other):
        return self.iddef <= other.iddef
    
    def __ge__(self, other):
        return self.iddef >= other.iddef
    
    def __hash__(self):
        return self.iddef