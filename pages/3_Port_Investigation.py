import streamlit as st
import time

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🚪 Port Investigation")
st.caption("LEVEL 2 — The Door Has a Number")

st.divider()


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "port_scan_complete" not in st.session_state:
    st.session_state.port_scan_complete = False

if "port_level_complete" not in st.session_state:
    st.session_state.port_level_complete = False


# --------------------------------------------------
# RESET FUNCTION
# --------------------------------------------------

def reset_port_scan():
    """Clear previous scan results when the target changes."""

    st.session_state.port_scan_complete = False
    st.session_state.port_level_complete = False

    # Remove previous evidence-check answer
    if "port_conclusion" in st.session_state:
        del st.session_state["port_conclusion"]


# --------------------------------------------------
# MISSION BRIEFING
# --------------------------------------------------

st.subheader("🎯 Mission Objective")

st.write("""
Host discovery has identified three systems that appear reachable.

Your next task is to investigate the communication endpoints exposed
by those systems.

In networking, a **port** acts as a numbered communication endpoint.
An open port may indicate that a service is listening and accepting
connections.
""")

st.info(
    "RULE: An open port is evidence of an exposed communication endpoint. "
    "It does not automatically prove that the system is vulnerable."
)

st.divider()

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.subheader("🧠 Make Your Prediction")

prediction = st.radio(
    "What information are you trying to discover?",
    [
        "Which ports appear open or closed and what services may be exposed",
        "The passwords used by the target",
        "Whether every application on the host is vulnerable",
        "The contents of every file stored on the host"
    ],
    index=None
)

if prediction:

    if prediction == (
        "Which ports appear open or closed and what services may be exposed"
    ):
        st.success(
            "Correct. Port investigation helps identify exposed communication "
            "endpoints and possible services."
        )

    else:
        st.error(
            "That information cannot be concluded simply from a basic port "
            "investigation. Stay within the current reconnaissance objective."
        )

st.divider()


# --------------------------------------------------
# SELECT INVESTIGATION TYPE
# --------------------------------------------------

st.subheader("📡 Choose Investigation Type")

scan_type = st.selectbox(
    "Select an investigation approach:",
    [
        "Select an approach...",
        "TCP Connect Scan",
        "SYN Scan",
        "UDP Scan"
    ]
)

if scan_type == "TCP Connect Scan":
    st.write(
        "**TCP Connect Scan:** Attempts to establish a full TCP connection "
        "with the target service."
    )

elif scan_type == "SYN Scan":
    st.write(
        "**SYN Scan:** Sends a TCP SYN probe and interprets the response "
        "without necessarily completing the full connection."
    )

elif scan_type == "UDP Scan":
    st.write(
        "**UDP Scan:** Investigates UDP communication endpoints, which do not "
        "use the TCP three-way handshake."
    )

st.divider()

# --------------------------------------------------
# SELECT TARGET
# --------------------------------------------------

st.subheader("🎯 Select Investigation Target")

target = st.selectbox(
    "Choose one of the discovered hosts:",
    [
        "Select a host...",
        "Host A — 192.168.56.10",
        "Host B — 192.168.56.20",
        "Host C — 192.168.56.30"
    ],
    key="port_target",
    on_change=reset_port_scan
)

if target == "Host A — 192.168.56.10":
    st.info("Selected target: Host A | IP Address: 192.168.56.10")

elif target == "Host B — 192.168.56.20":
    st.info("Selected target: Host B | IP Address: 192.168.56.20")

elif target == "Host C — 192.168.56.30":
    st.info("Selected target: Host C | IP Address: 192.168.56.30")

st.divider()




# --------------------------------------------------
# START INVESTIGATION
# --------------------------------------------------

st.subheader("▶ Run Port Investigation")

can_run = (
    target != "Select a host..."
    and prediction == (
        "Which ports appear open or closed and what services may be exposed"
    )
    and scan_type != "Select an approach..."
)

if not can_run:
    st.warning(
        "Select a target, make the correct prediction, and choose an "
        "investigation approach before continuing."
    )


if st.button(
    "🚪 START PORT INVESTIGATION",
    disabled=not can_run
):

    with st.status("Investigating target...", expanded=True) as status:

        st.write(f"Target selected: {target}")
        time.sleep(0.6)

        st.write(f"Investigation method: {scan_type}")
        time.sleep(0.6)

        st.write("Probing selected communication endpoints...")
        time.sleep(0.8)

        st.write("Interpreting responses...")
        time.sleep(0.6)

        status.update(
            label="Port investigation complete",
            state="complete",
            expanded=False
        )

    # Save the completed investigation
    st.session_state.port_scan_complete = True
    st.session_state.port_scan_target = target


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

# Only show results if the CURRENT target is the one scanned
if (
    st.session_state.port_scan_complete
    and st.session_state.get("port_scan_target") == target
):

    target_scanned = st.session_state.port_scan_target

    st.success(
        f"Evidence collected from: {target_scanned}"
    )

    st.subheader("📋 Investigation Results")

    # ---------------- HOST A ----------------

    if "Host A" in target_scanned:

        st.code(
            """
PORT      STATE     SERVICE
22/tcp    closed    ssh
80/tcp    open      http
443/tcp   closed    https
""",
            language="text"
        )

        st.info(
            "Interesting finding: TCP port 80 appears OPEN. "
            "This suggests an exposed HTTP communication endpoint."
        )

    # ---------------- HOST B ----------------

    elif "Host B" in target_scanned:

        st.code(
            """
PORT      STATE     SERVICE
22/tcp    open      ssh
80/tcp    closed    http
443/tcp   filtered  https
""",
            language="text"
        )

        st.info(
            "Interesting finding: TCP port 22 appears OPEN. "
            "This suggests an exposed SSH communication endpoint."
        )

    # ---------------- HOST C ----------------

    elif "Host C" in target_scanned:

        st.code(
            """
PORT      STATE     SERVICE
53/tcp    open      domain
80/tcp    closed    http
443/tcp   closed    https
""",
            language="text"
        )

        st.info(
            "Interesting finding: TCP port 53 appears OPEN. "
            "This suggests a DNS-related service may be exposed."
        )

    st.divider()


    # --------------------------------------------------
    # PORT STATE INTERPRETATION
    # --------------------------------------------------

    st.subheader("🧾 Evidence Check")

    conclusion = st.radio(
        "Which interpretation is best supported by the scan evidence?",
        [
            "An OPEN port proves the entire host is vulnerable",
            (
                "An OPEN port suggests a communication endpoint is "
                "accessible and should be investigated further"
            ),
            "A CLOSED port means the host does not exist",
            "A FILTERED port proves that no service is running"
        ],
        index=None,
        key="port_conclusion"
    )

    correct_conclusion = (
        "An OPEN port suggests a communication endpoint is "
        "accessible and should be investigated further"
    )

    if conclusion == correct_conclusion:

        st.success(
            "Correct. An open port provides evidence of an accessible "
            "communication endpoint. Further investigation is required to "
            "understand the actual service and its security posture."
        )

        st.session_state.port_level_complete = True

    elif conclusion:

        st.error(
            "Be careful not to overstate the evidence. Port states describe "
            "how the endpoint responded to the investigation, not whether "
            "the entire host is automatically secure or vulnerable."
        )


# --------------------------------------------------
# LEVEL COMPLETE
# --------------------------------------------------

if (
    st.session_state.port_level_complete
    and st.session_state.get("port_scan_target") == target
):

    st.divider()

    st.success(
        "✓ LEVEL COMPLETE — PORT STATES INTERPRETED"
    )

    st.write(
        "You have identified exposed communication endpoints and learned "
        "that port information must be interpreted carefully. The next "
        "stage is to examine evidence from the network itself."
    )