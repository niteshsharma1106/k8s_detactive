# from state_store import load_state

# state = load_state("34bf2a81-8aaa-4f73-bec1-b13ab5c43c66")
# print(state["hypotheses"])
# print(state["action_plan"])

# ----------
from state_store import load_state

state = load_state("90fd41ff-9b1e-47ee-ad96-c90a3dfe4264")

print("STATUS:", state["status"])
print("FINAL REPORT:", state.get("final_report"))

