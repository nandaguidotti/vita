from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from backend.common.auth_users import check_credentials  # Importa do seu arquivo

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if check_credentials(credentials.username, credentials.password):
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credential",
        headers={"WWW-Authenticate": "Basic"},
    )