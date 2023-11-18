import os
import subprocess
import json
import logging
from typing import Dict, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class TerraformService:
    def __init__(self):
        self.working_dir = settings.TERRAFORM_WORKING_DIR
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
    
    def _run_command(self, cmd: list, cwd: str = None) -> tuple:
        """Run terraform command and return output"""
        
        work_dir = cwd or self.working_dir
        
        try:
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Terraform command failed: {result.stderr}")
                raise Exception(f"Terraform error: {result.stderr}")
            
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            raise Exception("Terraform command timed out")
    
    def provision_database(
        self,
        name: str,
        db_type: str,
        size: str,
        namespace: str
    ) -> Dict:
        """Provision database using Terraform"""
        
        # Create a workspace directory for this database
        db_dir = os.path.join(self.working_dir, f"db-{name}")
        os.makedirs(db_dir, exist_ok=True)
        
        # Generate terraform configuration
        # In real scenario, you'd use modules or templates
        tf_config = self._generate_db_config(name, db_type, size, namespace)
        
        with open(os.path.join(db_dir, "main.tf"), "w") as f:
            f.write(tf_config)
        
        # Initialize terraform
        logger.info(f"Initializing terraform for database {name}")
        self._run_command(["terraform", "init"], cwd=db_dir)
        
        # Apply configuration
        logger.info(f"Applying terraform for database {name}")
        stdout, _ = self._run_command(
            ["terraform", "apply", "-auto-approve", "-json"],
            cwd=db_dir
        )
        
        # Get outputs
        logger.info("Getting terraform outputs")
        output_cmd = ["terraform", "output", "-json"]
        stdout, _ = self._run_command(output_cmd, cwd=db_dir)
        
        outputs = json.loads(stdout)
        
        # Parse outputs to return connection details
        return {
            "host": outputs.get("host", {}).get("value"),
            "port": outputs.get("port", {}).get("value", 5432),
            "database_name": outputs.get("database_name", {}).get("value"),
            "username": outputs.get("username", {}).get("value"),
            "secret_name": f"{name}-db-credentials"
        }
    
    def _generate_db_config(
        self,
        name: str,
        db_type: str,
        size: str,
        namespace: str
    ) -> str:
        """Generate Terraform configuration for database"""
        
        # This is a simplified example
        # In production, you'd use proper modules
        
        instance_class = {
            "small": "db.t3.micro",
            "medium": "db.t3.small",
            "large": "db.t3.medium"
        }.get(size, "db.t3.micro")
        
        config = f'''
terraform {{
  required_providers {{
    kubernetes = {{
      source = "hashicorp/kubernetes"
      version = "~> 2.0"
    }}
  }}
}}

# This is a placeholder - in real scenario you'd provision actual RDS/CloudSQL
# For now just create a K8s service placeholder

resource "kubernetes_service" "db" {{
  metadata {{
    name = "{name}"
    namespace = "{namespace}"
  }}
  spec {{
    selector = {{
      app = "{name}"
    }}
    port {{
      port = 5432
      target_port = 5432
    }}
  }}
}}

output "host" {{
  value = "{name}.{namespace}.svc.cluster.local"
}}

output "port" {{
  value = 5432
}}

output "database_name" {{
  value = "{name}"
}}

output "username" {{
  value = "{name}_user"
}}
'''
        return config
    
    def destroy_database(self, name: str):
        """Destroy database infrastructure"""
        
        db_dir = os.path.join(self.working_dir, f"db-{name}")
        
        if not os.path.exists(db_dir):
            logger.warning(f"Database directory not found: {db_dir}")
            return
        
        logger.info(f"Destroying terraform for database {name}")
        self._run_command(
            ["terraform", "destroy", "-auto-approve"],
            cwd=db_dir
        )
