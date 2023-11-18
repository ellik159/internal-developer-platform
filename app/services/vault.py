import hvac

class VaultService:
    def __init__(self):
        self.client = hvac.Client(url="http://localhost:8200")
        # TODO: add auth
    
    def store_secret(self, path: str, data: dict):
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=data
        )
