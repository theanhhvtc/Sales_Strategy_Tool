import streamlit as st
import pandas as pd
import altair as alt
import time

st.set_page_config(page_title="Thế Anh Chu Lê - Sales Tool", page_icon="💊", layout="wide")

# --- PHẦN 1: HỆ THỐNG ĐĂNG NHẬP (LOGIN SYSTEM) ---
def check_password():
    """Kiểm tra mật khẩu nhập vào có khớp với Secrets không"""
    def password_entered():
        if st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Xóa pass khỏi bộ nhớ tạm cho an toàn
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "🔒 Vui lòng nhập mật khẩu truy cập:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "🔒 Vui lòng nhập mật khẩu truy cập:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("❌ Mật khẩu không đúng. Vui lòng thử lại.")
        return False
    else:
        return True

# --- NẾU CHƯA ĐĂNG NHẬP THÌ DỪNG LẠI TẠI ĐÂY ---
if not check_password():
    st.stop()

# =========================================================
# TỪ ĐÂY TRỞ XUỐNG LÀ NỘI DUNG CHÍNH CỦA APP
# =========================================================

# --- CẤU HÌNH ẢNH CV ---
cv_img_url = "https://raw.githubusercontent.com/theanhhvtc/Sales_Strategy_Tool/main/cv_img.jpg" 

# --- CSS TRANG TRÍ ---
st.markdown(f"""
<style>
    .target-box {{ background-color: #d1eaed; padding: 15px; border-radius: 10px; border-left: 5px solid #00cec9; }}
    
    /* Box kết quả chính (Sẽ nằm ở đầu) */
    .result-box-top {{ 
        background-color: #ffeaa7; 
        padding: 10px 15px; 
        border-radius: 10px; 
        border-left: 5px solid #fdcb6e; 
        margin-top: 10px;
        min-height: 88px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    
    .big-number {{ font-size: 24px; font-weight: bold; color: #2d3436; }}
    .pct-text {{ font-size: 18px; color: #0984e3; font-weight: normal; margin-left: 8px; }}
    
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
        background-color: white;
    }}
    
    #cv-image:hover {{
        transform: scale(1.1);
    }}
    
    /* CSS MỚI CHO DÒNG REVIEW TIỀN */
    .money-text {{ color: #2ecc71; font-weight: bold; font-size: 16px; }}
    .diff-text {{ font-size: 14px; color: #636e72; }}
</style>
""", unsafe_allow_html=True)

# --- CHÈN ẢNH CV ---
st.markdown(f"""
<img id="cv-image" src="{cv_img_url}" title="Liên hệ: Thế Anh Chu Lê">
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.title("💊 Tool Tính Doanh Số Dược Phẩm")
st.caption("Công cụ hỗ trợ ra quyết định kinh doanh - Developed by Thế Anh Chu Lê")

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. Thông số Cơ bản")
    # Giữ nguyên .0 để tránh Warning
    price = st.number_input("Giá bán (VNĐ)", value=120000.0, step=1000.0, format="%.0f")
    base_cogs = st.number_input("Giá vốn (VNĐ)", value=30000.0, step=1000.0, format="%.0f")
    
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
    
    # INPUT DOANH THU CŨ
    st.markdown('<p style="color: #d63031; font-size: 24px; font-weight: bold; margin-bottom: 5px;">Doanh thu hiện tại (VNĐ)</p>', unsafe_allow_html=True)
    
    current_rev = st.number_input(
        "Label An", 
        value=550000000.0, 
        step=10000000.0, 
        label_visibility="collapsed",
        format="%.0f"
    )
    # Review hiển thị số
    st.markdown(f"👉 Hiển thị: <span class='money-text'>{current_rev:,.0f} VNĐ</span>", unsafe_allow_html=True)
    
    st.markdown("---") 

    st.markdown("<b>Khuyến mại hiện tại (KM1):</b>", unsafe_allow_html=True)
    c1a, c1b = st.columns(2)
    with c1a: buy_1 = st.number_input("Mua (SL)", value=3, key="b1")
    with c1b: get_1 = st.number_input("Tặng (SL)", value=1, key="g1")

    # Tính toán KM1
    added_cost_1 = (get_1 * base_cogs) / buy_1
    total_cogs_unit_1 = base_cogs + added_cost_1
    
    cogs_amount_1 = current_rev * (total_cogs_unit_1 / price)
    opex_amount_1 = current_rev * total_opex_pct
    target_profit = current_rev - cogs_amount_1 - opex_amount_1
    
    # Tính % Lợi nhuận
    profit_margin_1 = (target_profit / current_rev) * 100 if current_rev > 0 else 0
    
    st.markdown(f"""
    <div class="target-box">
        <p>Lợi nhuận hiện tại:</p>
        <p class="big-number">
            {target_profit:,.0f} VNĐ
            <span class="pct-text">({profit_margin_1:.1f}%)</span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Giá vốn hiện tại/sp = {base_cogs:,.0f} + {added_cost_1:,.0f} (KM) = **{total_cogs_unit_1:,.0f} VNĐ/sp**")

# === KỊCH BẢN 2 ===
with col2:
    st.subheader("2️⃣ Kịch bản Mới (KM thêm)")
    
    st.markdown('<p style="color: #d63031; font-size: 24px; font-weight: bold; margin-bottom: 5px;">Doanh thu CẦN ĐẠT (VNĐ)</p>', unsafe_allow_html=True)
    
    # Placeholder giữ chỗ
    result_placeholder = st.empty()
    
    result_placeholder.markdown("""
    <div class="result-box-top">
        <p style="color: #636e72;">Đang tính toán...</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("<b>Khuyến mại thêm (KM2):</b>", unsafe_allow_html=True)
    c2a, c2b = st.columns(2)
    with c2a: buy_2 = st.number_input("Mua (SL) Thêm", value=20, key="b2")
    with c2b: get_2 = st.number_input("Tặng (SL) Thêm", value=3, key="g2")
    
    # --- TÍNH TOÁN LOGIC KỊCH BẢN 2 ---
    cost_km1 = (get_1 * base_cogs) / buy_1  
    cost_km2 = (get_2 * base_cogs) / buy_2  
    total_cogs_unit_2 = base_cogs + cost_km1 + cost_km2
    
    cogs_pct_2 = total_cogs_unit_2 / price
    net_margin_pct_2 = 1 - (cogs_pct_2 + total_opex_pct)
    
    st.write("🔻 **Giá vốn mới/sp:**")
    st.markdown(f"{base_cogs:,.0f} (Gốc) + {cost_km1:,.0f} (KM {buy_1} Tặng {get_1}) + {cost_km2:,.0f} (KM {buy_2} Tặng {get_2}) = **{total_cogs_unit_2:,.0f} VNĐ/sp**")

    # TÍNH TOÁN FINAL
    required_rev = 0 
    if net_margin_pct_2 <= 0:
        result_placeholder.error("⛔ LỖ VỐN! Không thể tính doanh thu mục tiêu.")
        st.error(f"⛔ QUÁ TẢI! Tổng giá vốn ({total_cogs_unit_2:,.0f}đ) + Vận hành > Giá bán.")
    else:
        required_rev = target_profit / net_margin_pct_2
        diff_rev = required_rev - current_rev
        pct_increase = (diff_rev / current_rev) * 100
        
        # BẮN KẾT QUẢ LÊN PLACEHOLDER
        result_placeholder.markdown(f"""
        <div class="result-box-top">
            <span class="big-number" style="color:#d63031">{required_rev:,.0f} VNĐ</span>
            <span class="diff-text">Cần tăng: <b>{diff_rev:+,.0f} VNĐ</b> ({pct_increase:+.1f}%)</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.latex(r"DoanhThu = \frac{\text{Lợi Nhuận Cũ}}{\text{Biên Lãi Mới (" + f"{net_margin_pct_2*100:.1f}\%" + r")}}")

# =========================================================
# PHẦN MỚI: BIỂU ĐỒ PHÂN TÍCH ĐỘ NHẠY (SENSITIVITY ANALYSIS)
# =========================================================
st.markdown("---")
st.subheader("📈 Phân tích Độ nhạy: Giá vốn vs Áp lực Doanh thu")
st.caption("Biểu đồ này trả lời câu hỏi: Nếu tiếp tục tăng khuyến mại (tăng giá vốn), doanh thu phải đạt bao nhiêu?")

# 1. Tạo dữ liệu giả lập (Simulation)
# Mức tăng giá vốn hiện tại do KM
current_added_cost = cost_km1 + cost_km2 

sim_data = []
for extra_cost in range(0, 55000, 2000): # Bước nhảy 2000đ
    # Giá vốn giả định
    sim_total_cogs = base_cogs + extra_cost
    
    # Biên lãi giả định
    sim_cogs_pct = sim_total_cogs / price
    sim_net_margin = 1 - (sim_cogs_pct + total_opex_pct)
    
    # Chỉ tính nếu còn lãi dương
    if sim_net_margin > 0.01: # Lãi > 1% mới tính
        sim_req_rev = target_profit / sim_net_margin
        
        # Đánh dấu điểm hiện tại của bạn
        is_current = "Dự báo"
        # Nếu mức giá vốn này gần bằng mức hiện tại của bạn (sai số 1000đ)
        if abs(extra_cost - current_added_cost) < 1000: 
             is_current = "Hiện tại"

        sim_data.append({
            "Giá vốn tăng thêm": extra_cost,
            "Tổng giá vốn/sp": sim_total_cogs,
            "Doanh thu cần đạt": sim_req_rev,
            "Loại": is_current
        })

df_sim = pd.DataFrame(sim_data)

# 2. Vẽ biểu đồ đường
if not df_sim.empty:
    line = alt.Chart(df_sim).mark_line(strokeWidth=3).encode(
        x=alt.X('Tổng giá vốn/sp', title='Tổng giá vốn (VNĐ/sp)'),
        y=alt.Y('Doanh thu cần đạt', title='Doanh thu mục tiêu (VNĐ)'),
        color=alt.value("#bdc3c7")
    )

    points = alt.Chart(df_sim).mark_circle(size=100).encode(
        x='Tổng giá vốn/sp',
        y='Doanh thu cần đạt',
        color=alt.Color('Loại', scale=alt.Scale(domain=['Dự báo', 'Hiện tại'], range=['#bdc3c7', '#d63031'])),
        tooltip=[
            alt.Tooltip('Tổng giá vốn/sp', format=',.0f'),
            alt.Tooltip('Doanh thu cần đạt', format=',.0f'),
            'Loại'
        ]
    )

    chart_sensitivity = (line + points).properties(
        height=400
    ).interactive()

    st.altair_chart(chart_sensitivity, use_container_width=True)

# --- FOOTER BẢN QUYỀN ---
st.markdown("""
<div class="footer">
    <p>© 2025 Developed by <b>Thế Anh Chu Lê</b>. All rights reserved.<br>
    <i>Dữ liệu chỉ mang tính chất mô phỏng nội bộ.</i></p>
</div>
""", unsafe_allow_html=True)
