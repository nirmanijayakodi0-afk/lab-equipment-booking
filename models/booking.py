
from extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    equipment_id = db.Column(
        db.Integer,
        db.ForeignKey("equipment.id"),
        nullable=False,
    )

    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending",
    )
    rejection_reason = db.Column(db.String(250), nullable=True)

    student = db.relationship(
        "User",
        back_populates="bookings",
    )
    equipment = db.relationship(
        "Equipment",
        back_populates="bookings",
    )
