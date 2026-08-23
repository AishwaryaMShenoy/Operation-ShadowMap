import streamlit as st
import time

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🤝 TCP Connection Lab")
st.caption("LEVEL 4 — Before the Conversation Begins")

st.divider()


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "tcp_lab_complete" not in st.session_state:
    st.session_state.tcp_lab_complete = False

if "tcp_connection_started" not in st.session_state:
    st.session_state.tcp_connection_started = False


# --------------------------------------------------
# GET TARGET FROM PREVIOUS LEVEL
# --------------------------------------------------

target = st.session_state.get("port_scan_target")

if not target:
    st.warning(
        "No target investigation was found. Complete Port Investigation "
        "before entering the TCP Connection Lab."
    )
    st.stop()


# --------------------------------------------------
# DEFINE TARGET DETAILS
# --------------------------------------------------

if "Host A" in target:
    target_name = "Host A"
    target_ip = "192.168.56.10"
    service = "HTTP"
    service_port = 80
    client_port = 51524

elif "Host B" in target:
    target_name = "Host B"
    target_ip = "192.168.56.20"
    service = "SSH"
    service_port = 22
    client_port = 51525

else:
    target_name = "Host C"
    target_ip = "192.168.56.30"
    service = "DNS"
    service_port = 53
    client_port = 53000


# --------------------------------------------------
# MISSION BRIEFING
# --------------------------------------------------

st.subheader("🎯 Mission Objective")

st.write(
    f"""
Your earlier investigation identified **{target_name} ({target_ip})**
and observed communication with its **{service} service on TCP port
{service_port}**.

Before application data can be exchanged over TCP, the communicating
systems establish a connection.

Your task is to reconstruct that connection process using the observed
network evidence.
"""
)

st.info(
    "RULE: TCP connection establishment follows a defined sequence. "
    "Identify each step using the observed TCP flags."
)

st.divider()


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.subheader("🧠 Make Your Prediction")

prediction = st.radio(
    "Before inspecting the evidence, what do you expect to observe?",
    [
        "A sequence of TCP control messages used to establish a connection",
        "An immediate HTTP/SSH/DNS response without a connection",
        "A vulnerability exploit",
        "The target's stored passwords"
    ],
    index=None,
    key="tcp_prediction"
)

correct_prediction = (
    "A sequence of TCP control messages used to establish a connection"
)

if prediction == correct_prediction:
    st.success(
        "Correct. TCP uses control flags to establish a connection before "
        "reliable application data exchange begins."
    )

elif prediction:
    st.error(
        "That does not match the purpose of the TCP connection-establishment "
        "process."
    )

st.divider()


# --------------------------------------------------
# START CONNECTION INVESTIGATION
# --------------------------------------------------

st.subheader("▶ Reconstruct Connection")

can_run = prediction == correct_prediction

if not can_run:
    st.warning(
        "Make the correct prediction before reconstructing the connection."
    )


if st.button("🤝 INSPECT TCP CONNECTION", disabled=not can_run):

    with st.status("Inspecting TCP communication...", expanded=True) as status:

        st.write(
            f"Examining connection attempt to {target_ip}:{service_port}..."
        )
        time.sleep(0.7)

        st.write("Identifying TCP control flags...")
        time.sleep(0.7)

        st.write("Reconstructing connection sequence...")
        time.sleep(0.7)

        status.update(
            label="TCP connection evidence ready",
            state="complete",
            expanded=False
        )

    st.session_state.tcp_connection_started = True


# --------------------------------------------------
# CONNECTION EVIDENCE
# --------------------------------------------------

if st.session_state.tcp_connection_started:

    st.success("TCP connection evidence reconstructed.")

    st.subheader("🔎 Connection Sequence")

    st.code(
        f"""
CLIENT (192.168.56.5:{client_port})
        |
        |  SYN
        |---------------------------->
        |                             SERVER ({target_ip}:{service_port})
        |                             {service}
        |  SYN + ACK
        |<----------------------------
        |
        |  ACK
        |---------------------------->
        |
        |  CONNECTION ESTABLISHED
""",
        language="text"
    )

    st.divider()


    # --------------------------------------------------
    # STEP 1
    # --------------------------------------------------

    st.subheader("🧩 Connection Question 1")

    step_one = st.radio(
        "What is the purpose of the initial SYN?",
        [
            "Request to begin a TCP connection",
            "Confirmation that the connection is complete",
            "Transfer of the complete application response",
            "Proof that the server is vulnerable"
        ],
        index=None,
        key="tcp_step_one"
    )

    if step_one == "Request to begin a TCP connection":
        st.success(
            "Correct. The initial SYN begins the TCP connection-establishment "
            "process."
        )

    elif step_one:
        st.error(
            "The first SYN is used to initiate the connection process."
        )


    # --------------------------------------------------
    # STEP 2
    # --------------------------------------------------

    st.subheader("🧩 Connection Question 2")

    step_two = st.radio(
        "What does the SYN + ACK response indicate?",
        [
            "The server acknowledges the request and agrees to establish a connection",
            "The server has been exploited",
            "The TCP connection has already transferred application data",
            "The server is closing the connection"
        ],
        index=None,
        key="tcp_step_two"
    )

    correct_step_two = (
        "The server acknowledges the request and agrees to establish a connection"
    )

    if step_two == correct_step_two:
        st.success(
            "Correct. The server acknowledges the client's SYN and sends "
            "its own SYN as part of the connection establishment."
        )

    elif step_two:
        st.error(
            "Focus on the two flags: acknowledgement plus synchronization."
        )


    # --------------------------------------------------
    # STEP 3
    # --------------------------------------------------

    st.subheader("🧩 Connection Question 3")

    step_three = st.radio(
        "What completes the TCP three-way handshake?",
        [
            "The client's final ACK",
            "A second SYN from the server",
            "An HTTP response",
            "Closing the connection"
        ],
        index=None,
        key="tcp_step_three"
    )

    if step_three == "The client's final ACK":
        st.success(
            "Correct. After the final ACK, the TCP connection is established "
            "and application-layer communication can proceed."
        )

    elif step_three:
        st.error(
            "Look at the final message in the reconstructed sequence."
        )


# --------------------------------------------------
# LEVEL COMPLETION
# --------------------------------------------------

if (
    st.session_state.tcp_connection_started
    and step_one == "Request to begin a TCP connection"
    and step_two == correct_step_two
    and step_three == "The client's final ACK"
):
    st.session_state.tcp_lab_complete = True


if st.session_state.tcp_lab_complete:

    st.divider()

    st.success(
        "✓ LEVEL COMPLETE — TCP CONNECTION RECONSTRUCTED"
    )

    st.write(
        f"""
You reconstructed the TCP three-way handshake used to establish
communication with **{target_name}**.

**SYN → SYN/ACK → ACK → Connection Established**

Now that the connection process is understood, the next stage can focus
on learning more about the service exposed on the target.
"""
    )