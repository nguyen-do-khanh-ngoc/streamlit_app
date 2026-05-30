import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from fractions import Fraction
import re
import copy

# ==========================================
# 1. CÀI ĐẶT GIAO DIỆN & CSS
# ==========================================
st.set_page_config(page_title="LP Solver - Simplex", layout="centered", initial_sidebar_state="collapsed")

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

* { font-family: 'Montserrat', sans-serif !important; }

.stApp {
    background-image: url("https://images.pexels.com/photos/37060630/pexels-photo-37060630.jpeg"); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {
    background-color: rgba(255, 255, 255, 0.95); 
    border-radius: 15px; 
    padding: 3rem;
    box-shadow: -15px 26px 50px rgba(30, 58, 138, 0.3) !important; 
    border: 3px dotted #3b82f6 !important; 
    max-width: 900px !important; 
    margin: auto !important; 
    margin-top: 8vh !important; 
    margin-bottom: 8vh !important;
}

div[data-baseweb="input"] > div, 
div[data-baseweb="number-input"] > div,
div[data-baseweb="select"] > div {
    border-radius: 10px !important; 
    border: 2px solid #93c5fd !important; 
    background-color: #eff6ff !important; 
}

input {
    color: #1e3a8a !important; 
    -webkit-text-fill-color: #1e3a8a !important;
    font-weight: bold !important;
    text-align: center !important; 
}

button[data-testid="baseButton-primary"] {
    background-color: #3b82f6 !important; 
    border: none !important;
    border-radius: 25px !important; 
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4); 
    width: 100%; 
    margin-top: 10px !important; 
    transition: all 0.3s ease;
}

button[data-testid="baseButton-primary"] * {
    color: #ffffff !important; 
    font-weight: bold !important;
    font-size: 1.2rem !important;
}

button[data-testid="baseButton-primary"]:hover {
    background-color: #1d4ed8 !important; 
    transform: translateY(-2px); 
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

tieu_de_html = """
<div style="text-align: center; margin-top: -65px; margin-bottom: 30px;">
    <span style="display: inline-block; background: white; padding: 5px 25px; font-size: 24px; font-weight: bold; color: #1e3a8a; border-radius: 10px; border: 2px solid #3b82f6;">
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
        self.original_num_vars = num_vars
        self.original_num_constraints = num_constraints
        self.objective_type = objective_type.upper() 
        self.pivot_rule = pivot_rule.upper() 
        self.max_iterations = 1000 
        self.iteration_count = 0 

        self.c = [Fraction(str(val)) for val in c]
        self.b = [Fraction(str(val)) for val in b]
        self.A = [[Fraction(str(val)) for row_val in row] for row in A]

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

        leaving_var = min(self.B, key=lambda v: (self.dictionary[v]['const'], self._sort_key(v)))
        self.pivot('x0', leaving_var, self.objective_func)

        status = self.simplex_loop(self.objective_func)
        if status == "UNBOUNDED": return False 

        W_opt = self.objective_func.get('const', Fraction(0))
        if W_opt > 0: return False 

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
            if self.iteration_count > self.max_iterations: return "MAX_ITERATIONS_REACHED"

            self._save_history(objective_func)

            entering_candidates = [v for v in self.N if objective_func.get(v, Fraction(0)) < 0]
            if not entering_candidates: return "OPTIMAL" 

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

            if not leaving_candidates: return "UNBOUNDED" 

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

    def plot_feasible_region(self):
        if self.original_num_vars != 2:
            return None, "Chỉ hỗ trợ vẽ đồ thị bài toán có đúng 2 biến quyết định."
        if self.var_signs[0] != ">=0" or self.var_signs[1] != ">=0":
            return None, "Chỉ hỗ trợ vẽ đồ thị khi biến gốc x >= 0."

        A_float = np.array([[float(val) for val in row] for row in self.A])
        b_float = np.array([float(val) for val in self.b])
        A_full = np.vstack([A_float, [-1, 0], [0, -1]])
        b_full = np.append(b_float, [0, 0])

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
        if not valid_points: return None, "Miền khả thi rỗng (Infeasible Region)."

        valid_points = np.unique(np.round(valid_points, decimals=5), axis=0)
        center = np.mean(valid_points, axis=0)
        angles = np.arctan2(valid_points[:, 1] - center[1], valid_points[:, 0] - center[0])
        sorted_indices = np.argsort(angles)
        polygon = valid_points[sorted_indices]

        fig, ax = plt.subplots(figsize=(6, 4))
        poly_patch = Polygon(polygon, closed=True, fill=True, color='#93c5fd', alpha=0.6, edgecolor='#1e3a8a')
        ax.add_patch(poly_patch)
        ax.plot(polygon[:, 0], polygon[:, 1], 'bo', color='#1e3a8a', label='Đỉnh khả thi')

        if self.status == "OPTIMAL" and hasattr(self, 'final_vars'):
            opt_x1 = float(self.final_vars['x1'])
            opt_x2 = float(self.final_vars['x2'])
            ax.plot(opt_x1, opt_x2, 'ro', color='#dc2626', markersize=8, label=f'Tối ưu ({opt_x1:.2f}, {opt_x2:.2f})')

        max_x = np.max(polygon[:, 0]) * 1.5 if np.max(polygon[:, 0]) > 0 else 10
        max_y = np.max(polygon[:, 1]) * 1.5 if np.max(polygon[:, 1]) > 0 else 10
        ax.set_xlim(-0.5, max_x)
        ax.set_ylim(-0.5, max_y)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlabel('$x_1$', fontsize=10)
        ax.set_ylabel('$x_2$', fontsize=10)
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.3)
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
        val = st.number_input(f"x{j+1}", value=0.0, step=1.0, key=f"c_{j}")
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
            val = st.number_input(f"x{j+1}", value=0.0, step=1.0, key=f"A_{i}_{j}", label_visibility="collapsed")
            row_A.append(val)
    A_matrix.append(row_A)
    
    with cols_cons[n_vars]:
        sign = st.selectbox("Dấu", ["<=", ">=", "="], key=f"sign_{i}", label_visibility="collapsed")
        bound_signs.append(sign)
        
    with cols_cons[n_vars + 1]:
        b_val = st.number_input("b", value=0.0, step=1.0, key=f"b_{i}", label_visibility="collapsed")
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
if st.button("GIẢI BÀI TOÁN", type="primary"):
    
    # Truyền luật Pivot mà bạn vừa chọn vào solver
    solver = SimplexDictionarySolver(
        num_vars=n_vars,
        num_constraints=n_cons,
        objective_type=obj_type,
        c=c_coeffs,
        A=A_matrix,
        b=b_vector,
        bound_signs=bound_signs,
        var_signs=var_signs,
        pivot_rule=pivot_rule # 🟢 Truyền luật pivot vào đây
    )
    
    with st.spinner("Đang tính toán..."):
        solver.solve()
    
    st.markdown("---")
    st.markdown("### 📊 KẾT QUẢ")
    
    if solver.status == "INFEASIBLE":
        st.error("🚨 Bài toán VÔ NGHIỆM (Không tìm thấy miền khả thi).")
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
    
    # Dùng hộp thoại ẩn/hiện (expander) để trang web không bị dài quá mức
    with st.expander("Bấm vào đây để xem chi tiết từng bảng Từ vựng"):
        if not solver.history:
            st.info("Chưa có bước lặp nào được ghi nhận.")
        else:
            for idx, step in enumerate(solver.history):
                st.markdown(f"**🔹 BƯỚC {idx}** *(Cơ sở B = {step['B']} | Phi cơ sở N = {step['N']})*")
                
                # In hàm Z
                z_eq = format_equation("Z", step['obj'], step['N'])
                st.markdown(f"<div class='history-eq'><b>{z_eq}</b></div>", unsafe_allow_html=True)
                
                # In các phương trình w_i, x_i
                for b_var in step['B']:
                    if b_var in step['dict']:
                        eq_str = format_equation(b_var, step['dict'][b_var], step['N'])
                        st.markdown(f"<div class='history-eq'>{eq_str}</div>", unsafe_allow_html=True)
                
                st.write("") # Tạo khoảng trống giữa các bước
