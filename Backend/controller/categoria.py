from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.categoria import categoriaEntrada, categoriaSaida

router = APIRouter(prefix="/categoria", tags=["Categoria"])

# Cadastrar: o banco gera o ID (precisa do Identity ativado).
@router.post("", response_model=categoriaSaida,
             status_code=status.HTTP_201_CREATED)
def cadastrar_categoria(dados: categoriaEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("categoria")
        .insert(conteudo)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(
            status_code=502,
            detail="O Supabase não retornou a categoria cadastrada.",
        )
    return resposta.data[0]

# Listar os registros, ordenados pelo ID.
@router.get("", response_model=list[categoriaSaida])
def listar_categorias():
    resposta = (
        supabase.table("categoria")
        .select("*")
        .order("id_categoria")
        .execute()
    )
    return resposta.data

@router.get("/{id_categoria}", response_model=categoriaSaida)
def consultar_categoria(id_categoria: int):
    resposta = (
        supabase.table("categoria")
        .select("*")
        .eq("id_categoria", id_categoria)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Categoria não encontrada.")
    return resposta.data[0]

@router.put("/{id_categoria}", response_model=categoriaSaida)
def atualizar_categoria(id_categoria: int, dados: categoriaEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("categoria")
        .update(conteudo)
        .eq("id_categoria", id_categoria)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Categoria não encontrada.")
    return resposta.data[0]

@router.delete("/{id_categoria}",
               status_code=status.HTTP_204_NO_CONTENT)
def excluir_categoria(id_categoria: int):
    resposta = (
        supabase.table("categoria")
        .delete()
        .eq("id_categoria", id_categoria)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Categoria não encontrada.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)