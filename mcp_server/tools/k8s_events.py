from kubernetes import client
from auth.kube_api_client import get_api_client


def get_events(cluster: str, namespace: str) -> list:
    """
    Fetch namespace events.
    """
    api_client = get_api_client(cluster)
    v1 = client.CoreV1Api(api_client)

    events = v1.list_namespaced_event(namespace=namespace)
    return [e.to_dict() for e in events.items]
