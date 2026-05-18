# Panduan Integrasi & Penggunaan API Produk

Dokumen ini menjelaskan cara kerja sistem manajemen produk (Melihat Katalog dan Menambah Produk) yang menghubungkan **Streamlit (Frontend)** dengan **FastAPI + Supabase (Backend)**.

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

### B. Cara Menjalankan Aplikasi (Rutinitas)

Anda harus menjalankan **dua terminal** secara bersamaan.

**Terminal 1: Menjalankan Backend (FastAPI)**
```powershell
cd backend
python -m uvicorn main:app --reload
```
*API akan berjalan di: `http://localhost:8000`*

**Terminal 2: Menjalankan Frontend (Streamlit)**
```powershell
cd frontend
python -m streamlit run Home.py
```
*Aplikasi akan berjalan di: `http://localhost:8501`*

---

## 🛠️ Dokumentasi Teknis Frontend (Streamlit)

Frontend berinteraksi dengan Backend menggunakan library `requests`. Fitur produk ini melibatkan pengambilan data biasa (JSON) dan pengiriman file gambar (`multipart/form-data`).

### 1. Mengambil Daftar Produk (Katalog)
Mengambil semua data produk dari database, termasuk link gambar yang otomatis dibuat dan disimpan di Supabase Storage.
*   **Endpoint**: `GET /products`
*   **Contoh Kode Frontend**:
    ```python
    import requests
    import streamlit as st

    def get_products():
        try:
            # Panggil API GET /products
            response = requests.get("http://localhost:8000/products")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Gagal mengambil produk: {e}")
            return []

    # Cara menampilkan di Halaman Katalog
    st.title("Katalog Produk")
    products = get_products()
    
    # Menampilkan menggunakan grid/columns
    cols = st.columns(3)
    for index, p in enumerate(products):
        with cols[index % 3]:
            if p.get("image_url"):
                st.image(p["image_url"], use_container_width=True)
            st.subheader(p["name"])
            st.write(f"Harga: Rp {p['price']:,.0f}")
            st.write(f"Sisa Stok: {p['stock']}")
            with st.expander("Detail"):
                st.write(p.get("description", "Tidak ada deskripsi"))
    ```

### 2. Menambah Produk Baru (Dengan Upload Gambar)
Mengirim data teks (nama, harga, dll) bersamaan dengan **file gambar** ke backend. Backend akan menghandle upload ke Supabase Storage dan menyimpan link-nya ke database.
*   **Endpoint**: `POST /products`
*   **Contoh Kode Frontend**:
    ```python
    import requests
    import streamlit as st

    def add_product(name, description, price, stock, image_file):
        url = "http://localhost:8000/products"
        
        # 1. Data teks dikirim sebagai parameter `data`
        form_data = {
            "name": name,
            "description": description,
            "price": price,
            "stock": stock
        }
        
        # 2. File gambar dikirim sebagai parameter `files`
        # Format tuple: ('nama_field_api', ('nama_file_asli', isi_file_bytes, 'tipe_konten'))
        files = {
            "image": (image_file.name, image_file.getvalue(), image_file.type)
        }
        
        try:
            # Gunakan requests.post dengan param data dan files
            response = requests.post(url, data=form_data, files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Gagal menambah produk: {e}")
            return None

    # Cara membuat form di Halaman Admin
    st.title("Tambah Produk Baru")
    with st.form("form_tambah_produk"):
        name = st.text_input("Nama Produk")
        desc = st.text_area("Deskripsi")
        price = st.number_input("Harga", min_value=0)
        stock = st.number_input("Stok", min_value=0)
        img_file = st.file_uploader("Upload Gambar", type=["jpg", "png", "jpeg", "webp"])
        
        submit_btn = st.form_submit_button("Simpan Produk")
        
        if submit_btn:
            if not name or not img_file:
                st.warning("Nama produk dan gambar wajib diisi!")
            else:
                with st.spinner("Sedang mengunggah..."):
                    res = add_product(name, desc, price, stock, img_file)
                    if res:
                        st.success("Produk berhasil ditambahkan!")
                        st.rerun() # Refresh halaman agar data terbaru muncul
    ```

---

## ⚠️ Catatan Penting untuk Integrasi

1. **Format Upload File (`multipart/form-data`)**
   Saat menggunakan library `requests` di Python, JANGAN menggunakan parameter `json=...` jika Anda sedang mengirim file. Gunakan kombinasi parameter `data=...` (untuk inputan teks) dan `files=...` (untuk file gambar) agar requests secara otomatis mengatur header menjadi `multipart/form-data`.
   
2. **Keamanan Supabase (RLS)**
   Jika saat menambah produk muncul error `403 Unauthorized` dari API, pastikan Anda telah memberikan akses `INSERT` untuk role `anon` pada bagian **Storage Policies** di bucket `product-images` di dashboard Supabase.

---
*Dibuat untuk project Lumière - 2026*