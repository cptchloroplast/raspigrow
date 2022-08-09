from secrets import compare_digest
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.settings import Settings

security = HTTPBasic()


def authenitcated(
    creds: HTTPBasicCredentials = Depends(security),
    settings: Settings = Depends(Settings.depends),
):
    if not (
        compare_digest(creds.username, settings.AUTH_USERNAME)
        or compare_digest(creds.password, settings.AUTH_PASSWORD)
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Bad username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return creds.username
