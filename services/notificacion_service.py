from sqlalchemy.orm import Session
from schemas.notificacion import NotificacionCreate
from repositories.notificacion_repository import NotificacionRepository
from repositories.usuario_repository import UsuarioRepository

class NotificacionService:
    def __init__(self, repository: NotificacionRepository, usr_repo: UsuarioRepository):
        self.repository = repository
        self.usr_repo = usr_repo

    def get_notificaciones(self, db: Session):
        return self.repository.get_all(db)

    def get_notificacion_by_id(self, db: Session, notificacion_id: int):
        notificacion = self.repository.get_by_id(db, notificacion_id)
        if not notificacion:
            raise ValueError("Notificación no existente en los registros.")
        return notificacion

    def create_notificacion(self, db: Session, data: NotificacionCreate):
        # Impedimos redactores que no forman parte del sistema organico
        emisor = self.usr_repo.get_by_id(db, data.usuario_id)
        if not emisor:
            raise ValueError("Emisor No Encontrado: El usuario redactor especificado no existe en la base de datos.")
            
        return self.repository.create(db, data)
