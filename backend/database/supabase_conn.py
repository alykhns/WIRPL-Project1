import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Memuat variabel lingkungan dari berkas .env (pastikan file .env ada di root project)
# Kita gunakan path absolut atau asumsikan dijalankan dari root
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError(
        "Kredensial Supabase gagal dimuat! Pastikan berkas .env sudah "
        "berisi SUPABASE_URL serta SUPABASE_KEY."
    )

supabase: Client = create_client(url, key)
