import streamlit as st

# 1. Cài đặt tiêu đề trang web
st.set_page_config(page_title="App Tính Tổng - Montserrat Blue", layout="centered")

# 2. Đưa đoạn CSS font Montserrat & màu XANH DƯƠNG vào
custom_css = """
<style>
/* Nạp font Montserrat từ Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

/* 1. ĐỔI TOÀN BỘ FONT THÀNH MONTSERRAT */
* {
    font-family: 'Montserrat', sans-serif !important;
}

/* Nền mây trời */
.stApp {
    background-image: url("https://wptutbyserahwang.wordpress.com/wp-content/uploads/2019/10/18.gif"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 2. KHUNG TỔNG ÉP 2 LỚP NỀN */
.block-container {
    /* Gộp cả 2 lớp nền vào chung: Lớp trắng mờ ở trên, lớp ảnh ở dưới */
    background-image: 
        /* Lớp 1 (NEN-MO): Dùng gradient trải đều màu trắng mờ 88.8% */
        linear-gradient(rgba(255, 255, 255, 0.888), rgba(255, 255, 255, 0.888)),
        /* Lớp 2 (NEN-ANH): Ảnh background của bạn */
        url("https://wptutbyserahwang.wordpress.com/wp-content/uploads/2020/04/197.jpg?w=560");
    
    background-size: cover;
    background-position: center;

    /* 🟢 TUYỆT CHIÊU CẮT LỚP Ở ĐÂY 🟢 */
    /* Lớp trắng mờ sẽ dừng lại ở mép trong, còn lớp ảnh sẽ tràn ra ngoài tạo thành viền */
    background-clip: padding-box, border-box;
    background-origin: padding-box, border-box;

    /* Độ dày của phần viền ảnh (Thay cho padding 2% của bạn) */
    border: 20px solid transparent !important; 
    border-radius: 20px; 
    
    padding: 2rem; /* Khoảng đệm của NEN-MO */
    
    max-width: 750px !important; 
    margin: auto !important; 
    
    /* Vẫn giữ lại quả bóng đổ 30 độ siêu nghệ thuật */
    box-shadow: -15px 26px 50px rgba(30, 58, 138, 0.3) !important; 
}

div[data-testid="stMain"] {
    justify-content: center !important;
}

/* 3. LÀM ĐỀU CÁC Ô NHẬP LIỆU (Ẩn nút cộng trừ) */
button[aria-label="Step Up"], button[aria-label="Step Down"] {
    display: none !important;
}

/* Viền ô nhập số đổi sang màu XANH DƯƠNG NHẠT TRỰC QUAN */
div[data-baseweb="input"] > div, 
div[data-baseweb="number-input"] > div {
    border-radius: 15px !important; 
    border: 2px solid #93c5fd !important; 
    background-color: #eff6ff !important; /* Nền trong ô xanh dương siêu nhạt */
}

/* Chữ số người dùng nhập vào màu XANH DƯƠNG ĐẬM */
input {
    color: #1e3a8a !important; 
    -webkit-text-fill-color: #1e3a8a !important;
    font-weight: bold !important;
    font-size: 1.2rem !important;
    text-align: center !important; 
}

/* 4. SỬA NÚT TÍNH TOÁN THÀNH MÀU XANH DƯƠNG */
button[data-testid="baseButton-primary"] {
    background-color: #3b82f6 !important; /* Nền nút Xanh dương sáng */
    border: none !important;
    border-radius: 25px !important; 
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4); /* Bóng đổ xanh dương mờ */
    width: 100%; 
    margin-top: 20px !important; 
    transition: all 0.3s ease;
}

/* Chữ trắng nổi bật trên nền nút xanh dương */
button[data-testid="baseButton-primary"] * {
    color: #ffffff !important; 
    font-weight: bold !important;
    font-size: 1.2rem !important;
}

/* Hiệu ứng khi rê chuột vào nút tính toán */
button[data-testid="baseButton-primary"]:hover {
    background-color: #1d4ed8 !important; /* Đổi sang màu Xanh dương đậm đầm mắt hơn */
    transform: translateY(-2px); 
}

/* Đổi màu chữ tiêu đề và văn bản thành XANH DƯƠNG ĐẬM */
h1, h2, h3, h4, p {
    color: #1e3a8a !important;
}

/* 5. CÔNG CỤ CANH GIỮA DẤU CỘNG, BẰNG, HỎI CHẤM */
.math-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 45px;
    font-size: 2rem;
    font-weight: bold;
    color: #1e3a8a;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 3. GIAO DIỆN BÀI TOÁN TÍNH TỔNG
# ==========================================
st.markdown("### 🧩 BÀI TOÁN TÍNH TỔNG")
st.write("") 

col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 2])

with col1:
    x1 = st.number_input("x1", value=0.0, step=1.0, label_visibility="collapsed")

with col2:
    st.markdown("<div class='math-icon'>+</div>", unsafe_allow_html=True)

with col3:
    x2 = st.number_input("x2", value=0.0, step=1.0, label_visibility="collapsed")

with col4:
    st.markdown("<div class='math-icon'>=</div>", unsafe_allow_html=True)

with col5:
    result_placeholder = st.empty()
    result_placeholder.markdown("<div class='math-icon'>?</div>", unsafe_allow_html=True)

st.write("") 

# ==========================================
# 4. XỬ LÝ NÚT BẤM
# ==========================================
if st.button("TÍNH TOÁN", type="primary"):
    ket_qua = x1 + x2
    result_placeholder.markdown(f"<div class='math-icon'>{ket_qua}</div>", unsafe_allow_html=True)
