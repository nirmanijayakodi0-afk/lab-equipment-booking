
"""Equipment model for the Lab Equipment Booking System."""

from extensions import db


class Equipment(db.Model):
    """Represent equipment available in the laboratory."""

    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    category = db.Column(
        db.String(50),
        nullable=False,
    )

    description = db.Column(
        db.String(250),
        nullable=False,
        default="",
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Available",
    )

    bookings = db.relationship(
        "Booking",
        back_populates="equipment",
    )

    def __repr__(self):
        """Return a readable representation of equipment."""
        return (
            f"<Equipment {self.id}: {self.name} "
            f"({self.status})>"
        )
