import streamlit as st
import time

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🛡️ Blue Team Response")
st.caption("FINAL STAGE — From Finding to Defense")

st.divider()


# --------------------------------------------------
# INITIALIZE SESSION STATE
# --------------------------------------------------

if "blue_team_started" not in st.session_state:
    st.session_state.blue_team_started = False

if "blue_team_complete" not in st.session_state:
    st.session_state.blue_team_complete = False


# --------------------------------------------------
# GET TARGET
# --------------------------------------------------

target = st.session_state.get("port_scan_target")

if not target:
    st.warning(
        "No investigation target was found. Complete the previous "
        "investigation levels before entering the Blue Team Response stage."
    )
    st.stop()


# --------------------------------------------------
# RESET IF TARGET CHANGES
# --------------------------------------------------

if (
    st.session_state.get("blue_team_target")
    and st.session_state.get("blue_team_target") != target
):

    st.session_state.blue_team_started = False
    st.session_state.blue_team_complete = False

    for key in [
        "blue_priority",
        "blue_action",
        "blue_conclusion"
    ]:
        if key in st.session_state:
            del st.session_state[key]


# --------------------------------------------------
# TARGET-SPECIFIC FINDING
# --------------------------------------------------

if "Host A" in target:

    target_name = "Host A"

    finding_summary = (
        "An accessible /backup/ resource was identified through the "
        "HTTP service. The resource exposed backup-related information "
        "that should not be unnecessarily accessible."
    )

    correct_priority = (
        "Restrict access to the exposed backup resource"
    )

    correct_action = (
        "Contain the exposure, review access controls, and securely manage the backup files"
    )

    correct_conclusion = (
        "The exposure should be remediated and monitoring should be used to detect further suspicious access"
    )


elif "Host B" in target:

    target_name = "Host B"

    finding_summary = (
        "An SSH service is externally reachable and forms part of the "
        "host's exposed attack surface."
    )

    correct_priority = (
        "Review and harden the exposed SSH service"
    )

    correct_action = (
        "Review configuration, restrict unnecessary access, and monitor authentication activity"
    )

    correct_conclusion = (
        "The exposed service should be securely configured and continuously monitored"
    )


else:

    target_name = "Host C"

    finding_summary = (
        "A DNS service is reachable and responds authoritatively, making "
        "it an exposed component requiring appropriate security controls."
    )

    correct_priority = (
        "Review and secure the exposed DNS service"
    )

    correct_action = (
        "Review DNS configuration, restrict unnecessary exposure, and monitor unusual queries"
    )

    correct_conclusion = (
        "The exposed DNS service should be securely configured and monitored for suspicious activity"
    )


# --------------------------------------------------
# BLUE TEAM BRIEFING
# --------------------------------------------------

st.subheader("🚨 Incident Handoff")

st.write(
    f"""
The investigation of **{target_name}** has been completed and the
following security-relevant finding has been handed to the defensive
team:

**{finding_summary}**

Your role is now to decide how the organization should respond.

A responsible response should focus on:

**Containment → Investigation → Remediation → Monitoring**
"""
)

st.info(
    "BLUE TEAM RULE: Prioritize reducing exposure while preserving enough "
    "evidence to understand what happened."
)

st.divider()


# --------------------------------------------------
# PRIORITY DECISION
# --------------------------------------------------

st.subheader("1️⃣ Set Response Priority")

priority = st.radio(
    "What should be prioritized first?",
    [
        correct_priority,
        "Ignore the finding because compromise has not been proven",
        "Immediately delete all systems",
        "Publish the exposed information"
    ],
    index=None,
    key="blue_priority"
)

if priority == correct_priority:

    st.success(
        "Correct. The first priority is to reduce the identified exposure "
        "using a controlled response."
    )

elif priority:

    st.error(
        "The finding should be addressed proportionally rather than ignored "
        "or handled destructively."
    )


st.divider()


# --------------------------------------------------
# RESPONSE ACTION
# --------------------------------------------------

st.subheader("2️⃣ Choose Defensive Action")

action = st.radio(
    "Which response is most appropriate?",
    [
        correct_action,
        "Assume the problem will disappear on its own",
        "Ignore all logs and evidence",
        "Remove security controls to simplify access"
    ],
    index=None,
    key="blue_action"
)

if action == correct_action:

    st.success(
        "Correct. A good response combines containment, remediation, "
        "and investigation."
    )

elif action:

    st.error(
        "Choose an action that actively reduces risk and supports "
        "continued investigation."
    )


st.divider()


# --------------------------------------------------
# START RESPONSE
# --------------------------------------------------

st.subheader("▶ Execute Response Plan")

can_respond = (
    priority == correct_priority
    and action == correct_action
)

if not can_respond:

    st.warning(
        "Select the appropriate response priority and defensive action "
        "before continuing."
    )


if st.button(
    "🛡️ EXECUTE BLUE TEAM RESPONSE",
    disabled=not can_respond
):

    with st.status(
        "Executing defensive response...",
        expanded=True
    ) as status:

        st.write("Preserving relevant investigation evidence...")
        time.sleep(0.6)

        st.write("Reducing unnecessary exposure...")
        time.sleep(0.7)

        st.write("Reviewing affected security controls...")
        time.sleep(0.7)

        st.write("Preparing monitoring and follow-up actions...")
        time.sleep(0.7)

        status.update(
            label="Defensive response complete",
            state="complete",
            expanded=False
        )

    st.session_state.blue_team_started = True
    st.session_state.blue_team_target = target


# --------------------------------------------------
# FINAL RESPONSE REVIEW
# --------------------------------------------------

if (
    st.session_state.blue_team_started
    and st.session_state.get("blue_team_target") == target
):

    st.success(
        "Initial Blue Team response completed."
    )

    st.subheader("📋 Response Review")

    conclusion = st.radio(
        "What is the best final response principle?",
        [
            correct_conclusion,
            "Once the exposure is hidden, no monitoring is needed",
            "Security findings should always be ignored unless a full compromise is proven",
            "The investigation should end without remediation"
        ],
        index=None,
        key="blue_conclusion"
    )

    if conclusion == correct_conclusion:

        st.success(
            "Correct. Effective defense combines remediation with monitoring "
            "and continued security assessment."
        )

        st.session_state.blue_team_complete = True

    elif conclusion:

        st.error(
            "Reducing exposure is only part of the response. Monitoring and "
            "follow-up are important for detecting further activity."
        )


# --------------------------------------------------
# FINAL DEBRIEF
# --------------------------------------------------

if (
    st.session_state.blue_team_complete
    and st.session_state.get("blue_team_target") == target
):

    st.divider()

    st.success(
        "🎓 MISSION COMPLETE — RED TEAM TO BLUE TEAM"
    )

    st.subheader("🏆 Final Debrief")

    st.write(
        f"""
You completed a full evidence-driven security investigation involving
**{target_name}**.

The virtual lab demonstrated how offensive and defensive cybersecurity
activities connect:

**RECONNAISSANCE**
→ Discover systems and exposed services

**ENUMERATION**
→ Gather detailed information

**ANALYSIS**
→ Interpret network and service evidence

**ATTACK SURFACE REVIEW**
→ Prioritize areas requiring further assessment

**SECURITY FINDING**
→ Identify evidence-based risk without overstating conclusions

**BLUE TEAM RESPONSE**
→ Contain, remediate, and monitor
"""
    )

    st.balloons()

    st.success(
        "Congratulations — you completed the Interactive Ethical Hacking "
        "and Defense Lab."
    )