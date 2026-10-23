
"""Create two staff accounts for the Lab Equipment Booking System."""

from getpass import getpass

from sqlalchemy import func, select

from app import create_app
from extensions import db
from models import User


def create_staff_account(username, email, password):
    """Create a staff account if its username and email are unused."""

    existing_user = db.session.scalar(
        select(User).where(
            (func.lower(User.username) == username.lower())
            | (func.lower(User.email) == email.lower())
        )
    )

    if existing_user:
        print(f"Skipped {username}: username or email already exists.")
        return

    staff = User(
        username=username,
        email=email,
        role="staff",
    )
    staff.set_password(password)

    db.session.add(staff)
    db.session.commit()

    print(f"Created staff account: {username}")


def main():
    app = create_app()

    with app.app_context():
        accounts = [
            ("staff1", "staff1@lab.local"),
            ("staff2", "staff2@lab.local"),
        ]

        for username, email in accounts:
            print(f"\nSet password for {username} ({email})")

            password = getpass("Password (minimum 8 characters): ")
            confirm_password = getpass("Confirm password: ")

            if len(password) < 8:
                print("Password must contain at least 8 characters.")
                continue

            if password != confirm_password:
                print("Passwords do not match. Account not created.")
                continue

            create_staff_account(username, email, password)


if __name__ == "__main__":
    main()
