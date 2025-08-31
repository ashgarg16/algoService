import bcrypt
import secrets
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User

SECRET_KEY = "CHANGE_ME_TO_RANDOM_SECRET"  # store in env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def register_user(self, email: str, password: str, role: str = "user") -> bool:
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        new_user = User(
            email=email.lower(),
            password_hash=hashed_pw.decode("utf-8"),
            role=role,
            created_at=datetime.utcnow(),
        )
        try:
            self.db.add(new_user)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def delete_user(self, requester_email: str, target_email: str) -> bool:
        requester = self.db.query(User).filter(User.email == requester_email).first()
        if not requester or requester.role != "admin":
            return False
        target = self.db.query(User).filter(User.email == target_email).first()
        if not target:
            return False
        self.db.delete(target)
        self.db.commit()
        return True

    def login_user(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email.lower()).first()
        if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None
        access_token = self.create_access_token({"sub": user.email, "role": user.role})
        refresh_token = self.create_refresh_token({"sub": user.email})
        return {"access_token": access_token, "refresh_token": refresh_token}

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def refresh_access_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "refresh":
                return None
            email = payload.get("sub")
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return None
            return self.create_access_token({"sub": user.email, "role": user.role})
        except JWTError:
            return None

    def generate_reset_token(self, email: str) -> str:
        user = self.db.query(User).filter(User.email == email.lower()).first()
        if not user:
            return None
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        self.db.commit()
        return token

    def reset_password(self, token: str, new_password: str) -> bool:
        user = self.db.query(User).filter(User.reset_token == token).first()
        if not user:
            return False
        hashed_pw = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))       