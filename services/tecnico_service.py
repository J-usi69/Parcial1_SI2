from sqlalchemy.orm import Session
from schemas.tecnico import TecnicoCreate, TecnicoUpdate
from repositories.tecnico_repository import TecnicoRepository

class TecnicoService:
    def __init__(self, repository: TecnicoRepository):
        self.repository = repository

    def get_tecnicos(self, db: Session, current_user):
        if current_user.is_staff:
            return self.repository.get_all(db)
        elif current_user.empresa_id:
            return self.repository.get_by_empresa(db, current_user.empresa_id)
        return []

    def get_tecnico(self, db: Session, tecnico_id: int, current_user):
        tecnico = self.repository.get_by_id(db, tecnico_id)
        if not tecnico:
            raise ValueError(f"Técnico {tecnico_id} no encontrado.")
        self._validate_scope(db, current_user, tecnico)
        return tecnico

    def create_tecnico(self, db: Session, data: TecnicoCreate, current_user):
        """
        Aplica las 4 validaciones explícitas del modelo Tecnico:
          [1] usuario.type == "empresa"
          [2] usuario tiene rol "tecnico"
          [3] misma empresa/sucursal que el registrador
          [4] relación 1:1 — no existe ya un Tecnico para ese usuario_id
        """
        from models.usuario import Usuario
        from models.rol_usuario import RolUsuario
        from models.rol import Rol

        # [4] 1:1 — evitar duplicado antes del hit DB (UniqueConstraint en DB como respaldo)
        existing = self.repository.get_by_usuario_id(db, data.usuario_id)
        if existing:
            raise ValueError("Este usuario ya tiene una entidad Técnico registrada (relación 1:1).")

        # Obtener el usuario destino
        usuario = db.query(Usuario).filter(Usuario.id == data.usuario_id).first()
        if not usuario:
            raise ValueError("El usuario especificado no existe.")

        # [1] usuario.type == "empresa"
        if usuario.type != "empresa":
            raise ValueError(
                "Validación [1]: Solo usuarios de tipo 'empresa' pueden ser registrados como técnicos."
            )

        # [2] usuario tiene rol "tecnico" activo
        rol_tecnico = (
            db.query(RolUsuario)
            .join(Rol, RolUsuario.rol_id == Rol.id)
            .filter(RolUsuario.usuario_id == data.usuario_id, Rol.nombre == "tecnico")
            .first()
        )
        if not rol_tecnico:
            raise ValueError(
                "Validación [2]: El usuario no tiene el rol 'tecnico' asignado. Asigna el rol antes de crear la entidad Técnico."
            )

        # [3] misma empresa/sucursal que el administrador que registra
        if not current_user.is_staff:
            if usuario.empresa_id != current_user.empresa_id:
                raise PermissionError(
                    "Validación [3]: El usuario a registrar como técnico no pertenece a tu empresa."
                )

        return self.repository.create(db, data)

    def update_tecnico(self, db: Session, tecnico_id: int, data: TecnicoUpdate, current_user):
        tecnico = self.repository.get_by_id(db, tecnico_id)
        if not tecnico:
            raise ValueError("Técnico no encontrado.")
        self._validate_scope(db, current_user, tecnico)
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, tecnico_id, clean_update)

    def inactivar_tecnico(self, db: Session, tecnico_id: int, current_user):
        tecnico = self.repository.get_by_id(db, tecnico_id)
        if not tecnico:
            raise ValueError("Técnico no encontrado.")
        self._validate_scope(db, current_user, tecnico)
        return self.repository.logical_delete(db, tecnico_id)

    def _validate_scope(self, db: Session, current_user, tecnico):
        if current_user.is_staff:
            return
        from models.usuario import Usuario
        usuario = db.query(Usuario).filter(Usuario.id == tecnico.usuario_id).first()
        if not usuario or usuario.empresa_id != current_user.empresa_id:
            raise PermissionError("Violación de Ámbito: Este técnico no pertenece a tu empresa.")
