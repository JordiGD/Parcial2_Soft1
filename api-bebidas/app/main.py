"""
API de Bebidas - VirtualCoffee
FastAPI con PostgreSQL y SQLAlchemy
"""
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db, Base
from .models import Bebida, BebidaCreate, BebidaRepository, BebidaDB

app = FastAPI(
    title="VirtualCoffee - API Bebidas",
    description="API para gestionar el menú de bebidas",
    version="2.0.0"
)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Endpoint raíz - Health check"""
    return {
        "message": "API de Bebidas - VirtualCoffee",
        "version": "2.0.0",
        "status": "active",
        "database": "PostgreSQL"
    }


@app.get("/menu", response_model=List[Bebida])
def get_menu(db: Session = Depends(get_db)):
    """Obtiene el menú completo de bebidas"""
    try:
        bebidas_db = BebidaRepository.get_all(db)
        return [Bebida.model_validate(bebida) for bebida in bebidas_db]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el menú: {str(e)}"
        )


@app.get("/menu/{name}", response_model=Bebida)
def get_bebida_by_name(name: str, db: Session = Depends(get_db)):
    """Busca una bebida por nombre"""
    try:
        bebida_db = BebidaRepository.get_by_name(db, name)
        if not bebida_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bebida '{name}' no encontrada en el menú"
            )
        return Bebida.model_validate(bebida_db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar bebida: {str(e)}"
        )


@app.post("/menu", response_model=Bebida, status_code=status.HTTP_201_CREATED)
def create_bebida(bebida: BebidaCreate, db: Session = Depends(get_db)):
    """Crea una nueva bebida en el menú"""
    try:
        if BebidaRepository.exists_by_name_and_size(db, bebida.name, bebida.size):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una bebida '{bebida.name}' con tamaño '{bebida.size}'"
            )
        
        nueva_bebida_db = BebidaRepository.create(db, bebida)
        return Bebida.model_validate(nueva_bebida_db)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear bebida: {str(e)}"
        )


@app.delete("/menu/{bebida_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bebida(bebida_id: int, db: Session = Depends(get_db)):
    """Elimina una bebida del menú"""
    try:
        if not BebidaRepository.delete_by_id(db, bebida_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bebida con ID {bebida_id} no encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar bebida: {str(e)}"
        )

@app.post("/menu/seed", status_code=status.HTTP_201_CREATED)
def seed_menu(db: Session = Depends(get_db)):
    """Inicializa el menú con bebidas de ejemplo"""
    bebidas_ejemplo = [
        {"name": "Latte", "size": "small", "price": 2.50},
        {"name": "Latte", "size": "medium", "price": 3.50},
        {"name": "Latte", "size": "large", "price": 4.50},
        {"name": "Espresso", "size": "small", "price": 2.00},
        {"name": "Espresso", "size": "medium", "price": 2.75},
        {"name": "Cappuccino", "size": "medium", "price": 3.25},
        {"name": "Cappuccino", "size": "large", "price": 4.00},
        {"name": "Americano", "size": "medium", "price": 2.50},
        {"name": "Americano", "size": "large", "price": 3.25},
        {"name": "Mocha", "size": "large", "price": 4.75},
    ]
    
    created_count = 0
    for bebida_data in bebidas_ejemplo:
        try:
            if not BebidaRepository.exists_by_name_and_size(
                db, bebida_data["name"], bebida_data["size"]
            ):
                bebida_create = BebidaCreate(**bebida_data)
                BebidaRepository.create(db, bebida_create)
                created_count += 1
        except Exception:
            continue
    
    return {
        "message": f"Menú inicializado con {created_count} bebidas",
        "total_bebidas": len(BebidaRepository.get_all(db))
    }