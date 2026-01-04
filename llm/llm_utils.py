# agent_platform/llm/llm_utils.py
import json


def invoke_json(llm, prompt: str) -> dict:
    """
    Invoke LLM and safely parse JSON from its response.
    Works with ChatOllama / LangChain AIMessage objects.
    """
    response = llm.invoke(prompt)

    # LangChain returns AIMessage, not raw string
    if hasattr(response, "content"):
        raw = response.content
    else:
        raw = response

    try:
        return json.loads(raw)
    except Exception as e:
        raise ValueError(f"LLM returned invalid JSON: {raw}") from e
