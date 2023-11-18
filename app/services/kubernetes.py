import yaml
from kubernetes import client, config

class KubernetesService:
    def __init__(self):
        try:
            config.load_kube_config()
        except:
            config.load_incluster_config()
        
        self.core_v1 = client.CoreV1Api()
    
    def create_namespace(self, name: str, labels=None):
        body = client.V1Namespace(
            metadata=client.V1ObjectMeta(
                name=name,
                labels=labels or {}
            )
        )
        self.core_v1.create_namespace(body)
        return True
