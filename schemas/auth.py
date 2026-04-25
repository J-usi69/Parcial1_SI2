from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    usuario_id: Optional[int] = None
    permisos_efectivos: List[str] = []

class LoginRequest(BaseModel):
    email: str
    password: str
