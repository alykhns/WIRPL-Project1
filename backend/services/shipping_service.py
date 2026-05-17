import sys
from pathlib import Path

# Menghubungkan ke berkas client Supabase di folder root
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from supabase_client import supabase

# ==========================================
# DATA MASTER (Simulasi Kurir & Pembayaran)
# ==========================================
SHIPPING_DATA = {
    "reg": {"name": "J&T Regular", "cost": 15000, "eta": "2-3 Hari"},
    "yes": {"name": "JNE YES (Yakin Esok Sampai)", "cost": 30000, "eta": "1 Hari"},
    "cargo": {"name": "Sicepat Cargo", "cost": 50000, "eta": "5-7 Hari"}
}

PAYMENT_DATA = {
    "tf_bank": {"name": "Transfer Bank (BCA/Mandiri)", "type": "Manual Verification"},
    "gopay": {"name": "GoPay / QRIS", "type": "Instant"},
    "cod": {"name": "Cash on Delivery (COD)", "type": "Pay on Spot"}
}

# ==========================================
# FUNGSI API SHIPPING & PAYMENT
# ==========================================

def get_shipping_methods():
    """Mengembalikan semua daftar metode pengiriman yang tersedia untuk UI."""
    return [{"id": key, **value} for key, value in SHIPPING_DATA.items()]


def get_payment_methods():
    """Mengembalikan semua daftar metode pembayaran yang tersedia untuk UI."""
    return [{"id": key, **value} for key, value in PAYMENT_DATA.items()]


def calculate_shipping_cost(method_id: str) -> int:
    """
    Mengambil nominal ongkos kirim berdasarkan ID metode pengiriman.
    Jika ID tidak ditemukan, otomatis mengembalikan 0.
    """
    method = SHIPPING_DATA.get(method_id)
    if method:
        return method["cost"]
    return 0


def confirm_payment(order_id: int, proof_url: str = None):
    """
    Mengonfirmasi bahwa customer sudah membayar pesanan.
    Mengubah status pesanan di database menjadi 'Diproses' (Paid).
    """
    try:
        # Menyiapkan data yang akan di-update
        update_data = {"status": "Diproses"}
        
        # Jika ada fitur upload bukti transfer, simpan URL-nya ke kolom jika tersedia
        if proof_url:
            update_data["payment_proof_url"] = proof_url

        # Eksekusi update ke order_table di Supabase
        supabase.table("order_table") \
            .update(update_data) \
            .eq("order_id", order_id) \
            .execute()
            
        return {"success": True, "message": "Pembayaran berhasil dikonfirmasi! Pesanan segera diproses."}
    except Exception as e:
        print(f"Error saat konfirmasi pembayaran: {e}")
        return {"success": False, "message": f"Gagal konfirmasi pembayaran: {str(e)}"}


# ==========================================
# BLOK TESTING (Unit Test)
# ==========================================
if __name__ == "__main__":
    print("--- MEMULAI UJI COBA API SHIPPING & PAYMENT ---")
    
    # 1. Tes Ambil Data Kurir
    shipping_list = get_shipping_methods()
    print(f"\n[1] Daftar Pengiriman:\n{shipping_list}")
    
    # 2. Tes Hitung Ongkir
    ongkir_yes = calculate_shipping_cost("yes")
    print(f"\n[2] Cek Ongkir JNE YES: Rp {ongkir_yes:,}")
    
    # 3. Tes Ambil Data Metode Bayar
    payment_list = get_payment_methods()
    print(f"\n[3] Daftar Pembayaran:\n{payment_list}")
    
    print("\n✅ API Shipping & Payment Sukses Dijalankan Tanpa Error!")