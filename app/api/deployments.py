from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def trigger_deployment(app_name: str):
    # TODO: integrate with ArgoCD
    return {"app": app_name, "status": "deploying"}
