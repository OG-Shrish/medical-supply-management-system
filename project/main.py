import os
from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "development-secret-key")

database_url = os.getenv("DATABASE_URL", "sqlite:///medical.db")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 300
}

db = SQLAlchemy(app)

params = {}


class Medicines(db.Model):
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    medicines = db.Column(db.String(500), nullable=False)
    products = db.Column(db.String(500))
    amount = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)


class Posts(db.Model):
    __tablename__ = "posts"

    mid = db.Column(db.Integer, primary_key=True)
    medical_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)


class Addmp(db.Model):
    __tablename__ = "addmp"

    sno = db.Column(db.Integer, primary_key=True)
    medicine = db.Column(db.String(500), nullable=False)


class Addpd(db.Model):
    __tablename__ = "addpd"

    sno = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)



@app.route("/")
def home():
    return render_template("index.html", params=params)


@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        post = Posts(
            medical_name=request.form.get("medical_name", "").strip(),
            owner_name=request.form.get("owner_name", "").strip(),
            phone_no=request.form.get("phone_no", "").strip(),
            address=request.form.get("address", "").strip()
        )

        db.session.add(post)
        db.session.commit()

        flash("Medical info added", "success")

    return render_template("insert.html", params=params)


@app.route("/medicines", methods=["GET", "POST"])
def medicines():
    if request.method == "POST":
        entry = Medicines(
            mid=request.form.get("mid", "").strip(),
            name=request.form.get("name", "").strip(),
            medicines=request.form.get("medicines", "").strip(),
            products=request.form.get("products", "").strip(),
            email=request.form.get("email", "").strip(),
            amount=int(request.form.get("amount", 0))
        )

        db.session.add(entry)
        db.session.commit()

        flash("Order placed", "success")

    return render_template("medicine.html", params=params)


@app.route("/list")
def list_orders():
    posts = Medicines.query.order_by(Medicines.id.desc()).all()

    return render_template(
        "post.html",
        posts=posts,
        params=params
    )


@app.route("/deletemp/<int:id>")
def deletemp(id):
    post = db.session.get(Medicines, id)

    if post:
        db.session.delete(post)
        db.session.commit()

    return redirect("/list")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form.get("search", "").strip()

        medicine = Addmp.query.filter_by(medicine=name).first()
        product = Addpd.query.filter_by(product=name).first()

        if medicine or product:
            flash("Item Available", "success")
        else:
            flash("Item Not Found", "danger")

    return render_template("search.html", params=params)


@app.route("/addmp", methods=["POST"])
def addmp():
    medicine = request.form.get("medicine", "").strip()

    if medicine:
        db.session.add(Addmp(medicine=medicine))
        db.session.commit()

    return redirect("/items")


@app.route("/addpd", methods=["POST"])
def addpd():
    product = request.form.get("product", "").strip()

    if product:
        db.session.add(Addpd(product=product))
        db.session.commit()

    return redirect("/items2")


@app.route("/items")
def items():
    data = Addmp.query.order_by(Addmp.sno.desc()).all()

    return render_template(
        "items.html",
        data=data,
        params=params
    )


@app.route("/items2")
def items2():
    data = Addpd.query.order_by(Addpd.sno.desc()).all()

    return render_template(
        "items2.html",
        data=data,
        params=params
    )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)