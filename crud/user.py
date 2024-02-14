from models import User
from sqlmodel import Session


def create_user(
    session: Session,
    password: str,
    first_name: str,
    last_name: str,
    email: str,
    age: int,
    phone_number: str,
):
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        age=age,
        phone_number=phone_number,
        password=password,
    )

    session.add(user)
    session.commit()
