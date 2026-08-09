import os
from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from ml_utils import predict_risk


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "development-secret-key")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not configured")

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


class InventoryBatch(db.Model):
    __tablename__ = "inventory_batches"

    batch_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(100), nullable=False)
    quantity_remaining = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    avg_daily_sale = db.Column(db.Float, nullable=False)


class ExpiryAlert(db.Model):
    __tablename__ = "expiry_alerts"

    alert_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(
        db.Integer,
        db.ForeignKey("inventory_batches.batch_id"),
        nullable=False
    )
    risk_flag = db.Column(db.Integer, nullable=False)
    prediction_date = db.Column(db.Date, nullable=False)


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


@app.route("/expiry_results")
def expiry_results():
    results = (
        db.session.query(
            InventoryBatch.medicine_name,
            ExpiryAlert.risk_flag,
            ExpiryAlert.prediction_date
        )
        .join(
            ExpiryAlert,
            InventoryBatch.batch_id == ExpiryAlert.batch_id
        )
        .order_by(ExpiryAlert.prediction_date.desc())
        .all()
    )

    return render_template(
        "expiry_results.html",
        results=results,
        params=params
    )


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


@app.route("/check_expiry")
def check_expiry():
    batches = InventoryBatch.query.all()

    for batch in batches:
        risk_value = predict_risk(
            batch.quantity_remaining,
            batch.expiry_date,
            batch.avg_daily_sale
        )

        alert = ExpiryAlert.query.filter_by(
            batch_id=batch.batch_id
        ).first()

        if alert:
            alert.risk_flag = risk_value
            alert.prediction_date = date.today()
        else:
            db.session.add(
                ExpiryAlert(
                    batch_id=batch.batch_id,
                    risk_flag=risk_value,
                    prediction_date=date.today()
                )
            )

    db.session.commit()

    flash("Expiry Risk Prediction Completed", "success")

    return redirect("/expiry_results")


@app.route("/add_inventory", methods=["POST"])
def add_inventory():
    try:
        quantity = int(request.form.get("quantity", 0))
        avg_sale = float(request.form.get("avg_sale", 0))
        expiry_date = datetime.strptime(
            request.form.get("expiry_date"),
            "%Y-%m-%d"
        ).date()

        if quantity < 0 or avg_sale < 0:
            raise ValueError

        batch = InventoryBatch(
            medicine_name=request.form.get(
                "medicine_name",
                ""
            ).strip(),
            quantity_remaining=quantity,
            expiry_date=expiry_date,
            avg_daily_sale=avg_sale
        )

        db.session.add(batch)
        db.session.flush()

        risk_value = predict_risk(
            quantity,
            expiry_date,
            avg_sale
        )

        db.session.add(
            ExpiryAlert(
                batch_id=batch.batch_id,
                risk_flag=risk_value,
                prediction_date=date.today()
            )
        )

        db.session.commit()

        flash(
            "Inventory added & risk predicted automatically",
            "success"
        )

    except (ValueError, TypeError):
        db.session.rollback()
        flash("Invalid inventory data", "danger")

    return redirect("/")


@app.route("/inventory")
def inventory_page():
    return render_template(
        "add_inventory.html",
        params=params
    )


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)