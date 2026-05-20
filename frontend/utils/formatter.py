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
        "delivered":  "rgba(46, 125, 50, 0.1)",
        "shipping":   "rgba(230, 81, 0, 0.1)",
        "processing": "rgba(21, 101, 192, 0.1)",
        "cancelled":  "rgba(183, 28, 28, 0.1)",
    }
    return backgrounds.get(status.lower(), "rgba(138, 132, 118, 0.1)")