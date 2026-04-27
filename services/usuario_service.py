from sqlalchemy.orm import Session
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from repositories.usuario_repository import UsuarioRepository
from services.auth_service import AuthService

class UsuarioService:
    def __init__(self, repository: UsuarioRepository, auth_svc: AuthService):
        self.repository = repository
        self.auth_svc = auth_svc

    def get_user_by_correo(self, db: Session, correo: str):
        return self.repository.get_by_correo(db, correo.lower())

    def get_usuarios(self, db: Session, current_user):
        from models.usuario import Usuario
        query = db.query(Usuario)
        if current_user.is_staff: # Superuser / Moderador
            return query.all()
        elif current_user.type.lower() == "empresa":
            if current_user.sucursal_id:
                # Tecnico / Encargado: solo su sucursal
                return query.filter(Usuario.sucursal_id == current_user.sucursal_id).all()
            else:
                # Admin Taller: toda su empresa
                return query.filter(Usuario.empresa_id == current_user.empresa_id).all()
        else:
            # Cliente: solo a si mismo
            return query.filter(Usuario.id == current_user.id).all()

    def get_usuario_by_id(self, db: Session, usuario_id: int, current_user):
        user = self.repository.get_by_id(db, usuario_id)
        if not user:
            raise ValueError("Usuario no encontrado en el sistema.")
            
        self._validate_scope(current_user, target_usuario_id=user.id, target_empresa_id=user.empresa_id, target_sucursal_id=user.sucursal_id)
        return user
        
    def _validate_scope(self, current_user, target_usuario_id=None, target_empresa_id=None, target_sucursal_id=None):
        if current_user.is_staff:
            return True
        if current_user.type.lower() == "cliente":
            if target_usuario_id and target_usuario_id != current_user.id:
                raise PermissionError("Violación de Ámbito: No tiene acceso a este recurso.")
            if target_empresa_id or target_sucursal_id:
                raise PermissionError("Violación de Ámbito: Un cliente no puede operar sobre empresas o sucursales.")
        elif current_user.type.lower() == "empresa":
            if target_empresa_id and target_empresa_id != current_user.empresa_id:
                raise PermissionError("Violación de Ámbito: No puede operar sobre otra empresa.")
            if current_user.sucursal_id and target_sucursal_id and target_sucursal_id != current_user.sucursal_id:
                raise PermissionError("Violación de Ámbito: No puede operar sobre otra sucursal.")
        return True

    def create_usuario(self, db: Session, data: UsuarioCreate, rol_id_basico: int, current_user):
        self._validate_scope(current_user, target_empresa_id=data.empresa_id, target_sucursal_id=data.sucursal_id)
        correo_normalizado = data.correo.lower()
        
        existing = self.repository.get_by_correo(db, correo_normalizado)
        if existing:
            raise ValueError(f"El correo {correo_normalizado} ya consta en nuestros registros.")
            
        if data.type.lower() == "cliente":
            if data.empresa_id or data.sucursal_id:
                raise ValueError("Un usuario de tipo cliente no puede pertenecer a una empresa ni sucursal.")
                
        elif data.type.lower() == "empresa":
            if not data.empresa_id:
                raise ValueError("Por diseño, un perfil catalogado como Empresa no puede existir sin su entidad Padre apuntada en empresa_id.")
            
            from models.rol import Rol
            rol = db.query(Rol).filter(Rol.id == rol_id_basico).first()
            if rol and rol.nombre in ["encargado_taller", "tecnico"]:
                if not data.sucursal_id:
                    raise ValueError(f"El rol {rol.nombre} requiere estar asignado a una sucursal específica.")
                    
            # Validar limites de suscripcion basados en el owner de la empresa
            from models.usuario import Usuario
            from models.suscripcion import Suscripcion
            owner = db.query(Usuario).filter(Usuario.empresa_id == data.empresa_id, Usuario.is_owner == True).first()
            if owner:
                suscripcion = db.query(Suscripcion).filter(Suscripcion.id == owner.suscripcion_id).first()
                if suscripcion:
                    current_users = db.query(Usuario).filter(Usuario.empresa_id == data.empresa_id, Usuario.is_active == True).count()
                    if current_users >= suscripcion.max_usuarios:
                        raise ValueError(f"Límite de usuarios alcanzado ({suscripcion.max_usuarios}) para la suscripción operativa de la empresa.")
        
        pass_hash = self.auth_svc.hash_password(data.password)
        
        db_data = data.model_dump(exclude={'password'})
        db_data['correo'] = correo_normalizado
        db_data['password_hash'] = pass_hash
        
        nuevo_usuario = self.repository.create(db, db_data)
        
        from repositories.rol_usuario_repository import RolUsuarioRepository
        from schemas.rol_usuario import RolUsuarioCreate
        
        rol_repo = RolUsuarioRepository()
        rol_repo.create(db, RolUsuarioCreate(rol_id=rol_id_basico, usuario_id=nuevo_usuario.id))
        
        return nuevo_usuario

    def update_perfil(self, db: Session, usuario_id: int, data: UsuarioUpdate, current_user):
        user = self.repository.get_by_id(db, usuario_id)
        if not user:
            raise ValueError("Identidad de base extraviada.")
            
        self._validate_scope(current_user, target_usuario_id=user.id, target_empresa_id=user.empresa_id, target_sucursal_id=user.sucursal_id)
            
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update_perfil(db, usuario_id, clean_update)

    def inactivar_cuenta(self, db: Session, usuario_id: int, current_user):
        user = self.repository.get_by_id(db, usuario_id)
        if not user:
            raise ValueError("Incapacidad técnica para extinguir a un usuario que no habita la matriz.")
            
        self._validate_scope(current_user, target_usuario_id=user.id, target_empresa_id=user.empresa_id, target_sucursal_id=user.sucursal_id)
        if user.is_owner:
            raise ValueError("No se puede inactivar al Administrador Principal de una empresa operando. Debe transferir la titularidad primero.")
        return self.repository.set_inactive(db, usuario_id)
