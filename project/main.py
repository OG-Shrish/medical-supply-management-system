from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)


class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    medicines = db.Column(db.String(500), nullable=False)
    products = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mid = db.Column(db.String(120), nullable=False)


class Posts(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    medical_name = db.Column(db.String(80), nullable=False)
    owner_name = db.Column(db.String(200), nullable=False)
    phone_no = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(120), nullable=False)


class Addmp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    medicine = db.Column(db.String(500), nullable=False)


class Addpd(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.String(120), nullable=True)
    action = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(100), nullable=False)


@app.route("/")
def hello():
    return render_template("index.html", params=params)


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session and session['user'] == params['user']:
        posts = Posts.query.all()
        return render_template("dashbord.html", params=params, posts=posts)

    if request.method == "POST":
        username = request.form.get("uname")
        password = request.form.get("password")

        if username == params['user'] and password == params['password']:
            session['user'] = username
            flash("You are Logged in", "primary")
            return redirect("/login")
        else:
            flash("Wrong credentials", "danger")

    return render_template("login.html", params=params)


@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("You are logged out", "primary")
    return redirect("/login")


@app.route("/insert", methods=["GET", "POST"])
def insert():
    if 'user' not in session:
        return redirect("/login")

    if request.method == "POST":
        post = Posts(
            mid=request.form.get("mid"),
            medical_name=request.form.get("medical_name"),
            owner_name=request.form.get("owner_name"),
            phone_no=request.form.get("phone_no"),
            address=request.form.get("address")
        )
        db.session.add(post)
        db.session.commit()
        flash("Medical details added", "success")

    return render_template("insert.html", params=params)


@app.route("/list")
def post():
    if 'user' not in session:
        return redirect("/login")

    posts = Medicines.query.all()
    return render_template("post.html", params=params, posts=posts)


@app.route("/items")
def items():
    if 'user' not in session:
        return redirect("/login")

    posts = Addmp.query.all()
    return render_template("items.html", params=params, posts=posts)


@app.route("/items2")
def items2():
    if 'user' not in session:
        return redirect("/login")

    posts = Addpd.query.all()
    return render_template("items2.html", params=params, posts=posts)


@app.route("/search", methods=["GET", "POST"])
def search():
    if 'user' not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("search")
        med = Addmp.query.filter_by(medicine=name).first()
        prod = Addpd.query.filter_by(product=name).first()

        if med or prod:
            flash("Item is available", "success")
        else:
            flash("Item not available", "danger")

    return render_template("search.html", params=params)


@app.route("/addmp", methods=["POST"])
def addmp():
    if 'user' not in session:
        return redirect("/login")

    med = Addmp(medicine=request.form.get("medicine"))
    db.session.add(med)
    db.session.commit()
    flash("Medicine added", "success")
    return redirect("/search")


@app.route("/addpd", methods=["POST"])
def addpd():
    if 'user' not in session:
        return redirect("/login")

    prod = Addpd(product=request.form.get("product"))
    db.session.add(prod)
    db.session.commit()
    flash("Product added", "success")
    return redirect("/search")


@app.route("/medicines", methods=["GET", "POST"])
def medicine():
    if 'user' not in session:
        return redirect("/login")

    if request.method == "POST":
        entry = Medicines(
            mid=request.form.get("mid"),
            name=request.form.get("name"),
            medicines=request.form.get("medicines"),
            products=request.form.get("products"),
            email=request.form.get("email"),
            amount=request.form.get("amount")
        )
        db.session.add(entry)
        db.session.commit()
        flash("Order placed successfully", "success")

    return render_template("medicine.html", params=params)


@app.route("/sp")
def sp():
    if 'user' not in session:
        return redirect("/login")

    posts = Medicines.query.all()
    return render_template("store.html", params=params, posts=posts)


@app.route("/details")
def details():
    if 'user' not in session:
        return redirect("/login")

    posts = Logs.query.all()
    return render_template("details.html", params=params, posts=posts)


@app.route("/edit/<string:mid>", methods=["GET", "POST"])
def edit(mid):
    if 'user' not in session:
        return redirect("/login")

    post = Posts.query.filter_by(mid=mid).first()
    if not post:
        return redirect("/login")

    if request.method == "POST":
        post.medical_name = request.form.get("medical_name")
        post.owner_name = request.form.get("owner_name")
        post.phone_no = request.form.get("phone_no")
        post.address = request.form.get("address")
        db.session.commit()
        flash("Data updated", "success")
        return redirect("/login")

    return render_template("edit.html", params=params, post=post)


@app.route("/delete/<string:mid>")
def delete(mid):
    if 'user' not in session:
        return redirect("/login")

    post = Posts.query.filter_by(mid=mid).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Deleted successfully", "warning")

    return redirect("/login")


@app.route("/deletemp/<string:id>")
def deletemp(id):
    if 'user' not in session:
        return redirect("/login")

    post = Medicines.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Deleted successfully", "primary")

    return redirect("/list")


app.run(debug=True)
