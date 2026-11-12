import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from httpx import RequestError
from postgrest.exceptions import APIError
from controller.pessoa import router as router_pessoa
from controller.motivo_saude import router as router_motivo_saude
from controller.ingrediente import router as router_ingrediente
from controller.categoria import router as router_categoria

logger = logging.getLogger("uvicorn.error")
app = FastAPI(
    title="Biblioteca de receitas - API de pessoas",
    description="CRUD com Supabase por HTTPS.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

app.include_router(router_pessoa)
app.include_router(router_motivo_saude)
app.include_router(router_ingrediente)
app.include_router(router_categoria)

@app.exception_handler(APIError)
async def tratar_erro_supabase(request: Request, erro: APIError):
    logger.error("Erro na operação do Supabase: %s", erro)
    return JSONResponse(
        status_code=502,
        content={"detail": (
            "O Supabase recusou a operação. "
            "Confira a mensagem no terminal."
        )},
    )

@app.exception_handler(RequestError)
async def tratar_erro_rede(request: Request, erro: RequestError):
    logger.error("Falha de comunicação: %s", type(erro).__name__)
    return JSONResponse(
        status_code=503,
        content={"detail": (
            "Não foi possível acessar o Supabase. "
            "Verifique a conexão com a internet."
        )},
    )