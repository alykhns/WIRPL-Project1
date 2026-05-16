def format_price(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")

def get_status_color(status):
    colors = {
        "delivered":  "#2E7D32",
        "shipping":   "#E65100",
        "processing": "#1565C0",
        "cancelled":  "#B71C1C",
    }
    return colors.get(status.lower(), "#8A8476")

def get_status_bg(status):
    backgrounds = {
        "delivered":  "#E8F5E9",
        "shipping":   "#FFF3E0",
        "processing": "#E3F2FD",
        "cancelled":  "#FFEBEE",
    }
    return backgrounds.get(status.lower(), "#F5F5F5")