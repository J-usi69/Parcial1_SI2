from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db import get_db

SECRET_KEY = "Fase1_Auth_Secret_No_En_Prod"
ALGORITHM = "HS256"

# Puesta en marcha oficial de passlib bajo la capa de Auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class AuthService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=60))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
        
    def decode_access_token(self, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            return None

    def get_effective_permissions(self, db, usuario_id: int) -> list[str]:
        # ORM Maestro: Acorta y compila los permisos activos que subyacen debajo de Múltiples Roles
        from models.permiso import Permiso
        from models.rol_permiso import RolPermiso
        from models.rol_usuario import RolUsuario
        
        permisos = db.query(Permiso.nombre)\
            .join(RolPermiso, Permiso.id == RolPermiso.permiso_id)\
            .join(RolUsuario, RolPermiso.rol_id == RolUsuario.rol_id)\
            .filter(RolUsuario.usuario_id == usuario_id)\
            .filter(RolPermiso.vigente == True)\
            .distinct().all()
            
        return [p[0] for p in permisos]

def auth_service_dep():
    return AuthService()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    auth_svc: AuthService = Depends(auth_service_dep)
):
    token = credentials.credentials
    payload = auth_svc.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token no decodificable o expirado.")
        
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(status_code=401, detail="Token inválido (Sin Subject).")
        
    from models.usuario import Usuario
    user = db.query(Usuario).filter(Usuario.id == int(user_id_str)).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado.")
        
    if not user.is_active:
        raise HTTPException(status_code=401, detail="El usuario está inactivo o bloqueado.")
        
    return user

def require_permissions(required_permissions: list[str]):
    def permission_checker(
        current_user = Depends(get_current_user),
        db: Session = Depends(get_db),
        auth_svc: AuthService = Depends(auth_service_dep),
    ):
        efectivos = auth_svc.get_effective_permissions(db, current_user.id)
        
        for req in required_permissions:
            if req not in efectivos:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail=f"Acceso Denegado. Se requiere el permiso: {req}"
                )
        return current_user
        
    return permission_checker
