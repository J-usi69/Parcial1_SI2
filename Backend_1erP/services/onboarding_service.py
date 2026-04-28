from sqlalchemy.orm import Session
from schemas.onboarding import OnboardingTallerRequest
from schemas.usuario import RegistroClienteRequest
from models.empresa import Empresa
from models.sucursal import Sucursal
from models.usuario import Usuario
from models.rol_usuario import RolUsuario
from models.rol import Rol
from models.suscripcion import Suscripcion
from services.auth_service import AuthService
from models.enums import TipoUsuario

class OnboardingService:
    def __init__(self, auth_svc: AuthService):
        self.auth_svc = auth_svc

    def registrar_taller(self, db: Session, data: OnboardingTallerRequest):
        try:
            # Check limits before doing anything (at least check if email exists)
            correo_norm = data.admin.correo.lower()
            if db.query(Usuario).filter(Usuario.correo == correo_norm).first():
                raise ValueError(f"El correo {correo_norm} ya consta en nuestros registros.")
                
            # 1. Crear Empresa
            empresa = Empresa(**data.empresa.model_dump())
            db.add(empresa)
            db.flush() # Para obtener el ID sin commitear la transaccion
            
            # 2. Crear Sucursal
            sucursal_data = data.sucursal.model_dump()
            sucursal_data['empresa_id'] = empresa.id
            sucursal = Sucursal(**sucursal_data)
            db.add(sucursal)
            db.flush()
            
            # 3. Crear Usuario Administrador (Dueño)
            susc_empresa = db.query(Suscripcion).filter(Suscripcion.titulo == "suscripcion_base_empresas").first()
            if not susc_empresa:
                raise ValueError("Suscripción base comercial no encontrada en el sistema.")
                
            rol_admin = db.query(Rol).filter(Rol.nombre == "administrador_taller").first()
            if not rol_admin:
                raise ValueError("Rol base administrador_taller no encontrado en el sistema.")
            
            admin_data = data.admin.model_dump(exclude={'password'})
            admin_data['password_hash'] = self.auth_svc.hash_password(data.admin.password)
            admin_data['correo'] = correo_norm
            admin_data['type'] = TipoUsuario.empresa
            admin_data['is_owner'] = True
            admin_data['empresa_id'] = empresa.id
            admin_data['suscripcion_id'] = susc_empresa.id
            admin_data['sucursal_id'] = None 
            
            usuario = Usuario(**admin_data)
            db.add(usuario)
            db.flush()
            
            # 4. Asignar Rol
            rol_usuario = RolUsuario(rol_id=rol_admin.id, usuario_id=usuario.id)
            db.add(rol_usuario)
            
            db.commit()
            db.refresh(empresa)
            db.refresh(sucursal)
            db.refresh(usuario)
            
            return {
                "message": "Onboarding de taller completado con éxito.",
                "empresa": empresa,
                "sucursal": sucursal,
                "admin": usuario
            }
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Fallo en el onboarding del taller: {str(e)}")

    def registrar_cliente(self, db: Session, data: RegistroClienteRequest):
        try:
            correo_norm = data.correo.lower()
            if db.query(Usuario).filter(Usuario.correo == correo_norm).first():
                raise ValueError(f"El correo {correo_norm} ya consta en nuestros registros.")
                
            susc_cliente = db.query(Suscripcion).filter(Suscripcion.titulo == "suscripcion_base_clientes").first()
            if not susc_cliente:
                raise ValueError("Suscripción base de cliente no encontrada en el sistema.")
                
            rol_cliente = db.query(Rol).filter(Rol.nombre == "cliente").first()
            if not rol_cliente:
                raise ValueError("Rol base cliente no encontrado en el sistema.")
                
            cliente_data = data.model_dump(exclude={'password'})
            cliente_data['password_hash'] = self.auth_svc.hash_password(data.password)
            cliente_data['correo'] = correo_norm
            cliente_data['type'] = TipoUsuario.cliente
            cliente_data['is_owner'] = False
            cliente_data['empresa_id'] = None
            cliente_data['sucursal_id'] = None
            cliente_data['suscripcion_id'] = susc_cliente.id
            
            usuario = Usuario(**cliente_data)
            db.add(usuario)
            db.flush()
            
            rol_usuario = RolUsuario(rol_id=rol_cliente.id, usuario_id=usuario.id)
            db.add(rol_usuario)
            
            db.commit()
            db.refresh(usuario)
            
            return usuario
        except Exception as e:
            db.rollback()
            raise ValueError(f"Fallo en el registro de cliente: {str(e)}")
