# Panduan Integrasi & Penggunaan API Produk

Dokumen ini menjelaskan cara kerja sistem manajemen produk (Melihat Katalog, Menambah, Mengedit, dan Menghapus) yang menghubungkan **Streamlit (Frontend)** dengan **FastAPI + Supabase (Backend)**.

---

## 🚀 Cara Menjalankan Project

### A. Jika Belum Pernah Install Apapun (First Time Setup)

1. **Pastikan Python Terinstall**
   Cek dengan perintah: `python --version` (Minimal Python 3.9+).

2. **Setup Environment & Library**
   Buka terminal di folder root project, lalu jalankan:
   ```powershell
   # Install dependensi untuk Backend
   pip install -r backend/requirements.txt supabase python-multipart

   # Install dependensi untuk Frontend
   pip install -r frontend/requirements.txt
   ```

3. **Konfigurasi Variabel Lingkungan (.env)**
   Buat file `.env` di folder root project dan isi dengan kredensial Supabase Anda:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   ```

---

## 🛠️ Dokumentasi Teknis Frontend (Streamlit)

### 1. Mengambil Daftar Produk (Katalog)
*   **Endpoint**: `GET /products`
*   **Contoh Kode**:
    ```python
    import requests
    response = requests.get("http://localhost:8000/products")
    products = response.json()
    ```

### 2. Menambah Produk Baru
*   **Endpoint**: `POST /products`
*   **Catatan**: Wajib menyertakan file gambar.
*   **Contoh Kode**:
    ```python
    files = {"image": (image_file.name, image_file.getvalue(), image_file.type)}
    data = {"name": name, "price": price, "stock": stock, "description": desc}
    response = requests.post("http://localhost:8000/products", data=data, files=files)
    ```

### 3. Mengedit Produk (Update)
Mengubah data produk yang sudah ada. Semua field bersifat **opsional**; data di database hanya akan berubah jika Anda mengirimkan nilainya.
*   **Endpoint**: `PUT /products/{product_id}`
*   **Contoh Kode Frontend**:
    ```python
    def update_product(product_id, name=None, price=None, stock=None, image_file=None):
        url = f"http://localhost:8000/products/{product_id}"
        
        # Kirim data teks (hanya yang tidak None)
        data = {}
        if name: data["name"] = name
        if price: data["price"] = price
        if stock is not None: data["stock"] = stock
        
        # Kirim file gambar jika ada
        files = None
        if image_file:
            files = {"image": (image_file.name, image_file.getvalue(), image_file.type)}
            
        response = requests.put(url, data=data, files=files)
        return response.json()
    ```

### 4. Menghapus Produk (Delete)
Menghapus produk dari database secara permanen.
*   **Endpoint**: `DELETE /products/{product_id}`
*   **Contoh Kode Frontend**:
    ```python
    def delete_product(product_id):
        url = f"http://localhost:8000/products/{product_id}"
        response = requests.delete(url)
        if response.status_code == 200:
            st.success("Produk berhasil dihapus!")
        else:
            st.error("Gagal menghapus produk")
    ```

---

## ⚠️ Catatan Penting untuk Integrasi

1. **Keamanan Supabase (RLS)**
   Jika API Edit/Delete memberikan error `403 Forbidden`, jalankan perintah SQL berikut di dashboard Supabase:
   ```sql
   -- Aktifkan izin Update dan Delete untuk anon
   CREATE POLICY "Allow anon update" ON public.product_table FOR UPDATE TO anon USING (true);
   CREATE POLICY "Allow anon delete" ON public.product_table FOR DELETE TO anon USING (true);
   ```

2. **Partial Update (PUT)**
   Saat memanggil API Edit, Anda tidak perlu mengirimkan semua data. Jika user hanya ingin mengganti stok, cukup kirim `stock` saja di body request. Data lainnya akan tetap aman di database.

---
*Dibuat untuk project Lumière - 2026*
