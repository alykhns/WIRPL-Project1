import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Memuat variabel lingkungan dari berkas .env
load_dotenv()

# 2. Mengambil URL dan API Key anon dari .env
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# 3. Validasi untuk memastikan kredensial tidak kosong
if not url or not key:
    raise ValueError(
        "Kredensial Supabase gagal dimuat! Pastikan berkas .env sudah "
        "berada di folder root dan berisi SUPABASE_URL serta SUPABASE_KEY."
    )

# 4. Inisialisasi client Supabase yang akan digunakan di seluruh halaman aplikasi
supabase: Client = create_client(url, key)