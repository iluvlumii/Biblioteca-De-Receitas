from datetime import date
from pydantic import BaseModel, Field, field_validator

class pessoaEntrada(BaseModel):
    nome_pessoa: str = Field(min_length=1, max_length=150)
    email_pessoa: str = Field(min_length=3, max_length=150)
    senha_pessoa: str = Field(min_length=6)
    datanasc_pessoa: date
    crm_nutricionista: str | None = None

    @field_validator("nome_pessoa")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError(
                "O nome da pessoa não pode ficar vazio."
            )
        return valor

    @field_validator("email_pessoa")
    @classmethod
    def validar_email(cls, valor: str) -> str:
        valor = valor.strip().lower()
        if "@" not in valor:
            raise ValueError("Informe um e-mail válido.")
        return valor

class loginEntrada(BaseModel):
    email_pessoa: str
    senha_pessoa: str

    @field_validator("email_pessoa")
    @classmethod
    def normalizar_email(cls, valor: str) -> str:
        return valor.strip().lower()

class pessoaSaida(BaseModel):
    id_pessoa: int
    nome_pessoa: str
    email_pessoa: str
    datanasc_pessoa: date
    crm_nutricionista: str | None = None