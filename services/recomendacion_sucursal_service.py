from sqlalchemy.orm import Session
from schemas.recomendacion_sucursal import RecomendacionSucursalCreate
from repositories.recomendacion_sucursal_repository import RecomendacionSucursalRepository
from models.solicitud import Solicitud
from models.recomendacion_sucursal import RecomendacionSucursal


class RecomendacionSucursalService:
    def __init__(self, repository: RecomendacionSucursalRepository):
        self.repository = repository

    # ------------------------------------------------------------------
    # Validación de ámbito — usada solo por flujos humanos
    # ------------------------------------------------------------------
    def _validate_scope(self, db: Session, current_user, solicitud_id: int):
        """
        Tenant isolation para acceso humano a recomendaciones.
        - cliente: solo sus solicitudes
        - empresa (admin/encargado): solo solicitudes de su empresa
        - superuser/moderador (is_staff): acceso global
        """
        if current_user.is_staff:
            return

        sol = db.query(Solicitud).filter(Solicitud.id == solicitud_id).first()
        if not sol:
            raise ValueError("Solicitud no encontrada.")

        if current_user.type == "cliente":
            if sol.cliente_id != current_user.id:
                raise PermissionError(
                    "Violacion de ambito: No tienes acceso a las recomendaciones de esta solicitud."
                )
        elif current_user.type == "empresa":
            # Verificar que la solicitud pertenece a la empresa del usuario
            if not current_user.empresa_id:
                raise PermissionError("Tu usuario no tiene empresa asociada.")
            from models.sucursal import Sucursal
            suc = db.query(Sucursal).filter(Sucursal.id == sol.sucursal_id).first()
            if not suc or suc.empresa_id != current_user.empresa_id:
                raise PermissionError(
                    "Violacion de ambito: Esta solicitud no pertenece a tu empresa."
                )
        else:
            # Cualquier otro tipo de usuario sin is_staff ni empresa definida
            raise PermissionError("No tienes permisos para acceder a recomendaciones.")

    # ------------------------------------------------------------------
    # Consultas (expuestas a actores humanos)
    # ------------------------------------------------------------------
    def get_recomendacion(self, db: Session, recomendacion_id: int, current_user):
        rec = self.repository.get_by_id(db, recomendacion_id)
        if not rec:
            raise ValueError("Recomendacion no encontrada.")
        self._validate_scope(db, current_user, rec.solicitud_id)
        return rec

    def get_por_solicitud(self, db: Session, solicitud_id: int, current_user):
        self._validate_scope(db, current_user, solicitud_id)
        return self.repository.get_by_solicitud(db, solicitud_id)

    # ------------------------------------------------------------------
    # Flujo INTERNO del sistema — sin validación de rol humano
    # Llamado únicamente por el backend tras crear la solicitud.
    # ------------------------------------------------------------------
    def _generar_recomendacion_inicial(self, db: Session, solicitud_id: int):
        """
        Genera la clasificación y recomendación de sucursal de forma autónoma
        como actor de sistema. No depende del rol del usuario que originó la solicitud.
        Invocado internamente desde SolicitudService.create_solicitud.
        """
        from services.ia_clasificacion_service import IAClasificacionService
        from models.sucursal import Sucursal
        from models.tecnico import Tecnico
        from sqlalchemy import func
        from repositories.clasificacion_incidente_repository import ClasificacionIncidenteRepository

        ia_svc = IAClasificacionService()

        # Obtener clasificación más reciente (ya persistida por ClasificacionIncidenteService)
        clasif_repo = ClasificacionIncidenteRepository()
        clasif = clasif_repo.get_latest_by_solicitud(db, solicitud_id)
        if not clasif:
            # Si no hay clasificación (ej: error previo), no persistimos recomendaciones vacías
            return []

        # Inactivar recomendaciones previas si existiesen
        db.query(RecomendacionSucursal).filter(
            RecomendacionSucursal.solicitud_id == solicitud_id
        ).update({"recomendacion_activa": False})

        # Obtener sucursales activas y sus conteos de técnicos activos
        sucursales = db.query(Sucursal).filter(Sucursal.status == "activo").all()
        tecnicos_counts = (
            db.query(Tecnico.sucursal_id, func.count(Tecnico.id).label("total"))
            .filter(Tecnico.status == "activo")
            .group_by(Tecnico.sucursal_id)
            .all()
        )
        tecnicos_map = {tc.sucursal_id: tc.total for tc in tecnicos_counts}

        # Input para la IA: distancia y precio son None porque no hay datos reales todavía.
        # Esto hace que el motor sea honesto y deje criterios_evaluados con distancia_evaluada=False.
        suc_disponibles = [
            {
                "sucursal_id":     s.id,
                "precio_local":    None,   # Sin datos reales → honesto
                "distancia_km":    None,   # Sin coordenadas reales → honesto
                "disponible":      True,
                "tecnicos_activos": tecnicos_map.get(s.id, 0),
            }
            for s in sucursales
        ]

        clasif_data = {
            "nivel_prioridad":              clasif.nivel_prioridad,
            "requiere_tecnico_especializado": clasif.requiere_tecnico_especializado,
        }

        recom_data = ia_svc.recomendar_sucursales(solicitud_id, clasif_data, suc_disponibles)

        creadas = []
        for rd in recom_data:
            creadas.append(self.repository.create(db, RecomendacionSucursalCreate(**rd)))

        db.commit()
        return creadas

    # ------------------------------------------------------------------
    # Recálculo MANUAL — por actor humano con permiso validado
    # ------------------------------------------------------------------
    def recalcular_recomendacion(self, db: Session, solicitud_id: int, current_user):
        """
        Recalcula recomendaciones de sucursal bajo demanda de un actor humano
        (encargado_taller / administrador_taller). Valida permisos estrictamente.
        """
        self._validate_scope(db, current_user, solicitud_id)

        if current_user.type not in ("empresa",) and not current_user.is_staff:
            raise PermissionError(
                "Solo el personal del taller o administradores pueden recalcular recomendaciones."
            )

        # Delegamos al flujo interno (mismo algoritmo, actor distinto)
        return self._generar_recomendacion_inicial(db, solicitud_id)

    # ------------------------------------------------------------------
    # Creación interna de registro único (usada por seeder / tests)
    # ------------------------------------------------------------------
    def create_recomendacion(self, db: Session, data: RecomendacionSucursalCreate):
        return self.repository.create(db, data)
