import enum

class TipoUsuario(str, enum.Enum):
    cliente = "cliente"
    empresa = "empresa"

class EstadoUsuario(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    baneado = "baneado"

class EstadoTecnico(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    ocupado = "ocupado"

class MarcaVehiculo(str, enum.Enum):
    nissan = "nissan"
    chevrolet = "chevrolet"
    suzuki = "suzuki"
    toyota = "toyota"
    hyundai = "hyundai"
    kia = "kia"
    ford = "ford"
    otra_marca = "otra_marca"

class DestinatarioNotificacion(str, enum.Enum):
    todos = "todos"
    solo_tecnicos = "solo_tecnicos"
    solo_admin_taller = "solo_admin_taller"

class EstadoNotificacion(str, enum.Enum):
    enviado = "enviado"
    pendiente = "pendiente"
    error = "error"

class EstadoOrganizacion(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"

class EstadoSolicitud(str, enum.Enum):
    pendiente_taller = "pendiente_taller"
    rechazada = "rechazada"
    aceptada = "aceptada"
    tecnico_asignado = "tecnico_asignado"
    en_camino = "en_camino"
    punto_encuentro = "punto_encuentro"
    trabajo_en_proceso = "trabajo_en_proceso"
    finalizada = "finalizada"
    cancelada = "cancelada"

class EstadoAsignacion(str, enum.Enum):
    pendiente = "pendiente"
    aceptada = "aceptada"
    rechazada = "rechazada"

class EstadoDiagnostico(str, enum.Enum):
    borrador = "borrador"
    confirmado = "confirmado"

# --- Enums Bloque F ---

class NivelPrioridad(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"

class FuenteClasificacion(str, enum.Enum):
    ia_local = "ia_local"
    ia_externa = "ia_externa"
    reglas_heuristicas = "reglas_heuristicas"
    manual = "manual"

class EstadoRevisionClasificacion(str, enum.Enum):
    pendiente = "pendiente"
    validada = "validada"
    cuestionada = "cuestionada"
    reclasificada = "reclasificada"

class PropietarioMetodoPago(str, enum.Enum):
    cliente = "cliente"
    sucursal = "sucursal"

class TipoMetodoPago(str, enum.Enum):
    efectivo = "efectivo"
    qr = "qr"
    pasarela_pago = "pasarela_pago"

class EstadoPago(str, enum.Enum):
    pendiente = "pendiente"
    pagado = "pagado"
    verificado = "verificado"
    rechazado = "rechazado"
    cancelado = "cancelado"
