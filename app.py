import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Tính Doanh Thu Mục Tiêu (Target Revenue)", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    .target-box { background-color: #d1eaed; padding: 15px; border-radius: 10px; border-left: 5px solid #00cec9; }
    .result-box { background-color: #ffeaa7; padding: 15px; border-radius: 10px; border-left: 5px solid #fdcb6e; }
    .big-number { font-size: 24px; font-weight: bold; color: #2d3436; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Tính Doanh Số Để Giữ Nguyên Lợi Nhuận Tuyệt Đối")

# --- 1. SIDEBAR: CẤU HÌNH GỐC ---
with st.sidebar:
    st.header("1. Thông số Cơ bản")
    price = st.number_input("Giá bán niêm yết (VNĐ)", value=120000, step=1000)
    base_cogs = st.number_input("Giá vốn gốc (VNĐ)", value=30000, step=1000)
    
    st.header("2. Chi phí Vận hành (% Doanh thu)")
    # Nhập % như trong bảng Excel của bạn
    pct_mgmt = st.number_input("% Chi phí quản lý", value=10.0)
    pct_salary = st.number_input("% Lương Trình dược viên", value=15.0)
    pct_bonus = st.number_input("% Thưởng khách hàng", value=20.0)
    
    # Tổng chi phí vận hành (OpEx)
    total_opex_pct = (pct_mgmt + pct_salary + pct_bonus) / 100
    st.info(f"Tổng chi phí vận hành: {total_opex_pct*100:.1f}%")

# --- 2. GIAO DIỆN CHÍNH ---
col1, col2 = st.columns([1, 1.1])

# === KỊCH BẢN 1: HIỆN TẠI (ĐỂ TÌM CON SỐ 119 TRIỆU) ===
with col1:
    st.subheader("1️⃣ Kịch bản Cũ (Mốc chuẩn)")
    st.caption("Nhập thông số hiện tại để tính ra lợi nhuận cần đạt.")
    
    current_rev = st.number_input("Doanh thu hiện tại (VNĐ)", value=550000000, step=10000000)
    
    c1a, c1b = st.columns(2)
    with c1a: buy_1 = st.number_input("Mua (SL)", value=3, key="b1")
    with c1b: get_1 = st.number_input("Tặng (SL)", value=1, key="g1")

    # --- TÍNH TOÁN SCENARIO 1 ---
    # Giá vốn đơn vị trung bình sau khi KM
    # Mất vốn cho (Mua + Tặng) nhưng chỉ thu tiền của (Mua)
    # Cách tính của bạn: Giá vốn tăng thêm = (Tặng * Vốn) / Mua
    added_cogs_1 = (get_1 * base_cogs) / buy_1
    total_cogs_unit_1 = base_cogs + added_cogs_1
    
    # Tính chi phí & Lợi nhuận tuyệt đối
    # Tổng giá vốn = Doanh thu * (Giá vốn đơn vị / Giá bán)
    cogs_amount_1 = current_rev * (total_cogs_unit_1 / price)
    opex_amount_1 = current_rev * total_opex_pct
    
    target_profit = current_rev - cogs_amount_1 - opex_amount_1
    
    st.markdown(f"""
    <div class="target-box">
        <p>Lợi nhuận ròng hiện tại:</p>
        <p class="big-number">{target_profit:,.0f} VNĐ</p>
        <small>Đây là con số MỤC TIÊU (Fix cứng) cho kịch bản bên cạnh.</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Bảng chi tiết nhỏ
    st.write(f"- Giá vốn/sp: {total_cogs_unit_1:,.0f} đ (Gốc {base_cogs} + KM {added_cogs_1:,.0f})")
    st.write(f"- Biên lợi nhuận: {(target_profit/current_rev)*100:.1f}%")

# === KỊCH BẢN 2: TÍNH NGƯỢC DOANH THU ===
with col2:
    st.subheader("2️⃣ Kịch bản Mới (Cần đạt)")
    st.caption(f"Làm sao để vẫn lãi đúng {target_profit:,.0f} VNĐ?")
    
    st.markdown("---")
    c2a, c2b = st.columns(2)
    with c2a: buy_2 = st.number_input("Mua (SL) Mới", value=20, key="b2")
    with c2b: get_2 = st.number_input("Tặng (SL) Mới", value=3, key="g2")
    
    # --- TÍNH TOÁN SCENARIO 2 ---
    # 1. Giá vốn đơn vị mới
    added_cogs_2 = (get_2 * base_cogs) / buy_2
    total_cogs_unit_2 = base_cogs + added_cogs_2
    
    # 2. Tỷ lệ Giá vốn mới (COGS %)
    cogs_pct_2 = total_cogs_unit_2 / price
    
    # 3. Tỷ lệ Lợi nhuận ròng mới (Net Margin %)
    # 100% - (Giá vốn % + Vận hành %)
    net_margin_pct_2 = 1 - (cogs_pct_2 + total_opex_pct)
    
    if net_margin_pct_2 <= 0:
        st.error(f"⛔ LỖ VỐN! Với KM Mua {buy_2} Tặng {get_2}, chi phí chiếm hơn 100% giá bán. Không thể hòa vốn.")
    else:
        # 4. TÍNH DOANH THU MỤC TIÊU (THE FORMULA)
        # Revenue = Target_Profit / Net_Margin_%
        required_rev = target_profit / net_margin_pct_2
        
        diff_rev = required_rev - current_rev
        pct_increase = (diff_rev / current_rev) * 100
        
        st.markdown(f"""
        <div class="result-box">
            <p>Doanh thu mới CẦN ĐẠT:</p>
            <p class="big-number" style="color:#d63031">{required_rev:,.0f} VNĐ</p>
            <p>Chênh lệch: <b>{diff_rev:+,.0f} VNĐ</b> ({pct_increase:+.1f}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 🔍 Giải thích logic:")
        st.write(f"1. Giá vốn 1 sp tăng lên: **{total_cogs_unit_2:,.0f} đ** (Do KM mới)")
        st.write(f"2. Tỷ suất lợi nhuận giảm còn: **{net_margin_pct_2*100:.2f}%** (Cũ là {(target_profit/current_rev)*100:.1f}%)")
        st.write(f"3. Để kiếm được **{target_profit:,.0f}**, phép tính là:")
        st.latex(r"DoanhThu = \frac{119,110,000}{" + f"{net_margin_pct_2:.4f}" + r"} \approx " + f"{required_rev:,.0f}")

# --- VẼ BIỂU ĐỒ SO SÁNH ---
st.divider()
st.subheader("📊 So sánh trực quan")

chart_df = pd.DataFrame({
    'Loại': ['Doanh Thu', 'Doanh Thu', 'Lợi Nhuận', 'Lợi Nhuận'],
    'Kịch bản': ['1. Cũ (550tr)', '2. Mới (Cần đạt)', '1. Cũ (550tr)', '2. Mới (Cần đạt)'],
    'Giá trị': [current_rev, required_rev if net_margin_pct_2 > 0 else 0, target_profit, target_profit]
})

c = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X('Kịch bản', axis=None),
    y=alt.Y('Giá trị', title='VNĐ'),
    color=alt.Color('Kịch bản', scale=alt.Scale(range=['#bdc3c7', '#0984e3'])),
    column=alt.Column('Loại', header=alt.Header(titleOrient="bottom", labelFontSize=14)),
    tooltip=['Loại', 'Kịch bản', alt.Tooltip('Giá trị', format=',.0f')]
).properties(width=200)

st.altair_chart(c)
