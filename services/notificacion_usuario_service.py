from sqlalchemy.orm import Session
from schemas.notificacion_usuario import NotificacionUsuarioCreate
from repositories.notificacion_usuario_repository import NotificacionUsuarioRepository
from repositories.notificacion_repository import NotificacionRepository
from repositories.usuario_repository import UsuarioRepository

class NotificacionUsuarioService:
    def __init__(
        self, 
        repository: NotificacionUsuarioRepository, 
        notif_repo: NotificacionRepository,
        usr_repo: UsuarioRepository
    ):
        self.repository = repository
        self.notif_repo = notif_repo
        self.usr_repo = usr_repo

    def asignar_destinatario(self, db: Session, data: NotificacionUsuarioCreate):
        notif = self.notif_repo.get_by_id(db, data.notificacion_id)
        if not notif:
            raise ValueError("Error de Relación: La notificación universal que intentas asignar a la bandeja no existe.")
            
        receptor = self.usr_repo.get_by_id(db, data.usuario_id)
        if not receptor:
            raise ValueError("Error de Relación: El usuario receptor destino no consta en el ecosistema.")
            
        existing = self.repository.get_by_user_and_notif(db, data.usuario_id, data.notificacion_id)
        if existing:
            raise ValueError("Restricción Superada: Este mensaje particular ya se encuentra alojado en la bandeja del usuario.")
            
        return self.repository.create(db, data)

    def marcar_leido(self, db: Session, usuario_id: int, notificacion_id: int):
        existing = self.repository.get_by_user_and_notif(db, usuario_id, notificacion_id)
        if not existing:
            raise ValueError("No se puede marcar como leída una notificación que no figura en tu bandeja.")
        return self.repository.update_leido(db, usuario_id, notificacion_id)

    def get_mis_notificaciones(self, db: Session, usuario_id: int):
        return self.repository.get_by_usuario(db, usuario_id)
