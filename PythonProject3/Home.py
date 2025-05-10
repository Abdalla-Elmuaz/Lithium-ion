import streamlit as st

def run():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://www.zimtu.com/wp-content/uploads/2023/12/DALL%C2%B7E-2023-12-29-08.29.23-A-cover-photo-for-a-blog-about-zinc-ion-batteries.-The-image-should-feature-a-modern-clean-design-with-visual-elements-representing-zinc-ion-batteri.png');
            background-size: cover;
            background-position: center;
            height: 100%;
            width: 100%;
        }

        /* Style for all headings */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }

        .stHeader {
            color: white !important;
        }

        .stMarkdown, .stText, .stWrite, .css-1cpxqw2 {
            color: white !important;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #fafafa;
        }
        section[data-testid="stSidebar"] * {
            color: black !important;
        }
        /* Custom overlay box for the title */
        .overlay-title {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px 30px;
            border-radius: 12px;
            display: inline-block;
            margin-top: 30px;
        }

        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="overlay-title"><h1>Welcome to EV Graphene Enhanced Li-ion Batteries Application</h1></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    run()
