# Reglas del proyecto

Eres un experto en FastAPI y Angular trabajando en un entorno local.

## Arquitectura obligatoria
El proyecto sigue arquitectura por capas:
- routes: definición de endpoints
- controllers: manejo de requests y responses
- services: lógica de negocio
- repositories: acceso a datos
- models: entidades y esquemas

## Reglas estrictas
- No mezclar capas.
- No poner lógica de negocio en routes ni controllers.
- No acceder a base de datos desde controllers.
- El acceso a datos debe pasar por repositories.
- Los services orquestan la lógica.
- Respetar modularidad, tipado y mantenibilidad.
- Antes de hacer cambios grandes, proponer el plan.
- Al crear código nuevo, seguir la estructura existente del proyecto.
- Evitar archivos innecesarios.
- No renombrar carpetas base sin indicación explícita.
- Antes de modificar archivos, indicar cuáles serán tocados y por qué.
- No implementar funcionalidades fuera de la fase actual.
- No asumir reglas de negocio no definidas.
- No crear código provisional si no se solicita explícitamente.

## Contexto técnico
- Backend principal: FastAPI
- Frontend: Angular
- Entorno: local
- Futuro uso de IA local: Ollama como servicio externo del proyecto
- Objetivo: construir una plataforma inteligente de atención de emergencias vehiculares

## Contexto funcional del sistema
El sistema conecta clientes con talleres mecánicos para atender emergencias vehiculares.

La plataforma web está orientada a talleres, empresas, sucursales y técnicos.
La aplicación móvil está orientada al cliente que reporta incidentes.

El sistema debe permitir:
- gestión de usuarios
- gestión de roles y permisos
- gestión de empresas/talleres
- gestión de sucursales
- gestión de técnicos
- gestión de vehículos
- gestión de suscripciones
- posteriormente, gestión de incidentes, clasificación IA, asignación inteligente, diagnóstico y cierre del servicio

## Roles del sistema
Existen los siguientes roles de usuario:

- SuperUser:
  - puede cambiar roles y permisos
  - puede eliminar o editar usuarios de tipo cliente
  - tiene control total del sistema

- Moderador:
  - puede gestionar módulos como el SuperUser
  - no puede cambiar roles ni permisos
  - respecto a usuarios, solo puede banear usuarios

- Administrador de Taller:
  - registra la empresa
  - registra sucursales
  - registra técnicos
  - configura disponibilidad del taller

- Encargado de Taller:
  - evalúa solicitudes recibidas
  - acepta o rechaza trabajos
  - asigna un técnico disponible a una orden de servicio

- Tecnico:
  - atiende servicios
  - acepta o rechaza asignaciones
  - realiza el diagnóstico
  - cambia estados operativos del trabajo

- Cliente:
  - reporta incidentes

Si un usuario tiene rol Tecnico, debe existir su entidad o subtabla relacionada de técnico.
Si el usuario no tiene ese rol, no debe generarse dicha entidad especializada.

## Reglas de suscripción
- El usuario final tiene una suscripción base.
- Las suscripciones avanzadas aplican al taller o empresa.
- Las suscripciones del taller afectan la cantidad de sucursales permitidas.
- Las suscripciones del taller afectan la cantidad de técnicos permitidos.

## Fase actual
Estamos trabajando únicamente en la Fase 1.

### Fase 1 incluye:
- usuarios
- roles
- permisos
- rol_usuario
- rol_permiso
- empresas
- sucursales
- tecnicos
- suscripciones
- suscripcion_usuario
- vehiculos
- catálogos y estados base
- formularios base del sistema web

## Prohibido en esta fase
No implementar todavía:
- incidentes
- asignaciones
- clasificación IA
- diagnóstico
- pagos
- comisiones
- flujo operativo del servicio
- notificaciones en tiempo real
- lógica mobile del cliente

## Forma de trabajo esperada
Cuando se solicite una tarea:
1. analizar primero el impacto
2. identificar si pertenece a la fase actual
3. proponer un plan corto
4. indicar qué archivos se crearán o modificarán
5. implementar respetando arquitectura
6. resumir qué cambió al finalizar

## Prioridades
- código limpio
- rapidez
- cambios seguros sobre archivos reales
- bajo acoplamiento
- escalabilidad
- claridad de negocio
- respeto estricto de la fase actual