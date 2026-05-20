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
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")
        
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        customer_id = payload.get("sub")
        
        if not customer_id:
            raise HTTPException(status_code=401, detail="Invalid token: no customer_id")
        
        print(f"[AUTH] Verified customer_id: {customer_id}")
        return customer_id
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AUTH] Error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

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

        # 3. Kembalikan token yang ditandatangani backend agar verifier lokal bisa memvalidasi
        return {
            "token": create_token(user_id),
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
    print(f"[GET CART] Request received, authorization present: {bool(authorization)}")
    customer_id = get_customer_id(authorization)
    try:
        # 1. Ambil cart items untuk customer ini
        cart_response = supabase.table("cart_table").select("*").eq("customer_id", customer_id).execute()
        print(f"[GET CART] Found {len(cart_response.data)} items in cart")
        
        # 2. Untuk setiap cart item, ambil product details
        result = []
        for cart_item in cart_response.data:
            product_id = cart_item["product_id"]
            print(f"[GET CART] Fetching product {product_id}")
            
            try:
                # Ambil product details
                product_response = supabase.table("product_table").select("*").eq("product_id", product_id).execute()
                
                if product_response.data:
                    product = product_response.data[0]
                    # Combine cart item + product data
                    result.append({
                        "cart_id": cart_item["cart_id"],
                        "customer_id": cart_item["customer_id"],
                        "product_id": cart_item["product_id"],
                        "qty": cart_item["quantity"],
                        "quantity": cart_item["quantity"],
                        "product_name": product.get("product_name", "Unknown Product"),
                        "brand": product.get("brand", ""),
                        "price": product.get("price", 0),
                        "color": product.get("color", ""),
                        "size": product.get("size", ""),
                        "material": product.get("material", ""),
                        "style": product.get("style", ""),
                        "season": product.get("season", ""),
                        "category_id": product.get("category_id"),
                    })
                    print(f"[GET CART] Found product: {product.get('product_name')}")
                else:
                    # Produk tidak ditemukan, return cart item saja
                    print(f"[GET CART] Product {product_id} not found, returning cart item only")
                    result.append({
                        "cart_id": cart_item["cart_id"],
                        "customer_id": cart_item["customer_id"],
                        "product_id": cart_item["product_id"],
                        "qty": cart_item["quantity"],
                        "quantity": cart_item["quantity"],
                        "product_name": f"Product {product_id}",
                        "price": 0,
                    })
            except Exception as prod_err:
                print(f"[GET CART] Error fetching product {product_id}: {str(prod_err)}")
                # Return cart item dengan product basic info
                result.append({
                    "cart_id": cart_item["cart_id"],
                    "customer_id": cart_item["customer_id"],
                    "product_id": cart_item["product_id"],
                    "qty": cart_item["quantity"],
                    "quantity": cart_item["quantity"],
                    "product_name": f"Product {product_id}",
                    "price": 0,
                })
        
        print(f"[GET CART] Returning {len(result)} items")
        return result
    except Exception as e:
        print(f"[GET CART] Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Gagal mengambil cart: {str(e)}")

@app.post("/cart")
def add_to_cart(body: dict, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    try:
        # Accept both "qty" dan "quantity" dari frontend
        qty = body.get("qty", body.get("quantity", 1))
        product_id = body.get("product_id")
        
        print(f"[ADD TO CART] customer_id={customer_id}, product_id={product_id}, qty={qty}")
        
        if not product_id:
            raise HTTPException(status_code=400, detail="product_id is required")
        
        if qty < 1:
            raise HTTPException(status_code=400, detail="quantity must be at least 1")
        
        # Cek apakah produk sudah ada di cart user
        check_exist = supabase.table("cart_table").select("*").eq("customer_id", customer_id).eq("product_id", product_id).execute()
        
        print(f"[ADD TO CART] Found existing items: {len(check_exist.data)}")
        
        if check_exist.data:
            # Jika sudah ada, update quantity (tambahkan)
            existing_qty = check_exist.data[0]["quantity"]
            new_qty = existing_qty + qty
            response = supabase.table("cart_table").update({"quantity": new_qty}).eq("customer_id", customer_id).eq("product_id", product_id).execute()
            message = "Product quantity updated in cart"
            print(f"[ADD TO CART] Updated existing item: new_qty={new_qty}")
        else:
            # Jika belum ada, insert baris baru
            payload = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": qty,
            }
            response = supabase.table("cart_table").insert(payload).execute()
            message = "Product added to cart"
            print(f"[ADD TO CART] Inserted new item: {payload}")
        
        print(f"[ADD TO CART] Success - Response has {len(response.data)} items")
        return {"status": "success", "message": message, "data": response.data}
    except HTTPException as he:
        print(f"[ADD TO CART] HTTPException: {he.detail}")
        return {"status": "error", "detail": he.detail, "code": he.status_code}
    except Exception as e:
        print(f"[ADD TO CART] Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "detail": f"{type(e).__name__}: {str(e)}", "code": 500}

@app.put("/cart/{cart_id}")
def update_cart_item(cart_id: int, body: CartItemRequest, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    try:
        quantity = body.qty if body.qty is not None else body.quantity
        response = supabase.table("cart_table").update({"quantity": quantity}).eq("cart_id", cart_id).eq("customer_id", customer_id).execute()
        return {"message": "Cart updated", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal update cart: {str(e)}")

@app.delete("/cart/{cart_id}")
def delete_cart_item(cart_id: int, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    try:
        response = supabase.table("cart_table").delete().eq("cart_id", cart_id).eq("customer_id", customer_id).execute()
        return {"message": "Item removed", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menghapus cart: {str(e)}")

# ── PROFILE ───────────────────────────────────────────────────────────────────
@app.get("/customer/profile")
def get_profile(authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    try:
        # Get profile dari Supabase customer_table
        response = supabase.table("customer_table").select("*").eq("customer_id", customer_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil profile: {str(e)}")

@app.put("/customer/profile")
def update_profile(body: ProfileUpdate, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    try:
        # Update profile di Supabase customer_table
        update_data = {
            "first_name": body.first_name,
            "last_name": body.last_name,
            "phone_number": body.phone_number,
            "address": body.address,
            "city": body.city,
            "postal_code": body.postal_code,
        }
        response = supabase.table("customer_table").update(update_data).eq("customer_id", customer_id).execute()
        return {"message": "Profile updated", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal update profile: {str(e)}")

# ── ORDERS ────────────────────────────────────────────────────────────────────
@app.post("/orders")
def create_order(body: OrderRequest, authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    
    # 1. Simpan ke Supabase order_table
    order_id_num = uuid.uuid4().int % 1000000000
    order_id_str = f"LM-{order_id_num}"
    
    order_data = {
        "order_id": order_id_num,
        "customer_id": customer_id,
        "total_amount": body.total,
        "status": "PENDING_PAYMENT",
        "shipping_address": "",
        "city": "",
        "state_province": "",
        "postal_code": "",
        "tracking_number": f"TRK-{uuid.uuid4().hex[:10].upper()}",
        "payment_method": "manual"
    }
    
    try:
        supabase.table("order_table").insert(order_data).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan order: {str(e)}")

    # 2. Simpan detail item langsung ke Supabase order_items_table.
    detail_warnings = []
    for item in body.cart:
        try:
            supabase.table("order_items_table").insert({
                "item_id": uuid.uuid4().int % 1000000000,
                "order_id": order_id_num,
                "product_id": item.get("product_id"),
                "quantity": item.get("qty"),
                "price_at_purchase": item.get("price"),
            }).execute()
        except Exception as e:
            detail_warnings.append(str(e))
            print(f"Error inserting order item: {e}")
    response = {"order_id": order_id_str, "message": "Order created"}
    if detail_warnings:
        response["warnings"] = detail_warnings
    return response

@app.get("/orders/history")
def get_order_history(authorization: Optional[str] = Header(None)):
    customer_id = get_customer_id(authorization)
    try:
        response = supabase.table("order_table").select("*").eq("customer_id", customer_id).order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil riwayat order: {str(e)}")

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
    criteria: str = Form(...),
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
                "criteria": criteria,
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
    criteria: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    try:
        # 1. Kumpulkan data yang ingin diupdate saja
        update_data = {}
        if name is not None: update_data["name"] = name
        if description is not None: update_data["description"] = description
        if price is not None: update_data["price"] = price
        if stock is not None: update_data["stock"] = stock
        if criteria is not None: update_data["criteria"] = criteria

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
