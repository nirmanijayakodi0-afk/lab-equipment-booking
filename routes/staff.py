
"""Staff booking review routes."""

from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from extensions import db
from models import Booking

staff_bp = Blueprint("staff", __name__, url_prefix="/staff")


def staff_required(view):
    """Restrict a route to authenticated staff members."""

    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if current_user.role != "staff":
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view


@staff_bp.route("/dashboard")
@staff_required
def dashboard():
    statement = select(Booking).order_by(
        Booking.booking_date,
        Booking.start_time,
    )
    all_bookings = db.session.scalars(statement).all()

    return render_template("staff_dashboard.html", bookings=all_bookings)


@staff_bp.route("/bookings/<int:booking_id>/review", methods=["POST"])
@staff_required
def review_booking(booking_id):
    booking = db.session.get(Booking, booking_id)

    if booking is None:
        abort(404)

    if booking.status != "Pending":
        flash("This booking has already been reviewed.", "warning")
        return redirect(url_for("staff.dashboard"))

    decision = request.form.get("decision", "").strip()

    if decision not in {"Approved", "Rejected"}:
        abort(400)

    if decision == "Approved":
        if booking.equipment.status != "Available":
            flash(
                "This equipment is out of service. The request was not approved.",
                "danger",
            )
            return redirect(url_for("staff.dashboard"))

        conflict_statement = select(Booking.id).where(
            Booking.id != booking.id,
            Booking.equipment_id == booking.equipment_id,
            Booking.booking_date == booking.booking_date,
            Booking.status == "Approved",
            Booking.start_time < booking.end_time,
            Booking.end_time > booking.start_time,
        )

        if db.session.scalar(conflict_statement) is not None:
            flash(
                "Another booking has already been approved for this time.",
                "danger",
            )
            return redirect(url_for("staff.dashboard"))

        booking.status = "Approved"
        booking.rejection_reason = None
        flash("Booking approved successfully.", "success")

    else:
        reason = request.form.get("rejection_reason", "").strip()
        booking.status = "Rejected"
        booking.rejection_reason = reason or "Rejected by lab staff"
        flash("Booking rejected.", "success")

    db.session.commit()
    return redirect(url_for("staff.dashboard"))
