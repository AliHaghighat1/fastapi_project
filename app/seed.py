from app.database import SessionLocal
from app.models.user import User


def seed_users():
    db = SessionLocal()

    fake_users = [
        User(first_name="Ali", last_name="Mohammadi", gender="male", email="ali1@example.com", balance=120.50, is_active=True),
        User(first_name="Sara", last_name="Ahmadi", gender="female", email="sara@example.com", balance=250.00, is_active=True),
        User(first_name="Reza", last_name="Karimi", gender="male", email="reza@example.com", balance=80.75, is_active=False),
        User(first_name="Neda", last_name="Hosseini", gender="female", email="neda@example.com", balance=540.10, is_active=True),
        User(first_name="Amir", last_name="Rahimi", gender="male", email="amir@example.com", balance=15.00, is_active=True),
        User(first_name="Leila", last_name="Shirazi", gender="female", email="leila@example.com", balance=999.99, is_active=True),
        User(first_name="Hossein", last_name="Fathi", gender="male", email="hossein@example.com", balance=300.30, is_active=False),
        User(first_name="Zahra", last_name="Kazemi", gender="female", email="zahra@example.com", balance=45.20, is_active=True),
        User(first_name="Mehdi", last_name="Najafi", gender="male", email="mehdi@example.com", balance=670.00, is_active=True),
        User(first_name="Elham", last_name="Ghasemi", gender="female", email="elham@example.com", balance=10.00, is_active=False),
    ]

    db.add_all(fake_users)
    db.commit()
    db.close()

    print("Seed completed successfully!")


if __name__ == "__main__":
    seed_users()