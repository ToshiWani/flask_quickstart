from flask import Flask, render_template, __version__
from flask_pymongo import PyMongo
import sys

app = Flask(__name__)
app.config.from_object('isr_rotation.config')
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    dogs = mongo.db.dogs.find()
    count = dogs.count()
    if count < 1:
        mongo.db.dogs.insert_many([
            {'name': 'Bella', 'age': 1},
            {'name': 'Lucy', 'age': 5},
            {'name': 'Daisy', 'age': 10}
        ])

    versions = f'Python {sys.version.title()} | Flask {__version__}'

    return render_template('index.html', count=count, dogs=dogs, versions=versions)


if __name__ == '__main__':
    app.run()
