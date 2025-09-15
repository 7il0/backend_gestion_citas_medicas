from fastapi import APIRouter
from app.routers import specialties, appointment_types, patients, doctors, appointments

api_router = APIRouter()
api_router.include_router(specialties.router)
api_router.include_router(appointment_types.router)
api_router.include_router(patients.router)
api_router.include_router(doctors.router)
api_router.include_router(appointments.router)  