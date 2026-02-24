from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from ml_utils import predict_risk
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json
import os

pymysql.install_as_MySQLdb()

with open("config.json","r") as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = "medical"

app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)

# ================= DATABASE MODELS =================

class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.String(50))
    name = db.Column(db.String(100))
    medicines = db.Column(db.String(500))
    products = db.Column(db.String(500))
    amount = db.Column(db.Integer)
    email = db.Column(db.String(50))

class Posts(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    medical_name = db.Column(db.String(100))
    owner_name = db.Column(db.String(100))
    phone_no = db.Column(db.String(20))
    address = db.Column(db.String(50))

class Addmp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    medicine = db.Column(db.String(500))

class Addpd(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200))

# NEW INVENTORY MODEL

class InventoryBatch(db.Model):
    __tablename__ = 'inventory_batches'

    batch_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(100))
    quantity_remaining = db.Column(db.Integer)
    expiry_date = db.Column(db.Date)
    avg_daily_sale = db.Column(db.Float)

class ExpiryAlert(db.Model):
    __tablename__ = 'expiry_alerts'

    alert_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer)
    risk_flag = db.Column(db.Integer)
    prediction_date = db.Column(db.Date)

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html", params=params)

@app.route("/insert", methods=["GET","POST"])
def insert():
    if request.method=="POST":
        post = Posts(
            medical_name=request.form.get("medical_name"),
            owner_name=request.form.get("owner_name"),
            phone_no=request.form.get("phone_no"),
            address=request.form.get("address")
        )
        db.session.add(post)
        db.session.commit()
        flash("Medical info added","success")
    return render_template("insert.html", params=params)

@app.route("/medicines", methods=["GET","POST"])
def medicines():
    if request.method=="POST":
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
        flash("Order placed","success")
    return render_template("medicine.html", params=params)

@app.route("/list")
def list_orders():
    posts = Medicines.query.all()
    return render_template("post.html", posts=posts, params=params)

@app.route("/deletemp/<string:id>")
def deletemp(id):
    post = Medicines.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect("/list")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method=="POST":
        name=request.form.get("search")
        med=Addmp.query.filter_by(medicine=name).first()
        prod=Addpd.query.filter_by(product=name).first()
        if med or prod:
            flash("Item Available","success")
        else:
            flash("Item Not Found","danger")
    return render_template("search.html", params=params)

@app.route("/expiry_results")
def expiry_results():

    results = db.session.query(
        InventoryBatch.medicine_name,
        ExpiryAlert.risk_flag,
        ExpiryAlert.prediction_date
    ).join(
        ExpiryAlert,
        InventoryBatch.batch_id == ExpiryAlert.batch_id
    ).all()

    return render_template("expiry_results.html", results=results, params=params)

@app.route("/addmp", methods=["POST"])
def addmp():
    db.session.add(Addmp(medicine=request.form.get("medicine")))
    db.session.commit()
    return redirect("/items")

@app.route("/addpd", methods=["POST"])
def addpd():
    db.session.add(Addpd(product=request.form.get("product")))
    db.session.commit()
    return redirect("/items2")

@app.route("/items")
def items():
    data = Addmp.query.all()
    return render_template("items.html", data=data, params=params)

@app.route("/items2")
def items2():
    data = Addpd.query.all()
    return render_template("items2.html", data=data, params=params)

# ML ROUTE

@app.route("/check_expiry")
def check_expiry():
    os.system("python expiry_model.py")
    os.system("python predict_expiry.py")
    flash("Expiry Risk Prediction Completed","success")
    return redirect("/")

@app.route("/add_inventory", methods=["POST"])
def add_inventory():

    batch = InventoryBatch(
        medicine_name=request.form.get("medicine_name"),
        quantity_remaining=int(request.form.get("quantity")),
        expiry_date=datetime.strptime(request.form.get("expiry_date"), "%Y-%m-%d"),
        avg_daily_sale=float(request.form.get("avg_sale"))
    )

    db.session.add(batch)
    db.session.commit()

    risk_value = predict_risk(
        batch.quantity_remaining,
        batch.expiry_date,
        batch.avg_daily_sale
    )

    new_alert = ExpiryAlert(
        batch_id=batch.batch_id,
        risk_flag=risk_value,
        prediction_date=datetime.today()
    )

    db.session.add(new_alert)
    db.session.commit()

    flash("Inventory added & risk predicted automatically","success")
    return redirect("/")

@app.route("/inventory")
def inventory_page():
    return render_template("add_inventory.html", params=params)

# ================= RUN =================

if __name__=="__main__":
    app.run(debug=True)