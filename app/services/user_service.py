from slqalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from core.security import hash_password

def get_user_by_email(db:Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password)

    new_user = User(
        name = user.name,
        email = user.email,
        password = hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()