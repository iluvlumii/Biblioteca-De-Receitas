"""
Dashboard — Tacho (site de receitas)
Rotas FastAPI que alimentam o painel de métricas.

Instalar dependências:
    pip install fastapi uvicorn

Rodar:
    uvicorn nome_do_projeto.backend.dashboard:app --reload

Endpoints disponíveis:
    GET /dashboard/kpis
    GET /dashboard/acessos-diarios
    GET /dashboard/receitas-populares
    GET /dashboard/buscas-frequentes
    GET /dashboard/salvamentos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
import random

app = FastAPI(title="Tacho Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Em produção: restringir ao domínio do dashboard
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Dados simulados — substituir por queries reais ao banco de dados
# ---------------------------------------------------------------------------

def _gerar_acessos_diarios(dias: int = 30) -> list[dict]:
    """Gera série temporal de acessos dos últimos N dias."""
    hoje = date.today()
    base = 420
    return [
        {
            "data": str(hoje - timedelta(days=dias - i - 1)),
            "visitas": max(80, base + random.randint(-120, 200) + (i * 3)),
        }
        for i in range(dias)
    ]


RECEITAS_MOCK = [
    {"id": 1, "nome": "Macarrão ao alho e azeite",     "categoria": "Massas",    "visualizacoes": 8420, "salvamentos": 1230},
    {"id": 2, "nome": "Frango ao molho de limão",       "categoria": "Carnes",    "visualizacoes": 6910, "salvamentos":  980},
    {"id": 3, "nome": "Bolo de banana simples",         "categoria": "Doces",     "visualizacoes": 6340, "salvamentos": 1540},
    {"id": 4, "nome": "Salada mediterrânea",            "categoria": "Saladas",   "visualizacoes": 4870, "salvamentos":  620},
    {"id": 5, "nome": "Risoto de cogumelos",            "categoria": "Massas",    "visualizacoes": 4210, "salvamentos":  870},
    {"id": 6, "nome": "Omelete de legumes",             "categoria": "Café",      "visualizacoes": 3980, "salvamentos":  490},
    {"id": 7, "nome": "Feijão tropeiro",                "categoria": "Brasileira","visualizacoes": 3750, "salvamentos":  710},
    {"id": 8, "nome": "Vitamina de abacate",            "categoria": "Bebidas",   "visualizacoes": 3100, "salvamentos":  380},
]

BUSCAS_MOCK = [
    {"termo": "frango",         "contagem": 2840},
    {"termo": "bolo simples",   "contagem": 2310},
    {"termo": "sem glúten",     "contagem": 1980},
    {"termo": "macarrão",       "contagem": 1760},
    {"termo": "30 minutos",     "contagem": 1540},
    {"termo": "vegetariano",    "contagem": 1230},
    {"termo": "café da manhã",  "contagem":  980},
    {"termo": "sobremesa fácil","contagem":  870},
]

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/dashboard/kpis", summary="KPIs principais do período")
def get_kpis():
    """
    Retorna os indicadores-chave do site:
    - visitas totais (últimos 30 dias)
    - total de receitas publicadas
    - buscas realizadas
    - salvamentos
    """
    acessos = _gerar_acessos_diarios(30)
    total_visitas = sum(a["visitas"] for a in acessos)

    return {
        "periodo": "últimos 30 dias",
        "visitas_totais":      total_visitas,
        "receitas_publicadas": 412,
        "buscas_realizadas":   18_340,
        "salvamentos_totais":   9_870,
        "variacao": {
            "visitas":     "+12%",
            "buscas":       "+8%",
            "salvamentos": "+21%",
        },
    }


@app.get("/dashboard/acessos-diarios", summary="Série temporal de acessos")
def get_acessos_diarios(dias: int = 30):
    """
    Retorna acessos por dia nos últimos N dias (padrão: 30).
    Útil para gráfico de linha/área.
    """
    if dias < 1 or dias > 365:
        dias = 30
    return {"dias": dias, "serie": _gerar_acessos_diarios(dias)}


@app.get("/dashboard/receitas-populares", summary="Receitas mais acessadas")
def get_receitas_populares(limit: int = 8):
    """
    Retorna as receitas com mais visualizações no período,
    ordenadas de forma decrescente.
    """
    dados = sorted(RECEITAS_MOCK, key=lambda r: r["visualizacoes"], reverse=True)
    return {"receitas": dados[:limit]}


@app.get("/dashboard/buscas-frequentes", summary="Termos mais buscados")
def get_buscas_frequentes(limit: int = 8):
    """
    Retorna os termos de busca mais digitados pelos usuários,
    ordenados por frequência.
    """
    dados = sorted(BUSCAS_MOCK, key=lambda b: b["contagem"], reverse=True)
    return {"buscas": dados[:limit]}


@app.get("/dashboard/salvamentos", summary="Salvamentos por categoria")
def get_salvamentos():
    """
    Agrupa os salvamentos por categoria de receita.
    """
    por_categoria: dict[str, int] = {}
    for r in RECEITAS_MOCK:
        cat = r["categoria"]
        por_categoria[cat] = por_categoria.get(cat, 0) + r["salvamentos"]

    resultado = [
        {"categoria": k, "salvamentos": v}
        for k, v in sorted(por_categoria.items(), key=lambda x: x[1], reverse=True)
    ]
    return {"salvamentos_por_categoria": resultado}
