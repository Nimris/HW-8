
from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateTimeField, IntField, ListField, StringField, ReferenceField


class Authors(Document):
    # id = IntField(primary_key=True)
    fullname = StringField()
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()
    
class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField("Authors")
    quote = StringField()
    
