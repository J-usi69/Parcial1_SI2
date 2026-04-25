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

    def create_usuario(self, db: Session, data: UsuarioCreate, rol_id_basico: int):
        correo_normalizado = data.correo.lower()
        
        existing = self.repository.get_by_correo(db, correo_normalizado)
        if existing:
            raise ValueError(f"El correo {correo_normalizado} ya consta en nuestros registros.")
            
        if data.type.lower() == "empresa" and not data.empresa_id:
            raise ValueError("Por diseño, un perfil catalogado como Empresa no puede existir sin su entidad Padre apuntada en empresa_id.")
        
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

    def update_perfil(self, db: Session, usuario_id: int, data: UsuarioUpdate):
        user = self.repository.get_by_id(db, usuario_id)
        if not user:
            raise ValueError("Identidad de base extraviada.")
            
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update_perfil(db, usuario_id, clean_update)

    def inactivar_cuenta(self, db: Session, usuario_id: int):
        user = self.repository.get_by_id(db, usuario_id)
        if not user:
            raise ValueError("Incapacidad técnica para extinguir a un usuario que no habita la matriz.")
        return self.repository.set_inactive(db, usuario_id)
