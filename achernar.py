import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def solve_polynomial(coefficients):
    """
    다항 방정식의 계수를 입력받아 모든 근을 찾습니다.
    coefficients: [a_n, a_{n-1}, ..., a_1, a_0] 형태의 리스트 또는 넘파이 배열.
                  가장 높은 차수의 계수부터 낮은 차수의 계수(상수항) 순으로 입력합니다.
    """
    if not isinstance(coefficients, (list, np.ndarray)):
        st.error("계수는 리스트 또는 넘파이 배열이어야 합니다.")
        return None
    if len(coefficients) != 12: # 11차 방정식은 12개의 계수가 필요
        st.error("11차 방정식은 12개의 계수가 필요합니다. 현재 계수 개수: " + str(len(coefficients)))
        return None

    # numpy.roots는 최고차항 계수가 0일 경우 차수를 낮춰 계산하므로,
    # 입력된 계수가 11차를 의미하는지 확인
    if coefficients[0] == 0:
        st.warning("최고차항 (x^11)의 계수가 0입니다. 이 방정식은 11차 방정식이 아닐 수 있습니다.")
        # 만약 최고차항 계수가 0이 아니어야 한다면 여기서 에러 처리하거나 사용자에게 재입력 요청
        # 여기서는 경고만 하고 계산을 진행합니다.

    try:
        roots = np.roots(coefficients)
        return roots
    except Exception as e:
        st.error(f"근을 계산하는 중 오류가 발생했습니다: {e}")
        return None

# Streamlit 앱 시작
st.set_page_config(page_title="11차 방정식 해 찾기 및 시각화", layout="wide")

st.title("🔢 11차 방정식 해 찾기 및 시각화")
st.markdown("""
이 앱은 사용자가 11차 방정식의 계수를 입력하면, 해당 방정식의 모든 근을 찾고 실근의 경우 그래프로 시각화합니다.
**11차 방정식의 일반적인 형태:**
$a_{11}x^{11} + a_{10}x^{10} + \dots + a_1x + a_0 = 0$
""")

st.header("계수 입력 (총 12개)")
st.info("가장 높은 차수($x^{11}$)의 계수부터 상수항($x^0$)까지 순서대로 입력해주세요.")

# 계수 입력 폼
cols = st.columns(4)
coefficients_input = []
for i in range(12):
    with cols[i % 4]: # 4열로 나누어 표시
        default_value = 0.0
        # 예시로 몇몇 계수에 값을 넣어볼 수 있습니다.
        if i == 0: default_value = 1.0 # x^11 계수
        # if i == 11: default_value = -1.0 # 상수항
        # if i == 5: default_value = 0.5 # x^6 계수

        key_str = f"coeff_{11-i}"
        label_str = f"$a_{{{11-i}}}$ (x^{{{11-i}}})" if i != 11 else "$a_0$ (상수항)"

        coeff = st.number_input(label_str, value=default_value, key=key_str, format="%.2f")
        coefficients_input.append(coeff)

st.markdown("---")

if st.button("방정식 해 계산하기"):
    st.header("계산 결과")
    solutions = solve_polynomial(coefficients_input)

    if solutions is not None:
        st.subheader("찾은 근:")
        real_roots = []
        complex_roots = []

        for i, sol in enumerate(solutions):
            if np.isreal(sol):
                real_roots.append(sol.real)
                st.write(f"**해 {i+1}:** `{sol.real:.6f}` (실근)")
            else:
                complex_roots.append(sol)
                st.write(f"**해 {i+1}:** `{sol:.6f}` (복소근)")

        st.subheader("그래프 시각화 (실근)")
        if real_roots:
            # 방정식 함수 정의 (그래프 그리기용)
            def poly_function(x, coeffs):
                y = 0
                for i, coeff in enumerate(coeffs):
                    power = len(coeffs) - 1 - i
                    y += coeff * (x ** power)
                return y

            # x 범위 설정: 실근을 포함하도록 설정
            # 만약 실근이 없다면 기본 범위 설정
            min_x = min(real_roots) - 2 if real_roots else -5
            max_x = max(real_roots) + 2 if real_roots else 5
            x_vals = np.linspace(min_x, max_x, 1000)
            y_vals = poly_function(x_vals, coefficients_input)

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x_vals, y_vals, label='방정식 $y = P(x)$', color='blue')
            
            # x축과 y축 원점 표시
            ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
            ax.axvline(0, color='gray', linewidth=0.8, linestyle='--')

            # 실근 표시
            if real_roots:
                ax.scatter(real_roots, [0] * len(real_roots), color='red', s=100, zorder=5, label='실근')
                for r in real_roots:
                    ax.text(r, 0.1, f'{r:.2f}', fontsize=9, ha='center', va='bottom')

            ax.set_title("11차 방정식 그래프 및 실근")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
            st.caption("참고: 복소근은 이 그래프에 직접 표시되지 않습니다.")
        else:
            st.info("이 방정식에는 시각화할 실근이 없습니다.")

        if complex_roots:
            st.subheader("복소근 상세:")
            for i, sol in enumerate(complex_roots):
                st.write(f"- `{sol.real:.6f} + {sol.imag:.6f}i`")
