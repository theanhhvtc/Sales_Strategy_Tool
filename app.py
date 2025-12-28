import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="The Anh Chu Le - Sales Tool", page_icon="💊", layout="wide")

# --- CẤU HÌNH ẢNH CV ---
# Link ảnh CV của bạn (Giữ nguyên)
cv_img_url = "https://raw.githubusercontent.com/theanhhvtc/Sales_Strategy_Tool/main/cv_img.jpg" 

# --- CSS TRANG TRÍ (Đã xóa phần hình nền) ---
st.markdown(f"""
<style>
    /* 1. CSS cho các hộp số liệu (Giữ lại để làm đẹp kết quả) */
    .target-box {{ background-color: #d1eaed; padding: 15px; border-radius: 10px; border-left: 5px solid #00cec9; }}
    .result-box {{ background-color: #ffeaa7; padding: 15px; border-radius: 10px; border-left: 5px solid #fdcb6e; }}
    .big-number {{ font-size: 24px; font-weight: bold; color: #2d3436; }}
    
    /* 2. Footer bản quyền */
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ddd;
        z-index: 100;
    }}
    
    /* 3. Ảnh CV nhỏ ở góc phải dưới */
    #cv-image {{
        position: fixed;
        bottom: 50px; 
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 2px solid #ccc;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        z-index: 101;
        transition: transform 0.3s;
        object-fit: cover;
        background-color: white; /* Thêm nền trắng cho khung ảnh để nổi bật */
    }}
    
    #cv-image:hover {{
        transform: scale(1.1);
    }}
</style>
""", unsafe_allow_html=True)

# --- CHÈN ẢNH CV ---
st.markdown(f"""
<img id="cv-image" src="{cv_img_url}" title="Liên hệ: Thế Anh Chu Lê ">
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.title("💊 Tool Tính Doanh Số Dược Phẩm")
st.caption("Công cụ hỗ trợ ra quyết định kinh doanh - Developed by Thế Anh Chu Lê")

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. Thông số Cơ bản")
    price = st.number_input("Giá bán (VNĐ)", value=120000, step=1000)
    base_cogs = st.number_input("Giá vốn (VNĐ)", value=30000, step=1000)
    
    st.header("2. Chi phí Vận hành (% Doanh thu)")
    pct_mgmt = st.number_input("% Chi phí quản lý", value=10.0)
    pct_salary = st.number_input("% Lương Trình dược viên", value=15.0)
    pct_bonus = st.number_input("% Thưởng khách hàng", value=20.0)
    
    total_opex_pct = (pct_mgmt + pct_salary + pct_bonus) / 100
    st.info(f"Tổng chi phí vận hành: {total_opex_pct*100:.1f}%")

# --- GIAO DIỆN CHÍNH ---
col1, col2 = st.columns([1, 1.1])

# === KỊCH BẢN 1 ===
with col1:
    st.subheader("1️⃣ Kịch bản hiện tại")
    current_rev = st.number_input("Doanh thu hiện tại (VNĐ)", value=550000000, step=10000000)
    
    st.markdown("<b>Khuyến mại hiện tại (KM1):</b>", unsafe_allow_html=True)
    c1a, c1b = st.columns(2)
    with c1a: buy_1 = st.number_input("Mua (SL)", value=3, key="b1")
    with c1b: get_1 = st.number_input("Tặng (SL)", value=1, key="g1")

    # Tính toán
    added_cost_1 = (get_1 * base_cogs) / buy_1
    total_cogs_unit_1 = base_cogs + added_cost_1
    
    cogs_amount_1 = current_rev * (total_cogs_unit_1 / price)
    opex_amount_1 = current_rev * total_opex_pct
    target_profit = current_rev - cogs_amount_1 - opex_amount_1
    
    st.markdown(f"""
    <div class="target-box">
        <p>Lợi nhuận hiện tại:</p>
        <p class="big-number">{target_profit:,.0f} VNĐ</p>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Giá vốn 1 sp = {base_cogs:,.0f} + {added_cost_1:,.0f} (KM)")

# === KỊCH BẢN 2 ===
with col2:
    st.subheader("2️⃣ Kịch bản Mới (Cộng dồn)")
    st.markdown("---")
    st.markdown("<b>Khuyến mại thêm (KM2):</b>", unsafe_allow_html=True)
    c2a, c2b = st.columns(2)
    with c2a: buy_2 = st.number_input("Mua (SL) Thêm", value=20, key="b2")
    with c2b: get_2 = st.number_input("Tặng (SL) Thêm", value=3, key="g2")
    
    # Tính toán
    cost_km1 = (get_1 * base_cogs) / buy_1  
    cost_km2 = (get_2 * base_cogs) / buy_2  
    total_cogs_unit_2 = base_cogs + cost_km1 + cost_km2
    
    cogs_pct_2 = total_cogs_unit_2 / price
    net_margin_pct_2 = 1 - (cogs_pct_2 + total_opex_pct)
    
    st.write("🔻 **Giá vốn mới/sp:**")
    st.markdown(f"{base_cogs:,.0f} (Gốc) + {cost_km1:,.0f} (KM {buy_1} Tặng {get_1}) + {cost_km2:,.0f} (KM {buy_2} Tặng {get_2}) = **{total_cogs_unit_2:,.0f} VNĐ/sp**")

    required_rev = 0 
    if net_margin_pct_2 <= 0:
        st.error(f"⛔ QUÁ TẢI! Tổng giá vốn lên tới {total_cogs_unit_2:,.0f}đ/sp.")
    else:
        required_rev = target_profit / net_margin_pct_2
        diff_rev = required_rev - current_rev
        pct_increase = (diff_rev / current_rev) * 100
        
        st.markdown(f"""
        <div class="result-box">
            <p>Doanh thu mới CẦN ĐẠT:</p>
            <p class="big-number" style="color:#d63031">{required_rev:,.0f} VNĐ</p>
            <p>Cần tăng: <b>{diff_rev:+,.0f} VNĐ</b> ({pct_increase:+.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"DoanhThu = \frac{\text{Lợi Nhuận Cũ}}{\text{Biên Lãi Mới (" + f"{net_margin_pct_2*100:.1f}\%" + r")}}")

# --- BIỂU ĐỒ NGANG ---
st.divider()
chart_df = pd.DataFrame({
    'Loại': ['Doanh Thu', 'Doanh Thu', 'Giá Vốn/SP', 'Giá Vốn/SP'],
    'Kịch bản': ['1. Chỉ KM Cũ', '2. Cộng thêm KM Mới', '1. Chỉ KM Cũ', '2. Cộng thêm KM Mới'],
    'Giá trị': [current_rev, required_rev if net_margin_pct_2 > 0 else 0, total_cogs_unit_1, total_cogs_unit_2]
})

c = alt.Chart(chart_df).mark_bar().encode(
    y=alt.Y('Kịch bản', axis=None),
    x=alt.X('Giá trị', title='Giá trị (VNĐ)'),
    color=alt.Color('Kịch bản', scale=alt.Scale(range=['#7f8c8d', '#e74c3c'])),
    column=alt.Column('Loại', header=alt.Header(titleOrient="bottom")),
    tooltip=['Loại', 'Kịch bản', alt.Tooltip('Giá trị', format=',.0f')]
).properties(width=300)

st.altair_chart(c)

# --- FOOTER BẢN QUYỀN ---
st.markdown("""
<div class="footer">
    <p>© 2025 Developed by <b>The Anh Chu Le</b>. All rights reserved.<br>
    <i>Dữ liệu chỉ mang tính chất mô phỏng nội bộ.</i></p>
</div>
""", unsafe_allow_html=True)
