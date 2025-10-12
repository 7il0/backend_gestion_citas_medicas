from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.api.api_v1 import api_router

# Importar todos los modelos para que se creen las tablas
from app.models import user, patient, doctor, specialty, appointment_type, appointment

# Crea tablas y relaciones si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Gestión de Citas", version="1.0.0")

# CORS - Configuración para desarrollo y producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}
