
"""Application setup and homepage dashboard."""

import os

from flask import Flask, render_template
from flask_login import current_user
from sqlalchemy import func, select

from extensions import db, login_manager


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get(
            "SECRET_KEY",
            "local-development-key-change-before-deployment",
        ),
        SQLALCHEMY_DATABASE_URI="sqlite:///booking.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    # Import models so SQLAlchemy knows about their tables.
    import models  # noqa: F401

    # Register application routes.
    from routes.auth import auth_bp
    from routes.bookings import bookings_bp
    from routes.equipment import equipment_bp
    from routes.staff import staff_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(staff_bp)

    from models import Booking, Equipment

    @app.route("/")
    def home():
        # Count all equipment records, including out-of-service items.
        equipment_count = (
            db.session.scalar(
                select(func.count(Equipment.id))
            )
            or 0
        )

        booking_count = 0
        pending_count = 0

        if current_user.is_authenticated:
            if current_user.role == "student":
                booking_count = (
                    db.session.scalar(
                        select(func.count(Booking.id)).where(
                            Booking.student_id == current_user.id
                        )
                    )
                    or 0
                )

            elif current_user.role == "staff":
                pending_count = (
                    db.session.scalar(
                        select(func.count(Booking.id)).where(
                            Booking.status == "Pending"
                        )
                    )
                    or 0
                )

        return render_template(
            "home.html",
            equipment_count=equipment_count,
            booking_count=booking_count,
            pending_count=pending_count,
        )

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
