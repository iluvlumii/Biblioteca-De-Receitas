from pydantic import BaseModel, Field, field_validator

class ingredienteEntrada(BaseModel):
    nome_ingrediente: str = Field(min_length=1, max_length=150)
    unidade_padrao: str = Field(min_length=1, max_length=50)

    @field_validator("nome_ingrediente", "unidade_padrao")
    @classmethod
    def validar_texto(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError(
                "O campo não pode ficar vazio."
            )
        return valor

class ingredienteSaida(ingredienteEntrada):
    id_ingrediente: int