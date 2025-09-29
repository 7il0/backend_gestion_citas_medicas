# CRUD Endpoints Completados

Este documento describe los endpoints CRUD completos implementados para las entidades **Pacientes** y **Médicos**.

## 🏥 Pacientes (`/api/v1/pacientes`)

### ✅ Operaciones CRUD Completas

| Método | Endpoint | Descripción | Respuesta |
|--------|----------|-------------|-----------|
| `POST` | `/pacientes` | Crear nuevo paciente | `201 Created` |
| `GET` | `/pacientes` | Listar todos los pacientes (con búsqueda) | `200 OK` |
| `GET` | `/pacientes/{id}` | Obtener paciente por ID | `200 OK` |
| `PUT` | `/pacientes/{id}` | Actualizar paciente | `200 OK` |
| `DELETE` | `/pacientes/{id}` | Eliminar paciente | `204 No Content` |

### 📝 Schemas

- **PatientCreate**: Para crear pacientes
- **PatientUpdate**: Para actualizar pacientes (campos opcionales)
- **PatientOut**: Para respuestas

### 🔍 Funcionalidades Especiales

- **Búsqueda**: El endpoint GET `/pacientes?q=texto` permite buscar por nombre, email o DNI
- **Validaciones**: Email y DNI únicos
- **Actualización parcial**: Solo se actualizan los campos enviados

### 📋 Ejemplo de Uso

```bash
# Crear paciente
curl -X POST "http://localhost:8000/api/v1/pacientes" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Pérez",
    "email": "juan@email.com",
    "phone": "123456789",
    "dni": "12345678A"
  }'

# Obtener paciente por ID
curl -X GET "http://localhost:8000/api/v1/pacientes/1"

# Actualizar paciente
curl -X PUT "http://localhost:8000/api/v1/pacientes/1" \
  -H "Content-Type: application/json" \
  -d '{"phone": "987654321"}'

# Eliminar paciente
curl -X DELETE "http://localhost:8000/api/v1/pacientes/1"
```

---

## 👨‍⚕️ Médicos (`/api/v1/medicos`)

### ✅ Operaciones CRUD Completas

| Método | Endpoint | Descripción | Respuesta |
|--------|----------|-------------|-----------|
| `POST` | `/medicos` | Crear nuevo médico | `201 Created` |
| `GET` | `/medicos` | Listar todos los médicos | `200 OK` |
| `GET` | `/medicos/{id}` | Obtener médico por ID | `200 OK` |
| `PUT` | `/medicos/{id}` | Actualizar médico | `200 OK` |
| `DELETE` | `/medicos/{id}` | Eliminar médico | `204 No Content` |
| `GET` | `/medicos/{id}/disponibilidad` | Ver disponibilidad (endpoint especial) | `200 OK` |

### 📝 Schemas

- **DoctorCreate**: Para crear médicos
- **DoctorUpdate**: Para actualizar médicos (campos opcionales)
- **DoctorOut**: Para respuestas

### 🔍 Funcionalidades Especiales

- **Validación de horarios**: work_end_hour debe ser mayor que work_start_hour
- **Disponibilidad**: Endpoint especial para consultar slots disponibles
- **Actualización parcial**: Solo se actualizan los campos enviados

### 📋 Ejemplo de Uso

```bash
# Crear médico
curl -X POST "http://localhost:8000/api/v1/medicos" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Dr. María González",
    "specialty_id": 1,
    "work_start_hour": 8,
    "work_end_hour": 16,
    "slot_minutes": 30
  }'

# Obtener médico por ID
curl -X GET "http://localhost:8000/api/v1/medicos/1"

# Actualizar médico
curl -X PUT "http://localhost:8000/api/v1/medicos/1" \
  -H "Content-Type: application/json" \
  -d '{"slot_minutes": 45}'

# Ver disponibilidad
curl -X GET "http://localhost:8000/api/v1/medicos/1/disponibilidad?fecha=2024-01-15"

# Eliminar médico
curl -X DELETE "http://localhost:8000/api/v1/medicos/1"
```

---

## 🚀 Cómo Probar

1. **Iniciar el servidor**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Ejecutar tests automatizados**:
   ```bash
   python test_crud.py
   ```

3. **Usar la documentación interactiva**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## ✨ Resumen de Mejoras Implementadas

### Para Pacientes:
- ✅ GET por ID
- ✅ PUT (actualización)
- ✅ DELETE
- ✅ Schema PatientUpdate
- ✅ Validaciones de unicidad en actualizaciones

### Para Médicos:
- ✅ GET por ID  
- ✅ PUT (actualización)
- ✅ DELETE
- ✅ Schema DoctorUpdate
- ✅ Validaciones de horarios en actualizaciones

### Características Técnicas:
- ✅ Manejo de errores HTTP apropiados (404, 409, 400)
- ✅ Validaciones de negocio
- ✅ Actualización parcial de campos
- ✅ Respuestas consistentes
- ✅ Documentación automática con FastAPI

¡Ahora tienes CRUD completo para las entidades Pacientes y Médicos! 🎉
