import datetime
from demo import db


class Server(db.Document):
    last_checkin = db.DateTimeField(default=datetime.datetime.now,
                                    required=True)
    servername = db.StringField(verbose_name='Server Name',
                                max_length=32,
                                required=True)

class MongoHealthHack(db.Document):
    check_time = db.DateTimeField(default=datetime.datetime.now,
                                  required=True)
