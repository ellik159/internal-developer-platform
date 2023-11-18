import httpx
import logging
from typing import Dict, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class ArgoCDService:
    def __init__(self):
        self.base_url = f"https://{settings.ARGOCD_SERVER}/api/v1"
        self.headers = {
            "Authorization": f"Bearer {settings.ARGOCD_TOKEN}",
            "Content-Type": "application/json"
        }
    
    def create_application(
        self,
        name: str,
        namespace: str,
        repo_url: str,
        path: str,
        target_revision: str = "HEAD"
    ):
        """Create an ArgoCD application"""
        
        app_spec = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {
                "name": name,
                "namespace": settings.ARGOCD_NAMESPACE
            },
            "spec": {
                "project": "default",
                "source": {
                    "repoURL": repo_url,
                    "targetRevision": target_revision,
                    "path": path
                },
                "destination": {
                    "server": "https://kubernetes.default.svc",
                    "namespace": namespace
                },
                "syncPolicy": {
                    "automated": {
                        "prune": True,
                        "selfHeal": True
                    }
                }
            }
        }
        
        try:
            with httpx.Client(verify=settings.ARGOCD_VERIFY_SSL) as client:
                response = client.post(
                    f"{self.base_url}/applications",
                    headers=self.headers,
                    json=app_spec,
                    timeout=30
                )
                response.raise_for_status()
                logger.info(f"Created ArgoCD application: {name}")
                return response.json()
        except Exception as e:
            logger.error(f"Failed to create ArgoCD application: {e}")
            raise
    
    def sync_application(self, name: str):
        """Trigger sync for an application"""
        
        sync_request = {
            "revision": "HEAD",
            "prune": True,
            "dryRun": False
        }
        
        try:
            with httpx.Client(verify=settings.ARGOCD_VERIFY_SSL) as client:
                response = client.post(
                    f"{self.base_url}/applications/{name}/sync",
                    headers=self.headers,
                    json=sync_request,
                    timeout=30
                )
                response.raise_for_status()
                logger.info(f"Triggered sync for application: {name}")
                return response.json()
        except Exception as e:
            logger.error(f"Failed to sync application: {e}")
            raise
    
    def get_application_status(self, name: str) -> Dict:
        """Get application sync and health status"""
        
        try:
            with httpx.Client(verify=settings.ARGOCD_VERIFY_SSL) as client:
                response = client.get(
                    f"{self.base_url}/applications/{name}",
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                app_data = response.json()
                
                return {
                    "sync": app_data.get("status", {}).get("sync"),
                    "health": app_data.get("status", {}).get("health"),
                    "operationState": app_data.get("status", {}).get("operationState")
                }
        except Exception as e:
            logger.error(f"Failed to get application status: {e}")
            raise
    
    def delete_application(self, name: str):
        """Delete an ArgoCD application"""
        
        try:
            with httpx.Client(verify=settings.ARGOCD_VERIFY_SSL) as client:
                response = client.delete(
                    f"{self.base_url}/applications/{name}",
                    headers=self.headers,
                    timeout=30
                )
                response.raise_for_status()
                logger.info(f"Deleted ArgoCD application: {name}")
        except Exception as e:
            logger.error(f"Failed to delete application: {e}")
            raise
