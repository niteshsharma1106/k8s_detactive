#graph.py
from langgraph.graph import StateGraph, END
from state import IncidentState
from functools import partial

from nodes.event_interpreter import event_interpreter
from nodes.context_builder import context_builder
from nodes.evidence_collector import evidence_collector
from nodes.hypothesis_generator import hypothesis_generator
from nodes.hypothesis_validator import hypothesis_validator
from nodes.root_cause import root_cause_analyzer
from nodes.action_plan import action_plan_builder
from nodes.human_gate import human_gate
from nodes.decision_router import decision_router
from nodes.final_report import final_report


def build_graph(llm, tools):
    graph = StateGraph(IncidentState)

    # Use partial to "pre-fill" the llm and tools arguments
    graph.add_node("event_interpreter", partial(event_interpreter, llm=llm))
    graph.add_node("evidence_collector", partial(evidence_collector, tools=tools))
    graph.add_node("hypothesis_generator", partial(hypothesis_generator, llm=llm))






def build_graph(llm, tools):
    graph = StateGraph(IncidentState)

    # ===== Register nodes =====
    graph.add_node("event_interpreter", lambda s: event_interpreter(s, llm))
    graph.add_node("context_builder", context_builder)
    graph.add_node("evidence_collector", lambda s: evidence_collector(s, tools))
    graph.add_node("hypothesis_generator", lambda s: hypothesis_generator(s, llm))
    graph.add_node("hypothesis_validator", lambda s: hypothesis_validator(s, llm))
    graph.add_node("root_cause", lambda s: root_cause_analyzer(s, llm))
    graph.add_node("action_plan", lambda s: action_plan_builder(s, llm))
    graph.add_node("human_gate", human_gate)
    graph.add_node("decision_router", decision_router)
    graph.add_node("final_report", final_report)
    graph.add_edge("final_report", END)

    # ===== Entry =====
    graph.set_entry_point("event_interpreter")

    # ===== Linear investigation flow =====
    graph.add_edge("event_interpreter", "context_builder")
    graph.add_edge("context_builder", "evidence_collector")
    graph.add_edge("evidence_collector", "hypothesis_generator")
    graph.add_edge("hypothesis_generator", "hypothesis_validator")
    graph.add_edge("hypothesis_validator", "root_cause")
    graph.add_edge("root_cause", "action_plan")
    graph.add_edge("action_plan", "human_gate")

    # ===== Conditional resume after human decision =====
    graph.add_conditional_edges(
        "human_gate",
        decision_router,
        {
            "final_report": "final_report",
            "evidence_collector": "evidence_collector",
            "__end__": END,  # Map the stop condition to END
        }
    )


    # graph.add_conditional_edges(
    #     "human_gate", 
    #     decision_router,
    #     {
    #         "APPROVED": "final_report",
    #         "MORE_DATA": "evidence_collector",
    #         "REJECTED": END,
    #         "TIMEOUT": END
    #     }
    # )

    graph.add_edge("final_report", END)

    return graph.compile()

def evidence_collector(state: IncidentState, tools):
    # Now you can use tools.get_pod() etc.
    return {"some_key": "some_value"}