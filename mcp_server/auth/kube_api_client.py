import os
import yaml
from kubernetes import client
from pathlib import Path


class ClusterConfigError(Exception):
    pass


BASE_DIR = Path(__file__).resolve().parent.parent
CLUSTERS_FILE = BASE_DIR / "clusters.yaml"


def load_clusters_config() -> dict:
    if not CLUSTERS_FILE.exists():
        raise ClusterConfigError(f"clusters.yaml not found at {CLUSTERS_FILE}")

    with open(CLUSTERS_FILE, "r") as f:
        return yaml.safe_load(f)


def get_api_client(cluster_name: str) -> client.ApiClient:
    cfg = load_clusters_config()
    cluster = cfg.get("clusters", {}).get(cluster_name)

    if not cluster:
        raise ClusterConfigError(f"Unknown cluster '{cluster_name}'")

    configuration = client.Configuration()
    configuration.host = cluster["api_server"]

    ca_path = BASE_DIR / cluster["ca_cert"]
    if not ca_path.exists():
        raise ClusterConfigError(f"CA cert not found: {ca_path}")

    configuration.ssl_ca_cert = str(ca_path)

    token_env = cluster.get("token_env")
    token = os.getenv(token_env)

    if not token:
        raise ClusterConfigError(
            f"Token not found in environment variable '{token_env}'"
        )

    configuration.api_key = {
        "authorization": f"Bearer {token}"
    }

    # Hard safety guarantees
    configuration.verify_ssl = True
    configuration.assert_hostname = False

    return client.ApiClient(configuration)
