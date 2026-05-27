import streamlit as st

# 1. Cài đặt tiêu đề trang web
st.set_page_config(page_title="App Tính Tổng Cute", layout="centered")

# 2. Đưa đoạn CSS màu hồng & nền mây trời vào
custom_css = """
<style>
/* Nền mây trời */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500462918059-b1a0cb512f1d?q=80&w=1974&auto=format&fit=crop"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Khung kính mờ bo tròn */
.block-container {
    background-color: rgba(255, 255, 255, 0.85); 
    border-radius: 30px; 
    padding: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); 
    margin-top: 2rem;
}

/* Bo tròn ô nhập số, viền hồng */
div[data-baseweb="input"] > div, 
div[data-baseweb="number-input"] > div {
    border-radius: 15px !important; 
    border: 2px solid #ffb3c6 !important; 
    background-color: #fff0f3 !important; 
}

/* Nút bấm màu hồng */
button[data-testid="baseButton-primary"] {
    background-color: #ff4d6d !important; 
    border: none !important;
    border-radius: 25px !important; 
    color: white !important;
    font-weight: bold !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 10px rgba(255, 77, 109, 0.4); 
    transition: all 0.3s ease;
    width: 100%; /* Cho nút bấm dài ra bằng chiều ngang */
}

button[data-testid="baseButton-primary"]:hover {
    background-color: #c9184a !important; 
    transform: translateY(-2px); 
}

/* Chữ màu hồng */
h1, h2, h3, h4, p {
    color: #ff4d6d !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 3. GIAO DIỆN BÀI TOÁN TÍNH TỔNG
# ==========================================
st.markdown("### 🎀 BÀI TOÁN TÍNH TỔNG")

# Chia màn hình thành 5 cột
col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])

# Cột 1: Ô nhập x1
with col1:
    x1 = st.number_input("x1", value=0.0, step=1.0, label_visibility="collapsed")

# Cột 2: Hiển thị dấu cộng
with col2:
    st.markdown("<h2 style='text-align: center;'>+</h2>", unsafe_allow_html=True)

# Cột 3: Ô nhập x2
with col3:
    x2 = st.number_input("x2", value=0.0, step=1.0, label_visibility="collapsed")

# Cột 4: Hiển thị dấu bằng
with col4:
    st.markdown("<h2 style='text-align: center;'>=</h2>", unsafe_allow_html=True)

# Cột 5: Chỗ trống để chứa kết quả (hoặc hiển thị dấu ?)
with col5:
    result_placeholder = st.empty()
    result_placeholder.markdown("<h2 style='text-align: center;'>?</h2>", unsafe_allow_html=True)

st.write("") # Dòng trống cho thoáng
st.write("") 

# ==========================================
# 4. XỬ LÝ NÚT BẤM
# ==========================================
if st.button("TÍNH TOÁN", type="primary"):
    ket_qua = x1 + x2
    # Cập nhật kết quả vào vị trí dấu chấm hỏi
    result_placeholder.markdown(f"<h2 style='text-align: center;'>{ket_qua}</h2>", unsafe_allow_html=True)