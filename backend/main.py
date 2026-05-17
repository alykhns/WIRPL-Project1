from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
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
    conn = get_connection()
    cursor = conn.cursor()

    # Buat order_id unik sederhana
    import random
    order_id = random.randint(1000, 9999)

    for item in body.cart:
        cursor.execute("""
            INSERT INTO order_item (order_item_id, order_id, product_id, quantity, price_at_purchase)
            VALUES (%s, %s, %s, %s, %s)
        """, (random.randint(10000, 99999), order_id,
              item.get("product_id"), item.get("qty"), item.get("price")))

    conn.commit()
    cursor.close()
    conn.close()
    return {"order_id": f"LM-{order_id}", "message": "Order created"}

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

# ── PRODUCTS ──────────────────────────────────────────────────────────────────
@app.get("/products")
def get_products(category_id: Optional[int] = None, limit: int = 20, offset: int = 0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if category_id:
        cursor.execute("""
            SELECT * FROM product WHERE category_id = %s LIMIT %s OFFSET %s
        """, (category_id, limit, offset))
    else:
        cursor.execute("SELECT * FROM product LIMIT %s OFFSET %s", (limit, offset))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product