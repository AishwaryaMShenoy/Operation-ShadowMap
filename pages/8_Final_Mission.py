import streamlit as st
import time

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🏁 Final Investigation")
st.caption("LEVEL 7 — Follow the Evidence")

st.divider()


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "final_mission_started" not in st.session_state:
    st.session_state.final_mission_started = False

if "final_mission_complete" not in st.session_state:
    st.session_state.final_mission_complete = False


# --------------------------------------------------
# GET TARGET
# --------------------------------------------------

target = st.session_state.get("port_scan_target")

if not target:
    st.warning(
        "No previous target was found. Complete the earlier investigation "
        "levels before starting the Final Investigation."
    )
    st.stop()


# --------------------------------------------------
# RESET IF TARGET CHANGES
# --------------------------------------------------

if (
    st.session_state.get("final_mission_target")
    and st.session_state.get("final_mission_target") != target
):

    st.session_state.final_mission_started = False
    st.session_state.final_mission_complete = False

    for key in [
        "final_prediction",
        "final_method",
        "final_conclusion"
    ]:
        if key in st.session_state:
            del st.session_state[key]


# --------------------------------------------------
# TARGET-SPECIFIC MISSION DATA
# --------------------------------------------------

if "Host A" in target:

    target_name = "Host A"
    target_ip = "192.168.56.10"

    mission_objective = (
        "Investigate the previously discovered /backup/ resource and "
        "determine what evidence it exposes."
    )

    correct_method = (
        "Inspect the discovered resource and analyze the exposed information"
    )

    evidence = """
RESOURCE: /backup/

Directory listing observed:

- backup_notes.txt
- portal_backup.zip
- archive_2026.log

backup_notes.txt:

"Portal backup files are stored here temporarily.
Access restrictions should be reviewed before deployment."
"""

    correct_conclusion = (
        "The backup resource exposes information that may increase security risk and should be secured"
    )

    finding = (
        "The investigation identified an accessible backup-related resource "
        "containing information that should not necessarily be publicly exposed."
    )


elif "Host B" in target:

    target_name = "Host B"
    target_ip = "192.168.56.20"

    mission_objective = (
        "Assess the exposed SSH service and determine what information can "
        "be observed without attempting unauthorized access."
    )

    correct_method = (
        "Inspect the exposed service information and configuration evidence"
    )

    evidence = """
SERVICE: SSH

Observed information:

- SSH service reachable on TCP port 22
- Service banner: OpenSSH_8.2
- Authentication required
- No successful authentication observed
"""

    correct_conclusion = (
        "The SSH service is exposed and should be securely configured and monitored"
    )

    finding = (
        "The SSH service is externally reachable and forms part of the "
        "system's attack surface."
    )


else:

    target_name = "Host C"
    target_ip = "192.168.56.30"

    mission_objective = (
        "Investigate the observed DNS behavior and determine what "
        "security-relevant information can be concluded."
    )

    correct_method = (
        "Analyze the observed DNS responses and service behavior"
    )

    evidence = """
SERVICE: DNS

Observed information:

- DNS service reachable on TCP port 53
- Authoritative response observed
- Service responds to valid queries
- No exploitation evidence observed
"""

    correct_conclusion = (
        "The exposed DNS service should be assessed and securely configured"
    )

    finding = (
        "The DNS service is reachable and represents an exposed network "
        "interface requiring appropriate configuration and monitoring."
    )


# --------------------------------------------------
# MISSION BRIEFING
# --------------------------------------------------

st.subheader("🎯 Final Mission Objective")

st.write(
    f"""
Your investigation has followed the evidence to **{target_name}
({target_ip})**.

{mission_objective}

This final stage focuses on **evidence-based investigation**.

Your objective is not to assume that the target has been compromised.
Instead, inspect the available evidence and determine the most accurate
security conclusion.
"""
)

st.info(
    "RULE: A security finding should be based on observable evidence. "
    "Avoid claiming exploitation when the evidence only supports exposure "
    "or potential risk."
)

st.divider()


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.subheader("🧠 Make Your Prediction")

prediction = st.radio(
    "What should the final investigation attempt to establish?",
    [
        "What information or exposure is actually supported by the evidence",
        "That the target is definitely compromised",
        "That every exposed service is vulnerable",
        "The passwords of every user"
    ],
    index=None,
    key="final_prediction"
)

correct_prediction = (
    "What information or exposure is actually supported by the evidence"
)

if prediction == correct_prediction:

    st.success(
        "Correct. The investigation should remain evidence-based and "
        "only conclude what the observed information supports."
    )

elif prediction:

    st.error(
        "Do not decide the conclusion before examining the evidence."
    )


st.divider()


# --------------------------------------------------
# CHOOSE INVESTIGATION METHOD
# --------------------------------------------------

st.subheader("🛠️ Choose Investigation Method")

method = st.selectbox(
    "Choose the most appropriate next step:",
    [
        "Select a method...",
        correct_method,
        "Assume the target is compromised without evidence",
        "Destroy the exposed files",
        "Attempt unrelated password extraction"
    ],
    key="final_method"
)

if method == correct_method:

    st.success("Appropriate investigation method selected.")

elif method != "Select a method...":

    st.warning(
        "Choose the method that gathers relevant evidence while remaining "
        "within the scope of the investigation."
    )


st.divider()


# --------------------------------------------------
# START FINAL INVESTIGATION
# --------------------------------------------------

st.subheader("▶ Begin Final Investigation")

can_run = (
    prediction == correct_prediction
    and method == correct_method
)

if not can_run:

    st.warning(
        "Make the correct prediction and choose an evidence-based "
        "investigation method before continuing."
    )


if st.button(
    "🏁 BEGIN FINAL INVESTIGATION",
    disabled=not can_run
):

    with st.status(
        "Investigating prioritized target...",
        expanded=True
    ) as status:

        st.write(f"Target: {target_name} ({target_ip})")
        time.sleep(0.6)

        st.write("Reviewing previously collected evidence...")
        time.sleep(0.7)

        st.write("Inspecting prioritized component...")
        time.sleep(0.7)

        st.write("Collecting final investigation evidence...")
        time.sleep(0.7)

        status.update(
            label="Final investigation complete",
            state="complete",
            expanded=False
        )

    st.session_state.final_mission_started = True
    st.session_state.final_mission_target = target


# --------------------------------------------------
# DISPLAY FINAL EVIDENCE
# --------------------------------------------------

if (
    st.session_state.final_mission_started
    and st.session_state.get("final_mission_target") == target
):

    st.success("Final investigation evidence collected.")

    st.subheader("🔎 Investigation Evidence")

    st.code(
        evidence,
        language="text"
    )

    st.info(f"Finding: {finding}")

    st.divider()


    # --------------------------------------------------
    # FINAL CONCLUSION
    # --------------------------------------------------

    st.subheader("🧾 Final Assessment")

    conclusion = st.radio(
        "Which conclusion is best supported by the evidence?",
        [
            correct_conclusion,
            f"{target_name} has definitely been fully compromised",
            "The entire network has been proven vulnerable",
            "The evidence proves that all users' passwords were stolen"
        ],
        index=None,
        key="final_conclusion"
    )

    if conclusion == correct_conclusion:

        st.success(
            "Correct. The evidence supports a security finding that should "
            "be addressed, without making unsupported claims about "
            "compromise or exploitation."
        )

        st.session_state.final_mission_complete = True

    elif conclusion:

        st.error(
            "Stay within the evidence. The investigation may identify "
            "exposure or security risk without proving a complete compromise."
        )


# --------------------------------------------------
# MISSION COMPLETE
# --------------------------------------------------

if (
    st.session_state.final_mission_complete
    and st.session_state.get("final_mission_target") == target
):

    st.divider()

    st.success("🏆 FINAL INVESTIGATION COMPLETE")

    st.write(
        f"""
You completed an evidence-driven investigation of **{target_name}**.

Your investigation followed a structured path:

**Host Discovery → Port Investigation → Packet Analysis →
TCP Analysis → Service Enumeration → Attack Surface Analysis →
Final Investigation**

You identified a security-relevant finding without overstating what
the evidence proved.

The investigation now passes to the **Blue Team** for response and
remediation.
"""
    )