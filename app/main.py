from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.api.api_v1 import api_router

# Crea tablas y relaciones si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Gestión de Citas", version="1.0.0")

# CORS - Configuración para desarrollo y producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular dev server
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:4200",  # Angular dev server (127.0.0.1)
        "http://127.0.0.1:3000",  # React dev server (127.0.0.1)
        "*"  # Permite todos los orígenes (para desarrollo)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
    ],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}
