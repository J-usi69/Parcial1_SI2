from sqlalchemy.orm import Session
from schemas.rol_usuario import RolUsuarioCreate
from repositories.rol_usuario_repository import RolUsuarioRepository

class RolUsuarioService:
    def __init__(self, repository: RolUsuarioRepository):
        self.repository = repository

    def asignar_rol(self, db: Session, data: RolUsuarioCreate):
        existing = self.repository.get_by_user_and_rol(db, data.rol_id, data.usuario_id)
        if existing:
            raise ValueError("Restricción: El rol ya se encuentra asignado de antemano a esta persona.")
        return self.repository.create(db, data)

    def revocar_rol(self, db: Session, rol_id: int, usuario_id: int):
        existing = self.repository.get_by_user_and_rol(db, rol_id, usuario_id)
        if not existing:
            raise ValueError("Petición declinada: El usuario no cuenta con la posesión de este rol, interrupción de desvinculación evitada.")
        return self.repository.delete(db, rol_id, usuario_id)

    def get_roles_by_usuario(self, db: Session, usuario_id: int):
        return self.repository.get_roles_by_user(db, usuario_id)
