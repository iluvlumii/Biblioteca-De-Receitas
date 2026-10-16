from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    produtos = relationship(
        "Produto",
        back_populates="categoria"
    )


class Produto(Base):
    __tablename__ = "produto"

    id_produto = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(150),
        nullable=False
    )

    id_categoria = Column(
        Integer,
        ForeignKey("categoria.id_categoria"),
        nullable=False
    )

    categoria = relationship(
        "Categoria",
        back_populates="produtos"
    )

