cat << 'EOF' > main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models, schemas

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas sincronizadas no Supabase!")
    except Exception as e:
        print(f"⚠️ Aviso no arranque: {e}")
    yield

app = FastAPI(title="API FastAPI Supabase", lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "ok", "mensagem": "API e Supabase ativos!"}

@app.post("/items/", response_model=schemas.ItemResponse)
def criar_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(nome=item.nome, descricao=item.descricao)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[schemas.ItemResponse])
def listar_itens(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
EOF