from fastapi import APIRouter
from app.routers import auth, specialties, appointment_types, patients, doctors, appointments

api_router = APIRouter()

# Rutas públicas (sin autenticación)
api_router.include_router(auth.router)

# Rutas protegidas (requieren autenticación)
api_router.include_router(specialties.router)
api_router.include_router(appointment_types.router)
api_router.include_router(patients.router)
api_router.include_router(doctors.router)
api_router.include_router(appointments.router)