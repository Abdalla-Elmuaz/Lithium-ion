import streamlit as st
import viz
import script
import Home
import About
import Enn



def sidebar():

    st.sidebar.title("🔀 Sections")
    page = st.sidebar.radio("Go to", ["🏠Home","ℹ️ About","📊 Visualizations", "📈 Degragation Rate Enhanced","📈 Degragation Rate"])
    return page


def main():
    page = sidebar()

    if page == "🏠Home":
          # Calls the home_page function to display the content
        Home.run()
    elif page == "ℹ️ About":

        About.run()
    elif page == "📊 Visualizations":
        st.title("📊 Visualizations")
        viz.run()
    elif page == "📈 Degragation Rate":

        script.run()  # This should contain the model inputs and prediction UI
    elif page == "📈 Degragation Rate Enhanced":

        Enn.run()
    # This should contain your boxplot and any other plots




if __name__ == "__main__":
    main()