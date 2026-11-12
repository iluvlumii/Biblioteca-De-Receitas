from pydantic import BaseModel, Field, field_validator

class categoriaEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=150)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError(
                "O nome da categoria não pode ficar vazio."
            )
        return valor

class categoriaSaida(categoriaEntrada):
    id_categoria: int