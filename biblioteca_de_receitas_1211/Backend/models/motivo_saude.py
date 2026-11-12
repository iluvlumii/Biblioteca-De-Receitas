from pydantic import BaseModel, Field, field_validator

class motivoSaudeEntrada(BaseModel):
    nome_motivo: str = Field(min_length=1, max_length=150)

    @field_validator("nome_motivo")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError(
                "O do não pode ficar vazio."
            )
        return valor

class motivoSaudeSaida(motivoSaudeEntrada):
    id_motivo: int