import streamlit as st

st.set_page_config(
    page_title="Operation ShadowMap",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🕵️ OPERATION SHADOWMAP")

st.subheader("From Network Discovery to Security Finding")

st.write("""
An interactive reconnaissance and ethical hacking learning environment.
Navigate through the mission using the sidebar.
""")

st.divider()

st.info("""
MISSION STATUS: ACTIVE

Known Network:
192.168.56.0/24

Initial Intelligence:
Unknown hosts. Unknown services. Unknown attack surface.
""")

st.caption("Rule: No command without a prediction. No finding without evidence.")