# Azure DevOps Pipeline Setup Guide

This guide provides detailed instructions for setting up the Microsoft Sentinel Content Deployment pipeline in Azure DevOps.

## Overview

This repository uses Azure DevOps Pipelines to automatically deploy Microsoft Sentinel content (Analytics Rules, Workbooks, and Watchlists) from ARM templates stored in the repository.

## Prerequisites

- Azure DevOps organization and project
- Azure subscription with Microsoft Sentinel workspace
- Appropriate permissions to:
  - Create service connections in Azure DevOps
  - Manage pipelines in Azure DevOps
  - Deploy resources to the Azure subscription/resource group

## Step-by-Step Setup

### 1. Create Azure Service Connection

The service connection authenticates your pipeline to Azure.

1. **Navigate to Service Connections**:
   - Go to your Azure DevOps project
   - Click **Project Settings** (bottom left)
   - Under **Pipelines**, click **Service connections**

2. **Create New Connection**:
   - Click **New service connection**
   - Select **Azure Resource Manager**
   - Click **Next**

3. **Choose Authentication Method**:
   - Select **Service principal (automatic)** (recommended)
   - This automatically creates a service principal in Azure AD

4. **Configure the Connection**:
   - **Scope level**: Select **Subscription** or **Resource Group**
   - **Subscription**: Select your Azure subscription
   - **Resource group**: (Optional) Select the resource group containing your Sentinel workspace
   - **Service connection name**: Enter a name (e.g., `sentinel-deployer`)
   - **Description**: (Optional) Add a description
   - **Grant access permission to all pipelines**: Check this box for easier setup

5. **Save**:
   - Click **Save**
   - The service connection is now ready to use

### 2. Configure Pipeline Variables

You have two options for configuring variables:

#### Option A: Variable Group (Recommended for Multiple Pipelines)

1. **Create Variable Group**:
   - Go to **Pipelines** → **Library**
   - Click **+ Variable group**
   - Name it `sentinel-deployment-vars`

2. **Add Variables**:
   Add the following variables to the group:
   
   | Variable Name | Value | Secret? |
   |---------------|-------|---------|
   | `AZURE_SERVICE_CONNECTION` | Name of service connection from Step 1 | No |
   | `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID | No |
   | `AZURE_RESOURCE_GROUP` | Resource group containing Sentinel | No |
   | `SENTINEL_WORKSPACE_NAME` | Name of Sentinel workspace | No |

3. **Link to Pipeline**:
   - In `azure-pipelines.yml`, uncomment this line:
   ```yaml
   - group: sentinel-deployment-vars
   ```

#### Option B: Pipeline Variables (Simpler for Single Pipeline)

1. **Add Variables to Pipeline**:
   - Go to **Pipelines** → Select your pipeline
   - Click **Edit** → **Variables** (top right)
   - Add each variable with the values shown in Option A

2. **Pipeline YAML**:
   - Uncomment the variable definitions in `azure-pipelines.yml`:
   ```yaml
   AZURE_SERVICE_CONNECTION: 'your-service-connection-name'
   AZURE_SUBSCRIPTION_ID: 'your-subscription-id'
   AZURE_RESOURCE_GROUP: 'your-resource-group'
   SENTINEL_WORKSPACE_NAME: 'your-workspace-name'
   ```

### 3. Create the Pipeline

1. **Navigate to Pipelines**:
   - Go to **Pipelines** → **Pipelines**
   - Click **New pipeline** (or **Create Pipeline**)

2. **Connect to Your Repository**:
   - Select where your code is stored:
     - **Azure Repos Git** (if using Azure Repos)
     - **GitHub** (if using GitHub)
     - **Bitbucket Cloud**
     - Other options as needed
   - Select your repository

3. **Configure Pipeline**:
   - Select **Existing Azure Pipelines YAML file**
   - **Branch**: Select `main` (or your default branch)
   - **Path**: Select `/azure-pipelines.yml`
   - Click **Continue**

4. **Review and Run**:
   - Review the pipeline YAML
   - Click **Run** to test the pipeline
   - The pipeline will fail if variables are not configured

5. **Save the Pipeline**:
   - After configuration, click **Save** (or **Save and run**)

### 4. Grant Permissions (If Required)

If you didn't grant pipeline access to the service connection earlier:

1. Go to **Project Settings** → **Service connections**
2. Click on your service connection
3. Click **Security** (or the three dots → **Security**)
4. Add your pipeline to the allowed pipelines list

### 5. Configure Service Principal Permissions

Ensure the service principal has appropriate permissions in Azure:

1. **Find Service Principal**:
   - Go to **Azure Portal** → **Azure Active Directory** → **App registrations**
   - Search for the service connection name (or check the service connection details in Azure DevOps)

2. **Assign Permissions**:
   - Go to your resource group in Azure Portal
   - Click **Access control (IAM)**
   - Click **Add** → **Add role assignment**
   - **Role**: Select **Microsoft Sentinel Contributor** (or **Contributor**)
   - **Assign access to**: **User, group, or service principal**
   - **Select**: Search for your service principal
   - Click **Save**

## Testing the Pipeline

### Manual Run

1. Go to **Pipelines** → Select your pipeline
2. Click **Run pipeline**
3. Select the **environment** parameter (production, staging, or development)
4. Click **Run**
5. Monitor the pipeline execution

### Automatic Trigger

1. Add or modify a JSON file in the `templates/` directory:
   ```bash
   git add templates/analytics-rules/my-rule.json
   git commit -m "Add new analytics rule"
   git push
   ```

2. The pipeline will automatically trigger and deploy the changes

## Pipeline Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_SERVICE_CONNECTION` | Name of the Azure RM service connection | `sentinel-deployer` |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID (GUID) | `12345678-1234-1234-1234-123456789abc` |
| `AZURE_RESOURCE_GROUP` | Resource group containing Sentinel | `rg-sentinel-prod` |
| `SENTINEL_WORKSPACE_NAME` | Name of the Sentinel workspace | `sentinel-workspace-prod` |

## Pipeline Features

### Triggers

The pipeline automatically runs when:
- Changes are pushed to the `main` branch
- Changes affect files in `templates/**/*.json`

### Manual Parameters

When running manually, you can select:
- **environment**: Choose between production, staging, or development

### Caching

The pipeline caches Python packages to speed up subsequent runs.

### Stages and Jobs

- **Stage**: Deploy
  - **Job**: DeployContent
    - Checkout code
    - Set up Python 3.11
    - Cache pip packages
    - Install dependencies
    - Deploy Sentinel content
    - Logout from Azure

## Troubleshooting

### Pipeline Fails at "Deploy Sentinel Content" Step

**Error**: "Service connection not found"
- **Solution**: Verify the `AZURE_SERVICE_CONNECTION` variable matches the service connection name exactly

**Error**: "Subscription not found" or "Authorization failed"
- **Solution**: Check that the service principal has permissions on the subscription/resource group

### No Templates Deployed

**Error**: "Warning: No templates found to deploy"
- **Solution**: Ensure JSON files are in the correct directories (`templates/analytics-rules/`, `templates/workbooks/`, or `templates/watchlists/`)

### Authentication Errors

**Error**: "Failed to authenticate"
- **Solution**: Test the service connection in Azure DevOps settings
- **Solution**: Verify the service principal exists in Azure AD and has the correct permissions

### Variable Not Set

**Error**: "Environment variable X is required"
- **Solution**: Verify all required variables are configured in the variable group or pipeline variables

## Best Practices

1. **Use Variable Groups**: For multiple pipelines or environments
2. **Secure Variables**: Mark sensitive variables as secret
3. **Test Manually First**: Run the pipeline manually before relying on automatic triggers
4. **Monitor Logs**: Review pipeline logs for detailed error messages
5. **Version Control**: Keep the pipeline YAML in source control
6. **Least Privilege**: Grant only necessary permissions to the service principal

## Advanced Configuration

### Multi-Environment Setup

To deploy to multiple environments (dev, staging, prod):

1. Create separate variable groups for each environment
2. Modify the pipeline to use different variable groups based on the environment parameter
3. Use different service connections for different environments

### Custom Triggers

Modify the `trigger` section in `azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - 'templates/**/*.json'
    exclude:
      - 'templates/README.md'
```

### Approval Gates

Add approval requirements:

1. Go to **Pipelines** → **Environments**
2. Create a new environment (e.g., `production`)
3. Add **Approvals and checks**
4. Modify the pipeline to use the environment:

```yaml
jobs:
  - deployment: DeployContent
    environment: production
```

## Additional Resources

- [Azure DevOps Pipeline Documentation](https://docs.microsoft.com/azure/devops/pipelines/)
- [Azure DevOps Service Connections](https://docs.microsoft.com/azure/devops/pipelines/library/service-endpoints)
- [Azure DevOps Variables](https://docs.microsoft.com/azure/devops/pipelines/process/variables)
- [Microsoft Sentinel Documentation](https://docs.microsoft.com/azure/sentinel/)

## Support

For issues or questions:
1. Review the main [README.md](README.md)
2. Check the [CONTRIBUTING.md](CONTRIBUTING.md) guide
3. Review pipeline logs for error details
4. Consult Azure DevOps and Sentinel documentation
