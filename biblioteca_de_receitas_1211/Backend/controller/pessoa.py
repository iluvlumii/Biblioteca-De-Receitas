import hashlib
import hmac
import secrets
from fastapi import APIRouter, HTTPException, Response, status
from postgrest.exceptions import APIError
from database import supabase
from models.pessoa import loginEntrada, pessoaEntrada, pessoaSaida

router = APIRouter(prefix="/pessoa", tags=["Pessoa"])

ITERACOES = 200_000

def gerar_hash(senha: str) -> str:
    sal = secrets.token_hex(16)
    resumo = hashlib.pbkdf2_hmac(
        "sha256", senha.encode(), sal.encode(), ITERACOES
    ).hex()
    return f"{sal}${resumo}"

def conferir_senha(senha: str, guardado: str) -> bool:
    try:
        sal, resumo = guardado.split("$", 1)
    except ValueError:
        return False
    novo = hashlib.pbkdf2_hmac(
        "sha256", senha.encode(), sal.encode(), ITERACOES
    ).hex()
    return hmac.compare_digest(novo, resumo)

def preparar_conteudo(dados: pessoaEntrada) -> dict:
    conteudo = dados.model_dump(mode="json")
    conteudo["senha_pessoa"] = gerar_hash(conteudo["senha_pessoa"])
    return conteudo

# Cadastrar: o banco gera o ID.
@router.post("", response_model=pessoaSaida,
             status_code=status.HTTP_201_CREATED)
def cadastrar_pessoa(dados: pessoaEntrada):
    conteudo = preparar_conteudo(dados)
    try:
        resposta = (
            supabase.table("pessoa")
            .insert(conteudo)
            .execute()
        )
    except APIError as erro:
        if getattr(erro, "code", None) == "23505":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este e-mail já está cadastrado.",
            )
        raise
    if not resposta.data:
        raise HTTPException(
            status_code=502,
            detail="O Supabase não retornou a pessoa cadastrada.",
        )
    return resposta.data[0]

# Entrar: confere e-mail e senha.
@router.post("/login", response_model=pessoaSaida)
def entrar(dados: loginEntrada):
    resposta = (
        supabase.table("pessoa")
        .select("*")
        .eq("email_pessoa", dados.email_pessoa)
        .execute()
    )
    if not resposta.data or not conferir_senha(
        dados.senha_pessoa, resposta.data[0]["senha_pessoa"]
    ):
        raise HTTPException(401, "E-mail ou senha incorretos.")
    return resposta.data[0]

# Listar os registros acessíveis, ordenados pelo ID.
@router.get("", response_model=list[pessoaSaida])
def listar_pessoas():
    resposta = (
        supabase.table("pessoa")
        .select("*")
        .order("id_pessoa")
        .execute()
    )
    return resposta.data

@router.get("/{id_pessoa}", response_model=pessoaSaida)
def consultar_pessoa(id_pessoa: int):
    resposta = (
        supabase.table("pessoa")
        .select("*")
        .eq("id_pessoa", id_pessoa)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Pessoa não encontrada.")
    return resposta.data[0]

@router.put("/{id_pessoa}", response_model=pessoaSaida)
def atualizar_pessoa(id_pessoa: int, dados: pessoaEntrada):
    conteudo = preparar_conteudo(dados)
    resposta = (
        supabase.table("pessoa")
        .update(conteudo)
        .eq("id_pessoa", id_pessoa)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Pessoa não encontrada.")
    return resposta.data[0]

@router.delete("/{id_pessoa}",
               status_code=status.HTTP_204_NO_CONTENT)
def excluir_pessoa(id_pessoa: int):
    resposta = (
        supabase.table("pessoa")
        .delete()
        .eq("id_pessoa", id_pessoa)
        .execute()
    )
    if not resposta.data:
        raise HTTPException(404, "Pessoa não encontrada.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
