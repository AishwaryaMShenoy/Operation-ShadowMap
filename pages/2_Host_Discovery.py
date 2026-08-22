import streamlit as st
import time

st.title("🔍 Host Discovery")
st.caption("LEVEL 1 — Does anyone exist?")

st.divider()

# Mission briefing
st.subheader("🎯 Mission Objective")

st.write("""
You have been authorized to investigate the isolated network:

**192.168.56.0/24**

You do not know which hosts are currently active.
Before investigating ports or services, you must first discover which
systems respond on the network.
""")

st.info("RULE: Make a prediction before running the investigation.")

st.divider()

# Prediction section
st.subheader("🧠 Make Your Prediction")

prediction = st.radio(
    "What should be the first step in investigating an unknown network?",
    [
        "Attempt to exploit a host",
        "Discover which hosts are active",
        "Start guessing passwords",
        "Scan every possible vulnerability immediately"
    ],
    index=None
)

if prediction:
    if prediction == "Discover which hosts are active":
        st.success(
            "Correct. Before investigating services, we first need evidence "
            "that hosts are reachable."
        )
    else:
        st.error(
            "Not the best first step. We do not yet know which systems are "
            "present on the network."
        )

st.divider()

# Discovery technique
st.subheader("📡 Choose a Discovery Method")

method = st.selectbox(
    "Select a reconnaissance approach:",
    [
        "Select a method...",
        "ARP / Local Network Discovery",
        "ICMP Echo",
        "Host Discovery Scan"
    ]
)

if method != "Select a method...":
    if method == "ARP / Local Network Discovery":
        st.write(
            "ARP can help identify systems on a local network by observing "
            "address resolution activity."
        )

    elif method == "ICMP Echo":
        st.write(
            "ICMP Echo requests can be used to check whether a host responds, "
            "although a lack of response does not necessarily prove that the "
            "host does not exist."
        )

    elif method == "Host Discovery Scan":
        st.write(
            "A host discovery scan is used to identify systems that appear "
            "to be reachable before performing more detailed port scanning."
        )

st.divider()

# Run investigation
st.subheader("▶ Run Investigation")

can_run = (
    prediction == "Discover which hosts are active"
    and method != "Select a method..."
)

if not can_run:
    st.warning(
        "Complete the prediction and select a discovery method before "
        "running the investigation."
    )

# Initialize mission state
if "host_discovery_complete" not in st.session_state:
    st.session_state.host_discovery_complete = False


# Start investigation
if st.button("🔍 START HOST DISCOVERY", disabled=not can_run):

    with st.status("Investigating network...", expanded=True) as status:

        st.write("Checking network range: 192.168.56.0/24")
        time.sleep(0.7)

        st.write("Sending discovery probes...")
        time.sleep(0.7)

        st.write("Waiting for responses...")
        time.sleep(0.7)

        status.update(
            label="Host discovery complete",
            state="complete",
            expanded=False
        )

    # Remember that the investigation was completed
    st.session_state.host_discovery_complete = True


# Show results whenever discovery has been completed
if st.session_state.host_discovery_complete:

    st.success("Evidence collected: reachable hosts were identified.")

    st.subheader("📋 Discovery Results")

    results = [
        {
            "Host": "Host A",
            "IP Address": "192.168.56.10",
            "Status": "Reachable"
        },
        {
            "Host": "Host B",
            "IP Address": "192.168.56.20",
            "Status": "Reachable"
        },
        {
            "Host": "Host C",
            "IP Address": "192.168.56.30",
            "Status": "Reachable"
        }
    ]

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🧾 Evidence Check")

    conclusion = st.radio(
        "Based on the investigation, which conclusion is best supported?",
        [
            "Only these three hosts can possibly exist on the network",
            "These three hosts responded and appear reachable",
            "All other addresses are definitely unused",
            "All three hosts are vulnerable"
        ],
        index=None,
        key="conclusion"
    )

    if conclusion == "These three hosts responded and appear reachable":

        st.success(
            "Correct. Our conclusion should match the evidence: these "
            "hosts responded and appear reachable."
        )

        st.session_state.host_discovery_answered = True

    elif conclusion:

        st.error(
            "Be careful not to claim more than the evidence proves. "
            "A response supports reachability; no response does not "
            "necessarily prove that a host does not exist."
        )