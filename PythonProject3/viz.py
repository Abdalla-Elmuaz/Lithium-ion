import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
st.set_page_config(page_title="Li-ion Battery Analysis", layout="wide")
def run():
    st.markdown("""
        <style>
            /* Set background to light gray */
            .stApp {
            background-color: #f2f2f2;
                padding: 2rem;
            }

            /* Style main container with white and shadow */
            .main > div {
                background-color: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }

            /* Optional: round the sidebar edges and make a little cleaner */
            section[data-testid="stSidebar"] {
                background-color: #fafafa;
                border-right: 1px solid #ddd;
            }

            h1, h2, h3 {
                color: #333333;
            }
        </style>
    """, unsafe_allow_html=True)
    # Set Streamlit theme


    df_Li_ion_Battary = pd.read_csv('https://github.com/Abdalla-Elmuaz/Lithium-ion/blob/main/PythonProject3/liion_preprocessed_data.csv')
    df_Li_ion_Battary['Duration Bin'] = pd.cut(df_Li_ion_Battary['Charging Duration (min)'], bins=10)

    st.title("🔋 Lithium-Ion Battery Analysis Dashboard")

    # Sidebar
    st.sidebar.title("Section Analysis")
    section = st.sidebar.radio("Go to", [
        "Correlation Heatmaps",
        "Cycle Binning Heatmap",
        "SEI Thickness Analysis",
        "Li Plating Analysis",
        "Degradation vs Charging Mode",
        "Feature Importance"
    ])

    # 1. Correlation Heatmaps
    if section == "Correlation Heatmaps":
        st.subheader("📊 Correlation Heatmaps")

        selected_columns = [
            "Degradation Rate (%)", "Reaction_Rate_J", "SEI_Growth",
            "Plating_Risk", "Electrode_Area", "Charging Cycles", "Charging Duration (min)"
        ]
        corr_matrix = df_Li_ion_Battary[selected_columns].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap: Selected Features")
        st.pyplot(fig)

        selected_columns_enhanced = [
            "Degradation Rate (%)_Enhanced", "SEI_Growth_Enhanced", "Plating_Risk_Enhanced",
            "Electrode_Area_Enhanced", "Charging Cycles", "Charging Duration (min)"
        ]
        corr_matrix_enhanced = df_Li_ion_Battary[selected_columns_enhanced].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix_enhanced, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap: Enhanced Features")
        st.pyplot(fig)

    # 2. Cycle Binning Heatmap
    elif section == "Cycle Binning Heatmap":
        st.subheader("🔁 Average Feature Values by Charging Cycle Bin")
        df_binned = df_Li_ion_Battary.copy()
        df_binned['Cycle Bin'] = pd.qcut(df_binned['Charging Cycles'], q=10, labels=False)
        df_avg = df_binned.groupby('Cycle Bin')[['SEI_Growth', 'Plating_Risk', 'Degradation Rate (%)']].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(df_avg.T, annot=True, cmap='YlGnBu', fmt=".2f", ax=ax)
        ax.set_title('Average Feature Values by Charging Cycle Bin')
        st.pyplot(fig)

    # 3. SEI Thickness Analysis
    elif section == "SEI Thickness Analysis":
        st.subheader("📈 SEI Thickness Over Charging Duration")

        # Before graphene
        df_Li_ion_Battary['SEI Thickness'] = np.sqrt(df_Li_ion_Battary['Charging Duration (min)']) * df_Li_ion_Battary[
            'Degradation Rate (%)']
        df_Li_ion_Battary['Duration Bin'] = pd.cut(df_Li_ion_Battary['Charging Duration (min)'], bins=10)
        SEI_AVG_before = df_Li_ion_Battary.groupby('Duration Bin')[['Charging Duration (min)', 'SEI Thickness']].mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(SEI_AVG_before['Charging Duration (min)'], SEI_AVG_before['SEI Thickness'], color='blue', linewidth=2)
        ax.set_title('SEI Thickness over Charging Time [Before Graphene]')
        ax.set_xlabel('Charging Duration (min)')
        ax.set_ylabel('SEI Thickness (nm)')
        ax.grid(True)
        st.pyplot(fig)

        # After graphene
        df_Li_ion_Battary['SEI Thickness'] = np.sqrt(df_Li_ion_Battary['Charging Duration (min)']) * df_Li_ion_Battary[
            'Degradation Rate (%)_Enhanced']
        SEI_AVG_after = df_Li_ion_Battary.groupby('Duration Bin')[['Charging Duration (min)', 'SEI Thickness']].mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(SEI_AVG_after['Charging Duration (min)'], SEI_AVG_after['SEI Thickness'], color='red', linewidth=2)
        ax.set_title('SEI Thickness over Charging Time [After Graphene]')
        ax.set_xlabel('Charging Duration (min)')
        ax.set_ylabel('SEI Thickness (nm)')
        ax.grid(True)
        st.pyplot(fig)

    # 4. Li Plating Analysis
    elif section == "Li Plating Analysis":
        st.subheader("⚡ Lithium Plating over Time")

        # Before graphene
        df_Li_ion_Battary['Li Plating'] = (df_Li_ion_Battary['Current (A)'] * df_Li_ion_Battary[
            'Charging Duration (min)']) / df_Li_ion_Battary['Battery Temp (°C)']
        plating_AVG_before = df_Li_ion_Battary.groupby('Duration Bin')[['Charging Duration (min)', 'Li Plating']].mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(plating_AVG_before['Charging Duration (min)'], plating_AVG_before['Li Plating'], color='yellow',
                linewidth=2)
        ax.set_title('Li Plating over Charging Time [Before Graphene]')
        ax.set_xlabel('Charging Duration (min)')
        ax.set_ylabel('Li Plating')
        ax.grid(True)
        st.pyplot(fig)

        # After graphene (40% reduction)
        df_Li_ion_Battary['Li Plating Enhanced Index'] = df_Li_ion_Battary['Li Plating'] * 0.6
        plating_AVG_after = df_Li_ion_Battary.groupby('Duration Bin')[
            ['Charging Duration (min)', 'Li Plating Enhanced Index']].mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(plating_AVG_after['Charging Duration (min)'], plating_AVG_after['Li Plating Enhanced Index'],
                color='orange', linewidth=2)
        ax.set_title('Li Plating over Charging Time [After Graphene]')
        ax.set_xlabel('Charging Duration (min)')
        ax.set_ylabel('Li Plating')
        ax.grid(True)
        st.pyplot(fig)

    # 5. Degradation vs Charging Mode
    elif section == "Degradation vs Charging Mode":
        st.subheader("⚙️ Degradation Rate by Charging Mode")

        fig, ax = plt.subplots(figsize=(12, 5))
        sns.boxplot(data=df_Li_ion_Battary, x='Charging Mode', y='Degradation Rate (%)', palette="Set2", ax=ax)
        ax.set_title("Degradation Rate by Charging Mode (Before Enhancement)")
        ax.grid(True)
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(12, 5))
        sns.boxplot(data=df_Li_ion_Battary, x='Charging Mode', y='Degradation Rate (%)_Enhanced', palette="Set2", ax=ax)
        ax.set_title("Degradation Rate by Charging Mode (After Enhancement)")
        ax.grid(True)
        st.pyplot(fig)

    # 6. Feature Importance
    elif section == "Feature Importance":
        st.subheader("🌳 Feature Importance for Degradation Rate")

        X = df_Li_ion_Battary[
            ['SEI_Growth', 'Plating_Risk', 'Electrode_Area', 'Current (A)', 'Battery Temp (°C)', 'Charging Cycles']]
        y = df_Li_ion_Battary['Degradation Rate (%)']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='Importance', y='Feature', data=feature_importance_df, palette='viridis', ax=ax)
        ax.set_title("Feature Importance for Degradation Rate")
        st.pyplot(fig)
if __name__ == "__main__":
    run()
