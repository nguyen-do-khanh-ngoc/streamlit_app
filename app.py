import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from fractions import Fraction
import re
import copy
import os

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">', unsafe_allow_html=True)

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
    
        /* Lớp 2: Bóng mờ 30 độ rớt ra ngoài màn hình */
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

button[data-testid="baseButton-primary"] p,
button[data-testid="baseButton-primary"] div,
button[data-testid="baseButton-primary"] span,
button[data-testid="baseButton-primary"] * {
    color: #ffffff !important;
    font-weight: 900 !important; 
    font-size: 1.6rem !important; 
    letter-spacing: 2px !important; 
    text-transform: uppercase !important; 
}

button[data-testid="baseButton-primary"]:hover {
    background-color: #1d4ed8 !important; 
    transform: translateY(-4px) !important; 
    box-shadow: 0 12px 25px rgba(59, 130, 246, 0.6) !important; 
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

button[aria-label="Step Up"], 
button[aria-label="Step Down"] {
    background-color: transparent !important; 
}
button[aria-label="Step Up"] svg, 
button[aria-label="Step Down"] svg {
    fill: #1e3a8a !important; 
    color: #1e3a8a !important;
    transition: all 0.3s ease;
}

button[aria-label="Step Up"]:hover, 
button[aria-label="Step Down"]:hover,
button[aria-label="Step Up"]:active, 
button[aria-label="Step Down"]:active,
button[aria-label="Step Up"]:focus, 
button[aria-label="Step Down"]:focus {
    background-color: #3b82f6 !important; 
    border-color: #3b82f6 !important;
}

button[aria-label="Step Up"]:hover svg, 
button[aria-label="Step Down"]:hover svg,
button[aria-label="Step Up"]:active svg, 
button[aria-label="Step Down"]:active svg,
button[aria-label="Step Up"]:focus svg, 
button[aria-label="Step Down"]:focus svg {
    fill: #ffffff !important; 
    color: #ffffff !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
ul[data-baseweb="menu"] li {
    font-weight: bold !important; 
    color: #1e3a8a !important; 
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

tieu_de_html = """
<div style="text-align: center; margin-top: -20px; margin-bottom: 30px;">
    <span style="display: inline-block; background: white; padding: 10px 30px; font-size: 24px; font-weight: bold; color: #1e3a8a; border-radius: 15px; box-shadow: 0 8px 25px rgba(30, 58, 138, 0.15);">
        <i class="fa-solid fa-calculator" style="margin-right: 8px;"></i> QUY HOẠCH TUYẾN TÍNH (SIMPLEX)
    </span>
</div>
"""
st.markdown(tieu_de_html, unsafe_allow_html=True)

# ==========================================
# 2. CLASS LÕI THUẬT TOÁN
# ==========================================
class SimplexDictionarySolver:
    def __init__(self, num_vars, num_constraints, objective_type, c, A, b, bound_signs, var_signs, pivot_rule="BLAND"):
        self.original_num_vars = num_vars
        self.original_num_constraints = num_constraints
        self.objective_type = objective_type.upper() 

        self.pivot_rule = pivot_rule.upper() 
        self.max_iterations = 1000 
        self.iteration_count = 0 

        self.c = [Fraction(str(val).strip() if str(val).strip() != "" else "0") for val in c]
        self.b = [Fraction(str(val).strip() if str(val).strip() != "" else "0") for val in b]
        self.A = [[Fraction(str(val).strip() if str(val).strip() != "" else "0") for val in row] for row in A]

        self.bound_signs = [sign.strip() for sign in bound_signs]
        self.var_signs = [sign.replace(" ", "") for sign in var_signs]

        self.B = [] 
        self.N = [] 
        self.dictionary = {} 
        self.objective_func = {} 
        self.Z = {'const': Fraction(0)} 
        self.W = {'const': Fraction(0)} 

        self.status = "INITIALIZED" 
        self.has_infinite_solutions = False
        self.history = [] 

        self.original_var_mapping = {} 
        self.var_mapping = {} 
        self.original_Z_expr = {} 

    def standardize_problem(self):
        new_c = []
        new_A = [[] for _ in range(self.original_num_constraints)]
        var_idx = 1

        for j in range(self.original_num_vars):
            orig_var = f"x{j+1}"
            sign = self.var_signs[j]

            if sign == ">=0":
                new_var = f"x{var_idx}"
                self.original_var_mapping[orig_var] = [new_var]
                self.var_mapping[orig_var] = [(new_var, 1)] 
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

        is_max = (self.objective_type == 'MAX')
        multiplier = Fraction(-1) if is_max else Fraction(1)
        self.original_Z_expr = {'const': Fraction(0)}

        for j, var in enumerate(self.N):
            coeff = new_c[j] * multiplier
            self.original_Z_expr[var] = coeff
            self.Z[var] = coeff 

        final_A, final_b = [], []
        for i in range(self.original_num_constraints):
            if self.bound_signs[i] == '<=':
                final_A.append(new_A[i])
                final_b.append(self.b[i])
            elif self.bound_signs[i] == '>=':
                final_A.append([-val for val in new_A[i]])
                final_b.append(-self.b[i])
            elif self.bound_signs[i] == '=':
                final_A.append(new_A[i])
                final_b.append(self.b[i])
                final_A.append([-val for val in new_A[i]])
                final_b.append(-self.b[i])

        self.A = final_A
        self.b = final_b

    def build_initial_dictionary(self):
        for i in range(len(self.b)):
            w_var = f"w{i+1}"
            self.B.append(w_var)
            self.dictionary[w_var] = {'const': self.b[i]}
            for j, x_var in enumerate(self.N):
                self.dictionary[w_var][x_var] = -self.A[i][j]

        return any(val < 0 for val in self.b)

    def phase_1(self):
        self.N.append('x0')
        for w_var in self.B:
            self.dictionary[w_var]['x0'] = Fraction(1)

        self.objective_func = {'const': Fraction(0), 'x0': Fraction(1)}
        self.W = self.objective_func 
        for x_var in self.N:
            if x_var != 'x0': self.objective_func[x_var] = Fraction(0)

        self._save_history(self.objective_func)

        leaving_var = min(self.B, key=lambda v: (self.dictionary[v]['const'], self._sort_key(v)))
        self.pivot('x0', leaving_var, self.objective_func)

        status = self.simplex_loop(self.objective_func)
        if status == "UNBOUNDED":
            return False 

        W_opt = self.objective_func.get('const', Fraction(0))
        if W_opt > 0:
            return False 

        if W_opt == 0:
            if 'x0' in self.B:
                eq = self.dictionary['x0']
                valid_entering = [v for v in self.N if v != 'x0' and eq.get(v, Fraction(0)) != 0]
                if not valid_entering:
                    self.B.remove('x0')
                    del self.dictionary['x0']
                else:
                    entering_var = min(valid_entering, key=self._sort_key)
                    self.pivot(entering_var, 'x0', self.objective_func)

            if 'x0' in self.N: self.N.remove('x0')
            for b_var in self.B:
                if 'x0' in self.dictionary[b_var]:
                    del self.dictionary[b_var]['x0']
            return True

    def phase_2(self):
        self.objective_func = {'const': self.original_Z_expr['const']}
        for v in self.N: self.objective_func[v] = Fraction(0)

        for var, coeff in self.original_Z_expr.items():
            if var == 'const' or coeff == 0: continue

            if var in self.N:
                self.objective_func[var] = self.objective_func.get(var, Fraction(0)) + coeff
            elif var in self.B:
                eq = self.dictionary[var]
                self.objective_func['const'] += coeff * eq['const']
                for n_var in self.N:
                    self.objective_func[n_var] = self.objective_func.get(n_var, Fraction(0)) + coeff * eq.get(n_var, Fraction(0))

        self.Z = self.objective_func 
        self.status = self.simplex_loop(self.objective_func)

    def simplex_loop(self, objective_func):
        while True:
            self.iteration_count += 1
            if self.iteration_count > self.max_iterations:
                if self.pivot_rule == "DANTZIG":
                    self.pivot_rule = "BLAND"
                    self.iteration_count = 0
                else:
                    return "MAX_ITERATIONS_REACHED"

            self._save_history(objective_func)

            entering_candidates = [v for v in self.N if objective_func.get(v, Fraction(0)) < 0]

            if not entering_candidates:
                return "OPTIMAL" 

            if getattr(self, 'pivot_rule', 'BLAND') == "DANTZIG":
                min_coeff = min(objective_func[v] for v in entering_candidates)
                best_entering = [v for v in entering_candidates if objective_func[v] == min_coeff]
                entering_var = min(best_entering, key=self._sort_key)
            else:
                entering_var = min(entering_candidates, key=self._sort_key)

            leaving_candidates = []
            for b_var in self.B:
                coeff = self.dictionary[b_var].get(entering_var, Fraction(0))
                if coeff < 0:
                    ratio = self.dictionary[b_var]['const'] / abs(coeff)
                    leaving_candidates.append((ratio, b_var))

            if not leaving_candidates:
                return "UNBOUNDED" 

            min_ratio = min(leaving_candidates, key=lambda x: x[0])[0]
            best_candidates = [var for ratio, var in leaving_candidates if ratio == min_ratio]
            leaving_var = min(best_candidates, key=self._sort_key)

            self.pivot(entering_var, leaving_var, objective_func)

    def pivot(self, entering_var, leaving_var, objective):
        self.B.remove(leaving_var)
        self.N.remove(entering_var)
        self.B.append(entering_var)
        self.N.append(leaving_var)

        eq = self.dictionary[leaving_var]
        new_eq = {}
        coeff_enter = eq[entering_var] 

        new_eq['const'] = eq['const'] / (-coeff_enter)
        for var in eq:
            if var not in ['const', entering_var]:
                new_eq[var] = eq[var] / (-coeff_enter)
        new_eq[leaving_var] = Fraction(1) / coeff_enter

        del self.dictionary[leaving_var]
        self.dictionary[entering_var] = new_eq

        for b_var in self.B:
            if b_var == entering_var: continue
            b_eq = self.dictionary[b_var]
            if entering_var in b_eq:
                factor = b_eq[entering_var]
                b_eq['const'] += factor * new_eq['const']
                for n_var in self.N:
                    b_eq[n_var] = b_eq.get(n_var, Fraction(0)) + factor * new_eq.get(n_var, Fraction(0))
                del b_eq[entering_var]

        factor = objective.get(entering_var, Fraction(0))
        if factor != 0:
            objective['const'] += factor * new_eq['const']
            for n_var in self.N:
                objective[n_var] = objective.get(n_var, Fraction(0)) + factor * new_eq.get(n_var, Fraction(0))
            del objective[entering_var]

    def extract_solution(self):
        if self.status != "OPTIMAL": return

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

        self.Z_opt = self.objective_func['const']
        if self.objective_type == 'MAX':
            self.Z_opt = -self.Z_opt

    # ==========================================
    # BƯỚC 6: VẼ ĐỒ THỊ MIỀN KHẢ THI (ĐÃ ĐƯỢC FIX LỖI HOÀN TOÀN)
    # ==========================================
    def plot_feasible_region(self):
        if self.original_num_vars != 2:
            return None, "Lỗi: Chỉ hỗ trợ vẽ đồ thị cho bài toán có đúng 2 biến quyết định."

        A_float = np.array([[float(val) for val in row] for row in self.A])
        b_float = np.array([float(val) for val in self.b])

        A_bounds = []
        b_bounds = []

        if self.var_signs[0] == ">=0":
            A_bounds.append([-1, 0])
            b_bounds.append(0)
        elif self.var_signs[0] == "<=0":
            A_bounds.append([1, 0])
            b_bounds.append(0)

        if self.var_signs[1] == ">=0":
            A_bounds.append([0, -1])
            b_bounds.append(0)
        elif self.var_signs[1] == "<=0":
            A_bounds.append([0, 1])
            b_bounds.append(0)

        LIMIT = 1000
        A_bounds.extend([[1, 0], [-1, 0], [0, 1], [0, -1]])
        b_bounds.extend([LIMIT, LIMIT, LIMIT, LIMIT])

        if len(A_float) > 0:
            A_full = np.vstack([A_float, A_bounds])
        else:
            A_full = np.array(A_bounds)
        b_full = np.append(b_float, b_bounds)

        num_lines = len(b_full)
        points = []
        for i in range(num_lines):
            for j in range(i + 1, num_lines):
                A_sys = np.array([A_full[i], A_full[j]])
                b_sys = np.array([b_full[i], b_full[j]])
                try:
                    pt = np.linalg.solve(A_sys, b_sys)
                    points.append(pt)
                except np.linalg.LinAlgError:
                    continue 

        valid_points = []
        for pt in points:
            if np.all(np.dot(A_full, pt) <= b_full + 1e-7):
                valid_points.append(pt)

        if not valid_points:
            return None, "Miền khả thi rỗng (Infeasible Region)."

        valid_points = np.unique(np.round(valid_points, decimals=5), axis=0)

        if len(valid_points) >= 3:
            center = np.mean(valid_points, axis=0)
            angles = np.arctan2(valid_points[:, 1] - center[1], valid_points[:, 0] - center[0])
            sorted_indices = np.argsort(angles)
            polygon = valid_points[sorted_indices]
        else:
            polygon = valid_points

        fig, ax = plt.subplots(figsize=(8, 6))

        if len(polygon) >= 3:
            poly_patch = Polygon(polygon, closed=True, fill=True, color='lightblue', alpha=0.6, edgecolor='blue')
            ax.add_patch(poly_patch)
            ax.plot(polygon[:, 0], polygon[:, 1], 'bo', label='Các đỉnh khả thi')
        elif len(polygon) == 2:
            ax.plot(polygon[:, 0], polygon[:, 1], 'b-', linewidth=2, label='Miền khả thi (Đoạn thẳng)')
            ax.plot(polygon[:, 0], polygon[:, 1], 'bo')
        elif len(polygon) == 1:
            ax.plot(polygon[:, 0], polygon[:, 1], 'bo', label='Miền khả thi (1 điểm duy nhất)')

        if self.status == "OPTIMAL" and hasattr(self, 'final_vars'):
            opt_x1 = float(self.final_vars['x1'])
            opt_x2 = float(self.final_vars['x2'])
            ax.plot(opt_x1, opt_x2, 'ro', markersize=10, label=f'Tối ưu ({opt_x1:.2f}, {opt_x2:.2f})')

        if len(polygon) > 0:
            min_x, max_x = np.min(polygon[:, 0]), np.max(polygon[:, 0])
            min_y, max_y = np.min(polygon[:, 1]), np.max(polygon[:, 1])
            
            pad_x = (max_x - min_x) * 0.2 if max_x > min_x else 2
            pad_y = (max_y - min_y) * 0.2 if max_y > min_y else 2

            ax.set_xlim(min_x - pad_x, max_x + pad_x)
            ax.set_ylim(min_y - pad_y, max_y + pad_y)
        else:
            ax.set_xlim(-5, 5)
            ax.set_ylim(-5, 5)

        ax.axhline(0, color='black', linewidth=1.5)
        ax.axvline(0, color='black', linewidth=1.5)

        ax.set_xlabel('x1', fontsize=12)
        ax.set_ylabel('x2', fontsize=12)
        ax.set_title('Đồ thị Miền khả thi 2D', fontsize=14)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

        return fig, "Success"

    def solve(self):
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
        match = re.match(r"([a-zA-Z]+)(\d+)", var_name)
        if match:
            prefix = 0 if match.group(1) == 'x' else 1
            return (prefix, int(match.group(2)))
        return (2, 0)

    def _save_history(self, obj_func):
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
        val = st.text_input(f"x{j+1}", value="", placeholder="0", key=f"c_{j}") 
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
            vis = "visible" if i == 0 else "collapsed"
            val = st.text_input(f"x{j+1}", value="", placeholder="0", key=f"A_{i}_{j}", label_visibility=vis)
            row_A.append(val)
    A_matrix.append(row_A)
    
    with cols_cons[n_vars]:
        vis = "visible" if i == 0 else "collapsed"
        sign = st.selectbox("Dấu", ["<=", ">=", "="], key=f"sign_{i}", label_visibility=vis)
        bound_signs.append(sign)
        
    with cols_cons[n_vars + 1]:
        vis = "visible" if i == 0 else "collapsed"
        b_val = st.text_input("b", value="", placeholder="0", key=f"b_{i}", label_visibility=vis)
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
        "GIẢI BÀI TOÁN",
        type="primary",
        use_container_width=True,
        icon=":material/rocket_launch:"
    )

if btn_solve:
    try:
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
        st.markdown('### <i class="fa-solid fa-clipboard-check" style="color: #1e3a8a; margin-right: 8px;"></i> KẾT QUẢ', unsafe_allow_html=True)
        
        if solver.status == "INFEASIBLE":
            st.markdown('<h5 style="color:#ff4b4b;"><i class="fa-solid fa-circle-xmark"></i> Bài toán VÔ NGHIỆM (Không tìm thấy miền chấp nhận được).</h5>', unsafe_allow_html=True)
        elif solver.status == "UNBOUNDED":
            st.markdown('<h5 style="color:#ffaa00;"><i class="fa-solid fa-triangle-exclamation"></i> Bài toán KHÔNG GIỚI NỘI (Unbounded).</h5>', unsafe_allow_html=True)
        elif solver.status == "MAX_ITERATIONS_REACHED":
            st.markdown('<h5 style="color:#ff4b4b;"><i class="fa-solid fa-ban"></i> Lỗi: Vượt quá số vòng lặp tối đa.</h5>', unsafe_allow_html=True)
        elif solver.status == "OPTIMAL":
            if solver.has_infinite_solutions:
                st.markdown('<h5 style="color:#21c354;"><i class="fa-solid fa-layer-group"></i> Đã tìm thấy nghiệm tối ưu! (Có VÔ SỐ NGHIỆM)</h5>', unsafe_allow_html=True)
            else:
                st.markdown('<h5 style="color:#21c354;"><i class="fa-solid fa-circle-check"></i> Đã tìm thấy nghiệm tối ưu duy nhất!</h5>', unsafe_allow_html=True)
                
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric(label="Giá trị tối ưu (Z)", value=float(solver.Z_opt))
            with col_res2:
                if solver.has_infinite_solutions:
                    st.write("**Một trong các nghiệm tối ưu (x):**")
                else:
                    st.write("**Nghiệm tối ưu (x):**")
                    
                for var_name, val in solver.final_vars.items():
                    st.write(f"- {var_name} = {float(val)}")
            
            fig, plot_msg = solver.plot_feasible_region()
            if fig is not None:
                st.pyplot(fig)
            else:
                st.info(f"*(Không vẽ đồ thị: {plot_msg})*")
        
        st.markdown('### <i class="fa-solid fa-table-list" style="color: #1e3a8a; margin-right: 8px;"></i> CHI TIẾT TỪ VỰNG (BƯỚC LẶP)', unsafe_allow_html=True)
        
        with st.expander("Bấm vào đây để xem chi tiết từng bảng Từ vựng", expanded=True):
            if not solver.history:
                st.info("Chưa có bước lặp nào được ghi nhận.")
            else:
                current_phase = 0 
                
                for idx, step in enumerate(solver.history):
                    func_name = "E" if 'x0' in step['N'] or 'x0' in step['B'] else "Z"
                    phase_of_this_step = 1 if func_name == "W" else 2
                    
                    if phase_of_this_step == 1 and current_phase == 0:
                        st.markdown("<h4 style='color: #d97706; margin-top: 10px; margin-bottom: 15px;'><i class='fa-solid fa-flag' style='margin-right: 8px;'></i> BẮT ĐẦU PHA 1 (Tìm phương án cực biên khả thi)</h4>", unsafe_allow_html=True)
                        current_phase = 1
                    elif phase_of_this_step == 2 and current_phase == 1:
                        st.markdown("<hr style='margin: 30px 0; border: 2px dashed #059669;'><h4 style='color: #059669; margin-bottom: 15px;'><i class='fa-solid fa-flag-checkered' style='margin-right: 8px;'></i> KẾT THÚC PHA 1 ➔ BẮT ĐẦU PHA 2 (Tìm nghiệm tối ưu)</h4>", unsafe_allow_html=True)
                        current_phase = 2

                    st.markdown(f"<p style='font-size: 1.1rem; font-weight: bold; color: #1e3a8a;'>"
                                f"<i class='fa-solid fa-caret-right' style='color: #3b82f6; margin-right: 6px;'></i> BƯỚC {idx} "
                                f"<span style='font-weight: normal; font-size: 0.95rem; color: #475569;'>(Cơ sở B = {step['B']} | Phi cơ sở N = {step['N']})</span></p>", 
                                unsafe_allow_html=True)
                    
                    if idx < len(solver.history) - 1:
                        next_step = solver.history[idx + 1]
                        enter_var = list(set(next_step['B']) - set(step['B']))
                        leave_var = list(set(step['B']) - set(next_step['B']))
                        
                        if enter_var and leave_var:
                            st.markdown(f"<p style='margin-top: -10px; font-size: 1rem;'>"
                                        f"<span style='color: #2C5EAD; font-weight: bold;'> Chuẩn bị xoay - Biến vào: {enter_var[0]}</span> &nbsp; | &nbsp; "
                                        f"<span style='color: #1591DC; font-weight: bold;'>Biến ra: {leave_var[0]}</span></p>", 
                                        unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='margin-top: -10px; color: #2563eb; font-weight: bold;'> Bảng tối ưu (Kết thúc giải thuật)</p>", unsafe_allow_html=True)
                    
                    z_eq = format_equation(func_name, step['obj'], step['N'])
                    st.markdown(f"<div class='history-eq'><b>{z_eq}</b></div>", unsafe_allow_html=True)
                    
                    for b_var in step['B']:
                        if b_var in step['dict']:
                            eq_str = format_equation(b_var, step['dict'][b_var], step['N'])
                            st.markdown(f"<div class='history-eq'>{eq_str}</div>", unsafe_allow_html=True)
                    
                    st.write("") 
                    
    except ValueError:
        error_html = """
        <div style="background-color: #fef2f2; border-left: 6px solid #ef4444; padding: 15px 20px; border-radius: 8px; margin-top: 20px; box-shadow: 0 4px 6px rgba(239, 68, 68, 0.1);">
            <h4 style="color: #b91c1c; margin-top: 0; margin-bottom: 8px; font-weight: bold;">
                <i class="fa-solid fa-triangle-exclamation" style="margin-right: 8px;"></i> LỖI DỮ LIỆU ĐẦU VÀO!
            </h4>
            <p style="color: #991b1b; margin: 0; font-size: 1.05rem;">
                Vui lòng chỉ nhập <b>số</b> (ví dụ: <code>-5</code>, <code>3.14</code>) hoặc <b>phân số</b> (ví dụ: <code>1/2</code>, <code>-3/4</code>). Không nhập chữ cái hay ký tự lạ.
            </p>
        </div>
        """
        st.markdown(error_html, unsafe_allow_html=True)
