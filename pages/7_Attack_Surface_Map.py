import streamlit as st
import time

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🎯 Attack Surface Analysis")
st.caption("LEVEL 6 — Where Should You Look Next?")

st.divider()


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "attack_surface_started" not in st.session_state:
    st.session_state.attack_surface_started = False

if "attack_surface_complete" not in st.session_state:
    st.session_state.attack_surface_complete = False


# --------------------------------------------------
# GET TARGET FROM PREVIOUS INVESTIGATION
# --------------------------------------------------

target = st.session_state.get("port_scan_target")

if not target:
    st.warning(
        "No target investigation was found. Complete the Port Investigation "
        "level before entering Attack Surface Analysis."
    )
    st.stop()


# --------------------------------------------------
# RESET IF TARGET CHANGES
# --------------------------------------------------

if (
    st.session_state.get("attack_surface_target")
    and st.session_state.get("attack_surface_target") != target
):

    st.session_state.attack_surface_started = False
    st.session_state.attack_surface_complete = False

    for key in [
        "surface_prediction",
        "surface_focus",
        "surface_conclusion"
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

    exposed_components = [
        "HTTP service on TCP port 80",
        "Internal Portal web application",
        "Discovered /backup/ resource"
    ]

    correct_focus = (
        "Investigate the discovered /backup/ resource further"
    )

    focus_explanation = (
        "The /backup/ resource is newly discovered information exposed "
        "through the HTTP service. It represents a specific area that "
        "deserves further assessment."
    )

    correct_conclusion = (
        "The discovered resource increases the attack surface and should be assessed further"
    )


elif "Host B" in target:

    target_name = "Host B"
    target_ip = "192.168.56.20"
    service = "SSH"
    port = 22

    exposed_components = [
        "SSH service on TCP port 22",
        "OpenSSH service banner",
        "Authentication interface"
    ]

    correct_focus = (
        "Assess the exposed SSH service and its configuration"
    )

    focus_explanation = (
        "The SSH service is an externally reachable entry point. Its "
        "configuration and exposed behavior should be assessed further."
    )

    correct_conclusion = (
        "The exposed SSH service is part of the attack surface and warrants further assessment"
    )


else:

    target_name = "Host C"
    target_ip = "192.168.56.30"
    service = "DNS"
    port = 53

    exposed_components = [
        "DNS service on TCP port 53",
        "Authoritative DNS behavior",
        "DNS query interface"
    ]

    correct_focus = (
        "Investigate the exposed DNS service and its configuration"
    )

    focus_explanation = (
        "The responding DNS service is an exposed interface that may reveal "
        "additional information depending on its configuration."
    )

    correct_conclusion = (
        "The exposed DNS service forms part of the attack surface and should be assessed further"
    )


# --------------------------------------------------
# MISSION BRIEFING
# --------------------------------------------------

st.subheader("🎯 Mission Objective")

st.write(
    f"""
Your previous investigation identified **{target_name} ({target_ip})**
and gathered information about its exposed **{service} service**.

The **attack surface** consists of the systems, services, interfaces,
and resources that are exposed and could potentially be interacted with.

Your task is not to assume that something is vulnerable.

Instead, use the evidence collected so far to identify which exposed
component deserves further investigation.
"""
)

st.info(
    "RULE: A larger or more visible attack surface does not automatically "
    "mean a vulnerability exists. Prioritize investigation based on the "
    "evidence available."
)

st.divider()


# --------------------------------------------------
# REVIEW COLLECTED EVIDENCE
# --------------------------------------------------

st.subheader("📋 Evidence Collected So Far")

st.write(
    f"**Target:** {target_name} ({target_ip})"
)

st.write(
    f"**Previously identified service:** {service} on TCP port {port}"
)

st.write("**Observed attack-surface components:**")

for component in exposed_components:
    st.write(f"- {component}")

st.divider()


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.subheader("🧠 Make Your Prediction")

prediction = st.radio(
    "What is the purpose of attack surface analysis?",
    [
        "Identify and prioritize exposed components for further assessment",
        "Immediately exploit every exposed service",
        "Assume every open port is vulnerable",
        "Recover passwords from every system"
    ],
    index=None,
    key="surface_prediction"
)

correct_prediction = (
    "Identify and prioritize exposed components for further assessment"
)

if prediction == correct_prediction:

    st.success(
        "Correct. Attack surface analysis helps identify exposed areas "
        "and decide where further investigation should be focused."
    )

elif prediction:

    st.error(
        "Attack surface analysis focuses on identifying and prioritizing "
        "possible areas for further investigation—not immediately exploiting them."
    )

st.divider()


# --------------------------------------------------
# CHOOSE INVESTIGATION FOCUS
# --------------------------------------------------

st.subheader("🔍 Choose Investigation Focus")

focus_options = [
    "Select an area...",
    correct_focus,
    "Ignore the exposed services and stop investigating",
    "Assume the entire host is vulnerable without further evidence",
    "Attempt to access unrelated stored passwords"
]

focus = st.selectbox(
    "Based on the evidence, what should be investigated next?",
    focus_options,
    key="surface_focus"
)

if focus == correct_focus:

    st.success(
        "Good choice. This decision is based on evidence gathered during "
        "the previous investigation."
    )

elif focus != "Select an area...":

    st.warning(
        "Choose the option most directly supported by the evidence collected "
        "during enumeration."
    )

st.divider()


# --------------------------------------------------
# START ATTACK SURFACE REVIEW
# --------------------------------------------------

st.subheader("▶ Analyze Attack Surface")

can_analyze = (
    prediction == correct_prediction
    and focus == correct_focus
)

if not can_analyze:

    st.warning(
        "Make the correct prediction and select an evidence-based "
        "investigation focus before continuing."
    )


if st.button(
    "🎯 ANALYZE ATTACK SURFACE",
    disabled=not can_analyze
):

    with st.status(
        "Analyzing exposed components...",
        expanded=True
    ) as status:

        st.write(
            f"Reviewing exposed services on {target_name}..."
        )
        time.sleep(0.6)

        st.write(
            "Comparing discovered interfaces and resources..."
        )
        time.sleep(0.7)

        st.write(
            "Prioritizing evidence-based investigation targets..."
        )
        time.sleep(0.7)

        status.update(
            label="Attack surface analysis complete",
            state="complete",
            expanded=False
        )

    st.session_state.attack_surface_started = True
    st.session_state.attack_surface_target = target


# --------------------------------------------------
# DISPLAY ANALYSIS RESULTS
# --------------------------------------------------

if (
    st.session_state.attack_surface_started
    and st.session_state.get("attack_surface_target") == target
):

    st.success(
        f"Attack surface analysis completed for {target_name}."
    )

    st.subheader("📊 Analysis Result")

    st.info(
        f"Priority investigation area: **{correct_focus}**"
    )

    st.write(
        focus_explanation
    )

    st.divider()


    # --------------------------------------------------
    # EVIDENCE CHECK
    # --------------------------------------------------

    st.subheader("🧾 Evidence Check")

    conclusion = st.radio(
        "Which conclusion is best supported by the analysis?",
        [
            correct_conclusion,
            f"{target_name} is definitely vulnerable",
            "The exposed service has already been successfully exploited",
            "No further assessment is required"
        ],
        index=None,
        key="surface_conclusion"
    )

    if conclusion == correct_conclusion:

        st.success(
            "Correct. The analysis identifies an exposed area that warrants "
            "further assessment, without claiming that a vulnerability has "
            "already been proven."
        )

        st.session_state.attack_surface_complete = True

    elif conclusion:

        st.error(
            "The evidence identifies an area for further investigation, "
            "but it does not prove exploitation or vulnerability."
        )


# --------------------------------------------------
# LEVEL COMPLETE
# --------------------------------------------------

if (
    st.session_state.attack_surface_complete
    and st.session_state.get("attack_surface_target") == target
):

    st.divider()

    st.success(
        "✓ LEVEL COMPLETE — ATTACK SURFACE PRIORITIZED"
    )

    if "Host A" in target:

        st.write(
            """
You followed the evidence from an exposed port to a specific web resource.

**Host A → TCP/80 → HTTP Service → Internal Portal → `/backup/`**

The next mission will investigate this discovered resource and determine
what information it actually exposes.
"""
        )

    else:

        st.write(
            f"""
You identified the exposed **{service} service** as an important part
of the target's attack surface.

The next mission will move beyond general discovery and examine the
prioritized component more closely.
"""
        )