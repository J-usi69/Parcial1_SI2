import uuid
from sqlalchemy.orm import Session
from schemas.archivo import ArchivoCreate, ArchivoUpdate
from repositories.archivo_repository import ArchivoRepository
from models.solicitud import Solicitud
from models.diagnostico import Diagnostico
from models.pago import Pago
from models.asignacion import Asignacion
from models.tecnico import Tecnico
from models.sucursal import Sucursal

class ArchivoService:
    def __init__(self, repository: ArchivoRepository):
        self.repository = repository

    def _validate_scope(self, db: Session, current_user, entidad_tipo: str, entidad_id: int):
        if current_user.is_staff:
            return

        if entidad_tipo == "solicitud":
            sol = db.query(Solicitud).filter(Solicitud.id == entidad_id).first()
            if not sol:
                raise ValueError("Solicitud no encontrada.")
            if current_user.type == "cliente" and sol.cliente_id != current_user.id:
                raise PermissionError("No tienes acceso a esta solicitud.")
            if current_user.type == "empresa" and current_user.empresa_id:
                suc = db.query(Sucursal).filter(Sucursal.id == sol.sucursal_id).first()
                if not suc or suc.empresa_id != current_user.empresa_id:
                    raise PermissionError("No tienes acceso a esta solicitud.")
            # Si es tecnico, debe tener asignada la solicitud
            tecnico = db.query(Tecnico).filter(Tecnico.usuario_id == current_user.id).first()
            if tecnico:
                asig = db.query(Asignacion).filter(Asignacion.solicitud_id == sol.id, Asignacion.tecnico_id == tecnico.id).first()
                if not asig:
                    raise PermissionError("No estás asignado a esta solicitud.")
                    
        elif entidad_tipo == "diagnostico":
            diag = db.query(Diagnostico).filter(Diagnostico.id == entidad_id).first()
            if not diag:
                raise ValueError("Diagnóstico no encontrado.")
            # Delegamos validación al scope de la asignación/solicitud
            asig = db.query(Asignacion).filter(Asignacion.id == diag.asignacion_id).first()
            if not asig:
                 raise PermissionError("Asignación no encontrada.")
            self._validate_scope(db, current_user, "solicitud", asig.solicitud_id)
            
        elif entidad_tipo == "pago":
            pago = db.query(Pago).filter(Pago.id == entidad_id).first()
            if not pago:
                raise ValueError("Pago no encontrado.")
            self._validate_scope(db, current_user, "solicitud", pago.solicitud_id)
        else:
            raise ValueError("Tipo de entidad no soportado.")

    def get_archivo(self, db: Session, archivo_id: int, current_user):
        archivo = self.repository.get_by_id(db, archivo_id)
        if not archivo:
            raise ValueError("Archivo no encontrado.")
        self._validate_scope(db, current_user, archivo.entidad_tipo, archivo.entidad_id)
        return archivo

    def get_por_entidad(self, db: Session, entidad_tipo: str, entidad_id: int, current_user):
        self._validate_scope(db, current_user, entidad_tipo, entidad_id)
        return self.repository.get_by_entidad(db, entidad_tipo, entidad_id)

    def create_archivo(self, db: Session, data: ArchivoCreate, current_user):
        self._validate_scope(db, current_user, data.entidad_tipo, data.entidad_id)
        
        # Generar metadata interna
        ext = data.nombre_original.split('.')[-1] if '.' in data.nombre_original else 'bin'
        nombre_interno = f"{uuid.uuid4().hex}.{ext}"
        ruta = f"storage/{data.entidad_tipo}/{data.entidad_id}/{nombre_interno}"
        
        # TODO: En prod, aquí se realizaría la subida física a un bucket o FS local antes de guardar en DB.
        
        return self.repository.create(db, data, current_user.id, nombre_interno, ruta)

    def inactivar_archivo(self, db: Session, archivo_id: int, current_user):
        archivo = self.get_archivo(db, archivo_id, current_user)
        return self.repository.update(db, archivo_id, {"status": "inactivo"})
