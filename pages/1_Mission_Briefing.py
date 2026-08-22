import streamlit as st

st.title("🎯 Mission Briefing")

st.subheader("Welcome, Security Analyst")

st.write("""
You are an authorized security tester assigned to investigate
an unknown isolated network.

Your mission is to discover live hosts, identify exposed services,
analyze network traffic, and investigate a potential security finding.
""")

st.warning("Initial Intelligence: 192.168.56.0/24")