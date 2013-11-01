from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB':'db',
                                  'host':'mongodb://user:ChangeMe@mongodb/db',
                                  'replicaSet':'RS'}
app.config['SECRET_KEY'] = 'thisisasecret'

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from demo.views import health
    app.register_blueprint(health)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
