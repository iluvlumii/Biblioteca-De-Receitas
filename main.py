from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API do Projeto Integrador",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def inicio():
    return {"mensagem": "API funcionando"}


@app.post(
    "/categorias",
    response_model=schemas.CategoriaResponse
)
def criar_categoria(
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db)
):
    nova_categoria = models.Categoria(
        nome=categoria.nome
    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


@app.get(
    "/categorias",
    response_model=list[schemas.CategoriaResponse]
)
def listar_categorias(
    db: Session = Depends(get_db)
):
    return db.query(models.Categoria).all()


@app.post(
    "/produtos",
    response_model=schemas.ProdutoResponse
)
def criar_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db)
):
    categoria = (
        db.query(models.Categoria)
        .filter(
            models.Categoria.id_categoria
            == produto.id_categoria
        )
        .first()
    )

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    novo_produto = models.Produto(
        nome=produto.nome,
        id_categoria=produto.id_categoria
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return {
        "id_produto": novo_produto.id_produto,
        "nome": novo_produto.nome,
        "categoria": categoria.nome
    }


@app.get(
    "/produtos",
    response_model=list[schemas.ProdutoResponse]
)
def listar_produtos(
    db: Session = Depends(get_db)
):
    produtos = db.query(models.Produto).all()

    return [
        {
            "id_produto": produto.id_produto,
            "nome": produto.nome,
            "categoria": produto.categoria.nome
        }
        for produto in produtos
    ]