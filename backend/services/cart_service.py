import sys
from pathlib import Path

# Naik 3 tingkat dari cart_service.py -> services -> backend -> root folder
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from supabase_client import supabase

def get_cart_items():
    """Mengambil semua produk yang ada di keranjang belanja user yang sedang login."""
    try:
        # Mengambil data dari cart_table beserta info detail produk dari product_table
        response = supabase.table("cart_table") \
            .select("cart_id, quantity, product_table(product_id, name, price, stock, image_url)") \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get_cart_items: {e}")
        return []

def add_to_cart(product_id: int, quantity: int = 1):
    """Menambah produk ke keranjang. Jika produk sudah ada, jumlahnya akan ditambah."""
    try:
        user = supabase.auth.get_user()
        if not user or not user.user:
            return {"success": False, "message": "Silakan login terlebih dahulu!"}
        
        user_id = user.user.id

        # 1. Cek apakah produk tersebut sudah ada di keranjang user
        check_exist = supabase.table("cart_table") \
            .select("*") \
            .eq("customer_id", user_id) \
            .eq("product_id", product_id) \
            .execute()

        if check_exist.data:
            # Jika sudah ada, update jumlahnya (tambah)
            new_qty = check_exist.data[0]["quantity"] + quantity
            supabase.table("cart_table") \
                .update({"quantity": new_qty}) \
                .eq("customer_id", user_id) \
                .eq("product_id", product_id) \
                .execute()
        else:
            # Jika belum ada, masukkan baris baru
            supabase.table("cart_table") \
                .insert({
                    "customer_id": user_id,
                    "product_id": product_id,
                    "quantity": quantity
                }) \
                .execute()
                
        return {"success": True, "message": "Produk berhasil dimasukkan ke keranjang!"}
    except Exception as e:
        return {"success": False, "message": f"Gagal menambahkan ke keranjang: {str(e)}"}

def update_cart_quantity(product_id: int, quantity: int):
    """Mengubah jumlah (quantity) produk spesifik di keranjang secara langsung."""
    try:
        if quantity <= 0:
            return remove_from_cart(product_id)
            
        supabase.table("cart_table") \
            .update({"quantity": quantity}) \
            .eq("product_id", product_id) \
            .execute()
        return {"success": True, "message": "Jumlah produk berhasil diperbarui!"}
    except Exception as e:
        return {"success": False, "message": f"Gagal memperbarui jumlah: {str(e)}"}

def remove_from_cart(product_id: int):
    """Menghapus satu produk dari keranjang belanja."""
    try:
        supabase.table("cart_table") \
            .delete() \
            .eq("product_id", product_id) \
            .execute()
        return {"success": True, "message": "Produk dihapus dari keranjang!"}
    except Exception as e:
        return {"success": False, "message": f"Gagal menghapus produk: {str(e)}"}
    
