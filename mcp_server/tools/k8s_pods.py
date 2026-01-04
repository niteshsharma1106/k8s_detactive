#mcp_server/tools/k8s_pods.py
from kubernetes import client
from auth.kube_api_client import get_api_client


def get_pod(cluster: str, namespace: str, pod: str) -> dict:
    """
    Fetch pod spec and status (read-only).
    """
    api_client = get_api_client(cluster)
    v1 = client.CoreV1Api(api_client)

    pod_obj = v1.read_namespaced_pod(
        name=pod,
        namespace=namespace
    )
    return pod_obj.to_dict()

def get_pod_logs(cluster: str, namespace: str, pod: str, container: str = None) -> str:
    """Fetch logs for a specific pod/container."""
    api_client = get_api_client(cluster)
    v1 = client.CoreV1Api(api_client)
    
    logs = v1.read_namespaced_pod_log(
        name=pod,
        namespace=namespace,
        container=container
    )
    return logs
