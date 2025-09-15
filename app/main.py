from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.api.api_v1 import api_router

# Crea tablas y relaciones si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Gestión de Citas", version="1.0.0")

# CORS (ajusta origins según tu frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cambia por ["http://localhost:4200"] si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}
