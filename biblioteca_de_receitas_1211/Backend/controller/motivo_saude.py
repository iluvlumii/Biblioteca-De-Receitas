from fastapi import APIRouter, HTTPException, Response, status
from database import supabase
from models.motivo_saude import motivoSaudeEntrada, motivoSaudeSaida

router = APIRouter(prefix="/motivo-saude", tags=["Motivo de saúde"])

# Cadastrar: o banco gera o ID.
@router.post("", response_model=motivoSaudeSaida,
             status_code=status.HTTP_201_CREATED)
def cadastrar_motivo(dados: motivoSaudeEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("motivo_saude")
        .insert(conteudo)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(
            status_code=502,
            detail="O Supabase não retornou o motivo cadastrado.",
        )
    return resposta.data[0]

@router.get("", response_model=list[motivoSaudeSaida])
def listar_motivos():
    resposta = (
        supabase.table("motivo_saude")
        .select("*")
        .order("id_motivo")
        .execute()
    )
    return resposta.data

@router.get("/{id_motivo}", response_model=motivoSaudeSaida)
def consultar_motivo(id_motivo: int):
    resposta = (
        supabase.table("motivo_saude")
        .select("*")
        .eq("id_motivo", id_motivo)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Motivo não encontrado.")
    return resposta.data[0]

@router.put("/{id_motivo}", response_model=motivoSaudeSaida)
def atualizar_motivo(id_motivo: int, dados: motivoSaudeEntrada):
    conteudo = dados.model_dump(mode="json")
    resposta = (
        supabase.table("motivo_saude")
        .update(conteudo)
        .eq("id_motivo", id_motivo)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Motivo não encontrado.")
    return resposta.data[0]

@router.delete("/{id_motivo}",
               status_code=status.HTTP_204_NO_CONTENT)
def excluir_motivo(id_motivo: int):
    resposta = (
        supabase.table("motivo_saude")
        .delete()
        .eq("id_motivo", id_motivo)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Motivo não encontrado.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)