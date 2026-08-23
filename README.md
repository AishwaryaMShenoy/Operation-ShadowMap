# 🕵️ Operation ShadowMap

## From Network Discovery to Security Finding

Operation ShadowMap is an interactive cybersecurity learning environment built with Streamlit.

The project simulates a structured network investigation in an isolated environment. Users progress through multiple stages of reconnaissance and analysis, learning how to interpret evidence rather than simply treating tool output as proof.

The application emphasizes a central investigation principle:

> No command without a prediction. No finding without evidence.

---

## 🎯 Project Objective

The goal of Operation ShadowMap is to provide an interactive introduction to fundamental cybersecurity investigation concepts.

Users progress through a simulated investigation involving:

- Host discovery
- Port investigation
- Packet analysis
- TCP communication
- Service enumeration
- Attack surface analysis
- Evidence-based investigation
- Blue team response

Each stage builds on information collected in previous stages.

---

## 🗺️ Investigation Flow

### Level 1 — Host Discovery
Identify systems that appear reachable on the target network.

### Level 2 — Port Investigation
Investigate communication endpoints and interpret open, closed, and filtered port states.

### Level 3 — Packet Detective
Analyze simulated network traffic and identify meaningful evidence from packets.

### Level 4 — TCP Connection Lab
Explore the TCP communication process and understand the connection handshake.

### Level 5 — Invisible Host
Investigate service-level information and understand what can be learned from exposed services.

### Level 6 — Attack Surface Analysis
Combine previous findings to identify areas that may require further security investigation.

### Level 7 — Final Investigation
Follow the collected evidence and determine the conclusion best supported by the investigation.

### Final Stage — Blue Team Response
Shift perspective from investigation to defense and consider appropriate response actions.

---

## 🧠 Learning Approach

Operation ShadowMap is designed around evidence-based reasoning.

The application encourages users to:

1. Make a prediction before beginning an investigation.
2. Select an investigation method.
3. Observe the resulting evidence.
4. Interpret the evidence carefully.
5. Avoid drawing conclusions beyond what the evidence supports.

The simulation intentionally distinguishes between observations and conclusions. For example, an open port indicates an accessible communication endpoint but does not automatically prove that a system is vulnerable.

---

🛠️ Technologies Used

- Python
- Streamlit

---

▶️ Running the Project

1. Clone the repository
git clone <repository-url>

2. Navigate to the project directory
cd Operation-ShadowMap

3. Install Dependencies
pip install -r requirements.txt

4. Run the application
streamlit run Operation_Shadowmap.py

The application will open in your browser.

---
📁 Project Structure

Operation-ShadowMap/
│
├── pages/
│   ├── 1_Mission_Briefing.py
│   ├── 2_Host_Discovery.py
│   ├── 3_Port_Investigation.py
│   ├── 4_Packet_Detective.py
│   ├── 5_TCP_Handshake.py
│   ├── 6_Invisible_Host.py
│   ├── 7_Attack_Surface_Map.py
│   ├── 8_Final_Mission.py
│   └── 9_Blue_Team.py
│
├── Operation_Shadowmap.py
├── requirements.txt
└── README.md

⚠️ Disclaimer

Operation ShadowMap is an educational simulation designed for learning cybersecurity concepts and evidence-based investigation.

The hosts, network activity, services, and findings presented in the application are simulated. The project does not perform real-world network scanning or exploitation.