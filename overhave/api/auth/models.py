from datetime import datetime

from pydantic.fields import Field
from pydantic.main import BaseModel


class AuthToken(BaseModel):
    """Model for OAuth2 authorization token."""

    access_token: str
    expires_at: datetime
    token_type: str = Field("Bearer", const=True)


class AuthTokenData(BaseModel):
    """Model for OAuth2 authorization token data."""

    username: str


class AuthHeaders(BaseModel):
    """Model for OAuth2 authorization HTTP headers."""

    Authorization: str = Field("Bearer", const=True)


AUTH_HEADERS = AuthHeaders()
