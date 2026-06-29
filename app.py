"""
app.py — Tacho (site de receitas)
Ponto de entrada da aplicação FastAPI.

Instalar dependências:
    pip install fastapi uvicorn jinja2

Rodar:
    uvicorn backend.app:app --reload
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Tacho API", version="1.0.0")

# Arquivos estáticos (css, js, imagens)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Templates HTML
templates = Jinja2Templates(directory="frontend/paginas")


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, summary="Página inicial")
async def home(request: Request):
    """
    Rota raiz — serve a página inicial do site de receitas.
    """
    return templates.TemplateResponse("index.html", {"request": request})
