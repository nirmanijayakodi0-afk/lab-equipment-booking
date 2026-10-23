
"""Student booking request and history routes."""

from datetime import date, datetime, time, timedelta

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import select

from extensions import db
from models import Booking, Equipment

bookings_bp = Blueprint("bookings", __name__, url_prefix="/bookings")


def has_booking_conflict(
    equipment_id,
    booking_date,
    start_time,
    end_time,
    exclude_booking_id=None,
):
    """Check for overlapping pending or approved bookings."""

    statement = select(Booking.id).where(
        Booking.equipment_id == equipment_id,
        Booking.booking_date == booking_date,
        Booking.status.in_(["Pending", "Approved"]),
        Booking.start_time < end_time,
        Booking.end_time > start_time,
    )

    if exclude_booking_id is not None:
        statement = statement.where(Booking.id != exclude_booking_id)

    return db.session.scalar(statement) is not None


def render_booking_form(equipment_items, selected_equipment_id=""):
    """Render the booking form with the selected equipment and today's date."""

    return render_template(
        "booking_form.html",
        equipment=equipment_items,
        selected_equipment_id=str(selected_equipment_id),
        today=date.today().isoformat(),
    )


@bookings_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_booking():
    """Display the booking form and process student booking requests."""

    if current_user.role != "student":
        abort(403)

    equipment_items = db.session.scalars(
        select(Equipment).order_by(Equipment.name)
    ).all()

    if request.method == "GET":
        selected_equipment_id = request.args.get("equipment_id", "")

        # Only preselect a valid equipment ID.
        if selected_equipment_id:
            try:
                equipment_id = int(selected_equipment_id)
                selected_item = db.session.get(Equipment, equipment_id)

                if selected_item is None:
                    selected_equipment_id = ""
            except (ValueError, TypeError):
                selected_equipment_id = ""

        return render_booking_form(
            equipment_items,
            selected_equipment_id,
        )

    selected_equipment_id = request.form.get("equipment_id", "").strip()
    booking_date_value = request.form.get("booking_date", "").strip()
    start_time_value = request.form.get("start_time", "").strip()
    end_time_value = request.form.get("end_time", "").strip()

    try:
        equipment_id = int(selected_equipment_id)
        booking_date = date.fromisoformat(booking_date_value)
        start_time = time.fromisoformat(start_time_value)
        end_time = time.fromisoformat(end_time_value)
    except (ValueError, TypeError):
        flash("Please enter valid equipment, date, and times.", "danger")
        return render_booking_form(
            equipment_items,
            selected_equipment_id,
        )

    # HTML time inputs should provide whole-minute values.
    if start_time.second or start_time.microsecond:
        flash("Please enter a valid start time.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    if end_time.second or end_time.microsecond:
        flash("Please enter a valid end time.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    item = db.session.get(Equipment, equipment_id)

    if item is None:
        flash("The selected equipment does not exist.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    if item.status != "Available":
        flash("This equipment is currently out of service.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    now = datetime.now()

    if booking_date < now.date():
        flash("You cannot book equipment for a past date.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    start_datetime = datetime.combine(booking_date, start_time)
    end_datetime = datetime.combine(booking_date, end_time)

    if start_datetime <= now:
        flash("The booking start time must be in the future.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    if end_time <= start_time:
        flash("The end time must be later than the start time.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    duration = end_datetime - start_datetime

    if duration < timedelta(minutes=30):
        flash("Bookings must be at least 30 minutes long.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    if duration > timedelta(hours=4):
        flash("Bookings cannot exceed 4 hours.", "danger")
        return render_booking_form(equipment_items, selected_equipment_id)

    if has_booking_conflict(
        equipment_id,
        booking_date,
        start_time,
        end_time,
    ):
        flash(
            "This equipment already has an overlapping pending "
            "or approved booking.",
            "danger",
        )
        return render_booking_form(equipment_items, selected_equipment_id)

    booking = Booking(
        student_id=current_user.id,
        equipment_id=equipment_id,
        booking_date=booking_date,
        start_time=start_time,
        end_time=end_time,
        status="Pending",
    )

    db.session.add(booking)
    db.session.commit()

    flash("Booking request submitted for staff approval.", "success")
    return redirect(url_for("bookings.my_bookings"))


@bookings_bp.route("/mine")
@login_required
def my_bookings():
    """Show the current student's booking history."""

    if current_user.role != "student":
        abort(403)

    statement = (
        select(Booking)
        .where(Booking.student_id == current_user.id)
        .order_by(
            Booking.booking_date.desc(),
            Booking.start_time.desc(),
        )
    )

    user_bookings = db.session.scalars(statement).all()

    return render_template(
        "my_bookings.html",
        bookings=user_bookings,
    )
