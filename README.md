# Mi Primera API FastAPI - Bootcamp

**👤 Desarrollador**: allan duvan caro castillo
**📧 Email**: Wuelcom@users.noreply.github.com.
**  Privacidad**: Email configurado según mejores prácticas de GitHub
** 📅 Fecha de creación**: 2025-08-13 13:56:39
**📂 Ruta del proyecto**: /c/Users/Aprendiz/desarrollo-personal/allan-caro-bootcamp/mi-primera-api-fastapi
**💻 Equipo de trabajo**: BOGDFPCGMP5717

## 🔧 Configuración Local

Este proyecto está configurado para trabajo en equipo compartido:

- **Entorno virtual aislado**: `venv-personal/`
- **Configuración Git local**: Solo para este proyecto
- **Dependencias independientes**: No afecta otras instalaciones

## 🚀 Instalación y Ejecución

```bash
# 1. Activar entorno virtual personal
source venv-personal/bin/activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Ejecutar servidor de desarrollo
uvicorn main:app --reload --port 8000
```

## 📝 Notas del Desarrollador

- **Configuración Git**: Local únicamente, no afecta configuración global
- **Email de GitHub**: Configurado con email privado para proteger información personal
- **Entorno aislado**: Todas las dependencias en venv-personal/
- **Puerto por defecto**: 8000 (cambiar si hay conflictos)
- **Estado del bootcamp**: Semana 1 - Configuración inicial

## 🛠️ Troubleshooting Personal

- Si el entorno virtual no se activa: `rm -rf venv-personal && python3 -m venv venv-personal`
- Si hay conflictos de puerto: cambiar --port en uvicorn
- Si Git no funciona: verificar `git config user.name` y `git config user.email`
- Si necesitas cambiar el email: usar el email privado de GitHub desde Settings → Emails

## ¿Qué hace?

API mejorada con validación automática de datos y type hints.

## Nuevos Features (Semana 2)

- ✅ Type hints en todas las funciones
- ✅ Validación automática con Pydantic
- ✅ Endpoint POST para crear datos
- ✅ Parámetros de ruta (ejemplo: /products/{id})
- ✅ Búsqueda con parámetros query

## ¿Cómo ejecutar?

```bash
pip install fastapi pydantic uvicorn
uvicorn main:app --reload
```

