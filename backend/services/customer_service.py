import sys
from pathlib import Path

# Menghubungkan ke berkas client Supabase di folder root
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from supabase_client import supabase

def get_customer_profile():
    """Mengambil data profil customer yang sedang login saat ini."""
    try:
        response = supabase.table("customer_table").select("*").execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error saat mengambil profil: {e}")
        return None

def update_customer_profile(first_name: str, last_name: str, phone: str, address: str, city: str, state: str, country: str, postal_code: str):
    """Memperbarui data profil customer menggunakan RPC."""
    try:
        user = supabase.auth.get_user()
        if not user or not user.user:
            return {"success": False, "message": "User belum login!"}
        
        user_id = user.user.id

        supabase.rpc("update_profile", {
            "p_id": user_id,
            "p_fname": first_name,
            "p_lname": last_name,
            "p_phone": phone,
            "p_addr": address,
            "p_city": city,
            "p_state": state,
            "p_country": country,
            "p_zip": postal_code
        }).execute()
        
        return {"success": True, "message": "Profil berhasil diperbarui!"}
    except Exception as e:
        return {"success": False, "message": f"Gagal memperbarui profil: {str(e)}"}

