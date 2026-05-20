import sys
from pathlib import Path

# Menghubungkan ke berkas client Supabase di folder root
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from supabase_client import supabase

def process_checkout(payment_method: str, shipping_address: str):
    """
    Memproses checkout semua barang yang ada di keranjang.
    Fungsi ini memanggil Stored Procedure 'execute_checkout' di database 
    agar prosesnya otomatis, aman dari race condition, dan transaksional.
    """
    try:
        user = supabase.auth.get_user()
        if not user or not user.user:
            return {"success": False, "message": "Silakan login terlebih dahulu untuk checkout!"}
        
        user_id = user.user.id

        # Memanggil fungsi RPC (Remote Procedure Call) di Supabase
        # Asumsi parameter di SQL Anda dinamakan p_user_id, p_payment_method, p_shipping_address
        response = supabase.rpc("execute_checkout", {
            "p_user_id": user_id,
            "p_payment_method": payment_method,
            "p_shipping_address": shipping_address
        }).execute()
        
        return {"success": True, "message": "Checkout berhasil! Pesanan Anda sedang diproses."}
    
    except Exception as e:
        print(f"Error saat checkout: {e}")
        return {"success": False, "message": f"Checkout gagal: {str(e)}"}

def get_order_history():
    """Mengambil riwayat pesanan milik user yang sedang login."""
    try:
        # Karena RLS aktif di order_table, kita cukup 'select *'
        # Supabase akan otomatis hanya memberikan data milik user ini.
        response = supabase.table("order_table").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error mengambil riwayat pesanan: {e}")
        return []

def update_order_status(order_id: int, new_status: str):
    """
    Mengubah status pesanan (contoh: dari 'Pending' menjadi 'Dikirim' atau 'Selesai').
    Biasanya fungsi ini diakses di halaman admin/seller.
    """
    try:
        supabase.table("order_table") \
            .update({"status": new_status}) \
            .eq("order_id", order_id) \
            .execute()
        return {"success": True, "message": f"Status pesanan berhasil diubah menjadi {new_status}!"}
    except Exception as e:
        print(f"Error update status pesanan: {e}")
        return {"success": False, "message": f"Gagal mengubah status: {str(e)}"}
