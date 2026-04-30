import streamlit as st
import pandas as pd
from database import init_db, add_product, get_all_products, get_product_by_id, sell_product, get_sales_report

# Initialize database
init_db()

# Configure page
st.set_page_config(page_title="نظام إدارة المتجر", layout="wide", page_icon="🛒")

# Inject Custom CSS for Premium Luxury Style, RTL and Arabic Font
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

* {
    font-family: 'Cairo', sans-serif !important;
}

body, .stApp {
    direction: rtl;
    text-align: right;
    background: linear-gradient(135deg, #0d001a 0%, #1a0033 50%, #26004d 100%);
    background-attachment: fixed;
    color: #ffffff;
}

/* Glassmorphism for Dataframes, Containers, Tabs */
.stDataFrame, .stExpander, div[data-testid="stVerticalBlock"] > div > div {
    background: rgba(25, 10, 45, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px;
}
.stDataFrame {
    overflow-x: auto;
}

/* Hide Streamlit default background from elements and set desktop width */
[data-testid="stAppViewBlockContainer"] {
    background: transparent !important;
    max-width: 90% !important;
}

/* Adjust dataframe/table alignment */
.dataframe th, .dataframe td {
    text-align: right !important;
    color: #e0e0e0 !important;
    background: transparent !important;
    border-color: rgba(255,255,255,0.1) !important;
}
.dataframe th {
    background: rgba(138, 43, 226, 0.2) !important;
    font-weight: 700;
}

/* Fix sidebar alignment and apply Glassmorphism */
[data-testid="stSidebar"] {
    direction: rtl;
    background: rgba(15, 0, 30, 0.6) !important;
    backdrop-filter: blur(15px) !important;
    -webkit-backdrop-filter: blur(15px) !important;
    border-left: 1px solid rgba(255, 255, 255, 0.05);
}

/* Make headers look premium */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    text-shadow: 0 2px 10px rgba(138, 43, 226, 0.5);
}

/* Metric styling */
[data-testid="stMetricValue"] {
    direction: rtl;
    text-align: right;
    color: #d8b4fe !important;
}
[data-testid="stMetricLabel"] {
    color: #e0e0e0 !important;
}

/* Improve button aesthetics with gradient and hover */
div.stButton > button {
    background: linear-gradient(90deg, #8a2be2 0%, #4b0082 100%);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(138, 43, 226, 0.3);
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #9932cc 0%, #8a2be2 100%);
    border-color: #d8b4fe;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(138, 43, 226, 0.5);
    color: white;
}

/* Premium Selectbox / Input */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="base-input"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    transition: all 0.3s ease;
}
div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover, div[data-baseweb="base-input"]:hover {
    border: 1px solid #8a2be2 !important;
    box-shadow: 0 0 10px rgba(138, 43, 226, 0.3);
}

/* Input texts */
input, select {
    color: white !important;
}

/* Glassmorphism Sidebar Footer */
.sidebar-footer {
    position: relative;
    padding: 1.5rem;
    margin-top: 2rem;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    text-align: center;
    direction: rtl;
    transition: transform 0.3s ease;
}

.sidebar-footer:hover {
    transform: translateY(-5px);
    border-color: rgba(138, 43, 226, 0.4);
}

.sidebar-footer p {
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700;
    font-size: 1.1rem;
    color: #e0e0e0;
    margin-bottom: 0.5rem;
}

.sidebar-footer a.dev-name {
    text-decoration: none;
    color: #d8b4fe;
    font-weight: 800;
    transition: color 0.3s ease;
    display: block;
    margin-bottom: 1.2rem;
}

.sidebar-footer a.dev-name:hover {
    color: #ffffff;
    text-shadow: 0 0 8px rgba(216, 180, 254, 0.8);
}

.social-links {
    display: flex;
    justify-content: center;
    gap: 15px;
}

.social-links a {
    text-decoration: none;
    color: #b0b0b0;
    font-size: 1.8rem;
    transition: all 0.3s ease;
    display: inline-block;
}

.social-links a:hover {
    transform: translateY(-5px) scale(1.1);
}

.social-links .instagram:hover { color: #E1306C; filter: drop-shadow(0 0 8px #E1306C); }
.social-links .facebook:hover { color: #1877F2; filter: drop-shadow(0 0 8px #1877F2); }
.social-links .whatsapp:hover { color: #25D366; filter: drop-shadow(0 0 8px #25D366); }

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, rgba(138, 43, 226, 0.2) 0%, rgba(75, 0, 130, 0.3) 100%);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-title {
    font-family: 'Cairo', sans-serif !important;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    background: linear-gradient(to right, #d8b4fe, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: none; /* text-shadow doesn't work well with background-clip text */
}

.hero-subtitle {
    font-family: 'Cairo', sans-serif !important;
    font-size: 1.5rem;
    font-weight: 600;
    color: #e0e0e0 !important;
}

/* Tabs styling */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    flex-wrap: wrap !important;
}
[data-testid="stTabs"] button {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px 8px 0 0;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-bottom: none !important;
    color: #e0e0e0 !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 700;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    background: rgba(138, 43, 226, 0.3) !important;
    color: white !important;
    border-color: rgba(138, 43, 226, 0.5) !important;
}

/* Hover effects for cards */
.product-card, div[data-testid="stExpander"] {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.product-card:hover, div[data-testid="stExpander"]:hover {
    transform: scale(1.01);
    box-shadow: 0 8px 25px rgba(138, 43, 226, 0.4);
}

/* Hide mobile elements on desktop */
@media (min-width: 769px) {
    .mobile-only-wrapper + div { display: none !important; }
    .mobile-floating-footer { display: none !important; }
}

/* Responsive Mobile Adjustments */
@media (max-width: 768px) {
    /* Hide sidebar completely on mobile */
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }

    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding: 1rem !important;
        padding-bottom: 120px !important;
    }
    .hero-container {
        padding: 1.5rem 1rem;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 1.8rem !important;
    }
    .hero-subtitle {
        font-size: 1rem !important;
    }
    
    /* Floating Footer Styles */
    .mobile-floating-footer {
        display: block;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(15, 0, 30, 0.85) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-top: 1px solid rgba(138, 43, 226, 0.4);
        padding: 1rem;
        z-index: 9999;
        text-align: center;
        box-shadow: 0 -5px 25px rgba(0, 0, 0, 0.6);
    }
    .mobile-floating-footer p {
        font-family: 'Cairo', sans-serif !important;
        font-weight: 700;
        font-size: 1rem;
        color: #e0e0e0;
        margin-bottom: 0.3rem;
    }
    .mobile-floating-footer a.dev-name {
        text-decoration: none;
        color: #d8b4fe;
        font-weight: 800;
        margin-bottom: 0.8rem;
        display: inline-block;
    }
    .mobile-floating-footer .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    .mobile-floating-footer .social-links a {
        font-size: 1.6rem;
        color: #b0b0b0;
        transition: all 0.3s ease;
    }
    .mobile-floating-footer .social-links .instagram:active { color: #E1306C; }
    .mobile-floating-footer .social-links .facebook:active { color: #1877F2; }
    .mobile-floating-footer .social-links .whatsapp:active { color: #25D366; }
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">مرحباً بك في متجر الفخامة</div>
    <div class="hero-subtitle">إدارة المهندس أمجد سلام</div>
</div>
""", unsafe_allow_html=True)

# --- Authentication & Role System ---
admin_pass = "1234"
try:
    if "admin_password" in st.secrets:
        admin_pass = st.secrets["admin_password"]
except Exception:
    pass

is_admin = False

# 1. Desktop Authentication (Sidebar)
st.sidebar.markdown("### 👤 الملف الشخصي")
role_desktop = st.sidebar.selectbox("من يستخدم التطبيق؟", ["البائع", "المدير"], key="role_desktop")
if role_desktop == "المدير":
    password_desktop = st.sidebar.text_input("كلمة المرور", type="password", key="pass_desktop")
    if password_desktop == admin_pass:
        st.sidebar.success("تم تسجيل الدخول كمدير")
        is_admin = True
    elif password_desktop != "":
        st.sidebar.error("كلمة المرور خاطئة")

# 2. Mobile Authentication (Main Body)
st.markdown('<div class="mobile-only-wrapper"></div>', unsafe_allow_html=True)
mobile_auth_container = st.container()
with mobile_auth_container:
    st.markdown("### 👤 الملف الشخصي")
    role_mobile = st.selectbox("من يستخدم التطبيق؟", ["البائع", "المدير"], key="role_mobile")
    if role_mobile == "المدير":
        password_mobile = st.text_input("كلمة المرور", type="password", key="pass_mobile")
        if password_mobile == admin_pass:
            st.success("تم تسجيل الدخول كمدير")
            is_admin = True
        elif password_mobile != "":
            st.error("كلمة المرور خاطئة")

# Create tabs
if is_admin:
    tab1, tab2, tab3, tab4 = st.tabs(["نقطة البيع", "المخزن", "التقارير", "الإعدادات"])
else:
    tabs = st.tabs(["نقطة البيع"])
    tab1 = tabs[0]

# --- TAB 1: Point of Sale (نقطة البيع) ---
with tab1:
    st.header("نقطة البيع")
    
    products_df = get_all_products()
    if not products_df.empty:
        # Create a dictionary for mapping names to IDs
        available_products = products_df[products_df['quantity'] > 0]
        
        if not available_products.empty:
            product_options = {row['name']: row['id'] for _, row in available_products.iterrows()}
            selected_product_name = st.selectbox("اختر المنتج", options=list(product_options.keys()))
            
            if selected_product_name:
                selected_id = product_options[selected_product_name]
                product_data = get_product_by_id(selected_id)
                
                if product_data:
                    p_id, p_name, p_price, p_qty = product_data
                    st.info(f"السعر: {p_price} | الكمية المتاحة: {p_qty}")
                    
                    sell_qty = st.number_input("الكمية المباعة", min_value=1, max_value=p_qty, value=1, step=1)
                    
                    total = p_price * sell_qty
                    st.markdown(f"### المجموع: <span style='color:#f63366'>{total}</span>", unsafe_allow_html=True)
                    
                    if st.button("إتمام البيع"):
                        sell_product(selected_id, sell_qty, total)
                        st.success(f"تم بيع {sell_qty} من {p_name} بنجاح!")
                        st.rerun()
        else:
            st.warning("جميع المنتجات نفدت من المخزن!")
    else:
        st.warning("لا يوجد منتجات في المخزن، يرجى إضافة منتجات أولاً.")

# --- TAB 2: Inventory (قسم المخزن) ---
if is_admin:
    with tab2:
        st.header("إدارة المخزون")
        
        with st.expander("➕ إضافة منتج جديد", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_name = st.text_input("اسم المنتج")
            with col2:
                new_price = st.number_input("السعر", min_value=0.0, step=0.5, format="%f")
            with col3:
                new_qty = st.number_input("الكمية", min_value=0, step=1)
                
            if st.button("إضافة للمخزن"):
                if new_name and new_price > 0 and new_qty >= 0:
                    add_product(new_name, new_price, new_qty)
                    st.success("تمت إضافة المنتج بنجاح!")
                    st.rerun()
                else:
                    st.error("يرجى تعبئة جميع الحقول بشكل صحيح.")
    
        st.subheader("المنتجات الحالية")
        all_products = get_all_products()
        if not all_products.empty:
            # Rename columns for Arabic display
            display_df = all_products.rename(columns={
                'id': 'الرقم',
                'name': 'الاسم',
                'price': 'السعر',
                'quantity': 'الكمية'
            })
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("المخزن فارغ حالياً.")

# --- TAB 3: Reports (التقارير) ---
if is_admin:
    with tab3:
        st.header("تقارير المبيعات")
        
        sales_df = get_sales_report()
        
        if not sales_df.empty:
            total_revenue = sales_df['total_price'].sum()
            total_items_sold = sales_df['quantity'].sum()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("إجمالي المبيعات", f"{total_revenue:,.2f}")
            col2.metric("عدد القطع المباعة", f"{total_items_sold}")
            col3.metric("عدد العمليات", f"{len(sales_df)}")
            
            st.subheader("سجل العمليات")
            # Rename columns for Arabic display
            sales_display = sales_df.rename(columns={
                'id': 'رقم العملية',
                'product_name': 'المنتج',
                'quantity': 'الكمية المباعة',
                'total_price': 'الإجمالي',
                'sale_date': 'تاريخ العملية'
            })
            st.dataframe(sales_display, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد مبيعات حتى الآن.")

# --- TAB 4: Settings (الإعدادات) ---
if is_admin:
    with tab4:
        st.header("الإعدادات")
        st.info("هذا القسم قيد التطوير. سيتم إضافة إعدادات المتجر هنا مستقبلاً.")
        
        st.subheader("إعدادات المظهر")
        st.write("السمة الحالية: **Luxury Dark Glassmorphism** 💜")
        st.write("الخط المستخدم: **Cairo**")

# --- Sidebar Footer (Desktop) ---
st.sidebar.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<div class="sidebar-footer">
    <p>تم التطوير بواسطة</p>
    <a href="mailto:amjadsallam566@gmail.com" class="dev-name">المهندس أمجد سلام</a>
    <div class="social-links">
        <a href="https://wa.me/771158182" target="_blank" class="whatsapp"><i class="fab fa-whatsapp"></i></a>
        <a href="https://www.instagram.com/amjadsa11am?igsh=bHFveTRkcWFyOHdo" target="_blank" class="instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://www.facebook.com/share/1FUNSTGsg7/" target="_blank" class="facebook"><i class="fab fa-facebook"></i></a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Floating Footer (Mobile) ---
st.markdown("""
<div class="mobile-floating-footer">
    <p>تم التطوير بواسطة</p>
    <a href="mailto:amjadsallam566@gmail.com" class="dev-name">المهندس أمجد سلام</a>
    <div class="social-links">
        <a href="https://wa.me/771158182" target="_blank" class="whatsapp"><i class="fab fa-whatsapp"></i></a>
        <a href="https://www.instagram.com/amjadsa11am?igsh=bHFveTRkcWFyOHdo" target="_blank" class="instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://www.facebook.com/share/1FUNSTGsg7/" target="_blank" class="facebook"><i class="fab fa-facebook"></i></a>
    </div>
</div>
""", unsafe_allow_html=True)
