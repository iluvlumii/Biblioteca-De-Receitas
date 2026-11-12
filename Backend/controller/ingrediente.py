from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.ingrediente import ingredienteEntrada, ingredienteSaida

router = APIRouter(prefix="/ingrediente", tags=["Ingrediente"])

# Cadastrar: o banco gera o ID.
@router.post("", response_model=ingredienteSaida,
             status_code=status.HTTP_201_CREATED)
def cadastrar_ingrediente(dados: ingredienteEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("ingrediente")
        .insert(conteudo)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(
            status_code=502,
            detail="O Supabase não retornou o ingrediente cadastrado.",
        )
    return resposta.data[0]

# Listar os registros, ordenados pelo ID.
@router.get("", response_model=list[ingredienteSaida])
def listar_ingredientes():
    resposta = (
        supabase.table("ingrediente")
        .select("*")
        .order("id_ingrediente")
        .execute()
    )
    return resposta.data

@router.get("/{id_ingrediente}", response_model=ingredienteSaida)
def consultar_ingrediente(id_ingrediente: int):
    resposta = (
        supabase.table("ingrediente")
        .select("*")
        .eq("id_ingrediente", id_ingrediente)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Ingrediente não encontrado.")
    return resposta.data[0]

@router.put("/{id_ingrediente}", response_model=ingredienteSaida)
def atualizar_ingrediente(id_ingrediente: int, dados: ingredienteEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("ingrediente")
        .update(conteudo)
        .eq("id_ingrediente", id_ingrediente)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Ingrediente não encontrado.")
    return resposta.data[0]

@router.delete("/{id_ingrediente}",
               status_code=status.HTTP_204_NO_CONTENT)
def excluir_ingrediente(id_ingrediente: int):
    resposta = (
        supabase.table("ingrediente")
        .delete()
        .eq("id_ingrediente", id_ingrediente)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Ingrediente não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)