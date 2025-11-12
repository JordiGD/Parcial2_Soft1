"""
Modelos de base de datos SQLAlchemy para API Bebidas
"""
from sqlalchemy import Column, Integer, String, Float, Index
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from .database import Base

class BebidaDB(Base):
    """Modelo de base de datos para bebidas"""
    __tablename__ = "bebidas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    size = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    
    __table_args__ = (
        Index('idx_bebida_name_size', 'name', 'size'),
    )


class BebidaBase(BaseModel):
    """Modelo base para bebidas"""
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la bebida")
    size: str = Field(..., pattern="^(small|medium|large)$", description="Tamaño: small, medium, large")
    price: float = Field(..., gt=0, le=100, description="Precio debe ser positivo y menor a 100")
    
    @validator('name')
    def validate_name(cls, v):
        """Valida el nombre de la bebida"""
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title()
    
    @validator('size')
    def validate_size(cls, v):
        """Valida el tamaño"""
        valid_sizes = ['small', 'medium', 'large']
        if v.lower() not in valid_sizes:
            raise ValueError(f'Tamaño debe ser uno de: {", ".join(valid_sizes)}')
        return v.lower()


class BebidaCreate(BebidaBase):
    """Modelo para crear bebidas"""
    pass


class Bebida(BebidaBase):
    """Modelo completo de bebida con ID"""
    id: int
    
    class Config:
        from_attributes = True


class BebidaRepository:
    """Repositorio para operaciones de bebidas"""
    
    @staticmethod
    def get_all(db: Session) -> List[BebidaDB]:
        """Obtiene todas las bebidas"""
        return db.query(BebidaDB).all()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[BebidaDB]:
        """Busca bebida por nombre (primera coincidencia)"""
        return db.query(BebidaDB).filter(
            BebidaDB.name.ilike(f"%{name}%")
        ).first()
    
    @staticmethod
    def get_by_name_and_size(db: Session, name: str, size: str) -> Optional[BebidaDB]:
        """Busca bebida por nombre y tamaño exactos"""
        return db.query(BebidaDB).filter(
            BebidaDB.name.ilike(name),
            BebidaDB.size == size.lower()
        ).first()
    
    @staticmethod
    def create(db: Session, bebida: BebidaCreate) -> BebidaDB:
        """Crea una nueva bebida"""
        db_bebida = BebidaDB(
            name=bebida.name,
            size=bebida.size,
            price=bebida.price
        )
        db.add(db_bebida)
        db.commit()
        db.refresh(db_bebida)
        return db_bebida
    
    @staticmethod
    def delete_by_id(db: Session, bebida_id: int) -> bool:
        """Elimina bebida por ID"""
        bebida = db.query(BebidaDB).filter(BebidaDB.id == bebida_id).first()
        if bebida:
            db.delete(bebida)
            db.commit()
            return True
        return False
    
    @staticmethod
    def exists_by_name_and_size(db: Session, name: str, size: str) -> bool:
        """Verifica si existe una bebida con ese nombre y tamaño"""
        return db.query(BebidaDB).filter(
            BebidaDB.name.ilike(name),
            BebidaDB.size == size.lower()
        ).first() is not None