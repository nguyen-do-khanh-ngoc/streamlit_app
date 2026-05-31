import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from fractions import Fraction
import re
import copy
import os

os.makedirs(".streamlit", exist_ok=True)
with open(".streamlit/config.toml", "w") as f:
    f.write('[theme]\nprimaryColor="#3b82f6"\n')

# ==========================================
# 1. CÀI ĐẶT GIAO DIỆN & CSS
# ==========================================
st.set_page_config(page_title="LP Solver - Simplex", layout="centered", initial_sidebar_state="collapsed")

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

/* 🟢 ÁP DỤNG FONT CHỮ CHO TOÀN WEB NHƯNG CHỪA CÁC ICON RA */
html, body, p, div, h1, h2, h3, h4, h5, h6, span, button, input, label, li, table, td, th {
    font-family: 'Montserrat', sans-serif !important; 
}

/* 🟢 TRẢ LẠI FONT BIỂU TƯỢNG (ICON) MẶC ĐỊNH CHO STREAMLIT */
.material-symbols-rounded, .material-icons, [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}

.stApp {
    background-image: url("https://images.pexels.com/photos/37717845/pexels-photo-37717845.jpeg"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {
    background-color: rgba(255, 255, 255, 0.95); 
    border-radius: 25px !important; 
    padding: 3rem;
    box-shadow: 
        /* Lớp 1 (Trên cùng): Đệm màu xanh nhạt dày 25px */
        inset 0 0 0 20px #dbeafe, 
    
        /* Lớp 2: Bóng mờ 30 độ rớt ra ngoài màn hình (Giữ nguyên của bạn) */
        -15px 26px 50px rgba(30, 58, 138, 0.3) !important;
    border: 5px ridge #3b82f6 !important; 
    max-width: 900px !important; 
    margin: auto !important; 
    margin-top: 8vh !important; 
    margin-bottom: 8vh !important;
}

div[data-baseweb="input"] > div, 
div[data-baseweb="number-input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 10px !important; 
    border: 3px solid #93c5fd !important; 
    background-color: #eff6ff !important; 
}

input {
    color: #1e3a8a !important; 
    -webkit-text-fill-color: #1e3a8a !important;
    font-weight: bold !important;
    text-align: center !important;
}

div[data-testid="stButton"]{
    width:100% !important;
    display:flex !important;
    justify-content:center !important;
    margin-top:20px !important;
}

div[data-testid="stButton"] > button{
    width:100% !important;

    background:#3b82f6 !important;
    color:white !important;

    border:none !important;
    border-radius:50px !important;

    padding:16px 40px !important;

    font-size:1.35rem !important;
    font-weight:900 !important;
    letter-spacing:2px !important;
    text-transform:uppercase !important;

    box-shadow:0 8px 20px rgba(59,130,246,0.4) !important;

    transition:all 0.3s ease !important;
}

div[data-testid="stButton"] > button *{
    color:white !important;
    font-weight:900 !important;
    font-size:1.35rem !important;
    letter-spacing:2px !important;
    text-transform:uppercase !important;
}

div[data-testid="stButton"] > button:hover{
    background:#1d4ed8 !important;
    transform:translateY(-4px) !important;
    box-shadow:0 12px 25px rgba(59,130,246,0.6) !important;
}

div[data-testid="stButton"] > button:focus{
    outline:none !important;
}

/* Các đoạn ÉP CHỮ và HIỆU ỨNG RÊ CHUỘT bên dưới vẫn giữ nguyên y xì cũ nha */

/* 🟢 3. ÉP CHỮ BÊN TRONG: TRẮNG BÓC, TO VÀ SIÊU ĐẬM */
button[data-testid="baseButton-primary"] p,
button[data-testid="baseButton-primary"] div,
button[data-testid="baseButton-primary"] span,
button[data-testid="baseButton-primary"] * {
    color: #ffffff !important; /* Trắng tinh khôi */
    font-weight: 900 !important; /* 900 là độ in đậm tối đa */
    font-size: 1.6rem !important; /* Phóng to size chữ */
    letter-spacing: 2px !important; /* Giãn cách các chữ cái ra một xíu cho sang */
    text-transform: uppercase !important; /* Ép viết hoa toàn bộ */
}

/* 🟢 4. HIỆU ỨNG NHẢY LÊN KHI RÊ CHUỘT */
button[data-testid="baseButton-primary"]:hover {
    background-color: #1d4ed8 !important; 
    transform: translateY(-4px) !important; /* Nảy lên cao hơn xíu */
    box-shadow: 0 12px 25px rgba(59, 130, 246, 0.6) !important; /* Bóng đổ đậm hơn */
}

div[data-testid="stButton"] > button{
    display:flex !important;
    justify-content:center !important;
    align-items:center !important;
    gap:8px !important;
}

h1, h2, h3, h4, p, label {
    color: #1e3a8a !important;
}

/* Tùy chỉnh lịch sử các bước lặp */
.history-eq {
    background: #f8fafc;
    border-left: 4px solid #3b82f6;
    padding: 8px 15px;
    margin-bottom: 5px;
    font-family: 'Courier New', Courier, monospace !important;
    font-size: 1.1rem;
    color: #0f172a;
}

/* 1. Trạng thái bình thường: Nền trong suốt, Icon dấu cộng/trừ màu xanh đậm */
button[aria-label="Step Up"], 
button[aria-label="Step Down"] {
    background-color: transparent !important; 
}
button[aria-label="Step Up"] svg, 
button[aria-label="Step Down"] svg {
    fill: #1e3a8a !important; /* Lệnh đổ màu cho hình SVG */
    color: #1e3a8a !important;
    transition: all 0.3s ease;
}

/* 2. Trạng thái rê chuột (Hover) / Bấm (Active) / Đang chọn (Focus) */
button[aria-label="Step Up"]:hover, 
button[aria-label="Step Down"]:hover,
button[aria-label="Step Up"]:active, 
button[aria-label="Step Down"]:active,
button[aria-label="Step Up"]:focus, 
button[aria-label="Step Down"]:focus {
    background-color: #3b82f6 !important; /* Đổi nền nút thành xanh sáng */
    border-color: #3b82f6 !important;
}

/* 3. Đổi icon SVG thành màu trắng khi rê chuột vào */
button[aria-label="Step Up"]:hover svg, 
button[aria-label="Step Down"]:hover svg,
button[aria-label="Step Up"]:active svg, 
button[aria-label="Step Down"]:active svg,
button[aria-label="Step Up"]:focus svg, 
button[aria-label="Step Down"]:focus svg {
    fill: #ffffff !important; /* Tô trắng hình cộng/trừ */
    color: #ffffff !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
ul[data-baseweb="menu"] li {
    font-weight: bold !important; 
    color: #1e3a8a !important; /* Đảm bảo màu xanh đậm tone-sur-tone */
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

tieu_de_html = """
<div style="text-align: center; margin-top: -20px; margin-bottom: 30px;">
    <span style="display: inline-block; background: white; padding: 10px 30px; font-size: 24px; font-weight: bold; color: #1e3a8a; border-radius: 15px; box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);">
        🧩 QUY HOẠCH TUYẾN TÍNH (SIMPLEX)
    </span>
</div>
"""
st.markdown(tieu_de_html, unsafe_allow_html=True)

# ==========================================
# 2. CLASS LÕI THUẬT TOÁN
# ==========================================
class SimplexDictionarySolver:
    def __init__(self, num_vars, num_constraints, objective_type, c, A, b, bound_signs, var_signs, pivot_rule="BLAND"):
        """
        Khởi tạo và lưu trữ các tham số đầu vào gốc.
        Sử dụng Fraction để triệt tiêu hoàn toàn sai số dấu phẩy động.
        """
        self.original_num_vars = num_vars
        self.original_num_constraints = num_constraints
        self.objective_type = objective_type.upper() # 'MAX' hoặc 'MIN'

        self.pivot_rule = pivot_rule.upper() # 'BLAND' hoặc 'DANTZIG'
        self.max_iterations = 1000 # Ngưỡng tối đa để chống lặp vô tận
        self.iteration_count = 0 # Bộ đếm số bước xoay

        # Chuyển đổi toàn bộ dữ liệu số sang dạng phân số (Fraction) để tránh sai số
        self.c = [Fraction(str(val)) for val in c]
        self.b = [Fraction(str(val)) for val in b]
        self.A = [[Fraction(str(val)) for val in row] for row in A]

        self.bound_signs = [sign.strip() for sign in bound_signs]
        self.var_signs = [sign.replace(" ", "") for sign in var_signs]

        # Trạng thái hệ thống (Từ vựng)
        self.B = [] # Tập biến cơ sở
        self.N = [] # Tập biến phi cơ sở
        self.dictionary = {} # Lưu trữ hệ phương trình từ vựng: {var_B: {'const': val, var_N1: val, ...}}
        self.objective_func = {} # Lưu hàm mục tiêu hiện tại (Z hoặc W)
        self.Z = {'const': Fraction(0)} # Hàm mục tiêu chính (Từ Mã nguồn 1)
        self.W = {'const': Fraction(0)} # Hàm mục tiêu Pha 1 (Từ Mã nguồn 1)

        self.status = "INITIALIZED" # Trạng thái bài toán
        self.has_infinite_solutions = False
        self.history = [] # Lưu lại lịch sử từng bước để vẽ UI (hiển thị lên Streamlit)

        # Biến phụ trợ để lưu vết phục hồi nghiệm nguyên thủy (x <= 0, tùy ý)
        self.original_var_mapping = {} # Lưu vết biến đổi biến
        self.var_mapping = {} # Ví dụ: 'x1': [('x1_plus', 1), ('x1_minus', -1)]
        self.original_Z_expr = {} # Biểu thức Z sau khi chuẩn hóa biến

    # ==========================================
    # BƯỚC 0: CHUẨN HÓA BÀI TOÁN
    # ==========================================
    def standardize_problem(self):
        """
        Đưa bài toán về dạng chuẩn (MIN & <=) theo đúng mã giả.
        1. Chuẩn hóa biến (x <= 0, x tùy ý).
        2. Chuẩn hóa hàm MAX thành MIN.
        3. Tách dấu '=' thành <= và >=, đảo dấu >= thành <=.
        """
        new_c = []
        new_A = [[] for _ in range(self.original_num_constraints)]
        var_idx = 1

        # 1. Chuẩn hóa biến (x <= 0, x tùy ý)
        for j in range(self.original_num_vars):
            orig_var = f"x{j+1}"
            sign = self.var_signs[j]

            if sign == ">=0":
                new_var = f"x{var_idx}"
                self.original_var_mapping[orig_var] = [new_var]
                self.var_mapping[orig_var] = [(new_var, 1)] # 1 là hệ số dương
                new_c.append(self.c[j])
                for i in range(self.original_num_constraints): new_A[i].append(self.A[i][j])
                self.N.append(new_var)
                var_idx += 1

            elif sign == "<=0":
                new_var = f"x{var_idx}"
                self.original_var_mapping[orig_var] = [f"-{new_var}"]
                self.var_mapping[orig_var] = [(new_var, -1)]
                new_c.append(-self.c[j])
                for i in range(self.original_num_constraints): new_A[i].append(-self.A[i][j])
                self.N.append(new_var)
                var_idx += 1

            elif sign == "free" or sign == "tùyý":
                var_plus = f"x{var_idx}"
                var_minus = f"x{var_idx+1}"
                self.original_var_mapping[orig_var] = [var_plus, f"-{var_minus}"]
                self.var_mapping[orig_var] = [(var_plus, 1), (var_minus, -1)]
                new_c.extend([self.c[j], -self.c[j]])
                for i in range(self.original_num_constraints):
                    new_A[i].extend([self.A[i][j], -self.A[i][j]])
                self.N.extend([var_plus, var_minus])
                var_idx += 2

        # 2. Chuẩn hóa hàm mục tiêu (MAX -> MIN)
        is_max = (self.objective_type == 'MAX')
        multiplier = Fraction(-1) if is_max else Fraction(1)
        self.original_Z_expr = {'const': Fraction(0)}

        for j, var in enumerate(self.N):
            # Nếu gốc là MAX, ta nhân -1 để đưa về MIN
            coeff = new_c[j] * multiplier
            self.original_Z_expr[var] = coeff
            self.Z[var] = coeff # Đồng bộ trạng thái Z ban đầu

        # 3. Chuẩn hóa ràng buộc (Đưa về <=)
        final_A, final_b = [], []
        for i in range(self.original_num_constraints):
            if self.bound_signs[i] == '<=':
                final_A.append(new_A[i])
                final_b.append(self.b[i])
            elif self.bound_signs[i] == '>=':
                final_A.append([-val for val in new_A[i]])
                final_b.append(-self.b[i])
            elif self.bound_signs[i] == '=':
                # Tách thành <= và >= (rồi đảo dấu >= lập tức nhân -1 thành <=)
                final_A.append(new_A[i])
                final_b.append(self.b[i])
                final_A.append([-val for val in new_A[i]])
                final_b.append(-self.b[i])

        self.A = final_A
        self.b = final_b

    # ==========================================
    # BƯỚC 1: LẬP TỪ VỰNG VÀ RẼ NHÁNH
    # ==========================================
    def build_initial_dictionary(self):
        """
        Thêm biến bù (slack variables - w_i).
        Kiểm tra vector b để quyết định đi thẳng Pha 2 hay phải qua Pha 1.
        """
        for i in range(len(self.b)):
            w_var = f"w{i+1}"
            self.B.append(w_var)
            self.dictionary[w_var] = {'const': self.b[i]}
            for j, x_var in enumerate(self.N):
                # w_i = b_i - sum(a_ij * x_j) => Hệ số lưu trữ là -a_ij
                self.dictionary[w_var][x_var] = -self.A[i][j]

        # Rẽ nhánh: Có b_i < 0 không? Nếu có bất kỳ b_i < 0, bắt buộc qua Pha 1
        return any(val < 0 for val in self.b)

    # ==========================================
    # BƯỚC 2: PHA 1 (TÌM MIỀN KHẢ THI)
    # ==========================================
    def phase_1(self):
        """
        Thêm biến giả x0.
        Khởi tạo hàm mục tiêu W = x0.
        Special Pivot để đẩy x0 vào cơ sở.
        Gọi simplex_loop(W).
        Xử lý x0 sau khi kết thúc Pha 1.
        """
        # 1. Khởi tạo x0 và thêm vào tất cả các phương trình
        self.N.append('x0')
        for w_var in self.B:
            self.dictionary[w_var]['x0'] = Fraction(1)

        # Khởi tạo hàm mục tiêu Pha 1: MIN W = x0
        self.objective_func = {'const': Fraction(0), 'x0': Fraction(1)}
        self.W = self.objective_func # Đồng bộ biến W
        for x_var in self.N:
            if x_var != 'x0': self.objective_func[x_var] = Fraction(0)

        # 2. Special Initial Pivot: Ép x0 vào cơ sở, biến ra là w_k có b_k âm nhất
        leaving_var = min(self.B, key=lambda v: (self.dictionary[v]['const'], self._sort_key(v)))
        self.pivot('x0', leaving_var, self.objective_func)

        # 3. Chạy Simplex Pha 1
        status = self.simplex_loop(self.objective_func)
        if status == "UNBOUNDED":
            return False # Lý thuyết Pha 1 không thể Unbounded, nhưng đặt để an toàn

        # 4. Đánh giá Pha 1
        W_opt = self.objective_func.get('const', Fraction(0))
        if W_opt > 0:
            return False # Hệ vô nghiệm

        if W_opt == 0:
            # Nếu x0 vẫn kẹt trong cơ sở B
            if 'x0' in self.B:
                eq = self.dictionary['x0']
                # Tìm biến phi cơ sở có hệ số khác 0 để pivot x0 ra
                valid_entering = [v for v in self.N if v != 'x0' and eq.get(v, Fraction(0)) != 0]
                if not valid_entering:
                    # Ràng buộc dư thừa, xóa bỏ
                    self.B.remove('x0')
                    del self.dictionary['x0']
                else:
                    # Ưu tiên Bland rule để chọn biến vào
                    entering_var = min(valid_entering, key=self._sort_key)
                    self.pivot(entering_var, 'x0', self.objective_func)

            # Dọn dẹp hoàn toàn x0 khỏi hệ thống
            if 'x0' in self.N: self.N.remove('x0')
            for b_var in self.B:
                if 'x0' in self.dictionary[b_var]:
                    del self.dictionary[b_var]['x0']
            return True

    # ==========================================
    # BƯỚC 3: PHA 2 (TÌM NGHIỆM TỐI ƯU)
    # ==========================================
    def phase_2(self):
        """
        Khôi phục hàm Z gốc.
        Thế các biến cơ sở B vào Z.
        Gọi simplex_loop(Z).
        """
        # 1. Khôi phục hàm Z gốc
        self.objective_func = {'const': self.original_Z_expr['const']}
        for v in self.N: self.objective_func[v] = Fraction(0)

        # 2. Thế biểu thức của các biến (nếu chúng đang ở trong B) vào Z
        for var, coeff in self.original_Z_expr.items():
            if var == 'const' or coeff == 0: continue

            if var in self.N:
                self.objective_func[var] = self.objective_func.get(var, Fraction(0)) + coeff
            elif var in self.B:
                eq = self.dictionary[var]
                self.objective_func['const'] += coeff * eq['const']
                for n_var in self.N:
                    self.objective_func[n_var] = self.objective_func.get(n_var, Fraction(0)) + coeff * eq.get(n_var, Fraction(0))

        self.Z = self.objective_func # Cập nhật Z thực tế sau khi thế

        # 3. Chạy Simplex Pha 2
        self.status = self.simplex_loop(self.objective_func)

    # ==========================================
    # BƯỚC 4: HÀM CỐT LÕI - SIMPLEX LOOP
    # ==========================================
    def simplex_loop(self, objective_func):
        """
        Vòng lặp Simplex chung cho cả Pha 1 và Pha 2.
        - Chọn biến vào (Tùy chọn Quy tắc Bland hoặc Dantzig).
        - Chọn biến ra (Quy tắc tỷ số, hòa thì dùng Bland).
        - Cập nhật Dictionary (Pivot).
        - Tích hợp cơ chế Anti-Cycling (Tự động lùi về Bland nếu đạp vòng).
        Lưu ý: Dùng yield hoặc lưu vào self.history để theo dõi trạng thái.
        """
        while True:
            # --- CƠ CHẾ BỔ SUNG: Chống đạp vòng (Anti-Cycling Fallback) ---
            self.iteration_count += 1
            if self.iteration_count > self.max_iterations:
                if self.pivot_rule == "DANTZIG":
                    # Đang dùng Dantzig mà bị lặp vô hạn -> Ép về Bland để thoát
                    self.pivot_rule = "BLAND"
                    self.iteration_count = 0
                else:
                    # Nếu dùng Bland mà vẫn quá giới hạn (có thể do lỗi dữ liệu)
                    return "MAX_ITERATIONS_REACHED"

            self._save_history(objective_func)

            # 1. Kiểm tra dừng & Chọn Biến Vào (Entering)
            # Vì ta luôn dùng hàm MIN, ta tìm các biến phi cơ sở có hệ số < 0
            entering_candidates = [v for v in self.N if objective_func.get(v, Fraction(0)) < 0]

            if not entering_candidates:
                return "OPTIMAL" # Đã tối ưu (Mọi c_j >= 0)

            # --- CƠ CHẾ BỔ SUNG: Lựa chọn Quy tắc ---
            if getattr(self, 'pivot_rule', 'BLAND') == "DANTZIG":
                # Quy tắc DANTZIG: Chọn biến có hệ số âm nhất
                min_coeff = min(objective_func[v] for v in entering_candidates)
                best_entering = [v for v in entering_candidates if objective_func[v] == min_coeff]
                # Nếu hòa hệ số âm, dùng Bland để bẻ khóa
                entering_var = min(best_entering, key=self._sort_key)
            else:
                # Quy tắc BLAND (Mặc định): Chọn biến có chỉ số nhỏ nhất
                entering_var = min(entering_candidates, key=self._sort_key)

            # 2. Chọn Biến Ra (Leaving) - Quy tắc tỷ số
            leaving_candidates = []
            for b_var in self.B:
                coeff = self.dictionary[b_var].get(entering_var, Fraction(0))
                # Trong phương trình: x_B = b - |coeff| * x_in. Ta cần coeff < 0
                # coef âm nghĩa là khi chuyển vế nó mang dấu dương (b_i - c_ij*x_j)
                if coeff < 0:
                    ratio = self.dictionary[b_var]['const'] / abs(coeff)
                    leaving_candidates.append((ratio, b_var))

            if not leaving_candidates:
                return "UNBOUNDED" # Không bị chặn

            # Tìm ratio nhỏ nhất, nếu hòa thì chọn theo Bland
            min_ratio = min(leaving_candidates, key=lambda x: x[0])[0]
            best_candidates = [var for ratio, var in leaving_candidates if ratio == min_ratio]
            leaving_var = min(best_candidates, key=self._sort_key)

            # 3. Thực hiện Pivot (Cập nhật Dictionary)
            self.pivot(entering_var, leaving_var, objective_func)

    def pivot(self, entering_var, leaving_var, objective):
        """
        Thực hiện phép thế toán học: biểu diễn entering_var theo leaving_var
        và cập nhật toàn bộ hệ phương trình, hàm mục tiêu.
        """
        self.B.remove(leaving_var)
        self.N.remove(entering_var)
        self.B.append(entering_var)
        self.N.append(leaving_var)

        # Rút biến vào từ phương trình của biến ra (Rút entering theo leaving)
        eq = self.dictionary[leaving_var]
        new_eq = {}
        coeff_enter = eq[entering_var] # Chắc chắn < 0 theo logic chọn biến ra

        new_eq['const'] = eq['const'] / (-coeff_enter)
        for var in eq:
            if var not in ['const', entering_var]:
                new_eq[var] = eq[var] / (-coeff_enter)
        new_eq[leaving_var] = Fraction(1) / coeff_enter

        # Cập nhật Từ vựng cho biến vào
        del self.dictionary[leaving_var]
        self.dictionary[entering_var] = new_eq

        # Thế biến vào (vừa rút) vào các phương trình khác
        for b_var in self.B:
            if b_var == entering_var: continue
            b_eq = self.dictionary[b_var]
            if entering_var in b_eq:
                factor = b_eq[entering_var]
                b_eq['const'] += factor * new_eq['const']
                for n_var in self.N:
                    b_eq[n_var] = b_eq.get(n_var, Fraction(0)) + factor * new_eq.get(n_var, Fraction(0))
                del b_eq[entering_var]

        # Thế biến vào vào hàm mục tiêu
        factor = objective.get(entering_var, Fraction(0))
        if factor != 0:
            objective['const'] += factor * new_eq['const']
            for n_var in self.N:
                objective[n_var] = objective.get(n_var, Fraction(0)) + factor * new_eq.get(n_var, Fraction(0))
            del objective[entering_var]

    # ==========================================
    # BƯỚC 5: TRÍCH XUẤT KẾT QUẢ
    # ==========================================
    def extract_solution(self):
        """
        Nhận diện Vô số nghiệm (has_infinite_solutions).
        Tính giá trị biến nguyên thủy.
        Đảo dấu Z_opt nếu bài toán gốc là MAX.
        """
        if self.status != "OPTIMAL": return

        # 1. Nhận diện vô số nghiệm
        for n_var in self.N:
            if self.objective_func.get(n_var, Fraction(0)) == 0:
                has_negative_coeff = False
                for b_var in self.B:
                    if self.dictionary[b_var].get(n_var, Fraction(0)) < 0:
                        has_negative_coeff = True
                        break

                if not has_negative_coeff:
                    self.has_infinite_solutions = True
                else:
                    for b_var in self.B:
                        coeff = self.dictionary[b_var].get(n_var, Fraction(0))
                        if coeff < 0:
                            ratio = self.dictionary[b_var]['const'] / abs(coeff)
                            if ratio > 0:
                                self.has_infinite_solutions = True

        # 2. Tính giá trị biến nguyên thủy
        self.final_vars = {}
        for j in range(self.original_num_vars):
            orig_var = f"x{j+1}"
            total_val = Fraction(0)

            for mapped_var, sign_multiplier in self.var_mapping[orig_var]:
                val = Fraction(0)
                if mapped_var in self.B:
                    val = self.dictionary[mapped_var]['const']
                total_val += val * sign_multiplier

            self.final_vars[orig_var] = total_val

        # 3. Đảo dấu Z_opt nếu gốc là MAX
        self.Z_opt = self.objective_func['const']
        if self.objective_type == 'MAX':
            self.Z_opt = -self.Z_opt

    # ==========================================
    # BƯỚC 6: VẼ ĐỒ THỊ MIỀN KHẢ THI (CHỈ HỖ TRỢ 2 BIẾN)
    # ==========================================
    def plot_feasible_region(self):
        """
        Vẽ miền chấp nhận được lên trục tọa độ 2D.
        Yêu cầu: Bài toán gốc phải có đúng 2 biến và các biến phải >= 0.
        Trả về đối tượng Figure của matplotlib để render lên Streamlit.
        """
        if self.original_num_vars != 2:
            return None, "Lỗi: Chỉ hỗ trợ vẽ đồ thị cho bài toán có đúng 2 biến quyết định."

        # Kiểm tra điều kiện >= 0 của 2 biến gốc
        if self.var_signs[0] != ">=0" or self.var_signs[1] != ">=0":
            return None, "Lỗi: Đồ thị hiện tại chỉ hỗ trợ các biến gốc có điều kiện >= 0."

        # 1. Chuyển đổi ma trận A và b từ Fraction sang float để dùng Numpy
        A_float = np.array([[float(val) for val in row] for row in self.A])
        b_float = np.array([float(val) for val in self.b])

        # 2. Bổ sung 2 đường thẳng của trục tọa độ (x1 >= 0, x2 >= 0)
        # Tương đương: -1*x1 + 0*x2 <= 0 và 0*x1 + -1*x2 <= 0
        A_full = np.vstack([A_float, [-1, 0], [0, -1]])
        b_full = np.append(b_float, [0, 0])

        # 3. Tìm TẤT CẢ các giao điểm (Vertices) của các cặp đường thẳng
        num_lines = len(b_full)
        points = []
        for i in range(num_lines):
            for j in range(i + 1, num_lines):
                A_sys = np.array([A_full[i], A_full[j]])
                b_sys = np.array([b_full[i], b_full[j]])
                try:
                    # Giải hệ phương trình tuyến tính
                    pt = np.linalg.solve(A_sys, b_sys)
                    points.append(pt)
                except np.linalg.LinAlgError:
                    continue # Bỏ qua nếu 2 đường thẳng song song/trùng nhau

        # 4. Lọc các điểm thỏa mãn TẤT CẢ các ràng buộc (Miền khả thi)
        valid_points = []
        for pt in points:
            # Kiểm tra A*pt <= b (Cộng thêm 1e-7 để dung sai sai số dấu phẩy động)
            if np.all(np.dot(A_full, pt) <= b_full + 1e-7):
                valid_points.append(pt)

        if not valid_points:
            return None, "Miền khả thi rỗng (Infeasible Region)."

        # Loại bỏ các điểm trùng lặp
        valid_points = np.unique(np.round(valid_points, decimals=5), axis=0)

        # 5. Sắp xếp các điểm theo góc để vẽ đa giác lồi (Convex Polygon)
        center = np.mean(valid_points, axis=0)
        angles = np.arctan2(valid_points[:, 1] - center[1], valid_points[:, 0] - center[0])
        sorted_indices = np.argsort(angles)
        polygon = valid_points[sorted_indices]

        # 6. Khởi tạo hình vẽ Matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))

        # Vẽ đa giác miền khả thi
        poly_patch = Polygon(polygon, closed=True, fill=True, color='lightblue', alpha=0.6, edgecolor='blue')
        ax.add_patch(poly_patch)

        # Vẽ các điểm đỉnh (Vertices)
        ax.plot(polygon[:, 0], polygon[:, 1], 'bo', label='Các đỉnh khả thi')

        # Điểm tối ưu (nếu đã giải xong)
        if self.status == "OPTIMAL" and hasattr(self, 'final_vars'):
            opt_x1 = float(self.final_vars['x1'])
            opt_x2 = float(self.final_vars['x2'])
            ax.plot(opt_x1, opt_x2, 'ro', markersize=10, label=f'Tối ưu ({opt_x1:.2f}, {opt_x2:.2f})')

        # Thiết lập trục
        max_x = np.max(polygon[:, 0]) * 1.5 if np.max(polygon[:, 0]) > 0 else 10
        max_y = np.max(polygon[:, 1]) * 1.5 if np.max(polygon[:, 1]) > 0 else 10
        ax.set_xlim(-0.5, max_x)
        ax.set_ylim(-0.5, max_y)
        ax.axhline(0, color='black', linewidth=1.5)
        ax.axvline(0, color='black', linewidth=1.5)

        ax.set_xlabel('$x_1$', fontsize=12)
        ax.set_ylabel('$x_2$', fontsize=12)
        ax.set_title('Đồ thị Miền khả thi 2D', fontsize=14)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

        return fig, "Success"

    # ==========================================
    # HÀM ĐIỀU PHỐI & PHỤ TRỢ
    # ==========================================
    def solve(self):
        """Hàm điều phối chính"""
        self.standardize_problem()
        needs_phase_1 = self.build_initial_dictionary()

        if needs_phase_1:
            feasible = self.phase_1()
            if not feasible:
                self.status = "INFEASIBLE"
                return

        self.phase_2()
        self.extract_solution()

    def _sort_key(self, var_name):
        """Hỗ trợ Quy tắc Bland: Ưu tiên x1 < x2 < w1 < w2"""
        # Hàm giúp sắp xếp index của x1, x2, w1, w2... cho quy tắc Bland
        match = re.match(r"([a-zA-Z]+)(\d+)", var_name)
        if match:
            # Nhóm 'x' luôn ưu tiên xếp trước 'w', sau đó so sánh số
            prefix = 0 if match.group(1) == 'x' else 1
            return (prefix, int(match.group(2)))
        return (2, 0)

    def _save_history(self, obj_func):
        """Lưu lại trạng thái để vẽ giao diện từng bước (record history)"""
        state = {
            'B': list(self.B),
            'N': list(self.N),
            'dict': copy.deepcopy(self.dictionary),
            'obj': copy.deepcopy(obj_func)
        }
        self.history.append(state)

# ==========================================
# 3. GIAO DIỆN TƯƠNG TÁC NGƯỜI DÙNG
# ==========================================
st.markdown("### 1. Cấu hình bài toán")

# 🟢 THÊM Ô CHỌN LUẬT VÀO ĐÂY (Bland / Dantzig)
col_cfg1, col_cfg2, col_cfg3, col_cfg4 = st.columns(4)
with col_cfg1:
    n_vars = st.number_input("Số biến (n)", min_value=1, max_value=10, value=2, step=1)
with col_cfg2:
    n_cons = st.number_input("Ràng buộc (m)", min_value=1, max_value=10, value=2, step=1)
with col_cfg3:
    obj_type = st.selectbox("Mục tiêu", ["MAX", "MIN"])
with col_cfg4:
    pivot_rule = st.selectbox("Luật Pivot", ["Bland", "Dantzig"])

st.markdown("### 2. Hàm mục tiêu (Z)")
c_coeffs = []
cols_obj = st.columns(n_vars)
for j in range(n_vars):
    with cols_obj[j]:
        # Đổi thành text_input, giá trị mặc định là chữ "0"
        val = st.text_input(f"x{j+1}", value="0", key=f"c_{j}") 
        c_coeffs.append(val)

st.markdown("### 3. Hệ ràng buộc")

A_matrix = []
b_vector = []
bound_signs = []

for i in range(n_cons):
    cols_cons = st.columns(n_vars + 2)
    row_A = []
    
    for j in range(n_vars):
        with cols_cons[j]:
            # 🟢 TUYỆT CHIÊU: Chỉ hiện chữ x1, x2 ở hàng đầu tiên (i == 0)
            vis = "visible" if i == 0 else "collapsed"
            val = st.text_input(f"x{j+1}", value="0", key=f"A_{i}_{j}", label_visibility=vis)
            row_A.append(val)
    A_matrix.append(row_A)
    
    with cols_cons[n_vars]:
        vis = "visible" if i == 0 else "collapsed"
        sign = st.selectbox("Dấu", ["<=", ">=", "="], key=f"sign_{i}", label_visibility=vis)
        bound_signs.append(sign)
        
    with cols_cons[n_vars + 1]:
        vis = "visible" if i == 0 else "collapsed"
        b_val = st.text_input("b", value="0", key=f"b_{i}", label_visibility=vis)
        b_vector.append(b_val)

st.markdown("### 4. Ràng buộc dấu của biến")
var_signs = []
cols_bounds = st.columns(n_vars)
for j in range(n_vars):
    with cols_bounds[j]:
        sign_input = st.selectbox(f"Dấu x{j+1}", [">= 0", "<= 0", "Tùy ý (Free)"], key=f"var_sign_{j}")
        if ">= 0" in sign_input:
            var_signs.append(">=0")
        elif "<= 0" in sign_input:
            var_signs.append("<=0")
        else:
            var_signs.append("free")

# Hàm hỗ trợ in phương trình cho đẹp (đổi từ Fraction sang số thập phân)
def format_equation(var_name, expr_dict, N_vars):
    const_val = float(expr_dict.get('const', 0))
    res = f"{var_name} = {const_val:.2f}"
    for v in N_vars:
        coef = float(expr_dict.get(v, 0))
        if coef != 0:
            sign = "+" if coef > 0 else "-"
            res += f" {sign} {abs(coef):.2f}{v}"
    return res

# ==========================================
# 5. NÚT BẤM VÀ HIỂN THỊ KẾT QUẢ
# ==========================================
st.write("")

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    btn_solve = st.button(
        "🚀 GIẢI BÀI TOÁN",
        type="primary",
        use_container_width=True
    )
# Nếu nút được bấm thì chạy thuật toán
if btn_solve:
    solver = SimplexDictionarySolver(
        num_vars=n_vars,
        num_constraints=n_cons,
        objective_type=obj_type,
        c=c_coeffs,
        A=A_matrix,
        b=b_vector,
        bound_signs=bound_signs,
        var_signs=var_signs,
        pivot_rule=pivot_rule
    )
    
    with st.spinner("Đang tính toán..."):
        solver.solve()
    
    st.markdown("---")
    st.markdown("---")
    st.markdown("### 📊 KẾT QUẢ")
    
    if solver.status == "INFEASIBLE":
        st.error("🚨 Bài toán VÔ NGHIỆM (Không tìm thấy miền chấp nhận được).")
    elif solver.status == "UNBOUNDED":
        st.warning("⚠️ Bài toán KHÔNG GIỚI NỘI (Unbounded).")
    elif solver.status == "MAX_ITERATIONS_REACHED":
        st.error("🚨 Lỗi: Vượt quá số vòng lặp tối đa (Nghi ngờ thoái hóa lặp vô hạn).")
    elif solver.status == "OPTIMAL":
        if solver.has_infinite_solutions:
            st.success("✅ Đã tìm thấy nghiệm tối ưu! (Cảnh báo: Có VÔ SỐ NGHIỆM)")
        else:
            st.success("✅ Đã tìm thấy nghiệm tối ưu duy nhất!")
            
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="Giá trị tối ưu (Z)", value=float(solver.Z_opt))
        with col_res2:
            if solver.has_infinite_solutions:
                st.write("**Một trong các nghiệm tối ưu (x):**")
            else:
                st.write("**Nghiệm nguyên thủy (x):**")
                
            for var_name, val in solver.final_vars.items():
                st.write(f"- {var_name} = {float(val)}")
        
        # Thử vẽ đồ thị
        fig, plot_msg = solver.plot_feasible_region()
        if fig is not None:
            st.pyplot(fig)
        else:
            st.info(f"*(Không vẽ đồ thị: {plot_msg})*")
    
# 🟢 IN LỊCH SỬ CÁC BƯỚC TỪ VỰNG 🟢
    st.markdown("### 📝 CHI TIẾT TỪ VỰNG (BƯỚC LẶP)")
    
    with st.expander("Bấm vào đây để xem chi tiết từng bảng Từ vựng"):
        if not solver.history:
            st.info("Chưa có bước lặp nào được ghi nhận.")
        else:
            for idx, step in enumerate(solver.history):
                st.markdown(f"**🔹 BƯỚC {idx}** *(Cơ sở B = {step['B']} | Phi cơ sở N = {step['N']})*")
                
                # 🟢 DÙNG LOGIC SO SÁNH TẬP HỢP ĐỂ TÌM BIẾN VÀO/RA (Không cần sửa thuật toán gốc)
                if idx < len(solver.history) - 1:
                    next_step = solver.history[idx + 1]
                    # Lấy B của bước sau trừ B của bước hiện tại -> Lòi ra Biến vào
                    enter_var = list(set(next_step['B']) - set(step['B']))
                    # Lấy B của bước hiện tại trừ B của bước sau -> Lòi ra Biến ra
                    leave_var = list(set(step['B']) - set(next_step['B']))
                    
                    if enter_var and leave_var:
                        st.markdown(f"<p style='margin-top: -10px; font-size: 1rem;'>"
                                    f"<span style='color: #2C5EAD; font-weight: bold;'>🎯 Chuẩn bị xoay - Biến vào: {enter_var[0]}</span> &nbsp; | &nbsp; "
                                    f"<span style='color: #1591DC; font-weight: bold;'>Biến ra: {leave_var[0]}</span></p>", 
                                    unsafe_allow_html=True)
                else:
                    # Nếu là bước cuối cùng thì không còn biến vào/ra nữa
                    st.markdown(f"<p style='margin-top: -10px; color: #2563eb; font-weight: bold;'>✅ Bảng tối ưu (Kết thúc giải thuật)</p>", unsafe_allow_html=True)
                
                # Xác định tên hàm mục tiêu là W (Pha 1) hay Z (Pha 2)
                func_name = "W" if 'x0' in step['N'] or 'x0' in step['B'] else "Z"
                
                # In hàm Z/W
                z_eq = format_equation(func_name, step['obj'], step['N'])
                st.markdown(f"<div class='history-eq'><b>{z_eq}</b></div>", unsafe_allow_html=True)
                
                # In các phương trình w_i, x_i
                for b_var in step['B']:
                    if b_var in step['dict']:
                        eq_str = format_equation(b_var, step['dict'][b_var], step['N'])
                        st.markdown(f"<div class='history-eq'>{eq_str}</div>", unsafe_allow_html=True)
                
                st.write("") # Tạo khoảng trống
