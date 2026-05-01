import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.title("Stress-Strain")

labels_6 = ["11","22","33","23","31","12"]
labels_3 = ["x","y","xy"]

def show_matrix(M, name, labels):
    df = pd.DataFrame(M, columns=labels[:M.shape[1]], index=labels[:M.shape[0]])
    st.subheader(name)
    st.dataframe(df.style.format("{:.6f}"), use_container_width=True)

def safe_inverse(M):
    try:
        return np.linalg.inv(M)
    except:
        st.warning("Matrix singular → pakai pseudo-inverse")
        return np.linalg.pinv(M)

analysis = st.sidebar.selectbox(
    "Analysis Type",
    ["3D Stress-Strain", "2D Angle Lamina"]
)

if analysis == "3D Stress-Strain":

    sym = st.sidebar.selectbox(
        "Material Symmetry",
        ["Isotropic","Transversely Isotropic","Orthotropic","Monoclinic","Anisotropic"]
    )

    if sym == "Isotropic":
        st.subheader("Isotropic")
        st.info("Isotropic: 2 independent elastic constants")
        E = st.sidebar.number_input("E [GPa]", 0.01)
        nu = st.sidebar.number_input("ν", 0.01)

        S = np.array([
            [1/E,      -nu/E,  -nu/E,         0,                    0,                    0],
            [-nu/E,      1/E,  -nu/E,         0,                    0,                    0],
            [-nu/E,    -nu/E,    1/E,         0,                    0,                    0],
            [0,         0,         0,         2*(1 + nu)/E,         0,                    0],
            [0,         0,         0,         0,                    2*(1 + nu)/E,         0],
            [0,         0,         0,         0,                    0,          2*(1 + nu)/E]
        ])
        C = safe_inverse(S)

    elif sym == "Transversely Isotropic":
        st.subheader("Transversely Isotropic")
        st.info("Transversely Isotropic: 5 independent elastic constants")
        E1 = st.sidebar.number_input("E₁ [GPa]",0.01)
        E2 = st.sidebar.number_input("E₂ [GPa]",0.01)
        E3 = st.sidebar.number_input("E₃ [GPa]",0.01)
        nu12 = st.sidebar.number_input("ν₁₂",0.01)
        nu23 = st.sidebar.number_input("ν₂₃",0.01)
        G12 = st.sidebar.number_input("G₁₂ [GPa]",0.01)

        S = np.array([
            [1/E1,      -nu12/E1,        -nu12/E1,        0,                  0,       0],
            [-nu12/E1,  1/E2,            -nu23/E2,        0,                  0,       0],
            [-nu12/E1, -nu23/E2,         1/E2,            0,                  0,       0],
            [0,         0,               0,               2*(1 + nu23)/E2,    0,       0],
            [0,         0,               0,               0,                  1/G12,   0],
            [0,         0,               0,               0,                  0,       1/G12]
        ])
        C = safe_inverse(S)


    elif sym == "Orthotropic":
        st.subheader("Orthotropic")
        st.info("Orthotropic: 9 independent elastic constants")
        E1 = st.sidebar.number_input("E₁ [GPa]",0.01)
        E2 = st.sidebar.number_input("E₂ [GPa]",0.01)
        E3 = st.sidebar.number_input("E₃ [GPa]",0.01)

        nu12 = st.sidebar.number_input("ν₁₂",0.01)
        nu23 = st.sidebar.number_input("ν₂₃",0.01)
        nu31 = st.sidebar.number_input("ν₃₁",0.01)

        G12 = st.sidebar.number_input("G₁₂ [GPa]",0.01)
        G23 = st.sidebar.number_input("G₂₃ [GPa]",0.01)
        G31 = st.sidebar.number_input("G₃₁ [GPa]",0.01)


        S = np.array([
            [1/E1,      -nu12/E1,  -nu31/E1,  0,      0,      0],
            [-nu12/E1,  1/E2,      -nu23/E2,  0,      0,      0],
            [-nu31/E1, -nu23/E2,   1/E3,      0,      0,      0],
            [0,         0,         0,         1/G23,  0,      0],
            [0,         0,         0,         0,      1/G31,  0],
            [0,         0,         0,         0,      0,      1/G12]
        ]) 
        C = safe_inverse(S)

    elif sym == "Monoclinic":
        st.subheader("Monoclinic")
        st.info("Monoclinic: 13 independent elastic constants")

        C11 = st.sidebar.number_input("C11 [GPa]",0.0)
        C12 = st.sidebar.number_input("C12 [GPa]",0.0)
        C13 = st.sidebar.number_input("C13 [GPa]",0.0)
        C16 = st.sidebar.number_input("C16 [GPa]",0.0)
        C22 = st.sidebar.number_input("C22 [GPa]",0.0)
        C23 = st.sidebar.number_input("C23 [GPa]",0.0)
        C26 = st.sidebar.number_input("C26 [GPa]",0.0)
        C33 = st.sidebar.number_input("C33 [GPa]",0.0)
        C36 = st.sidebar.number_input("C36 [GPa]",0.0)
        C44 = st.sidebar.number_input("C44 [GPa]",0.0)
        C45 = st.sidebar.number_input("C45 [GPa]",0.0)
        C55 = st.sidebar.number_input("C55 [GPa]",0.0)
        C66 = st.sidebar.number_input("C66 [GPa]",0.0)

        C = np.array([
            [C11,C12,C13,0,0,C16],
            [C12,C22,C23,0,0,C26],
            [C13,C23,C33,0,0,C36],
            [0,0,0,C44,C45,0],
            [0,0,0,C45,C55,0],
            [C16,C26,C36,0,0,C66]
        ])
        S = safe_inverse(C)

    else:
        st.subheader("Anisotropic")
        st.info("Anisotropic: 21 independent elastic constants")
        C11 = st.sidebar.number_input("C11 [GPa]",0.0)
        C12 = st.sidebar.number_input("C12 [GPa]",0.0)
        C13 = st.sidebar.number_input("C13 [GPa]",0.0)
        C14 = st.sidebar.number_input("C14 [GPa]",0.0)
        C15 = st.sidebar.number_input("C15 [GPa]",0.0)
        C16 = st.sidebar.number_input("C16 [GPa]",0.0)
        C22 = st.sidebar.number_input("C22 [GPa]",0.0)
        C23 = st.sidebar.number_input("C23 [GPa]",0.0)
        C24 = st.sidebar.number_input("C24 [GPa]",0.0)
        C25 = st.sidebar.number_input("C25 [GPa]",0.0)
        C26 = st.sidebar.number_input("C26 [GPa]",0.0)
        C33 = st.sidebar.number_input("C33 [GPa]",0.0)
        C34 = st.sidebar.number_input("C34 [GPa]",0.0)
        C35 = st.sidebar.number_input("C35 [GPa]",0.0)
        C36 = st.sidebar.number_input("C36 [GPa]",0.0)
        C44 = st.sidebar.number_input("C44 [GPa]",0.0)
        C45 = st.sidebar.number_input("C45 [GPa]",0.0)
        C46 = st.sidebar.number_input("C46 [GPa]",0.0)
        C55 = st.sidebar.number_input("C55 [GPa]",0.0)
        C56 = st.sidebar.number_input("C56 [GPa]",0.0)
        C66 = st.sidebar.number_input("C66 [GPa]",0.0)

        C = np.array([
            [C11,C12,C13,C14,C15,C16],
            [C12,C22,C23,C24,C25,C26],
            [C13,C23,C33,C34,C35,C36],
            [C14,C24,C34,C44,C45,C46],
            [C15,C25,C35,C45,C55,C56],
            [C16,C26,C36,C46,C56,C66]
        ])
        S = safe_inverse(C)

    col1,col2 = st.columns(2)
    with col1:
        show_matrix(S,"[S]",labels_6)
    with col2:
        show_matrix(C,"[C]",labels_6)

    mode = st.radio("Mode",["ε → σ","σ → ε"])

    if mode=="ε → σ":
        eps = np.array([
            st.number_input("ε₁",0.0),
            st.number_input("ε₂",0.0),
            st.number_input("ε₃",0.0),
            st.number_input("γ₂₃",0.0),
            st.number_input("γ₃₁",0.0),
            st.number_input("γ₁₂",0.0)
        ])
        sig = C @ eps * 1000

        df = pd.DataFrame({
            "Komponen":["σ₁","σ₂","σ₃","τ₂₃","τ₃₁","τ₁₂"],
            "MPa":sig
        })
        st.dataframe(df)

    else:
        sig = np.array([
            st.number_input("σ₁",0.0),
            st.number_input("σ₂",0.0),
            st.number_input("σ₃",0.0),
            st.number_input("τ₂₃",0.0),
            st.number_input("τ₃₁",0.0),
            st.number_input("τ₁₂",0.0)
        ])/1000

        eps = S @ sig

        df = pd.DataFrame({
            "Komponen":["ε₁","ε₂","ε₃","γ₂₃","γ₃₁","γ₁₂"],
            "Value":eps
        })
        st.dataframe(df)


# analysis 2D Angle Lamina
else:
    st.header("2D Angle Lamina")

    E1 = st.sidebar.number_input("E₁ [GPa]",0.01)
    E2 = st.sidebar.number_input("E₂ [GPa]",0.01)
    nu12 = st.sidebar.number_input("ν₁₂",0.01)
    G12 = st.sidebar.number_input("G₁₂ [GPa]",0.01)
    theta = st.sidebar.number_input("θ [deg]",0.01)

    # 1) Local lamina compliance [S] dan reduced stiffness [Q]
    nu21 = nu12*E2/E1

    S = np.array([
        [1/E1, -nu12/E1, 0],    
        [-nu21/E2, 1/E2, 0],
        [0, 0, 1/G12]
    ])

    Q11 = E1/(1-nu12*nu21)
    Q22 = E2/(1-nu12*nu21)
    Q12 = nu12*E2/(1-nu12*nu21)
    Q66 = G12

    Q = np.array([[Q11,Q12,0],
                  [Q12,Q22,0],
                  [0,0,Q66]])

    # 2) Transformasi sudut θ untuk angle lamina
    t = np.radians(theta)
    c = np.cos(t)
    s = np.sin(t)

    Qbar = np.array([
        [Q11*c**4 + 2*(Q12+2*Q66)*s**2*c**2 + Q22*s**4,
         (Q11+Q22-4*Q66)*s**2*c**2 + Q12*(c**4+s**4),
         (Q11-Q12-2*Q66)*c**3*s - (Q22-Q12-2*Q66)*s**3*c],
        [(Q11+Q22-4*Q66)*s**2*c**2 + Q12*(c**4+s**4),
         Q11*s**4 + 2*(Q12+2*Q66)*s**2*c**2 + Q22*c**4,
         (Q11-Q12-2*Q66)*s**3*c - (Q22-Q12-2*Q66)*c**3*s],
        [(Q11-Q12-2*Q66)*c**3*s - (Q22-Q12-2*Q66)*s**3*c,
         (Q11-Q12-2*Q66)*s**3*c - (Q22-Q12-2*Q66)*c**3*s,
         (Q11+Q22-2*Q12-2*Q66)*s**2*c**2 + Q66*(s**4+c**4)]
    ])

    Sbar = safe_inverse(Qbar)

    # 3) Tampilkan matrix lokal dan matrix transformasi
    st.header("Local 2D Lamina")

    col1,col2 = st.columns(2)
    with col1:
        show_matrix(S,"Compliance Matrix [S]",labels_3)
    with col2:
        show_matrix(Q,"Stiffness Matrix [Q]",labels_3)

    st.header("Transformed Angle Lamina")

    col3,col4 = st.columns(2)
    with col3:
        show_matrix(Sbar,"Transformed Compliance Matrix [S-bar]",labels_3)
    with col4:
        show_matrix(Qbar,"Transformed Stiffness Matrix [Q-bar]",labels_3)

    # 4) Perhitungan stress-strain global
    st.header("2D Angle Lamina Stress-Strain")

    mode = st.radio("Mode",["ε → σ","σ → ε"])

    if mode=="ε → σ":
        eps = np.array([
            st.number_input("εₓ",0.0),
            st.number_input("εᵧ",0.0),
            st.number_input("γₓᵧ",0.0)
        ])

        sig = Qbar @ eps * 1000

        df = pd.DataFrame({
            "Komponen":["σₓ","σᵧ","τₓᵧ"],
            "MPa":sig
        })
        st.dataframe(df.style.format({"MPa":"{:.6f}"}), hide_index=True)

    else:
        sig = np.array([
            st.number_input("σₓ [MPa]",0.0),
            st.number_input("σᵧ [MPa]",0.0),
            st.number_input("τₓᵧ [MPa]",0.0)
        ])/1000

        eps = Sbar @ sig

        df = pd.DataFrame({
            "Komponen":["εₓ","εᵧ","γₓᵧ"],
            "Value":eps
        })
        st.dataframe(df.style.format({"Value":"{:.8e}"}), hide_index=True)
