import streamlit as st

# 1. Cài đặt tiêu đề trang web
st.set_page_config(page_title="App Tính Tổng Cute", layout="centered")

# 2. Đưa đoạn CSS màu hồng & nền mây trời vào
custom_css = """
<style>
/* Nền mây trời */
.stApp {
    background-image: url("https://images.pexels.com/photos/37060630/pexels-photo-37060630.jpeg"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Khung kính mờ (Giữ nguyên) */
.block-container {
    background-color: rgba(255, 255, 255, 0.85); 
    border-radius: 30px; 
    padding: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); 
    margin-top: 2rem;
}

/* Bo tròn ô nhập số, viền hồng (Giữ nguyên) */
div[data-baseweb="input"] > div, 
div[data-baseweb="number-input"] > div {
    border-radius: 15px !important; 
    border: 2px solid #ffb3c6 !important; 
    background-color: #fff0f3 !important; 
}

/* 🟢 SỬA LỖI CHỮ TRẮNG Ở ĐÂY 🟢 */
/* Đép chữ người dùng nhập vào thành màu đỏ đô */
input {
    color: #900c3f !important; 
    -webkit-text-fill-color: #900c3f !important; /* Chống trình duyệt tự đổi màu */
    font-weight: bold !important;
    font-size: 1.1rem !important;
}

/* Đổi màu 2 cái nút cộng/trừ đen thui thành màu hồng nhạt */
div[data-baseweb="number-input"] button {
    background-color: #ffb3c6 !important;
    color: white !important;
}

/* Nút bấm TÍNH TOÁN màu hồng */
button[data-testid="baseButton-primary"] {
    background-color: #ff4d6d !important; 
    border: none !important;
    border-radius: 25px !important; 
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 10px rgba(255, 77, 109, 0.4); 
    transition: all 0.3s ease;
    width: 100%; 
}

/* 🟢 SỬA CHỮ TRONG NÚT BẤM 🟢 */
/* Ép chữ trong nút bấm phải là màu trắng, in đậm, và to hơn */
button[data-testid="baseButton-primary"] p {
    color: white !important;
    font-weight: 900 !important;
    font-size: 1.2rem !important;
}

button[data-testid="baseButton-primary"]:hover {
    background-color: #c9184a !important; 
    transform: translateY(-2px); 
}

/* Chữ các tiêu đề màu hồng (Giữ nguyên) */
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
