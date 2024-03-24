import streamlit as st
from anthropic import Anthropic

# Assuming you have the OPENAI_API_KEY set in your Streamlit secrets
client = Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"],
)

# Hardcoded user credentials (use environment variables or a more secure method in production)
USER_ID = "admin"
PASSWORD = "password"


def login_page():
    st.title("Login Page")
    user_id = st.text_input("User ID", value="", max_chars=50)
    password = st.text_input("Password", value="", type="password", max_chars=50)

    if st.button("Login"):
        if user_id == USER_ID and password == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect User ID or Password")


def chat_interface():
    st.title("Thinkwell-AI")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
                model="claude-3-opus-20240229",
            ) as stream:
                response = st.write_stream(stream.text_stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


def logout_button():
    with st.sidebar:
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def main():
    # Setup page configuration
    st.set_page_config(
        page_title="Thinkwell-AI",
        page_icon=":brain:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://www.mentalhealth.gov/",
            "About": "This is a mental health support chat application.",
        },
    )

    # Custom background color and font color
    st.markdown(
        """
        <style>
        .stApp { background-color: #98FF98; } /* Mint green background */
        /* Font color for different elements */
        .st-af { color: #333333; } /* Primary text color */
        .st-ag { color: #333333; } /* Secondary text color, adjust as needed */
        /* You might need to inspect the page and target specific elements based on their class for more precision */
        h1, h2, h3, h4, h5, h6, p, .stTextInput>div>div>input { color: #333333; } /* Headers & text input */
        .stButton>button { color: #333333; } /* Button text */
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        chat_interface()
        logout_button()  # Moved the logout to the sidebar for logical placement
    else:
        login_page()


if __name__ == "__main__":
    main()
