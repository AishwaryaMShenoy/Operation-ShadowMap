import streamlit as st
import time

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🔎 Service Enumeration")
st.caption("LEVEL 5 — What Is Behind the Open Door?")

st.divider()


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "enumeration_complete" not in st.session_state:
    st.session_state.enumeration_complete = False

if "enumeration_level_complete" not in st.session_state:
    st.session_state.enumeration_level_complete = False


# --------------------------------------------------
# GET TARGET FROM PORT INVESTIGATION
# --------------------------------------------------

target = st.session_state.get("port_scan_target")

if not target:
    st.warning(
        "No target investigation was found. Complete Port Investigation "
        "before entering Service Enumeration."
    )
    st.stop()


# --------------------------------------------------
# RESET IF TARGET CHANGES
# --------------------------------------------------

if (
    st.session_state.get("enumeration_target")
    and st.session_state.get("enumeration_target") != target
):
    st.session_state.enumeration_complete = False
    st.session_state.enumeration_level_complete = False

    for key in [
        "enumeration_conclusion",
        "enumeration_prediction",
        "enumeration_method"
    ]:
        if key in st.session_state:
            del st.session_state[key]


# --------------------------------------------------
# DEFINE TARGET-SPECIFIC DETAILS
# --------------------------------------------------

if "Host A" in target:

    target_name = "Host A"
    target_ip = "192.168.56.10"
    service = "HTTP"
    port = 80

    technique = "HTTP service enumeration"

    evidence = """
PORT     STATE  SERVICE
80/tcp   open   http

Server: Apache/2.4
Title: Internal Portal
Discovered resource: /backup/
"""

    finding = (
        "The HTTP service exposes an additional resource at /backup/ "
        "that may require further investigation."
    )

    correct_conclusion = (
        "The HTTP service reveals an accessible resource that should be investigated further"
    )


elif "Host B" in target:

    target_name = "Host B"
    target_ip = "192.168.56.20"
    service = "SSH"
    port = 22

    technique = "Service banner enumeration"

    evidence = """
PORT     STATE  SERVICE
22/tcp   open   ssh

SSH-2.0-OpenSSH_8.2
Authentication required
"""

    finding = (
        "The SSH service exposes banner information identifying the "
        "service family."
    )

    correct_conclusion = (
        "The exposed service provides identifying information that can support further assessment"
    )


else:

    target_name = "Host C"
    target_ip = "192.168.56.30"
    service = "DNS"
    port = 53

    technique = "DNS service enumeration"

    evidence = """
PORT     STATE  SERVICE
53/tcp   open   domain

DNS service responding
Authoritative response observed
"""

    finding = (
        "The DNS service is responding and appears to provide authoritative "
        "information for at least one zone."
    )

    correct_conclusion = (
        "The DNS service behavior provides information that can support further investigation"
    )


# --------------------------------------------------
# MISSION BRIEFING
# --------------------------------------------------

st.subheader("🎯 Mission Objective")

st.write(
    f"""
Your earlier investigation identified **{target_name} ({target_ip})**
with an exposed **{service} service on TCP port {port}**.

Port scanning tells us that a communication endpoint is accessible.
Service enumeration goes one step further by gathering information
about what is actually running behind that endpoint.

Your task is to collect observable information from the exposed service
and interpret the evidence carefully.
"""
)

st.info(
    "RULE: Enumeration can reveal service information, banners, resources, "
    "and behavior. It does not automatically prove a vulnerability."
)

st.divider()


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.subheader("🧠 Make Your Prediction")

prediction = st.radio(
    "What is the main purpose of service enumeration?",
    [
        "Gather detailed information about an exposed service",
        "Immediately exploit every open port",
        "Recover all passwords from the target",
        "Prove that the host is vulnerable"
    ],
    index=None,
    key="enumeration_prediction"
)

correct_prediction = (
    "Gather detailed information about an exposed service"
)

if prediction == correct_prediction:

    st.success(
        "Correct. Enumeration gathers more detailed information about "
        "a discovered service to support further assessment."
    )

elif prediction:

    st.error(
        "That goes beyond the purpose of enumeration. First gather and "
        "interpret evidence about the exposed service."
    )

st.divider()


# --------------------------------------------------
# CHOOSE ENUMERATION METHOD
# --------------------------------------------------

st.subheader("🛠️ Choose Enumeration Method")

method_options = [
    "Select a method...",
    technique,
    "Password extraction",
    "Destructive attack"
]

method = st.selectbox(
    "Choose an appropriate investigation method:",
    method_options,
    key="enumeration_method"
)

if method == technique:

    st.success(
        f"Appropriate approach selected: {technique}."
    )

elif method != "Select a method...":

    st.warning(
        "That approach does not match the current objective of safely "
        "enumerating the exposed service."
    )

st.divider()


# --------------------------------------------------
# RUN ENUMERATION
# --------------------------------------------------

st.subheader("▶ Run Service Enumeration")

can_run = (
    prediction == correct_prediction
    and method == technique
)

if not can_run:

    st.warning(
        "Make the correct prediction and choose the appropriate enumeration "
        "method before continuing."
    )


if st.button(
    "🔎 START SERVICE ENUMERATION",
    disabled=not can_run
):

    with st.status("Enumerating exposed service...", expanded=True) as status:

        st.write(
            f"Target: {target_name} ({target_ip})"
        )
        time.sleep(0.6)

        st.write(
            f"Inspecting {service} service on TCP port {port}..."
        )
        time.sleep(0.7)

        st.write("Collecting observable service information...")
        time.sleep(0.7)

        st.write("Interpreting enumeration evidence...")
        time.sleep(0.6)

        status.update(
            label="Service enumeration complete",
            state="complete",
            expanded=False
        )

    st.session_state.enumeration_complete = True
    st.session_state.enumeration_target = target


# --------------------------------------------------
# DISPLAY ENUMERATION RESULTS
# --------------------------------------------------

if (
    st.session_state.enumeration_complete
    and st.session_state.get("enumeration_target") == target
):

    st.success(
        f"Enumeration evidence collected from {target_name}."
    )

    st.subheader("📋 Enumeration Results")

    st.code(
        evidence,
        language="text"
    )

    st.info(f"Finding: {finding}")

    st.divider()


    # --------------------------------------------------
    # EVIDENCE CHECK
    # --------------------------------------------------

    st.subheader("🧾 Evidence Check")

    conclusion = st.radio(
        "Which conclusion is best supported by the enumeration evidence?",
        [
            correct_conclusion,
            "The host has definitely been successfully exploited",
            "The entire system is proven vulnerable",
            "No further investigation is necessary"
        ],
        index=None,
        key="enumeration_conclusion"
    )

    if conclusion == correct_conclusion:

        st.success(
            "Correct. Enumeration provides evidence that can guide further "
            "investigation, but the observed information alone does not "
            "prove exploitation or vulnerability."
        )

        st.session_state.enumeration_level_complete = True

    elif conclusion:

        st.error(
            "Be careful not to claim more than the evidence supports. "
            "Enumeration identifies useful information and possible areas "
            "for further investigation."
        )


# --------------------------------------------------
# LEVEL COMPLETE
# --------------------------------------------------

if (
    st.session_state.enumeration_level_complete
    and st.session_state.get("enumeration_target") == target
):

    st.divider()

    st.success(
        "✓ LEVEL COMPLETE — SERVICE ENUMERATED"
    )

    if "Host A" in target:

        st.write(
            """
You identified an HTTP service and discovered an additional accessible
resource: **`/backup/`**.

This does not prove a vulnerability, but it provides a clear direction
for the next phase of the investigation.
"""
        )

    else:

        st.write(
            f"""
You gathered additional information about the exposed **{service}**
service on **{target_name}**.

The investigation can now move from basic discovery toward analyzing
the target's potential attack surface.
"""
        )