import streamlit as st

def run():
    st.markdown("""
        <style>
        .stApp {
            background-image: url('https://www.scienceteen.com/wp-content/uploads/2018/12/Graphene-battery-feature-image.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }

        .overlay-title {
            background-color: rgba(0, 0, 0, 0.65);
            padding: 30px;
            border-radius: 12px;
            margin-top: 30px;
        }

        h1, h2, h3, h4, h5, h6, p, li {
            color: white !important;
        }

        p, li {
            font-size: 20px !important;
        }

        .markdown-text-container {
            font-size: 20px !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #fafafa;
        }
        section[data-testid="stSidebar"] * {
            color: black !important;
        }

        
        </style>
    """, unsafe_allow_html=True)

    st.title("EV Graphene Enhanced Li-ion Batteries")



    st.markdown("""
    <div class="overlay-title">
    

    Reducing global carbon emissions to meet net-zero targets critically depends on the advancement of lithium-ion battery (LIB) technology in electric vehicles (EVs). However, LIBs are limited by performance degradation over time due to factors like solid electrolyte interphase (SEI) growth, lithium plating, and cathode structural changes.

    This study explores the transformative role of **graphene** in overcoming these challenges through mathematical modeling and comparative analysis. The findings reveal that:

    - ⚡ **Graphene integration reduces SEI layer thickness by 99%** — from approximately 40 nm to just 0.35 nm.  
    - 🔋 **Electrochemical reaction rates double**, enhancing lithium-ion intercalation efficiency.  
    - ❄️ **Dendritic lithium plating is significantly suppressed**, minimizing safety risks and performance decline.

    These advancements lead to longer battery lifespan, faster charging capabilities, and higher energy efficiency — all essential for reducing EV emissions and enabling scalable renewable energy storage.

    While scalable graphene production remains a challenge, the results highlight its **immense potential in building sustainable, next-generation energy systems**.</div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    run()
