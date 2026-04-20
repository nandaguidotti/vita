from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

USERS_HASHED = {
    "guidotti@usp.br": "$pbkdf2-sha256$29000$9T5HyJkzJsS4N8b4X0updQ$nMCqAc0UcUFMnPGoz3uWQGjZKbl1gtv/ddcAy6qdxfA",
}

def check_credentials(username: str, password: str) -> bool:
    hashed = USERS_HASHED.get(username)
    return bool(hashed and pwd_context.verify(password, hashed))

