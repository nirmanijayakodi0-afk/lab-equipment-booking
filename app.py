
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "local-development-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///booking.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), default="")
    status = db.Column(db.String(20), default="Available")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return """
    <h1>Lab Equipment Booking System</h1>
    <p>Your application is running successfully!</p>
    """


if __name__ == "__main__":
    app.run(debug=True)
