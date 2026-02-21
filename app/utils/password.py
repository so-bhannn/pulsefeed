from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(raw_password) -> str:
    hashed = pwd_context.hash(raw_password)
    return hashed

def verify_password(plain, hash) -> bool:
    return pwd_context.verify(plain, hash)