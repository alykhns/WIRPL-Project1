import streamlit as st
from utils.session import init_session
from utils.api_client import get_products, get_categories, get_product_filter_options
from components.product_card import product_grid
from components.style import inject_style
from components.navbar import render_navbar

st.set_page_config(page_title="Katalog Produk - Lumière", page_icon="🛍️", layout="wide")

inject_style()
init_session()
render_navbar()

st.markdown("""
    <div style='padding: 2rem 0 1rem'>
        <span style='font-size:0.68rem;letter-spacing:0.35em;text-transform:uppercase;color:var(--gold)'>Discover</span>
        <h1 style='font-family:"Cormorant Garamond",serif;font-weight:300;font-size:2.5rem;color:var(--text)'>
            Our <em style='color:var(--gold)'>Collection</em>
        </h1>
        <div style='width:40px;height:1px;background:var(--gold);margin-top:0.8rem;margin-bottom:2rem'></div>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# INIT SESSION STATE
# ============================================================
DEFAULTS = {
    "kat_search": "",
    "kat_category": "All",
    "kat_brand": "All",
    "kat_color": "All",
    "kat_size": "All",
    "kat_material": "All",
    "kat_style": "All",
    "kat_season": "All",
    "kat_sort": "Newest",
    "kat_price": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

qp = st.query_params
if "category" in qp:
    try:
        cid = int(qp["category"])
        st.session_state["_pending_cat_id"] = cid
    except ValueError:
        pass

# ============================================================
# LOAD FILTER OPTIONS
# ============================================================
cats = get_categories()
opts = get_product_filter_options()

cat_label_to_id = {"All": None}
id_to_label = {None: "All"}
for c in cats:
    cat_label_to_id[c["category_name"]] = c["category_id"]
    id_to_label[c["category_id"]] = c["category_name"]

if "_pending_cat_id" in st.session_state:
    pending_label = id_to_label.get(st.session_state["_pending_cat_id"])
    if pending_label:
        st.session_state["kat_category"] = pending_label
    del st.session_state["_pending_cat_id"]

min_p = float(opts.get("min_price", 0))
max_p = float(opts.get("max_price", 1000))
if st.session_state["kat_price"] is None:
    st.session_state["kat_price"] = (min_p, max_p)

# ============================================================
# FILTER UI
# ============================================================
search_val = st.text_input(
    "Cari Produk",
    value=st.session_state["kat_search"],
    placeholder="Cari nama produk atau brand…",
)
st.session_state["kat_search"] = search_val

c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
with c1:
    cat_val = st.selectbox("Kategori", list(cat_label_to_id.keys()),
                           index=list(cat_label_to_id.keys()).index(st.session_state["kat_category"]))
    st.session_state["kat_category"] = cat_val
with c2:
    size_opts = ["All"] + opts["sizes"]
    size_val = st.selectbox("Ukuran", size_opts,
                            index=size_opts.index(st.session_state["kat_size"]))
    st.session_state["kat_size"] = size_val
with c3:
    season_opts = ["All"] + [s.title() for s in opts["seasons"]]
    season_val = st.selectbox("Musim", season_opts,
                              index=season_opts.index(st.session_state["kat_season"]))
    st.session_state["kat_season"] = season_val
with c4:
    sort_opts = ["Newest", "Price ↑", "Price ↓", "Nama A–Z"]
    sort_val = st.selectbox("Urutkan", sort_opts,
                            index=sort_opts.index(st.session_state["kat_sort"]))
    st.session_state["kat_sort"] = sort_val

with st.expander("◇  Filter Lainnya"):
    f1, f2, f3 = st.columns(3)
    with f1:
        brand_opts = ["All"] + opts["brands"]
        brand_val = st.selectbox("Brand", brand_opts,
                                 index=brand_opts.index(st.session_state["kat_brand"]))
        st.session_state["kat_brand"] = brand_val
    with f2:
        color_opts = ["All"] + opts["colors"]
        color_val = st.selectbox("Warna", color_opts,
                                 index=color_opts.index(st.session_state["kat_color"]))
        st.session_state["kat_color"] = color_val
    with f3:
        style_opts = ["All"] + [s.title() for s in opts["styles"]]
        style_val = st.selectbox("Style", style_opts,
                                 index=style_opts.index(st.session_state["kat_style"]))
        st.session_state["kat_style"] = style_val

    f4, f5 = st.columns(2)
    with f4:
        material_opts = ["All"] + [m.title() for m in opts["materials"]]
        material_val = st.selectbox("Material", material_opts,
                                    index=material_opts.index(st.session_state["kat_material"]))
        st.session_state["kat_material"] = material_val
    with f5:
        price_val = st.slider(
            "Rentang Harga (USD)",
            min_value=min_p, max_value=max_p,
            value=st.session_state["kat_price"],
            step=10.0,
        )
        st.session_state["kat_price"] = price_val

# ============================================================
# RESOLVE FILTER VALUES → panggil API
# ============================================================
def _none_if_all(v):
    return None if v == "All" else v

sort_map = {
    "Newest": "newest",
    "Price ↑": "price_asc",
    "Price ↓": "price_desc",
    "Nama A–Z": "name_asc",
}

results = get_products(
    search=st.session_state["kat_search"] or None,
    category_id=cat_label_to_id.get(st.session_state["kat_category"]),
    brand=_none_if_all(st.session_state["kat_brand"]),
    color=_none_if_all(st.session_state["kat_color"]),
    size=_none_if_all(st.session_state["kat_size"]),
    material=(_none_if_all(st.session_state["kat_material"]) or "").lower() or None,
    style=(_none_if_all(st.session_state["kat_style"]) or "").lower() or None,
    season=(_none_if_all(st.session_state["kat_season"]) or "").lower() or None,
    min_price=st.session_state["kat_price"][0],
    max_price=st.session_state["kat_price"][1],
    sort_by=sort_map[st.session_state["kat_sort"]],
)

# ============================================================
# RESULT BAR + RESET
# ============================================================
rb_left, rb_right = st.columns([4, 1])
with rb_left:
    st.markdown(
        f"<div class='lum-result-bar'>"
        f"<span><strong>{len(results)}</strong> &nbsp;produk ditemukan</span>"
        f"<span>Sort: {st.session_state['kat_sort']}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )
with rb_right:
    if st.button("Reset Filter", use_container_width=True):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v
        st.session_state["kat_price"] = (min_p, max_p)
        st.rerun()

# ============================================================
# GRID
# ============================================================
if not results:
    st.info("Tidak ada produk yang cocok dengan kriteria pencarian Anda.")
else:
    product_grid(results, columns=2)