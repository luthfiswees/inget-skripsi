from mongoengine import *

class User(Document):
    message_id = IntField(required=True)
    state = StringField(max_length=4)
