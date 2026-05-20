# Panduan Integrasi & Penggunaan API Autentikasi

Dokumen ini menjelaskan cara kerja sistem autentikasi (Register, Login, Logout) yang menghubungkan **Streamlit (Frontend)** dengan **FastAPI + Supabase (Backend)**.

---

## 🚀 Cara Menjalankan Project

### A. Jika Belum Pernah Install Apapun (First Time Setup)

1. **Pastikan Python Terinstall**
   Cek dengan perintah: `python --version` (Minimal Python 3.9+).

2. **Setup Environment & Library**
   Buka terminal di folder root project, lalu jalankan:

   ```powershell
   # Install dependensi untuk Backend
   pip install -r backend/requirements.txt supabase

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

_API akan berjalan di: `http://localhost:8000`_

**Terminal 2: Menjalankan Frontend (Streamlit)**

```powershell
cd frontend
python -m streamlit run test-auth.py
```

_Tester autentikasi akan berjalan di: `http://localhost:8501`_

> Jika ingin membuka aplikasi utama, gunakan `Home.py`. Untuk pengujian login/register, gunakan `test-auth.py`.

---

## 🛠️ Dokumentasi Teknis Frontend (Streamlit)

Frontend berinteraksi dengan Backend menggunakan library `requests`. Semua logika ini berada di `frontend/utils/api_client.py`.

### 1. Register (Pendaftaran)

Mengirim data profil ke backend untuk didaftarkan ke Supabase Auth dan `customer_table`.

- **Endpoint**: `POST /register`
- **Contoh Kode Frontend**:

  ```python
  from utils.api_client import register
  import streamlit as st

  if st.button("Daftar Sekarang"):
      res = register(email, password, first_name, last_name, phone)
      if "user_id" in res:
          st.success("Registrasi Berhasil! Silakan Login.")
      else:
          st.error(f"Gagal: {res.get('detail')}")
  ```

### 2. Login (Masuk)

Mengambil token akses dari backend jika kredensial benar.

- **Endpoint**: `POST /login`
- **Contoh Kode Frontend**:

  ```python
  from utils.api_client import login
  import streamlit as st

  if st.button("Masuk"):
      user = login(email, password)
      if user:
          st.success(f"Halo {user['name']}, selamat datang kembali!")
          st.rerun() # Refresh halaman untuk memperbarui UI
      else:
          st.error("Email atau password salah")
  ```

### 3. Logout (Keluar)

Menghapus sesi aktif baik di sisi server maupun lokal.

- **Endpoint**: `POST /logout`
- **Contoh Kode Frontend**:

  ```python
  from utils.api_client import logout
  import streamlit as st

  if st.button("Keluar Akun"):
      logout() # Fungsi ini otomatis menghapus session_state dan refresh halaman
  ```

---

## 🔐 Manajemen Sesi (Session State)

Frontend menggunakan variabel berikut untuk melacak status user:

- `st.session_state["logged_in"]`: Boolean (True/False).
- `st.session_state["token"]`: String JWT untuk akses API yang butuh proteksi.
- `st.session_state["user_name"]`: String nama depan untuk ditampilkan di UI.

---

## 🧪 Cara Testing

Jika ingin mengetes fungsi API saja tanpa fitur belanja, gunakan file tester yang sudah disediakan:

```powershell
python -m streamlit run test-auth.py
```

---

_Dibuat untuk project Lumière - 2026_
