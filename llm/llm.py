import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://10.92.104.49:11434")
MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")


def get_llm():
    """
    Returns a deterministic local Ollama LLM instance.
    Single source of truth for model configuration.
    """
    return ChatOllama(
        base_url=OLLAMA_URL,
        model=MODEL,
        temperature=0,
    )
