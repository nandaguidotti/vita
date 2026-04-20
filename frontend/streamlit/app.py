import streamlit as st
import requests
import io
from PIL import Image

# -------------------------
# CONFIG
# -------------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="VITA Platform", layout="wide")


# -------------------------
# SESSION STATE
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.token = None


# -------------------------
# LOGIN (compacto)
# -------------------------
def login():
    st.markdown("##")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image("vita.png", width=150)
        st.markdown("### VITA Platform")
        st.markdown("##### Visionary Industrial Technology Architecture")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")

        if not submit:
            return

        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                json={"username": email, "password": password},
                timeout=10,
            )

            if response.status_code == 422:
                response = requests.post(
                    f"{API_URL}/auth/login",
                    data={
                        "username": email,
                        "password": password,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token") or data.get("token")

                st.session_state.authenticated = True
                st.session_state.token = token

                st.success("Login successful!")
                st.rerun()

            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Connection error: {e}")


# -------------------------
# SIDEBAR
# -------------------------
def sidebar():
    st.sidebar.image("vita.png", width=120)
    st.sidebar.markdown("### VITA Platform")

    menu = st.sidebar.radio(
        "Navigation",
        ["Overview", "AI Vision Module"]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    return menu


# -------------------------
# API STATUS
# -------------------------
def api_status():
    st.title("Overview")

    st.subheader("API Status")

    if st.button("Check connection"):
        try:
            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            r = requests.get(f"{API_URL}/", headers=headers)

            st.success("API connected!")
            st.json(r.json())

        except Exception as e:
            st.error(f"Error: {e}")


# -------------------------
# VISION MODULE
# -------------------------
def vision_module():
    st.title("AI Vision Module")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width="stretch")

        col1, col2 = st.columns(2)

        with col1:
            model = st.selectbox(
                "Model",
                ["yolov3-tiny", "yolov3"]
            )

        with col2:
            process = st.button("Run Detection")

        if process:
            try:
                file_bytes = uploaded_file.getvalue()

                files = {
                    "file": (
                        uploaded_file.name,
                        file_bytes,
                        uploaded_file.type or "image/jpeg"
                    )
                }

                response = requests.post(
                    f"{API_URL}/api/vision/detect",
                    params={"model": model},
                    files=files,
                    headers={
                        "Authorization": f"Bearer {st.session_state.token}"
                    }
                )

                if response.status_code == 200:
                    result_image = Image.open(io.BytesIO(response.content))
                    st.image(result_image, caption="Detection Result", width="stretch")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Processing error: {e}")

def architecture_6c():
    st.title("6C Architecture")

    st.markdown(
        "The VITA Platform is based on the 6C Architecture for Artificial Intelligence in industrial systems."
    )

    st.markdown(
        "Access the technical documentation of the VITA Platform below:" "[  📄 Open Documentation](http://127.0.0.1:8000/html/docs/)"
    )

    st.markdown("### Layers")

    layers = [
        ("Connection", "Data acquisition from sensors, systems, and external sources."),
        ("Conversion", "Data preprocessing and transformation into structured formats."),
        ("Cyber-Physical", "Integration of digital and physical systems (digital twin)."),
        ("Cognition", "AI models for prediction, detection, and analytics."),
        ("Configuration", "Decision-making and system adaptation."),
        ("Consciousness", "Continuous learning, monitoring, and system evolution."),
    ]

    cols = st.columns(3)


    st.image("plattform.png")
    for i, (title, desc) in enumerate(layers):
        with cols[i % 3]:
            st.markdown(f"#### {title}")
            st.markdown(f"{desc}")


# -------------------------
# DASHBOARD
# -------------------------
def dashboard():
    menu = sidebar()

    if menu == "Overview":
        api_status()
        architecture_6c()

    elif menu == "AI Vision Module":
        vision_module()

    elif menu == "6C Architecture":
        architecture_6c()


# -------------------------
# CONTROL
# -------------------------
if not st.session_state.authenticated:
    login()
else:
    dashboard()