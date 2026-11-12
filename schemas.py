from pydantic import BaseModel, ConfigDict


class CategoriaCreate(BaseModel):
    nome: str


class CategoriaResponse(BaseModel):
    id_categoria: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class ProdutoCreate(BaseModel):
    nome: str
    id_categoria: int


class ProdutoResponse(BaseModel):
    id_produto: int
    nome: str
    categoria: str