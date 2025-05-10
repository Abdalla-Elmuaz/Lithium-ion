import streamlit as st
import numpy as np
import pandas as pd
import joblib
import urllib.request

from sklearn.preprocessing import LabelEncoder

def run():
    url = 'https://raw.githubusercontent.com/Abdalla-Elmuaz/Lithium-ion/main/PythonProject3/lasso_model_en.pkl'
    urllib.request.urlretrieve(url, 'lasso_model_en.pkl')
    modellasso_en = joblib.load('lasso_model_en.pkl')

     
    # Load the saved model
    

   # load it
 # fix file extension

    # Page styling
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://www.zimtu.com/wp-content/uploads/2023/12/DALL%C2%B7E-2023-12-29-08.29.23-A-cover-photo-for-a-blog-about-zinc-ion-batteries.-The-image-should-feature-a-modern-clean-design-with-visual-elements-representing-zinc-ion-batteri.png');
            background-size: cover;
            background-position: center;
            color: white;
        }
        .stApp {
            background-color: rgba(0, 0, 0, 0.5);
            background-image: url('https://www.zimtu.com/wp-content/uploads/2023/12/DALL%C2%B7E-2023-12-29-08.29.23-A-cover-photo-for-a-blog-about-zinc-ion-batteries.-The-image-should-feature-a-modern-clean-design-with-visual-elements-representing-zinc-ion-batteri.png');
            background-size: cover;
            background-position: center;
        }
        h1, h2, h3, h4, h5, h6, p {
            color: white !important;
        }
        .stTextInput, .stSelectbox, .stNumberInput, .stButton, .stDateInput {
            color: white;
            background-color: rgba(0, 0, 0, 0.6);
            border: 1px solid white;
        }
        section[data-testid="stSidebar"] {
            background-color: #fafafa;
        }
        section[data-testid="stSidebar"] * {
            color: black !important;
        }
        .overlay-title {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px 30px;
            border-radius: 12px;
            display: inline-block;
            margin-top: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="overlay-title"><h1>🔋 Degradation Enhanced Rate  Prediction</h1></div>',
                unsafe_allow_html=True)



    # User Inputs
    soc = st.number_input('SOC (%)', min_value=0.0, max_value=100.0, step=1.0)
    voltage = st.number_input('Voltage (V)', min_value=0.0)
    current = st.number_input('Current (A)', min_value=0.0)
    battery_temp = st.number_input('Battery Temp (°C)', min_value=-50.0, max_value=100.0)
    ambient_temp = st.number_input('Ambient Temp (°C)', min_value=-50.0, max_value=100.0)
    charging_duration = st.number_input('Charging Duration (min)', min_value=0)
    charging_mode = st.selectbox('Charging Mode', ['Fast', 'Slow', 'Normal'])
    efficiency = st.number_input('Efficiency (%)', min_value=0.0, max_value=100.0, step=0.1)
    battery_type = st.selectbox('Battery Type', ['Li-ion'])
    charging_cycles = st.number_input('Charging Cycles', min_value=0)
    ev_model = st.selectbox('EV Model',['Model A','Model B','Model C'])
    optimal_class =st.number_input('Optimal Charging Duration Class',  min_value=0.0, max_value=100.0, step=0.1)

    # Create DataFrame
    df = pd.DataFrame({
        'SOC (%)': [soc],
        'Voltage (V)': [voltage],
        'Current (A)': [current],
        'Battery Temp (°C)': [battery_temp],
        'Ambient Temp (°C)': [ambient_temp],
        'Charging Duration (min)': [charging_duration],
        'Charging Mode': [charging_mode],
        'Efficiency (%)': [efficiency],
        'Battery Type': [battery_type],
        'Charging Cycles': [charging_cycles],
        'EV Model': [ev_model],
        'Optimal Charging Duration Class': [optimal_class],
    })

    # Feature Engineering
    k, A, m, rho = 0.01, 1.0, 0.1, 2.0
    df['c_minus_deltac_proxy'] = (df['SOC (%)'] / 100) * df['Voltage (V)'] / (df['Current (A)'] + 1e-6)
    df['Reaction_Rate_J'] = k * A * df['c_minus_deltac_proxy']
    df['SEI_Growth_Proxy'] = (df['Reaction_Rate_J'] * m) / (rho * A)
    df['Plating_Risk_Proxy'] = df['Current (A)'] / (df['Battery Temp (°C)'] + 1)
    df['Electrode_Area'] = 1 / (df['SEI_Growth_Proxy'] + 1e-6)
    df['Graphene_Enhanced'] = 1
    df['SEI_Growth_Proxy_Enhanced'] = df['SEI_Growth_Proxy'] * 0.5
    df['Plating_Risk_Proxy_Enhanced'] = df['Plating_Risk_Proxy'] * 0.6
    df['Electrode_Area_Enhanced'] = 1 / (df['SEI_Growth_Proxy_Enhanced'] + 1e-6)

    # Transform Skewed Columns
    skewed_cols = [
        'SEI_Growth_Proxy_Enhanced', 'c_minus_deltac_proxy',
        'Reaction_Rate_J', 'Electrode_Area_Enhanced', 'Plating_Risk_Proxy_Enhanced'
    ]
    df[skewed_cols] = np.sqrt(df[skewed_cols].clip(lower=0))

    for col in skewed_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df[col] = df[col].clip(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)

    # EV Model cleanup
    df['EV Model'] = df['EV Model'].replace({
        'Model A': 'A',
        'Model B': 'B',
        'Model C': 'C'
    })
    df['EV Model'] = df['EV Model'].str.replace(r'(?i)model', '', regex=True).str.strip()

    # Encoding
    label_encoders = {}
    for col in ['EV Model', 'Battery Type',]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    df['Charging Mode'] = df['Charging Mode'].map(df['Charging Mode'].value_counts())

    # Show processed input


    # Prediction
    if st.button("🔮 Predict Degradation Enhanced"):
        input_data = df.drop(['Ambient Temp (°C)',
       'Charging Mode', 'Battery Type',
       'EV Model', 'Optimal Charging Duration Class', 'c_minus_deltac_proxy',
       'Reaction_Rate_J', 'SEI_Growth_Proxy', 'Plating_Risk_Proxy',
       'Electrode_Area',
    ], axis=1)
        prediction = modellasso_en.predict(input_data)
        st.success(f"Predicted Degradation Rate: {prediction[0]:.4f}")

# Run the app
if __name__ == "__main__":
    run()
