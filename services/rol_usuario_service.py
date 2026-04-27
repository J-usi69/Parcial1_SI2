from sqlalchemy.orm import Session
from schemas.rol_usuario import RolUsuarioCreate
from repositories.rol_usuario_repository import RolUsuarioRepository

class RolUsuarioService:
    def __init__(self, repository: RolUsuarioRepository):
        self.repository = repository

    def asignar_rol(self, db: Session, data: RolUsuarioCreate, current_user):
        self._validate_scope(db, current_user, data.usuario_id)
        self._validate_role_assignment(db, current_user, data.rol_id)
        existing = self.repository.get_by_user_and_rol(db, data.rol_id, data.usuario_id)
        if existing:
            raise ValueError("Restricción: El rol ya se encuentra asignado de antemano a esta persona.")
        return self.repository.create(db, data)

    def revocar_rol(self, db: Session, rol_id: int, usuario_id: int, current_user):
        self._validate_scope(db, current_user, usuario_id)
        self._validate_role_assignment(db, current_user, rol_id)
        existing = self.repository.get_by_user_and_rol(db, rol_id, usuario_id)
        if not existing:
            raise ValueError("Petición declinada: El usuario no cuenta con la posesión de este rol, interrupción de desvinculación evitada.")
        return self.repository.delete(db, rol_id, usuario_id)

    def get_roles_by_usuario(self, db: Session, usuario_id: int, current_user):
        self._validate_scope(db, current_user, usuario_id)
        return self.repository.get_roles_by_user(db, usuario_id)
        
    def _validate_scope(self, db: Session, current_user, usuario_id: int):
        from models.usuario import Usuario
        if current_user.is_staff: return
        target = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not target: raise ValueError("Usuario objetivo no encontrado.")
        if current_user.type.lower() == "empresa" and current_user.empresa_id != target.empresa_id:
            raise PermissionError("Violación de Ámbito: El usuario objetivo pertenece a otra jurisdicción.")
        elif current_user.type.lower() == "cliente" and current_user.id != target.id:
            raise PermissionError("Violación de Ámbito: Operación denegada.")

    def _validate_role_assignment(self, db: Session, current_user, rol_id: int):
        if current_user.is_staff: return
        # Validar que si es un administrador de taller, solo asigne tecnico o encargado_taller
        from models.rol import Rol
        rol_obj = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol_obj: raise ValueError("El rol especificado no existe.")
        
        # Obtenemos los roles del current_user para ver si es admin
        roles_nombres = [ru.rol.nombre for ru in current_user.roles]
        if "administrador_taller" in roles_nombres:
            if rol_obj.nombre not in ["encargado_taller", "tecnico"]:
                raise PermissionError(f"Restricción de Negocio: Un Administrador de Taller no tiene autorización para asignar/revocar el rol '{rol_obj.nombre}'. Solo puede operar sobre 'encargado_taller' o 'tecnico'.")
        else:
            # Si no es staff ni administrador_taller, no debería poder asignar roles,
            # pero eso lo atrapa el Depends de permisos en el controlador.
            pass
