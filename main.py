import streamlit as st
import pandas as pd
import io

# =====================
# 🎨 ESTILO GENERAL
# =====================
st.set_page_config(page_title="Simulcredit", page_icon="💰", layout="centered")

st.markdown("""
    <style>
    body {
      background-color: #f8fbff;
      color: #0a2540;
      font-family: 'Poppins', sans-serif;
    }
    .stApp {
      background-color: #f8fbff;
    }
    .main-container {
      background-color: white;
      border-radius: 18px;
      box-shadow: 0 10px 30px rgba(0, 64, 128, 0.1);
      width: 520px;
      margin: 40px auto;
      padding: 40px 50px;
      border: 1px solid #e1ebf5;
    }
    h1 {
      color: #12355b;
      text-align: center;
      font-weight: 700;
      font-size: 2.1rem;
      letter-spacing: 1px;
      margin-bottom: 35px;
    }
    .brand-line {
      width: 70px;
      height: 3px;
      background-color: #164b88;
      margin: -15px auto 30px;
      border-radius: 3px;
    }
    .footer {
      text-align: center;
      color: #5d7da1;
      margin-top: 30px;
      font-size: 0.9rem;
      letter-spacing: 0.4px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================
# 🧮 FUNCIONES
# =====================
def generar_tabla_amortizacion(monto, tasa_anual, plazo_meses):
    if tasa_anual <= 0:
        cuota = monto / plazo_meses
        saldo = monto
        datos = []
        for i in range(1, plazo_meses + 1):
            interes = 0.0
            capital = cuota
            saldo -= capital
            datos.append([i, round(cuota,2), round(capital,2), round(interes,2), round(abs(saldo),2)])
        return pd.DataFrame(datos, columns=["Mes", "Pago total", "Capital", "Interés", "Saldo restante"])

    tasa_mensual = tasa_anual / 12 / 100
    cuota = monto * (tasa_mensual * (1 + tasa_mensual)**plazo_meses) / ((1 + tasa_mensual)**plazo_meses - 1)
    saldo = monto
    datos = []
    for i in range(1, plazo_meses + 1):
        interes = saldo * tasa_mensual
        capital = cuota - interes
        saldo -= capital
        datos.append([i, round(cuota, 2), round(capital, 2), round(interes, 2), round(abs(saldo), 2)])
    return pd.DataFrame(datos, columns=["Mes", "Pago total", "Capital", "Interés", "Saldo restante"])


# =====================
# 💻 INTERFAZ STREAMLIT
# =====================
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("<h1>SIMULCREDIT</h1>", unsafe_allow_html=True)
    st.markdown('<div class="brand-line"></div>', unsafe_allow_html=True)

    monto = st.number_input("Monto del crédito (USD)", min_value=0.0, step=100.0, format="%.2f")
    tasa = st.number_input("Tasa de interés anual (%)", min_value=0.0, step=0.1, format="%.2f")
    plazo = st.number_input("Plazo (meses)", min_value=1, step=1)

    calcular = st.button("Calcular crédito")

    if calcular:
        if monto <= 0 or plazo <= 0:
            st.error("⚠️ Por favor ingresa valores válidos (monto > 0, plazo > 0).")
        else:
            df = generar_tabla_amortizacion(monto, tasa, plazo)
            cuota = df['Pago total'].iloc[0]
            total_pagado = df['Pago total'].sum()
            total_intereses = df['Interés'].sum()

            st.markdown("""
                <div style="background:#eef6ff; padding:15px; border-radius:10px; margin-bottom:15px;">
                    <b>Resumen del crédito:</b><br>
                    Cuota mensual: <b>${:,.2f}</b><br>
                    Total pagado: <b>${:,.2f}</b><br>
                    Intereses totales: <b>${:,.2f}</b>
                </div>
            """.format(cuota, total_pagado, total_intereses), unsafe_allow_html=True)

            st.subheader("📊 Tabla de Amortización")
            st.dataframe(df, use_container_width=True)

            # Generar Excel para descarga
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)

            st.download_button(
                label="📥 Descargar Excel",
                data=excel_buffer,
                file_name="Tabla_Amortizacion_Simulcredit.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.markdown('<div class="footer">© 2025 Simulcredit | Plataforma de simulación financiera</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
