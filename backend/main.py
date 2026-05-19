from fastapi import FastAPI, HTTPException, Header, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import uuid
from database.connection import get_connection
from database.supabase_conn import supabase
from utils.jwt_helper import create_token, verify_token
from models.schemas import LoginRequest, RegisterRequest, CartItemRequest, ProfileUpdate, OrderRequest, PaymentRequest

app = FastAPI(title="Lumiere API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── helper ──────────────────────────────────────────────────────────────────
def get_customer_id(authorization: str):
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        return payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# ── ROOT ─────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Lumiere API is running"}

# ── AUTH ─────────────────────────────────────────────────────────────────────
@app.post("/register")
def register(body: RegisterRequest):
    try:
        # 1. Sign up user ke Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": body.email,
            "password": body.password,
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Gagal mendaftarkan user")

        user_id = auth_response.user.id

        # 2. Simpan profil ke customer_table menggunakan upsert untuk menghindari error duplikat
        customer_data = {
            "customer_id": user_id,
            "first_name": body.first_name,
            "last_name": body.last_name,
            "phone_number": body.phone_number
        }
        
        db_response = supabase.table("customer_table").upsert(customer_data).execute()
        
        return {
            "message": "Registrasi berhasil. Silakan cek email untuk verifikasi (jika diaktifkan).",
            "user_id": user_id
        }
    except Exception as e:
        # Jika terjadi error, kita bisa menangkap detailnya
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {error_msg}")

@app.post("/login")
def login(body: LoginRequest):
    try:
        # 1. Sign in menggunakan Supabase Auth
        response = supabase.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password
        })

        if not response.user:
            raise HTTPException(status_code=401, detail="Email atau password salah")

        user_id = response.user.id
        
        # 2. Ambil data profil dari customer_table
        profile = supabase.table("customer_table").select("first_name").eq("customer_id", user_id).single().execute()
        
        name = profile.data.get("first_name", "User") if profile.data else "User"

        # 3. Kembalikan token (access_token dari Supabase) dan info user
        return {
            "token": response.session.access_token,
            "customer_id": user_id,
            "name": name
        }
    except Exception as e:
        error_msg = str(e)
        if "invalid login credentials" in error_msg.lower():
            raise HTTPException(status_code=401, detail="Email atau password salah")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {error_msg}")

@app.post("/logout")
def logout():
    try:
        supabase.auth.sign_out()
        return {"message": "Logout berhasil"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal logout: {str(e)}")

# ── CART ─────────────────────────────────────────────────────────────────────
@app.get("/cart")
def get_cart(authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.cart_id, c.customer_id, c.product_id, c.qty,
               p.product_name, p.brand, p.price, p.color, p.size,
               p.material, p.style, p.season, p.category_id,
               LEFT(p.product_name, 1) AS image_initial
        FROM cart c
        JOIN product p ON p.product_id = c.product_id
        WHERE c.customer_id = %s
    """, (customer_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items

@app.post("/cart")
def add_to_cart(body: CartItemRequest, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cart (customer_id, product_id, qty)
        VALUES (%s, %s, %s)
    """, (customer_id, body.product_id, body.qty))
    conn.commit()
    cart_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"cart_id": cart_id, "message": "Item added to cart"}

@app.put("/cart/{cart_id}")
def update_cart_item(cart_id: int, body: CartItemRequest, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cart SET qty = %s
        WHERE cart_id = %s AND customer_id = %s
    """, (body.qty, cart_id, customer_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Cart updated"}

@app.delete("/cart/{cart_id}")
def delete_cart_item(cart_id: int, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM cart WHERE cart_id = %s AND customer_id = %s
    """, (cart_id, customer_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Item removed"}

# ── PROFILE ───────────────────────────────────────────────────────────────────
@app.get("/customer/profile")
def get_profile(authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, a.email FROM customer_table c
        JOIN auth_table a ON a.auth_id = c.auth_id
        WHERE c.customer_id = %s
    """, (customer_id,))
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.put("/customer/profile")
def update_profile(body: ProfileUpdate, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE customer_table
        SET first_name = %s, last_name = %s, phone_number = %s,
            address = %s, city = %s, postal_code = %s
        WHERE customer_id = %s
    """, (body.first_name, body.last_name, body.phone_number,
          body.address, body.city, body.postal_code, customer_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Profile updated"}

# ── ORDERS ────────────────────────────────────────────────────────────────────
@app.post("/orders")
def create_order(body: OrderRequest, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    
    # 1. Simpan ke Supabase order_table
    import random
    order_id_num = random.randint(1000, 9999)
    order_id_str = f"LM-{order_id_num}"
    
    order_data = {
        "order_id": order_id_num,
        "customer_id": customer_id,
        "total_amount": body.total,
        "status": "pending"
    }
    
    try:
        supabase.table("order_table").insert(order_data).execute()
    except Exception as e:
        print(f"Error Supabase Order: {e}")

    # 2. Simpan ke MySQL order_item (Opsional, untuk detail)
    conn = get_connection()
    cursor = conn.cursor()
    for item in body.cart:
        cursor.execute("""
            INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase)
            VALUES (%s, %s, %s, %s, %s)
        """, (random.randint(10000, 99999), order_id_num,
              item.get("product_id"), item.get("qty"), item.get("price")))

    conn.commit()
    cursor.close()
    conn.close()
    return {"order_id": order_id_str, "message": "Order created"}

@app.get("/orders/history")
def get_order_history(authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT oi.order_id, oi.product_id, oi.quantity, oi.price_at_purchase,
               p.product_name, p.brand
        FROM order_item oi
        JOIN product p ON p.product_id = oi.product_id
        WHERE oi.order_id IS NOT NULL
        LIMIT 20
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group by order_id
    orders = {}
    for row in rows:
        oid = str(row["order_id"])
        if oid not in orders:
            orders[oid] = {
                "order_id": f"LM-{oid}",
                "date": "2026",
                "status": "delivered",
                "items": [],
                "total": 0,
            }
        orders[oid]["items"].append({
            "product_name": row["product_name"],
            "brand": row["brand"],
            "qty": row["quantity"],
            "price_at_purchase": float(row["price_at_purchase"]) if row["price_at_purchase"] else 0,
        })
        orders[oid]["total"] += float(row["price_at_purchase"] or 0) * (row["quantity"] or 1)

    return list(orders.values())

# ── SHIPPING ──────────────────────────────────────────────────────────────────
@app.get("/shipping")
def get_shipping():
    return [
        {"id": 1, "name": "Regular", "estimate": "3-5 hari kerja", "price": 45000},
        {"id": 2, "name": "Express", "estimate": "1-2 hari kerja", "price": 85000},
        {"id": 3, "name": "Free Shipping", "estimate": "5-7 hari kerja", "price": 0},
    ]

# ── PAYMENT ───────────────────────────────────────────────────────────────────
@app.post("/payment")
def submit_payment(body: PaymentRequest, authorization: Optional[str] = Header(None)):
    get_customer_id(authorization)
    # Simulasi payment — di production konek ke payment gateway
    return {"status": "success", "method": body.method, "total": body.total}

# ── CATEGORIES ───────────────────────────────────────────────────────────────
@app.get("/categories")
def get_categories():
    try:
        # Mengambil semua kategori dari categories table (asumsi ada tabel ini di Supabase)
        response = supabase.table("categories").select("*").execute()
        return response.data
    except Exception as e:
        # Fallback jika tabel categories tidak ada, return mock data
        return [
            {"category_id": 1, "category_name": "Clothing"},
            {"category_id": 2, "category_name": "Accessories"},
            {"category_id": 3, "category_name": "Shoes"},
        ]

# ── ADMIN ────────────────────────────────────────────────────────────────────
@app.get("/admin/stats")
def get_admin_stats(authorization: Optional[str] = Header(None)):
    get_customer_id(authorization) # Simple auth check
    try:
        # Hitung total orders, revenue, dan products
        orders_res = supabase.table("order_table").select("total_amount", count="exact").execute()
        products_res = supabase.table("product_table").select("product_id", count="exact").execute()
        
        total_orders = orders_res.count if orders_res.count is not None else 0
        total_revenue = sum([o["total_amount"] for o in orders_res.data]) if orders_res.data else 0
        total_products = products_res.count if products_res.count is not None else 0
        
        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "total_products": total_products,
            "active_categories": 3 # Placeholder
        }
    except Exception as e:
        return {
            "total_orders": 0,
            "total_revenue": 0,
            "total_products": 0,
            "active_categories": 0,
            "error": str(e)
        }

@app.get("/admin/orders")
def get_all_orders(authorization: Optional[str] = Header(None)):
    get_customer_id(authorization)
    try:
        response = supabase.table("order_table").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil semua pesanan: {str(e)}")

@app.put("/admin/orders/{order_id}/status")
def admin_update_order_status(order_id: int, status: str = Form(...), authorization: Optional[str] = Header(None)):
    get_customer_id(authorization)
    try:
        response = supabase.table("order_table").update({"status": status}).eq("order_id", order_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
        return {"message": "Status pesanan berhasil diperbarui", "data": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memperbarui status pesanan: {str(e)}")

# ── PRODUCTS ──────────────────────────────────────────────────────────────────
@app.get("/products")
def get_products(limit: int = 20, offset: int = 0):
    try:
        # Mengambil data dari product_table menggunakan Supabase
        response = supabase.table("product_table").select("*").range(offset, offset + limit - 1).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil produk: {str(e)}")

@app.get("/products/{product_id}")
def get_product(product_id: int):
    try:
        # Mengambil satu data berdasarkan ID
        response = supabase.table("product_table").select("*").eq("product_id", product_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil detail produk: {str(e)}")

@app.post("/products")
async def create_product(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    stock: int = Form(0),
    image: UploadFile = File(...)
):
    try:
        print(f"DEBUG: Memulai proses tambah produk: {name}")
        # 1. Generate Nama File Unik
        file_ext = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        file_content = await image.read()

        # 2. Upload ke Supabase Storage
        try:
            print(f"DEBUG: Mencoba upload ke storage: {file_name}")
            storage_response = supabase.storage.from_("product-images").upload(
                path=file_name,
                file=file_content,
                file_options={"content-type": image.content_type}
            )
            print("DEBUG: Upload storage berhasil")
        except Exception as storage_err:
            print(f"DEBUG ERROR STORAGE: {str(storage_err)}")
            raise HTTPException(status_code=500, detail=f"Gagal di STORAGE (Upload Gambar): {str(storage_err)}")

        # 3. Dapatkan Public URL
        image_url = supabase.storage.from_("product-images").get_public_url(file_name)
        print(f"DEBUG: URL Gambar: {image_url}")

        # 4. Simpan ke Database
        try:
            print("DEBUG: Mencoba insert ke database")
            product_data = {
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "image_url": image_url
            }

            db_response = supabase.table("product_table").insert(product_data).execute()
            print("DEBUG: Insert database berhasil")

            return {
                "message": "Produk berhasil ditambahkan",
                "data": db_response.data[0] if db_response.data else None
            }
        except Exception as db_err:
            print(f"DEBUG ERROR DB: {str(db_err)}")
            raise HTTPException(status_code=500, detail=f"Gagal di DATABASE (Insert Tabel): {str(db_err)}")

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"DEBUG ERROR UMUM: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan sistem: {str(e)}")

@app.put("/products/{product_id}")
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    stock: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    try:
        # 1. Kumpulkan data yang ingin diupdate saja
        update_data = {}
        if name is not None: update_data["name"] = name
        if description is not None: update_data["description"] = description
        if price is not None: update_data["price"] = price
        if stock is not None: update_data["stock"] = stock

        # 2. Jika ada file gambar baru, upload ke Storage
        if image and image.filename:
            file_ext = image.filename.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{file_ext}"
            file_content = await image.read()

            supabase.storage.from_("product-images").upload(
                path=file_name,
                file=file_content,
                file_options={"content-type": image.content_type}
            )

            image_url = supabase.storage.from_("product-images").get_public_url(file_name)
            update_data["image_url"] = image_url

        # 3. Cek apakah ada data yang akan diupdate
        if not update_data:
            return {"message": "Tidak ada data yang diperbarui", "data": None}

        # 4. Update ke database
        db_response = supabase.table("product_table").update(update_data).eq("product_id", product_id).execute()

        if not db_response.data:
            raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

        return {
            "message": "Produk berhasil diperbarui",
            "data": db_response.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memperbarui produk: {str(e)}")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        # Hapus data dari product_table
        db_response = supabase.table("product_table").delete().eq("product_id", product_id).execute()

        if not db_response.data:
            raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

        return {"message": f"Produk dengan ID {product_id} berhasil dihapus"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menghapus produk: {str(e)}")
