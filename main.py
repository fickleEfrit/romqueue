import os
import random

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "eventdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Event(db.Model):
    name = db.Column(db.String(200), unique=False, nullable=False, primary_key=True)

    def __repr__(self):
        return "".format(self.name)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        event = Event(name=request.form.get("name"))
        db.session.add(event)
        db.session.commit()
    events = Event.query.all()
    return render_template("home.html", events=events)

@app.route("/random", methods=["GET", "POST"])
def rand():
    events = Event.query.all()
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

if __name__ == "__main__":
    app.run(debug=True)
