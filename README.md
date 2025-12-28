# Microsoft Sentinel Content Deployment

Automated deployment solution for Microsoft Sentinel content including Analytics Rules, Workbooks, and Watchlists using Azure DevOps Pipelines and Python.

## 🚀 Quick Start

**New to this project?** Check out the [Quick Start Guide](QUICKSTART.md) to get up and running in 5 minutes!

**Setting up Azure DevOps?** See the detailed [Azure DevOps Setup Guide](AZURE_DEVOPS_SETUP.md) for comprehensive instructions.

## 🚀 Features

- **Automated Deployment**: Deploy Sentinel content automatically via Azure DevOps Pipelines
- **Simple Workflow**: Just export ARM templates from Sentinel and upload them
- **Multiple Content Types**: Supports Analytics Rules, Workbooks, and Watchlists
- **BICEP Compatible**: Works with both ARM templates and BICEP
- **Python-Based**: Reliable deployment using Azure Python SDK

## 📋 Prerequisites

1. **Azure Resources**:
   - Existing Microsoft Sentinel workspace
   - Azure subscription with appropriate permissions

2. **Azure DevOps Project**:
   - Azure DevOps organization and project
   - Azure Resource Manager service connection configured

3. **Azure DevOps Pipeline Variables**:
   - `AZURE_SERVICE_CONNECTION`: Name of the Azure RM service connection
   - `AZURE_SUBSCRIPTION_ID`: Azure Subscription ID
   - `AZURE_RESOURCE_GROUP`: Resource Group containing Sentinel workspace
   - `SENTINEL_WORKSPACE_NAME`: Name of the Sentinel workspace

## 🛠️ Setup Instructions

### Step 1: Create Azure DevOps Service Connection

1. Go to your Azure DevOps project
2. Navigate to **Project Settings** → **Service connections**
3. Click **New service connection** → **Azure Resource Manager**
4. Select **Service principal (automatic)**
5. Configure the connection:
   - **Scope level**: Subscription
   - **Subscription**: Select your Azure subscription
   - **Resource group**: Select the resource group containing your Sentinel workspace
   - **Service connection name**: `sentinel-deployer` (or your preferred name)
6. Grant access permission to all pipelines (or configure as needed)
7. Click **Save**

### Step 2: Configure Pipeline Variables

1. In Azure DevOps, go to **Pipelines** → **Library**
2. Create a new variable group named `sentinel-deployment-vars` (or use pipeline variables)
3. Add the following variables:
   - `AZURE_SERVICE_CONNECTION`: Name of the service connection from Step 1
   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID
   - `AZURE_RESOURCE_GROUP`: Resource group name containing Sentinel workspace
   - `SENTINEL_WORKSPACE_NAME`: Name of the Sentinel workspace

### Step 3: Create the Pipeline

1. In Azure DevOps, go to **Pipelines** → **Create Pipeline**
2. Select **Azure Repos Git** (or your repository source)
3. Select your repository
4. Choose **Existing Azure Pipelines YAML file**
5. Select `/azure-pipelines.yml`
6. Click **Run** to test the pipeline

## 📦 How to Use

### Deploying Content

1. **Export ARM Template from Microsoft Sentinel**:
   - Go to your Sentinel workspace in Azure Portal
   - Navigate to the content you want to export (Analytics Rule, Workbook, or Watchlist)
   - Click "Export" and select "ARM Template"
   - Download the JSON file

2. **Add Template to Repository**:
   - Place the downloaded ARM template in the appropriate directory:
     - Analytics Rules: `templates/analytics-rules/`
     - Workbooks: `templates/workbooks/`
     - Watchlists: `templates/watchlists/`
   - Give it a descriptive filename (e.g., `brute-force-detection.json`)

3. **Commit and Push**:
   ```bash
   git add templates/
   git commit -m "Add new analytics rule for brute force detection"
   git push
   ```

4. **Automatic Deployment**:
   - The Azure DevOps Pipeline will automatically trigger
   - Your content will be deployed to the Sentinel workspace
   - Check the Pipelines tab to see deployment status

### Directory Structure

```
MSFTSentinelContentDeploy/
├── azure-pipelines.yml                    # Azure DevOps Pipeline definition
├── templates/
│   ├── analytics-rules/                   # Analytics Rules ARM templates
│   │   └── example-suspicious-signin.json
│   ├── workbooks/                         # Workbook ARM templates
│   │   └── example-security-overview.json
│   └── watchlists/                        # Watchlist ARM templates
│       └── example-high-value-assets.json
├── scripts/
│   └── deploy_sentinel_content.py         # Python deployment script
├── requirements.txt                        # Python dependencies
└── README.md                              # This file
```

## 🔍 Example Templates

The `templates/` directory contains example ARM templates for each content type. These serve as references for the expected format. Replace them with your actual exported templates.

## 🔧 Local Testing

You can test the deployment script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_RESOURCE_GROUP="your-resource-group"
export SENTINEL_WORKSPACE_NAME="your-workspace-name"

# Authenticate with Azure (one of these methods)
az login  # Interactive login
# OR use service principal
az login --service-principal -u <client-id> -p <client-secret> --tenant <tenant-id>

# Run the deployment script
python scripts/deploy_sentinel_content.py
```

## 📝 Supported Content Types

### Analytics Rules (Scheduled Queries)
Place ARM templates for analytics rules in `templates/analytics-rules/`. These include:
- Scheduled query rules
- Fusion rules
- Machine Learning Behavioral Analytics
- Microsoft security rules

### Workbooks
Place ARM templates for workbooks in `templates/workbooks/`. These are visualization dashboards for your security data.

### Watchlists
Place ARM templates for watchlists in `templates/watchlists/`. These are custom lists used in analytics rules and hunting queries.

## 🔐 Security Best Practices

1. **Use Service Connections**: Azure DevOps service connections provide secure, managed authentication
2. **Least Privilege**: Grant only necessary permissions to the service principal
3. **Review Changes**: Always review ARM templates before deployment
4. **Audit Logs**: Monitor Azure Activity Logs for deployment actions
5. **Protected Variables**: Mark sensitive pipeline variables as secret

## 🐛 Troubleshooting

### Deployment Fails with Authentication Error
- Verify pipeline variables are correctly set
- Ensure Azure service connection is properly configured
- Check that service principal has proper permissions on the resource group

### Template Deployment Error
- Validate ARM template JSON syntax
- Ensure workspace parameter is correctly set
- Check that resource types match Sentinel API versions
- Review pipeline logs for detailed error messages

### No Templates Found
- Verify templates are in the correct directories
- Ensure files have `.json` extension
- Check that templates follow the ARM template schema

### Pipeline Doesn't Trigger
- Verify the trigger paths in azure-pipelines.yml
- Check that changes are pushed to the main branch
- Ensure the pipeline is enabled in Azure DevOps

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for use with Microsoft Sentinel deployments.

## 🔗 Useful Links

- [Microsoft Sentinel Documentation](https://learn.microsoft.com/azure/sentinel/)
- [ARM Template Reference](https://learn.microsoft.com/azure/templates/)
- [Azure Python SDK](https://learn.microsoft.com/python/api/overview/azure/)
- [Azure DevOps Pipelines Documentation](https://learn.microsoft.com/azure/devops/pipelines/)
- [Azure DevOps Service Connections](https://learn.microsoft.com/azure/devops/pipelines/library/service-endpoints)
