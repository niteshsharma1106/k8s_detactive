
from kubernetes import client
from auth.kube_api_client import get_api_client


def get_scc_for_pod(cluster: str, namespace: str, pod: str) -> dict:
    api_client = get_api_client(cluster)
    v1 = client.CoreV1Api(api_client)

    pod_obj = v1.read_namespaced_pod(pod, namespace)

    return {
        "scc": pod_obj.metadata.annotations.get(
            "openshift.io/scc", "unknown"
        )
    }
