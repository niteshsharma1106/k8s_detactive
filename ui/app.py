#ui/app.py
import streamlit as st
from api_client import get_incidents, approve_incident
import time

st.set_page_config(page_title="Incident Detective", layout="wide")

# Custom CSS for UI polish
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    .stExpander { border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️ Autonomous Incident Detective")

# --- Header & Global Controls ---
col_head, col_ref = st.columns([8, 2])
with col_ref:
    if st.button("🔄 Sync Dashboard"):
        st.rerun()

# --- Data Fetching ---
# Status 'WAITING_FOR_HUMAN' = Action required
# Status 'INVESTIGATING' = Currently running in background tasks
# Status 'CLOSED' = History
pending = get_incidents(status="WAITING_FOR_HUMAN")
active = get_incidents(status="INVESTIGATING")
history = get_incidents(status="CLOSED")

# --- Dashboard Layout ---
tab1, tab2, tab3 = st.tabs(["📥 Pending Approval", "⚙️ Active Investigations", "📜 History"])

with tab1:
    if not pending:
        st.success("All quiet! No incidents awaiting your approval.")
    else:
        for incident in pending:
            inc_id = incident['incident_id']
            # Align with ingest.py state: use 'object_ref' instead of 'object'
            obj = incident.get('object_ref', {})
            
            with st.container(border=True):
                # Header Row
                c1, c2, c3 = st.columns([2, 4, 2])
                c1.error(f"🚨 {inc_id}")
                c2.subheader(f"{obj.get('kind', 'Pod')}: {obj.get('name', 'Unknown')}")
                c3.info(f"📍 {incident.get('cluster', 'acmclus01')}")

                # Investigation Content
                col_info, col_plan = st.columns([1, 1])
                
                with col_info:
                    st.markdown("### 🔍 Root Cause Analysis")
                    rc = incident.get("root_cause", {})
                    if rc and isinstance(rc, dict):
                        st.write(f"**Finding:** {rc.get('root_cause', 'N/A')}")
                        st.progress(rc.get('confidence', 0.5), text=f"Confidence: {rc.get('confidence')}")
                    else:
                        # Fallback to the raw event message if LLM hasn't updated root_cause yet
                        evt = incident.get("event", {})
                        st.write(f"**Raw Signal:** {evt.get('reason', 'Unknown')}")
                        st.write(f"**Message:** {evt.get('message', 'No message available')}")

                with col_plan:
                    st.markdown("### 🛠️ Proposed Action Plan")
                    plan = incident.get("action_plan", [])
                    if plan:
                        for idx, step in enumerate(plan):
                            st.code(f"# {step['description']}\n{step['command']}", language="bash")
                    else:
                        st.caption("No remediation plan generated yet.")

                # --- DEBUG SECTION: RAW PAYLOAD ---
                with st.expander("🛠️ Debug: Raw Sensor Payload"):
                    st.json(incident.get("event", {}))

                # Action Buttons
                btn_approve, btn_reject = st.columns(2)
                if btn_approve.button("✅ Approve & Execute", key=f"app-{inc_id}"):
                    with st.spinner(f"Resuming {inc_id}..."):
                        approve_incident(inc_id, "approve", "Approved via Streamlit")
                        st.toast(f"{inc_id} Approved!", icon="🚀")
                        time.sleep(1) 
                        st.rerun()

                if btn_reject.button("❌ Reject", key=f"rej-{inc_id}"):
                    approve_incident(inc_id, "reject", "Rejected via Streamlit")
                    st.toast(f"{inc_id} Rejected", icon="🗑️")
                    st.rerun()

with tab2:
    if not active:
        st.info("No background investigations running currently.")
    else:
        for inc in active:
            obj_name = inc.get('object_ref', {}).get('name', 'Unknown')
            st.write(f"⏳ **{inc['incident_id']}** - Analyzing `{obj_name}`...")
            st.caption(f"Reason: {inc.get('event', {}).get('reason')}")
            st.divider()

with tab3:
    if not history:
        st.write("No closed incidents found.")
    else:
        for inc in history:
            with st.expander(f"✅ {inc['incident_id']} - {inc.get('object_ref', {}).get('name')}"):
                st.write(f"**Final Decision:** {inc.get('human_decision', 'N/A')}")
                if inc.get('final_report'):
                    st.json(inc['final_report'])