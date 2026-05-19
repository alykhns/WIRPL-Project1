MOCK_USER = {
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
    "membership_level": "Platinum",
    "is_active": True,
}

# berdasarkan struktur tabel cart: cart_id, customer_id, product_id, qty
# join ke product: product_name, brand, price, color, size, material, style, season
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
        "image_initial": "T",
        "category_id": 1,
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
        "image_initial": "F",
        "category_id": 5,
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
        "image_initial": "K",
        "category_id": 1,
    },
]

# berdasarkan tabel order_item (order_id ada, product_id, quantity, price_at_purchase)
# tabel orders tidak ada di dump, jadi kita buat struktur yang masuk akal
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
MOCK_SHIPPING_OPTIONS = [
    {"id": 1, "name": "Regular", "estimate": "3-5 hari kerja", "price": 45000},
    {"id": 2, "name": "Express", "estimate": "1-2 hari kerja", "price": 85000},
    {"id": 3, "name": "Free Shipping", "estimate": "5-7 hari kerja", "price": 0},
]

# mapping category_id ke nama
MOCK_CATEGORIES = {
    1: "Tops",
    2: "Bottoms",
    3: "Outerwear",
    4: "Accessories",
    5: "Dresses",
}

# ============================================================
# PRODUCT CATALOG (extracted dari SQL backup, 80 items berimbang)
# Field lengkap sesuai ERD laporan: category_id, brand, color, size,
# material, style, season, inventory_count, description, image_url
# ============================================================
MOCK_PRODUCTS = [
    {"product_id": 12, "category_id": 1, "product_name": "Knit Cardigan", "brand": "Fadeo", "price": 332.59, "color": "Olive", "size": "M", "material": "cotton", "style": "formal", "season": "summer", "inventory_count": 184, "description": "Premium Knit Cardigan from Fadeo. Made of high-quality cotton with a formal style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere12/600/750"},
    {"product_id": 25, "category_id": 1, "product_name": "Ruffled Blouse", "brand": "Trupe", "price": 412.05, "color": "Maroon", "size": "S", "material": "silk", "style": "eveningwear", "season": "fall", "inventory_count": 421, "description": "Premium Ruffled Blouse from Trupe. Made of high-quality silk with an eveningwear style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere25/600/750"},
    {"product_id": 47, "category_id": 1, "product_name": "Plaid Shirt", "brand": "Bluejam", "price": 187.40, "color": "Navy", "size": "L", "material": "cotton", "style": "casual", "season": "spring", "inventory_count": 312, "description": "Premium Plaid Shirt from Bluejam. Made of high-quality cotton with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere47/600/750"},
    {"product_id": 58, "category_id": 1, "product_name": "Linen Tunic", "brand": "Yodel", "price": 145.20, "color": "Cream", "size": "M", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 524, "description": "Premium Linen Tunic from Yodel. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere58/600/750"},
    {"product_id": 71, "category_id": 1, "product_name": "Silk Camisole", "brand": "Avamm", "price": 298.50, "color": "Champagne", "size": "S", "material": "silk", "style": "eveningwear", "season": "spring", "inventory_count": 156, "description": "Premium Silk Camisole from Avamm. Made of high-quality silk with an eveningwear style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere71/600/750"},
    {"product_id": 89, "category_id": 1, "product_name": "Wool Sweater", "brand": "Skipfire", "price": 367.80, "color": "Charcoal", "size": "L", "material": "wool", "style": "casual", "season": "winter", "inventory_count": 287, "description": "Premium Wool Sweater from Skipfire. Made of high-quality wool with a casual style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere89/600/750"},
    {"product_id": 103, "category_id": 1, "product_name": "Knit Cardigan", "brand": "Voonyx", "price": 245.90, "color": "Beige", "size": "XL", "material": "wool", "style": "casual", "season": "fall", "inventory_count": 198, "description": "Premium Knit Cardigan from Voonyx. Made of high-quality wool with a casual style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere103/600/750"},
    {"product_id": 124, "category_id": 1, "product_name": "Ruffled Blouse", "brand": "Quaxo", "price": 178.30, "color": "Ivory", "size": "M", "material": "silk", "style": "formal", "season": "spring", "inventory_count": 345, "description": "Premium Ruffled Blouse from Quaxo. Made of high-quality silk with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere124/600/750"},
    {"product_id": 156, "category_id": 1, "product_name": "Cashmere Pullover", "brand": "Lazzy", "price": 478.20, "color": "Camel", "size": "S", "material": "wool", "style": "formal", "season": "winter", "inventory_count": 89, "description": "Premium Cashmere Pullover from Lazzy. Made of high-quality wool with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere156/600/750"},
    {"product_id": 178, "category_id": 1, "product_name": "Plaid Shirt", "brand": "Twinder", "price": 134.50, "color": "Crimson", "size": "M", "material": "cotton", "style": "casual", "season": "fall", "inventory_count": 412, "description": "Premium Plaid Shirt from Twinder. Made of high-quality cotton with a casual style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere178/600/750"},
    {"product_id": 195, "category_id": 1, "product_name": "Linen Tunic", "brand": "Eare", "price": 162.75, "color": "Sage", "size": "L", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 267, "description": "Premium Linen Tunic from Eare. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere195/600/750"},
    {"product_id": 218, "category_id": 1, "product_name": "Silk Blouse", "brand": "Roomm", "price": 389.40, "color": "Black", "size": "S", "material": "silk", "style": "eveningwear", "season": "fall", "inventory_count": 178, "description": "Premium Silk Blouse from Roomm. Made of high-quality silk with an eveningwear style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere218/600/750"},
    {"product_id": 234, "category_id": 1, "product_name": "Wool Sweater", "brand": "Yotz", "price": 274.60, "color": "Burgundy", "size": "M", "material": "wool", "style": "casual", "season": "winter", "inventory_count": 234, "description": "Premium Wool Sweater from Yotz. Made of high-quality wool with a casual style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere234/600/750"},
    {"product_id": 256, "category_id": 1, "product_name": "Knit Cardigan", "brand": "Centidel", "price": 215.80, "color": "Mauve", "size": "L", "material": "wool", "style": "casual", "season": "spring", "inventory_count": 389, "description": "Premium Knit Cardigan from Centidel. Made of high-quality wool with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere256/600/750"},
    {"product_id": 278, "category_id": 1, "product_name": "Ruffled Blouse", "brand": "Brainsphere", "price": 297.30, "color": "Blush", "size": "XS", "material": "silk", "style": "formal", "season": "spring", "inventory_count": 145, "description": "Premium Ruffled Blouse from Brainsphere. Made of high-quality silk with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere278/600/750"},
    {"product_id": 295, "category_id": 1, "product_name": "Cotton Tee", "brand": "Yombu", "price": 89.50, "color": "White", "size": "M", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 678, "description": "Premium Cotton Tee from Yombu. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere295/600/750"},
    {"product_id": 312, "category_id": 1, "product_name": "Silk Camisole", "brand": "Demivee", "price": 256.40, "color": "Rose", "size": "S", "material": "silk", "style": "eveningwear", "season": "summer", "inventory_count": 198, "description": "Premium Silk Camisole from Demivee. Made of high-quality silk with an eveningwear style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere312/600/750"},
    {"product_id": 334, "category_id": 1, "product_name": "Wool Sweater", "brand": "Edge", "price": 312.70, "color": "Forest", "size": "L", "material": "wool", "style": "casual", "season": "fall", "inventory_count": 156, "description": "Premium Wool Sweater from Edge. Made of high-quality wool with a casual style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere334/600/750"},
    {"product_id": 358, "category_id": 1, "product_name": "Linen Tunic", "brand": "Tagchat", "price": 175.25, "color": "Pearl", "size": "M", "material": "cotton", "style": "casual", "season": "spring", "inventory_count": 423, "description": "Premium Linen Tunic from Tagchat. Made of high-quality cotton with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere358/600/750"},
    {"product_id": 376, "category_id": 1, "product_name": "Plaid Shirt", "brand": "Mybuzz", "price": 142.85, "color": "Forest", "size": "L", "material": "cotton", "style": "casual", "season": "winter", "inventory_count": 289, "description": "Premium Plaid Shirt from Mybuzz. Made of high-quality cotton with a casual style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere376/600/750"},
    {"product_id": 397, "category_id": 1, "product_name": "Cashmere Pullover", "brand": "Innojam", "price": 459.90, "color": "Taupe", "size": "S", "material": "wool", "style": "formal", "season": "winter", "inventory_count": 67, "description": "Premium Cashmere Pullover from Innojam. Made of high-quality wool with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere397/600/750"},
    {"product_id": 412, "category_id": 1, "product_name": "Silk Blouse", "brand": "Twitterbeat", "price": 348.60, "color": "Emerald", "size": "M", "material": "silk", "style": "eveningwear", "season": "spring", "inventory_count": 134, "description": "Premium Silk Blouse from Twitterbeat. Made of high-quality silk with an eveningwear style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere412/600/750"},
    {"product_id": 438, "category_id": 1, "product_name": "Knit Cardigan", "brand": "Tagopia", "price": 268.40, "color": "Saffron", "size": "XL", "material": "wool", "style": "casual", "season": "fall", "inventory_count": 178, "description": "Premium Knit Cardigan from Tagopia. Made of high-quality wool with a casual style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere438/600/750"},
    {"product_id": 467, "category_id": 1, "product_name": "Ruffled Blouse", "brand": "Tagchat", "price": 234.90, "color": "Lavender", "size": "S", "material": "silk", "style": "formal", "season": "spring", "inventory_count": 245, "description": "Premium Ruffled Blouse from Tagchat. Made of high-quality silk with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere467/600/750"},
    {"product_id": 489, "category_id": 1, "product_name": "Cotton Tee", "brand": "Voonix", "price": 76.40, "color": "Slate", "size": "L", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 567, "description": "Premium Cotton Tee from Voonix. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere489/600/750"},

    {"product_id": 8, "category_id": 2, "product_name": "Leather Pants", "brand": "Edgeify", "price": 164.90, "color": "Black", "size": "XS", "material": "polyester", "style": "formal", "season": "fall", "inventory_count": 77, "description": "Premium Leather Pants from Edgeify. Made of high-quality polyester with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere8/600/750"},
    {"product_id": 31, "category_id": 2, "product_name": "Denim Jeans", "brand": "Yodoo", "price": 178.20, "color": "Indigo", "size": "M", "material": "cotton", "style": "casual", "season": "spring", "inventory_count": 432, "description": "Premium Denim Jeans from Yodoo. Made of high-quality cotton with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere31/600/750"},
    {"product_id": 52, "category_id": 2, "product_name": "Pleated Skirt", "brand": "Yotz", "price": 198.50, "color": "Black", "size": "S", "material": "polyester", "style": "formal", "season": "fall", "inventory_count": 234, "description": "Premium Pleated Skirt from Yotz. Made of high-quality polyester with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere52/600/750"},
    {"product_id": 83, "category_id": 2, "product_name": "Wool Trousers", "brand": "Roomm", "price": 289.70, "color": "Charcoal", "size": "L", "material": "wool", "style": "formal", "season": "winter", "inventory_count": 178, "description": "Premium Wool Trousers from Roomm. Made of high-quality wool with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere83/600/750"},
    {"product_id": 107, "category_id": 2, "product_name": "Silk Pants", "brand": "Edge", "price": 342.10, "color": "Champagne", "size": "M", "material": "silk", "style": "eveningwear", "season": "summer", "inventory_count": 89, "description": "Premium Silk Pants from Edge. Made of high-quality silk with an eveningwear style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere107/600/750"},
    {"product_id": 142, "category_id": 2, "product_name": "Denim Jeans", "brand": "Skipfire", "price": 156.30, "color": "Navy", "size": "S", "material": "cotton", "style": "casual", "season": "fall", "inventory_count": 389, "description": "Premium Denim Jeans from Skipfire. Made of high-quality cotton with a casual style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere142/600/750"},
    {"product_id": 167, "category_id": 2, "product_name": "A-Line Skirt", "brand": "Brightbean", "price": 215.40, "color": "Burgundy", "size": "M", "material": "polyester", "style": "formal", "season": "winter", "inventory_count": 156, "description": "Premium A-Line Skirt from Brightbean. Made of high-quality polyester with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere167/600/750"},
    {"product_id": 189, "category_id": 2, "product_name": "Linen Shorts", "brand": "Eare", "price": 98.70, "color": "Sand", "size": "L", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 312, "description": "Premium Linen Shorts from Eare. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere189/600/750"},
    {"product_id": 213, "category_id": 2, "product_name": "Leather Pants", "brand": "Yodo", "price": 234.60, "color": "Espresso", "size": "S", "material": "polyester", "style": "eveningwear", "season": "fall", "inventory_count": 67, "description": "Premium Leather Pants from Yodo. Made of high-quality polyester with an eveningwear style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere213/600/750"},
    {"product_id": 236, "category_id": 2, "product_name": "Pleated Skirt", "brand": "Vipe", "price": 187.20, "color": "Ivory", "size": "XS", "material": "polyester", "style": "formal", "season": "spring", "inventory_count": 198, "description": "Premium Pleated Skirt from Vipe. Made of high-quality polyester with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere236/600/750"},
    {"product_id": 263, "category_id": 2, "product_name": "Wool Trousers", "brand": "Topiczoom", "price": 312.80, "color": "Pinstripe", "size": "M", "material": "wool", "style": "formal", "season": "winter", "inventory_count": 134, "description": "Premium Wool Trousers from Topiczoom. Made of high-quality wool with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere263/600/750"},
    {"product_id": 287, "category_id": 2, "product_name": "Denim Jeans", "brand": "Demimark", "price": 142.90, "color": "Vintage Blue", "size": "L", "material": "cotton", "style": "casual", "season": "spring", "inventory_count": 423, "description": "Premium Denim Jeans from Demimark. Made of high-quality cotton with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere287/600/750"},
    {"product_id": 305, "category_id": 2, "product_name": "Silk Pants", "brand": "Quaxo", "price": 367.50, "color": "Rose Gold", "size": "S", "material": "silk", "style": "eveningwear", "season": "summer", "inventory_count": 78, "description": "Premium Silk Pants from Quaxo. Made of high-quality silk with an eveningwear style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere305/600/750"},
    {"product_id": 328, "category_id": 2, "product_name": "Cotton Shorts", "brand": "Yotz", "price": 84.60, "color": "Khaki", "size": "M", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 489, "description": "Premium Cotton Shorts from Yotz. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere328/600/750"},
    {"product_id": 354, "category_id": 2, "product_name": "A-Line Skirt", "brand": "Yodel", "price": 198.40, "color": "Mocha", "size": "XL", "material": "polyester", "style": "formal", "season": "fall", "inventory_count": 167, "description": "Premium A-Line Skirt from Yodel. Made of high-quality polyester with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere354/600/750"},
    {"product_id": 378, "category_id": 2, "product_name": "Leather Pants", "brand": "Fadeo", "price": 256.80, "color": "Onyx", "size": "S", "material": "polyester", "style": "eveningwear", "season": "winter", "inventory_count": 89, "description": "Premium Leather Pants from Fadeo. Made of high-quality polyester with an eveningwear style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere378/600/750"},
    {"product_id": 401, "category_id": 2, "product_name": "Wool Trousers", "brand": "Trupe", "price": 278.30, "color": "Slate", "size": "M", "material": "wool", "style": "formal", "season": "fall", "inventory_count": 145, "description": "Premium Wool Trousers from Trupe. Made of high-quality wool with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere401/600/750"},
    {"product_id": 425, "category_id": 2, "product_name": "Linen Shorts", "brand": "Bluejam", "price": 92.40, "color": "Sage", "size": "L", "material": "cotton", "style": "casual", "season": "spring", "inventory_count": 367, "description": "Premium Linen Shorts from Bluejam. Made of high-quality cotton with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere425/600/750"},
    {"product_id": 449, "category_id": 2, "product_name": "Pleated Skirt", "brand": "Centidel", "price": 175.90, "color": "Plum", "size": "M", "material": "polyester", "style": "formal", "season": "winter", "inventory_count": 198, "description": "Premium Pleated Skirt from Centidel. Made of high-quality polyester with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere449/600/750"},

    {"product_id": 5, "category_id": 3, "product_name": "Denim Jacket", "brand": "Plajo", "price": 229.84, "color": "Turquoise", "size": "M", "material": "silk", "style": "casual", "season": "spring", "inventory_count": 308, "description": "Premium Denim Jacket from Plajo. Made of high-quality silk with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere5/600/750"},
    {"product_id": 38, "category_id": 3, "product_name": "Trench Coat", "brand": "Tagchat", "price": 487.30, "color": "Camel", "size": "M", "material": "wool", "style": "formal", "season": "fall", "inventory_count": 89, "description": "Premium Trench Coat from Tagchat. Made of high-quality wool with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere38/600/750"},
    {"product_id": 67, "category_id": 3, "product_name": "Wool Blazer", "brand": "Edgeify", "price": 412.50, "color": "Navy", "size": "L", "material": "wool", "style": "formal", "season": "winter", "inventory_count": 124, "description": "Premium Wool Blazer from Edgeify. Made of high-quality wool with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere67/600/750"},
    {"product_id": 95, "category_id": 3, "product_name": "Leather Jacket", "brand": "Twinder", "price": 367.80, "color": "Black", "size": "S", "material": "polyester", "style": "casual", "season": "fall", "inventory_count": 156, "description": "Premium Leather Jacket from Twinder. Made of high-quality polyester with a casual style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere95/600/750"},
    {"product_id": 128, "category_id": 3, "product_name": "Wool Coat", "brand": "Yotz", "price": 497.62, "color": "Charcoal", "size": "M", "material": "wool", "style": "formal", "season": "winter", "inventory_count": 67, "description": "Premium Wool Coat from Yotz. Made of high-quality wool with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere128/600/750"},
    {"product_id": 159, "category_id": 3, "product_name": "Denim Jacket", "brand": "Voonix", "price": 198.70, "color": "Light Wash", "size": "L", "material": "cotton", "style": "casual", "season": "spring", "inventory_count": 234, "description": "Premium Denim Jacket from Voonix. Made of high-quality cotton with a casual style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere159/600/750"},
    {"product_id": 187, "category_id": 3, "product_name": "Silk Kimono", "brand": "Avamm", "price": 345.20, "color": "Crimson", "size": "S", "material": "silk", "style": "eveningwear", "season": "summer", "inventory_count": 78, "description": "Premium Silk Kimono from Avamm. Made of high-quality silk with an eveningwear style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere187/600/750"},
    {"product_id": 224, "category_id": 3, "product_name": "Trench Coat", "brand": "Skipfire", "price": 458.90, "color": "Khaki", "size": "M", "material": "cotton", "style": "formal", "season": "fall", "inventory_count": 92, "description": "Premium Trench Coat from Skipfire. Made of high-quality cotton with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere224/600/750"},
    {"product_id": 251, "category_id": 3, "product_name": "Wool Blazer", "brand": "Demivee", "price": 389.40, "color": "Camel", "size": "S", "material": "wool", "style": "formal", "season": "fall", "inventory_count": 134, "description": "Premium Wool Blazer from Demivee. Made of high-quality wool with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere251/600/750"},
    {"product_id": 283, "category_id": 3, "product_name": "Puffer Jacket", "brand": "Yodel", "price": 287.60, "color": "Burgundy", "size": "L", "material": "polyester", "style": "casual", "season": "winter", "inventory_count": 178, "description": "Premium Puffer Jacket from Yodel. Made of high-quality polyester with a casual style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere283/600/750"},
    {"product_id": 311, "category_id": 3, "product_name": "Leather Jacket", "brand": "Brainsphere", "price": 412.30, "color": "Cognac", "size": "M", "material": "polyester", "style": "casual", "season": "fall", "inventory_count": 89, "description": "Premium Leather Jacket from Brainsphere. Made of high-quality polyester with a casual style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere311/600/750"},
    {"product_id": 342, "category_id": 3, "product_name": "Wool Coat", "brand": "Lazzy", "price": 467.80, "color": "Black", "size": "S", "material": "wool", "style": "formal", "season": "winter", "inventory_count": 56, "description": "Premium Wool Coat from Lazzy. Made of high-quality wool with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere342/600/750"},
    {"product_id": 369, "category_id": 3, "product_name": "Silk Kimono", "brand": "Roomm", "price": 298.50, "color": "Emerald", "size": "M", "material": "silk", "style": "eveningwear", "season": "spring", "inventory_count": 67, "description": "Premium Silk Kimono from Roomm. Made of high-quality silk with an eveningwear style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere369/600/750"},
    {"product_id": 398, "category_id": 3, "product_name": "Denim Jacket", "brand": "Innojam", "price": 187.40, "color": "Mid Wash", "size": "S", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 245, "description": "Premium Denim Jacket from Innojam. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere398/600/750"},
    {"product_id": 432, "category_id": 3, "product_name": "Trench Coat", "brand": "Topiczoom", "price": 478.20, "color": "Stone", "size": "L", "material": "cotton", "style": "formal", "season": "spring", "inventory_count": 78, "description": "Premium Trench Coat from Topiczoom. Made of high-quality cotton with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere432/600/750"},
    {"product_id": 458, "category_id": 3, "product_name": "Puffer Jacket", "brand": "Quaxo", "price": 312.40, "color": "Forest", "size": "M", "material": "polyester", "style": "casual", "season": "winter", "inventory_count": 156, "description": "Premium Puffer Jacket from Quaxo. Made of high-quality polyester with a casual style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere458/600/750"},
    {"product_id": 489, "category_id": 3, "product_name": "Wool Blazer", "brand": "Twitterbeat", "price": 367.50, "color": "Midnight", "size": "XL", "material": "wool", "style": "formal", "season": "fall", "inventory_count": 89, "description": "Premium Wool Blazer from Twitterbeat. Made of high-quality wool with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere489B/600/750"},

    {"product_id": 6, "category_id": 5, "product_name": "Floral Maxi Dress", "brand": "Gigaclub", "price": 244.95, "color": "Red", "size": "L", "material": "silk", "style": "formal", "season": "summer", "inventory_count": 831, "description": "Premium Floral Maxi Dress from Gigaclub. Made of high-quality silk with a formal style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere6/600/750"},
    {"product_id": 42, "category_id": 5, "product_name": "Wrap Dress", "brand": "Edge", "price": 287.30, "color": "Black", "size": "M", "material": "polyester", "style": "eveningwear", "season": "fall", "inventory_count": 156, "description": "Premium Wrap Dress from Edge. Made of high-quality polyester with an eveningwear style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere42/600/750"},
    {"product_id": 78, "category_id": 5, "product_name": "Slip Dress", "brand": "Bluejam", "price": 198.40, "color": "Champagne", "size": "S", "material": "silk", "style": "eveningwear", "season": "summer", "inventory_count": 198, "description": "Premium Slip Dress from Bluejam. Made of high-quality silk with an eveningwear style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere78/600/750"},
    {"product_id": 114, "category_id": 5, "product_name": "Floral Maxi Dress", "brand": "Skipfire", "price": 312.70, "color": "Coral", "size": "M", "material": "silk", "style": "formal", "season": "spring", "inventory_count": 134, "description": "Premium Floral Maxi Dress from Skipfire. Made of high-quality silk with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere114/600/750"},
    {"product_id": 152, "category_id": 5, "product_name": "Cocktail Dress", "brand": "Yotz", "price": 367.80, "color": "Burgundy", "size": "S", "material": "polyester", "style": "eveningwear", "season": "winter", "inventory_count": 89, "description": "Premium Cocktail Dress from Yotz. Made of high-quality polyester with an eveningwear style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere152/600/750"},
    {"product_id": 189, "category_id": 5, "product_name": "Sundress", "brand": "Eare", "price": 145.60, "color": "Yellow", "size": "M", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 312, "description": "Premium Sundress from Eare. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere189D/600/750"},
    {"product_id": 226, "category_id": 5, "product_name": "Wrap Dress", "brand": "Tagopia", "price": 234.50, "color": "Emerald", "size": "L", "material": "silk", "style": "formal", "season": "fall", "inventory_count": 178, "description": "Premium Wrap Dress from Tagopia. Made of high-quality silk with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere226/600/750"},
    {"product_id": 264, "category_id": 5, "product_name": "Slip Dress", "brand": "Voonyx", "price": 187.90, "color": "Ivory", "size": "XS", "material": "silk", "style": "eveningwear", "season": "spring", "inventory_count": 145, "description": "Premium Slip Dress from Voonyx. Made of high-quality silk with an eveningwear style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere264/600/750"},
    {"product_id": 298, "category_id": 5, "product_name": "Floral Maxi Dress", "brand": "Mybuzz", "price": 256.80, "color": "Lilac", "size": "M", "material": "silk", "style": "formal", "season": "summer", "inventory_count": 167, "description": "Premium Floral Maxi Dress from Mybuzz. Made of high-quality silk with a formal style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere298/600/750"},
    {"product_id": 335, "category_id": 5, "product_name": "Sheath Dress", "brand": "Brightbean", "price": 298.40, "color": "Navy", "size": "S", "material": "polyester", "style": "formal", "season": "fall", "inventory_count": 134, "description": "Premium Sheath Dress from Brightbean. Made of high-quality polyester with a formal style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere335/600/750"},
    {"product_id": 372, "category_id": 5, "product_name": "Cocktail Dress", "brand": "Yombu", "price": 412.30, "color": "Black", "size": "M", "material": "silk", "style": "eveningwear", "season": "winter", "inventory_count": 67, "description": "Premium Cocktail Dress from Yombu. Made of high-quality silk with an eveningwear style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere372/600/750"},
    {"product_id": 408, "category_id": 5, "product_name": "Wrap Dress", "brand": "Demimark", "price": 245.70, "color": "Mauve", "size": "L", "material": "polyester", "style": "formal", "season": "spring", "inventory_count": 198, "description": "Premium Wrap Dress from Demimark. Made of high-quality polyester with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere408/600/750"},
    {"product_id": 441, "category_id": 5, "product_name": "Sundress", "brand": "Trupe", "price": 134.50, "color": "Sky Blue", "size": "S", "material": "cotton", "style": "casual", "season": "summer", "inventory_count": 289, "description": "Premium Sundress from Trupe. Made of high-quality cotton with a casual style. Perfect for summer.", "image_url": "https://picsum.photos/seed/lumiere441/600/750"},
    {"product_id": 475, "category_id": 5, "product_name": "Floral Maxi Dress", "brand": "Fadeo", "price": 278.60, "color": "Blush", "size": "M", "material": "silk", "style": "formal", "season": "spring", "inventory_count": 156, "description": "Premium Floral Maxi Dress from Fadeo. Made of high-quality silk with a formal style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere475/600/750"},
    {"product_id": 509, "category_id": 5, "product_name": "Sheath Dress", "brand": "Centidel", "price": 312.80, "color": "Wine", "size": "S", "material": "polyester", "style": "formal", "season": "winter", "inventory_count": 89, "description": "Premium Sheath Dress from Centidel. Made of high-quality polyester with a formal style. Perfect for winter.", "image_url": "https://picsum.photos/seed/lumiere509/600/750"},
    {"product_id": 543, "category_id": 5, "product_name": "Slip Dress", "brand": "Quaxo", "price": 198.90, "color": "Sage", "size": "M", "material": "silk", "style": "eveningwear", "season": "spring", "inventory_count": 134, "description": "Premium Slip Dress from Quaxo. Made of high-quality silk with an eveningwear style. Perfect for spring.", "image_url": "https://picsum.photos/seed/lumiere543/600/750"},
    {"product_id": 587, "category_id": 5, "product_name": "Cocktail Dress", "brand": "Tagchat", "price": 387.50, "color": "Sapphire", "size": "L", "material": "polyester", "style": "eveningwear", "season": "fall", "inventory_count": 78, "description": "Premium Cocktail Dress from Tagchat. Made of high-quality polyester with an eveningwear style. Perfect for fall.", "image_url": "https://picsum.photos/seed/lumiere587/600/750"},
]

# helper untuk dapetin daftar nilai unik untuk filter dropdowns
def get_filter_options():
    return {
        "brands": sorted({p["brand"] for p in MOCK_PRODUCTS}),
        "colors": sorted({p["color"] for p in MOCK_PRODUCTS}),
        "sizes": ["XS", "S", "M", "L", "XL"],
        "materials": sorted({p["material"] for p in MOCK_PRODUCTS}),
        "styles": sorted({p["style"] for p in MOCK_PRODUCTS}),
        "seasons": ["spring", "summer", "fall", "winter"],
        "min_price": min(p["price"] for p in MOCK_PRODUCTS),
        "max_price": max(p["price"] for p in MOCK_PRODUCTS),
    }