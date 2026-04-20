# common/security.py
import os, time
from typing import List

import jwt  # PyJWT
from jwt import ExpiredSignatureError, InvalidTokenError

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes

from backend.common.auth_users import check_credentials

# ======= CONFIG =======
JWT_SECRET = os.getenv("VITA_JWT_SECRET", "troca_isto_por_um_segredo_forte")
JWT_ALG = "HS256"
JWT_TTL = 60 * 60  # 1h

OAUTH_SCOPES = {
    "read":  "Read-only access",
    "write": "Write access",
    "admin": "Admin operations",
}

USER_SCOPES = {
    "guidotti@usp.br": ["read", "write", "admin"],
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes=OAUTH_SCOPES,
)

# ======= JWT helpers =======
def issue_token(username: str, scopes: List[str]) -> str:
    now = int(time.time())
    payload = {"sub": username, "scopes": scopes, "iat": now, "exp": now + JWT_TTL}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ======= Login endpoint handler =======
def login_handler(form: OAuth2PasswordRequestForm = Depends()):
    if not check_credentials(form.username, form.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    scopes = USER_SCOPES.get(form.username, ["read"])
    token = issue_token(form.username, scopes)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": JWT_TTL,
        "scopes": scopes,
    }

# ======= Dependency p/ rotas =======
def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)) -> str:
    payload = decode_token(token)
    user = payload.get("sub")
    token_scopes = payload.get("scopes", [])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    for s in security_scopes.scopes:
        if s not in token_scopes:
            raise HTTPException(status_code=403, detail=f"Missing scope: {s}")
    return user

# atalhos
secure_read  = Security(get_current_user, scopes=["read"])
secure_write = Security(get_current_user, scopes=["write"])
secure_admin = Security(get_current_user, scopes=["admin"])
