from sqlalchemy.orm import Session
from schemas.empresa import EmpresaCreate, EmpresaUpdate
from repositories.empresa_repository import EmpresaRepository

class EmpresaService:
    def __init__(self, repository: EmpresaRepository):
        self.repository = repository

    def get_empresas(self, db: Session):
        return self.repository.get_all(db)

    def get_empresa(self, db: Session, empresa_id: int):
        empresa = self.repository.get_by_id(db, empresa_id)
        if not empresa:
            raise ValueError(f"Empresa con ID {empresa_id} no existe.")
        return empresa

    def create_empresa(self, db: Session, data: EmpresaCreate):
        existing = self.repository.get_by_nit(db, data.nit)
        if existing:
            raise ValueError(f"Ya existe una empresa con ese NIT: '{data.nit}'")
        return self.repository.create(db, data)

    def update_empresa(self, db: Session, empresa_id: int, data: EmpresaUpdate):
        empresa = self.repository.get_by_id(db, empresa_id)
        if not empresa:
            raise ValueError("La empresa especificada no existe.")
            
        # Validar lógica cruzada: Si cambia el nit, que no amanse el de otro
        if data.nit and data.nit != empresa.nit:
            if self.repository.get_by_nit(db, data.nit):
                raise ValueError("El NIT propuesto ya figura como activo bajo el dominio de otra empresa.")
                
        # Exclude unset extrae un diccionario limpisimo sin meter falsos None
        clean_update = data.model_dump(exclude_unset=True)
        return self.repository.update(db, empresa_id, clean_update)

    def soft_delete_empresa(self, db: Session, empresa_id: int):
        empresa = self.repository.get_by_id(db, empresa_id)
        if not empresa:
            raise ValueError("Empresa no encontrada")
        return self.repository.logical_delete(db, empresa_id)
