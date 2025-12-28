#!/usr/bin/env python3
"""
Microsoft Sentinel Content Deployment Script

This script automatically discovers and deploys ARM templates for Microsoft Sentinel content
including Analytics Rules, Workbooks, and Watchlists.
"""

import os
import json
import sys
import glob
from typing import List, Dict, Any
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


class SentinelContentDeployer:
    """Deploy Microsoft Sentinel content from ARM templates."""
    
    def __init__(self, subscription_id: str, resource_group: str, workspace_name: str):
        """
        Initialize the deployer.
        
        Args:
            subscription_id: Azure subscription ID
            resource_group: Resource group containing the Sentinel workspace
            workspace_name: Name of the Sentinel workspace
        """
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        
        # Authenticate using default credentials (works with Azure CLI, Managed Identity, etc.)
        self.credential = DefaultAzureCredential()
        self.resource_client = ResourceManagementClient(self.credential, subscription_id)
        
    def discover_templates(self, templates_dir: str = "templates") -> Dict[str, List[str]]:
        """
        Discover all ARM template files in the templates directory.
        
        Args:
            templates_dir: Directory containing ARM templates
            
        Returns:
            Dictionary mapping content types to lists of template file paths
        """
        templates = {
            "analytics-rules": [],
            "workbooks": [],
            "watchlists": []
        }
        
        # Search for JSON files in each subdirectory
        for content_type in templates.keys():
            pattern = os.path.join(templates_dir, content_type, "*.json")
            templates[content_type] = glob.glob(pattern)
            
        return templates
    
    def load_template(self, template_path: str) -> Dict[str, Any]:
        """
        Load an ARM template from a file.
        
        Args:
            template_path: Path to the ARM template file
            
        Returns:
            Parsed ARM template as a dictionary
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def prepare_deployment_parameters(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare deployment parameters from template.
        
        Args:
            template: ARM template
            
        Returns:
            Parameters dictionary for deployment
        """
        parameters = {}
        
        # If template has parameters, create default values or use workspace name
        if "parameters" in template:
            for param_name, param_def in template["parameters"].items():
                if param_name.lower() == "workspace" or param_name.lower() == "workspacename":
                    parameters[param_name] = {"value": self.workspace_name}
                elif "defaultValue" in param_def:
                    parameters[param_name] = {"value": param_def["defaultValue"]}
                else:
                    # For required parameters without defaults, log a warning
                    # The deployment will proceed and let Azure validate
                    print(f"  Warning: Parameter '{param_name}' has no default value")
                    
        return parameters
    
    def deploy_template(self, template_path: str, deployment_name: str) -> bool:
        """
        Deploy a single ARM template to Azure.
        
        Args:
            template_path: Path to the ARM template file
            deployment_name: Name for the deployment
            
        Returns:
            True if deployment succeeded, False otherwise
        """
        try:
            print(f"Deploying {template_path}...")
            
            # Load the template
            template = self.load_template(template_path)
            
            # Prepare parameters
            parameters = self.prepare_deployment_parameters(template)
            
            # Prepare deployment properties
            deployment_properties = {
                "mode": "Incremental",  # Use string literal for compatibility
                "template": template,
                "parameters": parameters
            }
            
            # Start deployment
            deployment_async_operation = self.resource_client.deployments.begin_create_or_update(
                resource_group_name=self.resource_group,
                deployment_name=deployment_name,
                parameters={"properties": deployment_properties}
            )
            
            # Wait for deployment to complete
            deployment_result = deployment_async_operation.result()
            
            print(f"✓ Successfully deployed {template_path}")
            print(f"  Deployment state: {deployment_result.properties.provisioning_state}")
            
            return True
            
        except Exception as e:
            print(f"✗ Failed to deploy {template_path}: {str(e)}", file=sys.stderr)
            return False
    
    def deploy_all(self, templates_dir: str = "templates") -> Dict[str, int]:
        """
        Deploy all discovered templates.
        
        Args:
            templates_dir: Directory containing ARM templates
            
        Returns:
            Dictionary with deployment statistics
        """
        stats = {
            "total": 0,
            "succeeded": 0,
            "failed": 0
        }
        
        print(f"Discovering templates in {templates_dir}...")
        templates = self.discover_templates(templates_dir)
        
        # Deploy each content type
        for content_type, template_files in templates.items():
            if not template_files:
                print(f"No templates found for {content_type}")
                continue
                
            print(f"\nDeploying {len(template_files)} {content_type} template(s)...")
            
            for i, template_file in enumerate(template_files):
                stats["total"] += 1
                
                # Generate unique deployment name
                template_basename = os.path.splitext(os.path.basename(template_file))[0]
                deployment_name = f"sentinel-{content_type}-{template_basename}"
                
                # Deploy the template
                if self.deploy_template(template_file, deployment_name):
                    stats["succeeded"] += 1
                else:
                    stats["failed"] += 1
        
        return stats


def main():
    """Main entry point for the deployment script."""
    
    # Get configuration from environment variables
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    resource_group = os.environ.get("AZURE_RESOURCE_GROUP")
    workspace_name = os.environ.get("SENTINEL_WORKSPACE_NAME")
    templates_dir = os.environ.get("TEMPLATES_DIR", "templates")
    
    # Validate required environment variables
    if not subscription_id:
        print("Error: AZURE_SUBSCRIPTION_ID environment variable is required", file=sys.stderr)
        sys.exit(1)
    
    if not resource_group:
        print("Error: AZURE_RESOURCE_GROUP environment variable is required", file=sys.stderr)
        sys.exit(1)
    
    if not workspace_name:
        print("Error: SENTINEL_WORKSPACE_NAME environment variable is required", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 80)
    print("Microsoft Sentinel Content Deployment")
    print("=" * 80)
    print(f"Subscription ID: {subscription_id}")
    print(f"Resource Group: {resource_group}")
    print(f"Workspace Name: {workspace_name}")
    print(f"Templates Directory: {templates_dir}")
    print("=" * 80)
    print()
    
    # Create deployer instance
    deployer = SentinelContentDeployer(subscription_id, resource_group, workspace_name)
    
    # Deploy all templates
    stats = deployer.deploy_all(templates_dir)
    
    # Print summary
    print("\n" + "=" * 80)
    print("Deployment Summary")
    print("=" * 80)
    print(f"Total templates: {stats['total']}")
    print(f"Succeeded: {stats['succeeded']}")
    print(f"Failed: {stats['failed']}")
    print("=" * 80)
    
    # Exit with appropriate code
    if stats['failed'] > 0:
        sys.exit(1)
    elif stats['total'] == 0:
        print("\nWarning: No templates found to deploy")
        sys.exit(0)
    else:
        print("\n✓ All deployments completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
