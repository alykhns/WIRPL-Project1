MOCK_USER = {
    # Dari customer_table: customer_id, auth_id, first_name, last_name, email, phone_number
    # gender, birth_date, address, city, state_province, country, postal_code
    # membership_level, is_active, created_at
    "customer_id": 1,
    "auth_id": 5001,
    "first_name": "Faris",
    "last_name": "Lumiere",
    "email": "isla.lewis7@example.com",
    "phone_number": "08123456789",
    "gender": "Female",
    "birth_date": "2003-05-25",
    "address": "Jl. Anggrek No. 12",
    "city": "Jakarta Selatan",
    "state_province": "DKI Jakarta",
    "country": "Indonesia",
    "postal_code": "12345",
    "membership_level": "platinum",
    "is_active": True,
    "created_at": "2024-01-15T10:30:00",
}

# berdasarkan struktur tabel cart: cart_id, customer_id, product_id, qty
# join ke product table: product_name, brand, price, color, size, material, style, season
# dan fields tambahan: category_id, inventory_count, arrival_date, description, image_url
MOCK_CART = [
    {
        "cart_id": 1001,
        "customer_id": 1,
        "product_id": 500,
        "qty": 2,
        "product_name": "Tie-Dye T-shirt",
        "brand": "Ozu",
        "price": 91.21,
        "color": "Blue",
        "size": "S",
        "material": "polyester",
        "style": "casual",
        "season": "winter",
        "category_id": 1,
        "inventory_count": 150,
        "arrival_date": "2025-01-10",
        "description": "Trendy tie-dye t-shirt",
        "image_url": None,
    },
    {
        "cart_id": 1002,
        "customer_id": 1,
        "product_id": 6,
        "qty": 1,
        "product_name": "Floral Maxi Dress",
        "brand": "Gigaclub",
        "price": 244.95,
        "color": "Red",
        "size": "L",
        "material": "silk",
        "style": "formal",
        "season": "summer",
        "category_id": 5,
        "inventory_count": 831,
        "arrival_date": "2025-11-20",
        "description": "Elegant floral maxi dress for special occasions",
        "image_url": None,
    },
    {
        "cart_id": 1003,
        "customer_id": 1,
        "product_id": 29,
        "qty": 1,
        "product_name": "Knit Cardigan",
        "brand": "Lazzy",
        "price": 486.00,
        "color": "Pink",
        "size": "L",
        "material": "silk",
        "style": "casual",
        "season": "winter",
        "category_id": 1,
        "inventory_count": 500,
        "arrival_date": "2025-09-12",
        "description": "Soft silk knit cardigan in beautiful pink",
        "image_url": None,
    },
]

# berdasarkan tabel order_item: order_id, product_id, quantity, price_at_purchase
# tabel orders tidak ada di dump, jadi kita buat struktur yang masuk akal
# Status: delivered, shipping, processing, cancelled
MOCK_ORDERS = [
    {
        "order_id": "LM-001",
        "date": "01 Januari 2026",
        "status": "delivered",
        "items": [
            {"product_name": "Floral Maxi Dress", "brand": "Gigaclub", "qty": 1, "price_at_purchase": 244.95},
        ],
        "total": 244.95,
    },
    {
        "order_id": "LM-002",
        "date": "15 Februari 2026",
        "status": "shipping",
        "items": [
            {"product_name": "Knit Cardigan", "brand": "Lazzy", "qty": 2, "price_at_purchase": 486.00},
            {"product_name": "Plaid Shirt", "brand": "Ailane", "qty": 1, "price_at_purchase": 134.81},
        ],
        "total": 1106.81,
    },
    {
        "order_id": "LM-003",
        "date": "01 Maret 2026",
        "status": "processing",
        "items": [
            {"product_name": "Denim Jacket", "brand": "Plajo", "qty": 1, "price_at_purchase": 229.84},
        ],
        "total": 229.84,
    },
]

# tidak ada tabel shipping di dump, tapi ada procedure add_to_cart dan logika free shipping
# Definisi shipping options untuk mock data
MOCK_SHIPPING_OPTIONS = [
    {"id": 1, "name": "Regular", "estimate": "3-5 hari kerja", "price": 45000},
    {"id": 2, "name": "Express", "estimate": "1-2 hari kerja", "price": 85000},
    {"id": 3, "name": "Free Shipping", "estimate": "5-7 hari kerja", "price": 0},
]

# mapping category_id ke nama
# dari categories table: category_id, category_name
MOCK_CATEGORIES = {
    1: "Tops",
    2: "Bottoms",
    3: "Outerwear",
    4: "Accessories",
    5: "Dresses",
}

# contoh beberapa produk dari tabel product untuk keperluan display
# Dari product table: product_id, category_id, product_name, brand, price
# color, size, material, style, season
# inventory_count, arrival_date, description, image_url
MOCK_PRODUCTS_SAMPLE = [
    {"product_id": 1, "category_id": 1, "product_name": "Knit Cardigan", "brand": "Youbridge", "price": 194.64, "color": "Puce", "size": "L", "material": "polyester", "style": "casual", "season": "spring", "inventory_count": 660, "arrival_date": "2025-12-15", "description": "Cozy knit cardigan perfect for layering", "image_url": None},
    {"product_id": 6, "category_id": 5, "product_name": "Floral Maxi Dress", "brand": "Gigaclub", "price": 244.95, "color": "Red", "size": "L", "material": "silk", "style": "formal", "season": "summer", "inventory_count": 831, "arrival_date": "2025-11-20", "description": "Elegant floral maxi dress for special occasions", "image_url": None},
    {"product_id": 9, "category_id": 2, "product_name": "Leather Pants", "brand": "Tagcat", "price": 434.61, "color": "Red", "size": "XS", "material": "polyester", "style": "eveningwear", "season": "fall", "inventory_count": 89, "arrival_date": "2025-10-05", "description": "Premium quality leather pants", "image_url": None},
    {"product_id": 29, "category_id": 1, "product_name": "Knit Cardigan", "brand": "Lazzy", "price": 486.00, "color": "Pink", "size": "L", "material": "silk", "style": "casual", "season": "winter", "inventory_count": 500, "arrival_date": "2025-09-12", "description": "Soft silk knit cardigan in beautiful pink", "image_url": None},
    {"product_id": 74, "category_id": 5, "product_name": "Floral Maxi Dress", "brand": "Skinte", "price": 431.51, "color": "Teal", "size": "S", "material": "polyester", "style": "formal", "season": "spring", "inventory_count": 353, "arrival_date": "2025-08-30", "description": "Stunning teal floral maxi dress", "image_url": None},
]