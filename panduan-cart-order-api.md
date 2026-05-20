# Panduan Integrasi & Penggunaan API Cart dan Order

Dokumen ini menjelaskan cara kerja tabel transaksi pada schema Supabase project ini, yaitu `cart_table`, `order_table`, dan `order_items_table`.

---

## 🚀 Cara Menjalankan Project

### 1. Pastikan Backend dan Frontend Sudah Jalan

Jalankan backend FastAPI dan frontend Streamlit dari folder project:

```powershell
cd backend
python -m uvicorn main:app --reload
```

```powershell
cd frontend
python -m streamlit run Home.py
```

### 2. Pastikan Supabase Sudah Terkoneksi

Project ini memakai:

- `cart_table`
- `order_table`
- `order_items_table`
- `product_table`
- `customer_table`

### 3. Pastikan User Sudah Login

Banyak operasi cart dan order bergantung pada `auth.uid()` dan RLS. Jadi user harus login dulu agar data yang diambil atau diubah sesuai pemiliknya.

### 4. Cara Test Langsung dari Swagger UI

Kalau kamu tes lewat `http://127.0.0.1:8000/docs`, urutannya begini:

1. Buka endpoint `POST /login` lalu klik `Try it out`.
2. Isi email dan password user Supabase yang valid.
3. Klik `Execute`.
4. Ambil nilai `token` dari response.
5. Buka endpoint `GET /cart` atau `POST /cart`.
6. Klik `Try it out`, lalu isi header `authorization` dengan format:
   ```text
   Bearer <token>
   ```
7. Klik `Execute`.

Kalau header token belum diisi, `GET /cart` akan dibalas `401 Invalid token`.
Untuk endpoint yang butuh body, isi data langsung di form Swagger, lalu klik `Execute`.

---

## 🧺 `cart_table`

Tabel ini menyimpan isi keranjang user yang sedang login.

### Kolom Penting

- `cart_id`: ID unik baris cart
- `customer_id`: pemilik cart
- `product_id`: produk yang dimasukkan
- `quantity`: jumlah item
- `created_at`: waktu data dibuat

### Fungsi Umum

- Menambah produk ke cart
- Mengubah jumlah item
- Menghapus item dari cart
- Mengambil isi cart user aktif

### Alur Test dari Streamlit

1. Login ke app.
2. Tambahkan produk dari halaman katalog.
3. Buka halaman cart.
4. Pastikan item muncul, quantity bisa diubah, dan item bisa dihapus.

---

## 📦 `order_table`

Tabel ini menyimpan order utama setelah checkout.

### Kolom Penting

- `order_id`: ID order
- `customer_id`: pembeli
- `total_amount`: total transaksi
- `status`: status order seperti `PENDING_PAYMENT`, `PAID`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELED`
- `shipping_address`, `city`, `state_province`, `postal_code`: data pengiriman
- `tracking_number`: nomor resi
- `payment_method`: metode pembayaran
- `created_at`: waktu order dibuat

### Cara yang Disarankan

Order sebaiknya dibuat lewat proses checkout, bukan insert manual dari frontend. Tujuannya supaya:

- order dibuat konsisten
- detail item ikut tercatat
- stok produk ikut berkurang
- cart user bisa dikosongkan setelah checkout

### Alur Test dari Streamlit

1. Isi cart dulu.
2. Masuk ke halaman checkout.
3. Isi alamat dan pilih metode pembayaran.
4. Jalankan checkout.
5. Cek bahwa order baru muncul di `order_table`.

---

## 🧾 `order_items_table`

Tabel ini menyimpan detail item untuk setiap order.

### Kolom Penting

- `item_id`: ID unik detail item
- `order_id`: order induk
- `product_id`: produk yang dibeli
- `quantity`: jumlah item
- `price_at_purchase`: harga saat transaksi dibuat
- `created_at`: waktu data dibuat

### Cara Pakai

Biasanya tabel ini diisi otomatis oleh fungsi checkout. Jadi saat test normal, kamu tidak perlu insert manual ke tabel ini.

### Alur Test dari Streamlit

1. Checkout selesai.
2. Cek apakah `order_items_table` terisi sesuai item di cart.
3. Pastikan `price_at_purchase` sama dengan harga saat transaksi dibuat.

---

## 🧪 Alur Testing End-to-End

Kalau mau mengetes seluruh alur cart sampai order, gunakan langkah ini:

1. Jalankan backend FastAPI.
2. Buka Swagger di `http://127.0.0.1:8000/docs`.
3. Jalankan `POST /login` dengan email dan password yang valid.
4. Salin token dari response.
5. Jalankan `POST /cart` untuk menambah item.
6. Jalankan `GET /cart` untuk memastikan item masuk.
7. Jalankan `PUT /cart/{cart_id}` jika ingin mengubah quantity.
8. Jalankan `DELETE /cart/{cart_id}` jika ingin menghapus item.
9. Jalankan `POST /orders` jika endpoint order sudah siap dipakai di project kamu.
10. Jalankan `GET /orders/history` untuk melihat riwayat order.

---

## ⚠️ Catatan Penting

1. **Mode Mock di Frontend**
   Di `frontend/utils/api_client.py`, ada `USE_MOCK = True`. Kalau ingin test ke database asli, ubah menjadi `False`.

2. **RLS Harus Aktif**
   Pastikan policy untuk `cart_table`, `order_table`, dan `order_items_table` sudah aktif di Supabase.

3. **RPC Checkout Harus Cocok**
   Jika frontend memakai fungsi `execute_checkout`, pastikan parameter di kode dan di SQL sama. Kalau tidak sama, checkout bisa gagal.

4. **Nama Tabel Harus Konsisten**
   Schema baru memakai nama `cart_table`, `order_table`, dan `order_items_table`. Hindari mencampur dengan nama tabel lama seperti `cart`, `order_item`, atau `order_items`.

---

_Dibuat untuk project Lumière - 2026_
