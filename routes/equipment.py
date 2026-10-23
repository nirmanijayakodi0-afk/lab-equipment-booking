
"""Equipment catalogue and management routes."""

from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from extensions import db
from models import Equipment

equipment_bp = Blueprint("equipment", __name__, url_prefix="/equipment")


def staff_required(view):
    """Allow access only to authenticated staff members."""

    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if current_user.role != "staff":
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view


@equipment_bp.route("/")
@login_required
def list_equipment():
    selected_category = request.args.get("category", "").strip()

    query = select(Equipment).order_by(Equipment.name)

    if selected_category:
        query = query.where(Equipment.category == selected_category)

    equipment_items = db.session.scalars(query).all()

    categories = db.session.scalars(
        select(Equipment.category).distinct().order_by(Equipment.category)
    ).all()

    return render_template(
        "equipment.html",
        equipment=equipment_items,
        categories=categories,
        selected_category=selected_category,
    )


@equipment_bp.route("/add", methods=["GET", "POST"])
@staff_required
def add_equipment():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "Available").strip()

        if not name or not category:
            flash("Equipment name and category are required.", "danger")
        elif status not in {"Available", "Out of service"}:
            flash("Please choose a valid equipment status.", "danger")
        else:
            item = Equipment(
                name=name,
                category=category,
                description=description,
                status=status,
            )
            db.session.add(item)
            db.session.commit()

            flash("Equipment added successfully.", "success")
            return redirect(url_for("equipment.list_equipment"))

    return render_template("equipment_form.html", item=None)


@equipment_bp.route("/<int:equipment_id>/edit", methods=["GET", "POST"])
@staff_required
def edit_equipment(equipment_id):
    item = db.session.get(Equipment, equipment_id)

    if item is None:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "").strip()

        if not name or not category:
            flash("Equipment name and category are required.", "danger")
        elif status not in {"Available", "Out of service"}:
            flash("Please choose a valid equipment status.", "danger")
        else:
            item.name = name
            item.category = category
            item.description = description
            item.status = status

            db.session.commit()
            flash("Equipment updated successfully.", "success")
            return redirect(url_for("equipment.list_equipment"))

    return render_template("equipment_form.html", item=item)


@equipment_bp.route("/<int:equipment_id>/delete", methods=["POST"])
@staff_required
def delete_equipment(equipment_id):
    item = db.session.get(Equipment, equipment_id)

    if item is None:
        abort(404)

    if item.bookings:
        flash(
            "This equipment has booking records and cannot be deleted.",
            "warning",
        )
        return redirect(url_for("equipment.list_equipment"))

    db.session.delete(item)
    db.session.commit()

    flash("Equipment deleted successfully.", "success")
    return redirect(url_for("equipment.list_equipment"))
