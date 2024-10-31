from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///firstapp.db"
with app.app_context():
    db = SQLAlchemy(app)


class FirstApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")

        if fname and lname and email:
            firstapp = FirstApp(fname=fname, lname=lname, email=email)
            db.session.add(firstapp)
            db.session.commit()

    allpeople = FirstApp.query.all()

    return render_template("index.html", allpeople=allpeople)


@app.route("/home")
def home():
    return "Welcome to the Home Page"


@app.route("/delete/<int:sno>")
def delete(sno):
    # Fetch the person by sno and delete the record
    person_to_delete = FirstApp.query.filter_by(sno=sno).first()
    if person_to_delete:
        db.session.delete(person_to_delete)
        db.session.commit()
    
    # Reassign serial numbers to remaining records
    remaining_people = FirstApp.query.order_by(FirstApp.sno).all()
    for index, person in enumerate(remaining_people):
        person.sno = index + 1  # Assign new serial number in sequence
    db.session.commit()

    # Redirect to the index page to display the updated list
    return redirect("/")

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        if fname and lname and email:
            allpeople = FirstApp.query.filter_by(sno=sno).first()
            allpeople.fname = fname
            allpeople.lname = lname
            allpeople.email = email
            db.session.add(allpeople)
            db.session.commit()
            
        # Redirect to the home page (index) after updating
        return redirect(url_for('index'))

    allpeople = FirstApp.query.filter_by(sno=sno).first()
    return render_template("update.html", allpeople=allpeople)
    

@app.route("/")
def index():
    # Fetch all people from the database
    allpeople = FirstApp.query.all()
    return render_template('index.html', allpeople=allpeople)

if __name__ == "__main__":
    app.run(debug=True)


