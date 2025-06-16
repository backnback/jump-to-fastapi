from passlib.context import CryptContext
from domain.user.user_schema import UserCreate
from models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, or_


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                       password=pwd_context.hash(user_create.password1),
                       email=user_create.email)
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    stmt = select(User).where(
        or_(
            User.username == user_create.username,
            User.email == user_create.email
        )
    )
    return db.scalar(stmt)


def get_user(db: Session, username: str):
    stmt = select(User).where(User.username == username)
    return db.scalar(stmt)