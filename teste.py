import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if url and key:
    supabase = create_client(url, key)
    print("✅ Conectado ao Supabase via API com sucesso!")
else:
    print("❌ Variáveis não encontradas no arquivo .env")