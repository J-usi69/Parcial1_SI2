import enum

class TipoUsuario(str, enum.Enum):
    cliente = "Cliente"
    empresa = "Empresa"

class EstadoUsuario(str, enum.Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    baneado = "Baneado"

class EstadoTecnico(str, enum.Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    ocupado = "Ocupado"

class MarcaVehiculo(str, enum.Enum):
    nissan = "Nissan"
    chevrolet = "Chevrolet"
    suzuki = "Suzuki"
    toyota = "Toyota"
    hyundai = "Hyundai"
    kia = "Kia"
    ford = "Ford"
    otra_marca = "Otra Marca"

class DestinatarioNotificacion(str, enum.Enum):
    todos = "Todos"
    solo_tecnicos = "Solo Técnicos"
    solo_admin_taller = "Solo Administrador de Taller"

class EstadoNotificacion(str, enum.Enum):
    enviado = "enviado"
    pendiente = "pendiente"
    error = "error"

class EstadoOrganizacion(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
