import streamlit as st
import time

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("📡 Packet Detective")
st.caption("LEVEL 3 — Evidence on the Wire")

st.divider()


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "packet_analysis_started" not in st.session_state:
    st.session_state.packet_analysis_started = False

if "packet_level_complete" not in st.session_state:
    st.session_state.packet_level_complete = False


# --------------------------------------------------
# GET TARGET FROM PORT INVESTIGATION
# --------------------------------------------------

target = st.session_state.get("port_scan_target")

# Check whether Level 2 was completed
if not target:

    st.warning(
        "No target investigation was found. Complete the Port Investigation "
        "level first, then return to Packet Detective."
    )

    st.stop()


# --------------------------------------------------
# DEFINE TARGET INFORMATION
# --------------------------------------------------

if "Host A" in target:

    target_name = "Host A"
    target_ip = "192.168.56.10"
    service = "HTTP"
    service_port = "80"
    client_port = "51524"

    evidence = f"""
No.     Time        Source              Destination         Protocol   Info
1       0.000       192.168.56.5        {target_ip}       TCP        {client_port} → {service_port} [SYN]
2       0.001       {target_ip}       192.168.56.5        TCP        {service_port} → {client_port} [SYN, ACK]
3       0.002       192.168.56.5        {target_ip}       TCP        {client_port} → {service_port} [ACK]
4       0.010       192.168.56.5        {target_ip}       HTTP       GET / HTTP/1.1
5       0.025       {target_ip}       192.168.56.5        HTTP       HTTP/1.1 200 OK
"""

    activity_description = (
        "A client established a TCP connection and exchanged HTTP traffic "
        f"with {target_name}"
    )

elif "Host B" in target:

    target_name = "Host B"
    target_ip = "192.168.56.20"
    service = "SSH"
    service_port = "22"
    client_port = "51525"

    evidence = f"""
No.     Time        Source              Destination         Protocol   Info
1       0.000       192.168.56.5        {target_ip}       TCP        {client_port} → {service_port} [SYN]
2       0.001       {target_ip}       192.168.56.5        TCP        {service_port} → {client_port} [SYN, ACK]
3       0.002       192.168.56.5        {target_ip}       TCP        {client_port} → {service_port} [ACK]
4       0.010       {target_ip}       192.168.56.5        SSH        Server: SSH-2.0
5       0.020       192.168.56.5        {target_ip}       SSH        Client connection initiated
"""

    activity_description = (
        "A client established a TCP connection and initiated communication "
        f"with the SSH service on {target_name}"
    )

elif "Host C" in target:

    target_name = "Host C"
    target_ip = "192.168.56.30"
    service = "DNS"
    service_port = "53"
    client_port = "53000"

    evidence = f"""
No.     Time        Source              Destination         Protocol   Info
1       0.000       192.168.56.5        {target_ip}       TCP        {client_port} → {service_port} [SYN]
2       0.001       {target_ip}       192.168.56.5        TCP        {service_port} → {client_port} [SYN, ACK]
3       0.002       192.168.56.5        {target_ip}       TCP        {client_port} → {service_port} [ACK]
4       0.010       192.168.56.5        {target_ip}       DNS        Standard query
5       0.020       {target_ip}       192.168.56.5        DNS        Standard query response
"""

    activity_description = (
        "A client established a TCP connection and exchanged DNS traffic "
        f"with {target_name}"
    )


# --------------------------------------------------
# MISSION BRIEFING
# --------------------------------------------------

st.subheader("🎯 Mission Objective")

st.write(
    f"""
Your previous port investigation selected **{target_name} ({target_ip})**.

The investigation showed an exposed **{service}** service on
**TCP port {service_port}**.

A packet capture was collected while traffic was exchanged with this host.

Your task is to examine the evidence and determine what happened
on the network.
"""
)

st.info(
    "RULE: Packet analysis should be based on observable fields and "
    "protocol behavior—not assumptions."
)

st.divider()


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.subheader("🧠 Make Your Prediction")

prediction = st.radio(
    "What can packet analysis help you investigate?",
    [
        "Which systems communicated and how they exchanged data",
        "Every password stored on the network",
        "Whether every host is vulnerable",
        "The complete contents of every device"
    ],
    index=None,
    key="packet_prediction"
)

correct_prediction = (
    "Which systems communicated and how they exchanged data"
)

if prediction == correct_prediction:

    st.success(
        "Correct. Packet analysis can reveal communication between systems, "
        "protocol behavior, addresses, ports, and other observable evidence."
    )

elif prediction:

    st.error(
        "That conclusion goes beyond what packet analysis alone can prove."
    )

st.divider()


# --------------------------------------------------
# CHOOSE EVIDENCE
# --------------------------------------------------

st.subheader("🗂️ Select Evidence")

evidence_type = st.selectbox(
    "Choose the evidence you want to inspect:",
    [
        "Select evidence...",
        "Captured Network Traffic",
        "Application Source Code",
        "System Password Database"
    ],
    key="packet_evidence_type"
)

if evidence_type == "Captured Network Traffic":

    st.success(
        "Correct evidence selected. The packet capture can help reconstruct "
        "the observed network communication."
    )

elif evidence_type:

    st.warning(
        "That evidence source is outside the scope of this packet-analysis "
        "mission."
    )

st.divider()


# --------------------------------------------------
# START ANALYSIS
# --------------------------------------------------

st.subheader("▶ Inspect Packet Capture")

can_analyze = (
    prediction == correct_prediction
    and evidence_type == "Captured Network Traffic"
)

if not can_analyze:

    st.warning(
        "Make the correct prediction and select the relevant evidence before "
        "inspecting the packet capture."
    )


if st.button(
    "📡 INSPECT PACKET EVIDENCE",
    disabled=not can_analyze
):

    with st.status("Opening packet capture...", expanded=True) as status:

        st.write("Loading captured network traffic...")
        time.sleep(0.7)

        st.write(
            f"Identifying communication with {target_name}..."
        )
        time.sleep(0.7)

        st.write(
            f"Inspecting TCP and {service} activity..."
        )
        time.sleep(0.7)

        status.update(
            label="Packet evidence ready",
            state="complete",
            expanded=False
        )

    st.session_state.packet_analysis_started = True


# --------------------------------------------------
# PACKET EVIDENCE
# --------------------------------------------------

if st.session_state.packet_analysis_started:

    st.success(
        f"Packet evidence loaded for {target_name}."
    )

    st.subheader("🔎 Captured Traffic")

    st.code(
        evidence,
        language="text"
    )

    st.caption(
        "This is a simplified representation of packet-capture evidence."
    )

    st.divider()


    # --------------------------------------------------
    # QUESTION 1
    # --------------------------------------------------

    st.subheader("🧩 Evidence Question 1")

    endpoint_answer = st.radio(
        f"Which host appears to be providing the {service} service?",
        [
            "192.168.56.5",
            target_ip,
            "Both hosts equally provide the service",
            "The packet evidence does not contain enough information"
        ],
        index=None,
        key="packet_endpoint_answer"
    )

    if endpoint_answer == target_ip:

        st.success(
            f"Correct. {target_ip} responds from service port "
            f"{service_port}, matching the service identified during "
            "port investigation."
        )

    elif endpoint_answer:

        st.error(
            "Look at the direction of the responses and the service port."
        )


    # --------------------------------------------------
    # QUESTION 2
    # --------------------------------------------------

    st.subheader("🧩 Evidence Question 2")

    protocol_answer = st.radio(
        "What does the first three packets most clearly represent?",
        [
            "A TCP three-way handshake",
            "A DNS lookup",
            "A UDP exchange",
            "A completed vulnerability exploit"
        ],
        index=None,
        key="packet_protocol_answer"
    )

    if protocol_answer == "A TCP three-way handshake":

        st.success(
            "Correct. The SYN → SYN/ACK → ACK sequence represents "
            "the establishment of a TCP connection."
        )

    elif protocol_answer:

        st.error(
            "Focus on the TCP flags: SYN, SYN/ACK, and ACK."
        )


    # --------------------------------------------------
    # QUESTION 3
    # --------------------------------------------------

    st.subheader("🧩 Evidence Question 3")

    interpretation_answer = st.radio(
        "What is the best overall interpretation of this evidence?",
        [
            activity_description,
            f"{target_name} was successfully exploited",
            f"The packet capture proves the {service} service is vulnerable",
            "The network contains only two hosts"
        ],
        index=None,
        key="packet_interpretation_answer"
    )

    if interpretation_answer == activity_description:

        st.success(
            "Correct. The evidence supports normal communication with the "
            "identified service. It does not by itself prove exploitation "
            "or vulnerability."
        )

    elif interpretation_answer:

        st.error(
            "Do not infer exploitation or vulnerability from network "
            "communication alone. Stay with what the packets actually show."
        )


# --------------------------------------------------
# LEVEL COMPLETION
# --------------------------------------------------

if (
    st.session_state.packet_analysis_started
    and endpoint_answer == target_ip
    and protocol_answer == "A TCP three-way handshake"
    and interpretation_answer == activity_description
):

    st.session_state.packet_level_complete = True


if st.session_state.packet_level_complete:

    st.divider()

    st.success(
        "✓ LEVEL COMPLETE — NETWORK EVIDENCE INTERPRETED"
    )

    st.write(
        f"""
You reconstructed communication with **{target_name}**:

**Client → TCP connection → {target_name} → {service} communication**

The next mission will examine the connection process more closely.
"""
    )