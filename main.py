import random
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy
from os import environ as env

project_dir = os.path.dirname(os.path.abspath(__file__))
database = env.get("EVENTS_DB_URI", "sqlite:///{}".format(os.path.join(project_dir, "eventdatabase.db")))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database

db = SQLAlchemy(app)

class Event(db.Model):
    name = db.Column(db.String(200), unique=False, nullable=False, primary_key=True)
    completed = db.Column(db.Boolean, unique=False, nullable=False)
    def __repr__(self):
        return "".format(self.name)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        event = Event(name=request.form.get("name"), completed=False)
        db.session.add(event)
        db.session.commit()
    events = Event.query.filter_by(completed=False)
    return render_template("home.html", events=events)

@app.route("/random", methods=["GET", "POST"])
def rand():
    events = Event.query.filter_by(completed=False).all()
    event = random.choice(events)
    return render_template("random.html", event=event)

@app.route("/update", methods=["POST"])
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    event = Event.query.filter_by(name=oldname).first()
    event.name = newname
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    event = Event.query.filter_by(name=name).first()
    db.session.delete(event)
    db.session.commit()
    return redirect("/")

@app.route("/complete", methods=["POST"])
def complete():
    name = request.form.get("name")
    event = Event.query.filter_by(name=name).first()
    if event:
        event.completed = True
        db.session.commit()
    return redirect("/")

@app.route("/completed", methods=["GET", "POST"])
def completed():
    if request.form:
        event = Event.query.filter_by(name=request.form.get("name"))
        db.session.delete(event)
        db.sesion.commit()
    events = Event.query.filter_by(completed=True)
    return render_template("completed.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)
