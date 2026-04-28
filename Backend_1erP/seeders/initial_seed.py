import sys
import os
from datetime import datetime, timezone

# Añadir el root del proyecto al sys.path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from db import SessionLocal
from services.auth_service import AuthService
from models.enums import TipoUsuario, EstadoNotificacion, DestinatarioNotificacion

from models.suscripcion import Suscripcion
from models.rol import Rol
from models.permiso import Permiso
from models.rol_permiso import RolPermiso
from models.empresa import Empresa
from models.sucursal import Sucursal
from models.usuario import Usuario
from models.rol_usuario import RolUsuario
from models.notificacion import Notificacion
from models.notificacion_usuario import NotificacionUsuario
from models.tecnico import Tecnico
from models.vehiculo import Vehiculo
from models.servicio import Servicio
from models.servicio_sucursal import ServicioSucursal
from models.solicitud import Solicitud
from models.asignacion import Asignacion
from models.diagnostico import Diagnostico
from models.archivo import Archivo
from models.clasificacion_incidente import ClasificacionIncidente
from models.recomendacion_sucursal import RecomendacionSucursal
from models.metodo_pago import MetodoPago
from models.pago import Pago

def get_or_create(db: Session, model, defaults=None, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance, True

def seed():
    db = SessionLocal()
    auth_svc = AuthService()
    print("Iniciando Seeder Inicial...")

    try:
        # 1. Suscripciones
        print("Poblando Suscripciones...")
        susc_cliente, _ = get_or_create(db, Suscripcion, 
            titulo="suscripcion_base_clientes",
            defaults={"descripcion": "Plan gratuito base para usuarios cliente", "precio": 0.0, "duracion": 365, "estado": True, "max_sucursales": 1, "max_usuarios": 1}
        )
        susc_empresa, _ = get_or_create(db, Suscripcion, 
            titulo="suscripcion_base_empresas",
            defaults={"descripcion": "Plan comercial base para talleres mecánicos", "precio": 50.0, "duracion": 30, "estado": True, "max_sucursales": 5, "max_usuarios": 10}
        )

        # 2. Roles
        print("Poblando Roles...")
        roles_nombres = ["superuser", "moderador", "administrador_taller", "encargado_taller", "tecnico", "cliente"]
        roles_db = {}
        for nombre in roles_nombres:
            r, _ = get_or_create(db, Rol, nombre=nombre, defaults={"descripcion": f"Rol {nombre}"})
            roles_db[nombre] = r

        # 3. Permisos
        print("Poblando Permisos...")
        permisos_nombres = [
            # Bloques A-D: Estructura, Identidades, Accesos
            "ver_roles", "crear_roles", "editar_roles", "eliminar_roles",
            "ver_permisos", "crear_permisos", "editar_permisos", "eliminar_permisos",
            "ver_suscripciones", "crear_suscripciones", "editar_suscripciones", "desactivar_suscripciones",
            "ver_usuario", "crear_usuario", "editar_usuario", "inactivar_usuario",
            "asignar_rol", "revocar_rol",
            "ver_empresa", "crear_empresa", "editar_empresa", "inactivar_empresa",
            "ver_sucursal", "crear_sucursal", "editar_sucursal", "inactivar_sucursal",
            "ver_notificacion", "crear_notificacion", "marcar_notificacion_leida",
            # Bloque E: Vehículos
            "ver_vehiculo", "crear_vehiculo", "editar_vehiculo", "inactivar_vehiculo",
            # Bloque E: Servicios (catálogo corporativo)
            "ver_servicio", "crear_servicio", "editar_servicio", "inactivar_servicio",
            # Bloque E: Servicio-Sucursal (ajuste #2: permisos completos)
            "ver_servicio_sucursal", "asignar_servicio_sucursal",
            "editar_servicio_sucursal", "inactivar_servicio_sucursal",
            # Bloque E: Técnicos
            "ver_tecnico", "crear_tecnico", "editar_tecnico", "inactivar_tecnico",
            # Bloque E: Solicitudes
            "ver_solicitud", "crear_solicitud", "cancelar_solicitud",
            "decidir_solicitud", "actualizar_estado_servicio",
            # Bloque E: Asignaciones
            "ver_asignacion", "crear_asignacion", "responder_asignacion",
            # Bloque E: Diagnósticos
            "ver_diagnostico", "crear_diagnostico", "editar_diagnostico",
            # Bloque F: Archivos
            "ver_archivo", "crear_archivo", "inactivar_archivo",
            # Bloque F: Clasificación IA
            "ver_clasificacion_incidente", "reportar_clasificacion_incidente", "revalidar_clasificacion_incidente",
            # Bloque F: Recomendación Sucursal
            "ver_recomendacion_sucursal", "recalcular_recomendacion_sucursal",
            # Bloque F: Métodos de Pago
            "ver_metodo_pago", "crear_metodo_pago", "editar_metodo_pago", "inactivar_metodo_pago",
            # Bloque F: Pagos
            "ver_pago", "crear_pago", "editar_pago", "verificar_pago",
            # Bloque F: Comisiones
            "ver_comision", "crear_comision", "editar_comision",
        ]
        permisos_db = {}
        for nombre in permisos_nombres:
            p, _ = get_or_create(db, Permiso, nombre=nombre, defaults={"descripcion": f"Permite {nombre.replace('_', ' ')}"})
            permisos_db[nombre] = p

        # 4. Rol_Permiso (Asignación Completa Bloques A-E)
        print("Asociando Permisos a Roles...")

        # SuperUser: todos los permisos
        for p in permisos_db.values():
            get_or_create(db, RolPermiso, rol_id=roles_db["superuser"].id, permiso_id=p.id)

        # Moderador: lectura operativa + gestión estructural (sin cambiar roles/permisos)
        permisos_moderador = [
            "ver_suscripciones", "crear_suscripciones", "editar_suscripciones", "desactivar_suscripciones",
            "ver_usuario", "inactivar_usuario",
            "ver_empresa", "crear_empresa", "editar_empresa", "inactivar_empresa",
            "ver_sucursal", "crear_sucursal", "editar_sucursal", "inactivar_sucursal",
            "ver_notificacion", "crear_notificacion", "marcar_notificacion_leida",
            # Bloque E: solo lectura operativa (auditoría)
            "ver_vehiculo", "ver_servicio", "ver_servicio_sucursal",
            "ver_tecnico", "ver_solicitud", "ver_asignacion", "ver_diagnostico",
            # Bloque F: solo lectura operativa
            "ver_archivo", "ver_clasificacion_incidente", "ver_recomendacion_sucursal",
            "ver_metodo_pago", "ver_pago", "ver_comision",
        ]
        for p_name in permisos_moderador:
            get_or_create(db, RolPermiso, rol_id=roles_db["moderador"].id, permiso_id=permisos_db[p_name].id)

        # Administrador de Taller
        permisos_admin = [
            "ver_usuario", "crear_usuario", "editar_usuario", "inactivar_usuario",
            "asignar_rol", "revocar_rol",
            "ver_empresa", "editar_empresa",
            "ver_sucursal", "crear_sucursal", "editar_sucursal", "inactivar_sucursal",
            "ver_notificacion", "crear_notificacion", "marcar_notificacion_leida",
            # Bloque E
            "ver_servicio", "crear_servicio", "editar_servicio", "inactivar_servicio",
            "ver_servicio_sucursal", "asignar_servicio_sucursal",
            "editar_servicio_sucursal", "inactivar_servicio_sucursal",
            "ver_tecnico", "crear_tecnico", "editar_tecnico", "inactivar_tecnico",
            "ver_solicitud", "decidir_solicitud",
            "ver_asignacion", "crear_asignacion",
            "ver_diagnostico",
            # Bloque F
            "ver_archivo", "crear_archivo", "inactivar_archivo",
            "ver_clasificacion_incidente", "revalidar_clasificacion_incidente",
            "ver_recomendacion_sucursal", "recalcular_recomendacion_sucursal",
            "ver_metodo_pago", "crear_metodo_pago", "editar_metodo_pago", "inactivar_metodo_pago",
            "ver_pago", "editar_pago", "verificar_pago",
            "ver_comision", "crear_comision", "editar_comision",
        ]
        for p_name in permisos_admin:
            get_or_create(db, RolPermiso, rol_id=roles_db["administrador_taller"].id, permiso_id=permisos_db[p_name].id)

        # Encargado de Taller
        permisos_encargado = [
            "ver_usuario", "ver_empresa", "ver_sucursal",
            "ver_notificacion", "crear_notificacion", "marcar_notificacion_leida",
            # Bloque E
            "ver_servicio", "ver_servicio_sucursal",
            "asignar_servicio_sucursal", "editar_servicio_sucursal",
            "ver_tecnico",
            "ver_solicitud", "decidir_solicitud",
            "ver_asignacion", "crear_asignacion",
            "ver_diagnostico",
            # Bloque F
            "ver_archivo", "crear_archivo",
            "ver_clasificacion_incidente", "revalidar_clasificacion_incidente",
            "ver_recomendacion_sucursal",
            "ver_metodo_pago", "ver_pago", "editar_pago", "verificar_pago",
            "ver_comision",
        ]
        for p_name in permisos_encargado:
            get_or_create(db, RolPermiso, rol_id=roles_db["encargado_taller"].id, permiso_id=permisos_db[p_name].id)

        # Tecnico
        permisos_tecnico = [
            "ver_sucursal", "ver_notificacion", "marcar_notificacion_leida",
            # Bloque E
            "ver_solicitud", "actualizar_estado_servicio",
            "ver_asignacion", "responder_asignacion",
            "ver_diagnostico", "crear_diagnostico", "editar_diagnostico",
            # Bloque F
            "ver_archivo", "crear_archivo",
            "ver_clasificacion_incidente", "ver_recomendacion_sucursal",
            "ver_pago",
        ]
        for p_name in permisos_tecnico:
            get_or_create(db, RolPermiso, rol_id=roles_db["tecnico"].id, permiso_id=permisos_db[p_name].id)

        # Cliente
        permisos_cliente = [
            "ver_empresa", "ver_sucursal",
            "ver_notificacion", "marcar_notificacion_leida",
            # Bloque E
            "ver_vehiculo", "crear_vehiculo", "editar_vehiculo", "inactivar_vehiculo",
            "ver_solicitud", "crear_solicitud", "cancelar_solicitud",
            "ver_diagnostico",
            # Bloque F
            "ver_archivo", "crear_archivo",
            "ver_clasificacion_incidente", "reportar_clasificacion_incidente",
            "ver_recomendacion_sucursal",
            "ver_metodo_pago", "crear_metodo_pago", "editar_metodo_pago", "inactivar_metodo_pago",
            "ver_pago", "crear_pago",
        ]
        for p_name in permisos_cliente:
            get_or_create(db, RolPermiso, rol_id=roles_db["cliente"].id, permiso_id=permisos_db[p_name].id)

        # 5. Empresa
        print("Creando Empresa base...")
        empresa, _ = get_or_create(db, Empresa, nit="1234567890", defaults={
            "razon_soc": "Taller Veltra Motors S.R.L.",
            "nombre": "Veltra Motors",
            "status": "activo"
        })

        # 6. Sucursal
        print("Creando Sucursal base...")
        sucursal, _ = get_or_create(db, Sucursal, nombre="Veltra Norte", defaults={
            "direccion": "Av. Banzer Km 5.5",
            "telefono": "77700001",
            "empresa_id": empresa.id,
            "status": "activo"
        })

        # 7. Usuarios
        print("Creando Usuarios de prueba...")
        usuarios_data = [
            {"correo": "admin@veltra.com", "nombres": "Admin", "apellidos": "Supremo", "type": TipoUsuario.empresa, "rol": "superuser", "suscripcion_id": susc_empresa.id, "empresa_id": None, "sucursal_id": None, "is_owner": False},
            {"correo": "moderador@veltra.com", "nombres": "Moderador", "apellidos": "Global", "type": TipoUsuario.empresa, "rol": "moderador", "suscripcion_id": susc_empresa.id, "empresa_id": None, "sucursal_id": None, "is_owner": False},
            {"correo": "gerente@taller.com", "nombres": "Gerente", "apellidos": "Taller", "type": TipoUsuario.empresa, "rol": "administrador_taller", "suscripcion_id": susc_empresa.id, "empresa_id": empresa.id, "sucursal_id": None, "is_owner": True},
            {"correo": "encargado@taller.com", "nombres": "Jefe", "apellidos": "Patio", "type": TipoUsuario.empresa, "rol": "encargado_taller", "suscripcion_id": susc_empresa.id, "empresa_id": empresa.id, "sucursal_id": sucursal.id, "is_owner": False},
            {"correo": "tecnico@taller.com", "nombres": "Maestro", "apellidos": "Mecanico", "type": TipoUsuario.empresa, "rol": "tecnico", "suscripcion_id": susc_empresa.id, "empresa_id": empresa.id, "sucursal_id": sucursal.id, "is_owner": False},
            {"correo": "juan@cliente.com", "nombres": "Juan", "apellidos": "Perez", "type": TipoUsuario.cliente, "rol": "cliente", "suscripcion_id": susc_cliente.id, "empresa_id": None, "sucursal_id": None, "is_owner": False},
            {"correo": "multirole@taller.com", "nombres": "Multi", "apellidos": "Rol", "type": TipoUsuario.empresa, "rol": "administrador_taller", "suscripcion_id": susc_empresa.id, "empresa_id": empresa.id, "sucursal_id": None, "is_owner": False} 
        ]

        usuarios_db = {}
        for ud in usuarios_data:
            u, created = get_or_create(db, Usuario, correo=ud["correo"], defaults={
                "ci": f"CI-{ud['nombres'][:3]}",
                "nombres": ud["nombres"],
                "apellidos": ud["apellidos"],
                "password_hash": auth_svc.hash_password("123456"), # Clave estándar para pruebas
                "telefono": "60000000",
                "type": ud["type"],
                "suscripcion_id": ud["suscripcion_id"],
                "empresa_id": ud["empresa_id"],
                "sucursal_id": ud["sucursal_id"],
                "is_owner": ud["is_owner"]
            })
            usuarios_db[ud["correo"]] = u
            
            # 8. Rol_Usuario
            get_or_create(db, RolUsuario, usuario_id=u.id, rol_id=roles_db[ud["rol"]].id)

        # Asignar segundo rol al usuario de prueba multirol
        multi_user = usuarios_db["multirole@taller.com"]
        get_or_create(db, RolUsuario, usuario_id=multi_user.id, rol_id=roles_db["tecnico"].id)

        # 8b. Tecnico seed — cumple las 4 validaciones del modelo:
        # [1] usuario.type == empresa  ✓ (tecnico@taller.com es tipo empresa)
        # [2] tiene rol "tecnico"      ✓ (asignado en paso 8)
        # [3] misma empresa/sucursal   ✓ (empresa_id == empresa.id)
        # [4] relación 1:1            ✓ (get_or_create previene duplicado)
        print("Creando entidad Técnico seed...")
        tecnico_usuario = usuarios_db["tecnico@taller.com"]
        get_or_create(db, Tecnico, usuario_id=tecnico_usuario.id, defaults={
            "especialidad": "Mecánica General",
            "estado_operativo": "activo"
        })

        # 9. Notificaciones
        print("Creando Notificaciones...")
        admin_user_id = usuarios_db["admin@veltra.com"].id
        
        notif_global, _ = get_or_create(db, Notificacion, titulo="Bienvenida a Veltra", defaults={
            "descripcion": "El sistema está oficialmente operativo en Fase 1.",
            "ruta_destino": "/dashboard",
            "status": EstadoNotificacion.enviado,
            "user_type": DestinatarioNotificacion.todos,
            "usuario_id": admin_user_id
        })

        notif_tecnicos, _ = get_or_create(db, Notificacion, titulo="Nueva política de diagnóstico", defaults={
            "descripcion": "Por favor revisen el nuevo manual en la sección de recursos.",
            "ruta_destino": "/tecnicos/recursos",
            "status": EstadoNotificacion.enviado,
            "user_type": DestinatarioNotificacion.solo_tecnicos,
            "usuario_id": admin_user_id
        })

        # 10. Notificacion_Usuario
        print("Asignando Bandeja de Notificaciones...")
        # A Juan Cliente le llega la global, no leída
        get_or_create(db, NotificacionUsuario, notificacion_id=notif_global.id, usuario_id=usuarios_db["juan@cliente.com"].id, defaults={"leido": False})
        
        # Al Gerente le llega la global, ya leída
        get_or_create(db, NotificacionUsuario, notificacion_id=notif_global.id, usuario_id=usuarios_db["gerente@taller.com"].id, defaults={"leido": True})
        
        # Al Técnico le llegan ambas, una leída y otra no
        get_or_create(db, NotificacionUsuario, notificacion_id=notif_global.id, usuario_id=usuarios_db["tecnico@taller.com"].id, defaults={"leido": True})
        get_or_create(db, NotificacionUsuario, notificacion_id=notif_tecnicos.id, usuario_id=usuarios_db["tecnico@taller.com"].id, defaults={"leido": False})

        # --- BLOQUE E: OPERACIONES CORE ---
        print("Poblando Bloque E: Vehículos, Servicios y Flujo Operativo...")

        # 11. Vehículos
        juan_user = usuarios_db["juan@cliente.com"]
        vehiculo1, _ = get_or_create(db, Vehiculo, placa="7890-ABC", defaults={
            "usuario_id": juan_user.id, "marca": "toyota", "modelo": "corolla", 
            "anio": 2022, "color": "blanco", "cilindrada": "1800", "status": "activo"
        })
        vehiculo2, _ = get_or_create(db, Vehiculo, placa="4567-XYZ", defaults={
            "usuario_id": juan_user.id, "marca": "nissan", "modelo": "frontier", 
            "anio": 2020, "color": "gris", "cilindrada": "2500", "status": "activo"
        })

        # 12. Servicios (Catálogo)
        svc_aceite, _ = get_or_create(db, Servicio, nombre="Cambio de Aceite Premium", defaults={
            "empresa_id": empresa.id, "descripcion": "Aceite sintético + filtro", "precio_base": 300.0, "status": "activo"
        })
        svc_frenos, _ = get_or_create(db, Servicio, nombre="Mantenimiento de Frenos", defaults={
            "empresa_id": empresa.id, "descripcion": "Limpieza y ajuste", "precio_base": 150.0, "status": "activo"
        })

        # 13. Servicios por Sucursal (Pricing Operativo)
        ss_aceite, _ = get_or_create(db, ServicioSucursal, servicio_id=svc_aceite.id, sucursal_id=sucursal.id, defaults={
            "precio_local": 350.0, "disponible": True
        })
        ss_frenos, _ = get_or_create(db, ServicioSucursal, servicio_id=svc_frenos.id, sucursal_id=sucursal.id, defaults={
            "precio_local": 200.0, "disponible": True
        })

        # 14. Solicitudes Demo
        # Solicitud 1: Pendiente
        sol_pendiente, _ = get_or_create(db, Solicitud, cliente_id=juan_user.id, vehiculo_id=vehiculo1.id, sucursal_id=sucursal.id, estado="pendiente_taller", defaults={
            "servicio_sucursal_id": ss_aceite.id, "descripcion": "El auto suena raro al encender", "latitud": -17.783, "longitud": -63.182
        })

        # Solicitud 2: Ya asignada a técnico
        sol_con_tecnico, _ = get_or_create(db, Solicitud, cliente_id=juan_user.id, vehiculo_id=vehiculo2.id, sucursal_id=sucursal.id, estado="tecnico_asignado", defaults={
            "servicio_sucursal_id": ss_frenos.id, "descripcion": "Revisión preventiva de frenos", "latitud": -17.785, "longitud": -63.180
        })

        # 15. Asignaciones
        # tecnico_db ya fue creado en el paso 8b como entidad Tecnico
        tecnico_entidad = db.query(Tecnico).filter(Tecnico.usuario_id == usuarios_db["tecnico@taller.com"].id).first()
        
        asignacion, _ = get_or_create(db, Asignacion, solicitud_id=sol_con_tecnico.id, tecnico_id=tecnico_entidad.id, defaults={
            "estado": "aceptada"
        })

        # 16. Diagnósticos
        get_or_create(db, Diagnostico, asignacion_id=asignacion.id, defaults={
            "descripcion": "Pastillas de freno con 20% de vida útil. Se recomienda cambio.",
            "costo_estimado": 450.0,
            "estado": "borrador"
        })

        # --- BLOQUE F: DOCUMENTAL, ANALÍTICA Y COMERCIAL ---
        print("Poblando Bloque F: Clasificación, Pagos y Evidencias...")

        # 17. Clasificación IA y Recomendación (para la solicitud 1 pendiente)
        get_or_create(db, ClasificacionIncidente, solicitud_id=sol_pendiente.id, defaults={
            "categoria_incidente": "motor",
            "subcategoria_incidente": "encendido",
            "nivel_prioridad": "alta",
            "requiere_grua": True,
            "requiere_tecnico_especializado": True,
            "observaciones_modelo": "Basado en 'suena raro al encender', posible problema de motor o bujías.",
            "confianza_modelo": 0.88,
            "fuente_clasificacion": "reglas_heuristicas",
            "estado_revision": "pendiente"
        })

        get_or_create(db, RecomendacionSucursal, solicitud_id=sol_pendiente.id, sucursal_recomendada_id=sucursal.id, defaults={
            "score_recomendacion": 85.5,
            "criterios_evaluados": {"distancia_km": 3.2, "servicio_disponible": True},
            "justificacion_recomendacion": "Sucursal cercana con disponibilidad del servicio requerido.",
            "precio_estimado": 350.0,
            "distancia_estimada": 3.2
        })

        # 18. Métodos de Pago
        # Método para la sucursal (QR)
        mp_sucursal, _ = get_or_create(db, MetodoPago, propietario_tipo="sucursal", propietario_id=sucursal.id, tipo_pago="qr", defaults={
            "alias": "QR Principal Taller",
            "qr_imagen_ruta": "storage/qr/sucursal_1.png"
        })

        # 19. Pago (Para la solicitud 2 asignada, simulando pago por QR)
        get_or_create(db, Pago, solicitud_id=sol_con_tecnico.id, defaults={
            "cliente_id": juan_user.id,
            "metodo_pago_tipo": "qr",
            "metodo_pago_referencia_id": mp_sucursal.id,
            "monto": 200.0,
            "estado_pago": "verificado", # Lo marcamos verificado para que permita el diagnóstico
            "verificado_por_usuario_id": usuarios_db["encargado@taller.com"].id,
            "fecha_pago": datetime.now(timezone.utc),
            "fecha_verificacion": datetime.now(timezone.utc)
        })

        # 20. Evidencia (Archivo adjunto a la solicitud 2)
        get_or_create(db, Archivo, nombre_interno="evidencia_frenos.jpg", defaults={
            "entidad_tipo": "solicitud",
            "entidad_id": sol_con_tecnico.id,
            "nombre_original": "frenos.jpg",
            "mime_type": "image/jpeg",
            "tamano_bytes": 102400,
            "ruta": f"storage/solicitud/{sol_con_tecnico.id}/evidencia_frenos.jpg",
            "descripcion": "Foto enviada por el cliente",
            "subido_por_id": juan_user.id
        })

        print("\n✅ Seeder oficial actualizado con Bloque E y F exitosamente.")
        print("Base de datos lista con flujo operativo completo de prueba.")

        print("Nota: Todos los usuarios fueron creados con la contraseña '123456'")

    except Exception as e:
        print(f"\n❌ Error durante el seeder: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
