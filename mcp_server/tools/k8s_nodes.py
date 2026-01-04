
from kubernetes import client
from auth.kube_api_client import get_api_client

def get_node(cluster: str, node: str) -> dict:
    """
    Fetch node status and conditions.
    """
    v1, _ = load_client(cluster)
    return v1.read_node(node).to_dict()
