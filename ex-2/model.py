from mongoengine import Document
from mongoengine.fields import StringField, BooleanField

class Contact(Document):
    name = StringField()
    email = StringField()
    is_sent = BooleanField(default=False)
    adress = StringField()
    
    
    