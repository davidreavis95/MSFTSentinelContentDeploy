# Microsoft Sentinel Content Deployment

Automated deployment solution for Microsoft Sentinel content including Analytics Rules, Workbooks, and Watchlists using GitHub Actions and Python.

## 🚀 Features

- **Automated Deployment**: Deploy Sentinel content automatically via GitHub Actions
- **Simple Workflow**: Just export ARM templates from Sentinel and upload them
- **Multiple Content Types**: Supports Analytics Rules, Workbooks, and Watchlists
- **BICEP Compatible**: Works with both ARM templates and BICEP
- **Python-Based**: Reliable deployment using Azure Python SDK

## 📋 Prerequisites

1. **Azure Resources**:
   - Existing Microsoft Sentinel workspace
   - Azure subscription with appropriate permissions

2. **Azure Service Principal** (for GitHub Actions):
   - Create an App Registration in Azure AD
   - Assign appropriate permissions to the Sentinel workspace
   - Configure federated credentials for GitHub Actions

3. **GitHub Repository Secrets**:
   - `AZURE_CLIENT_ID`: Service Principal Client ID
   - `AZURE_TENANT_ID`: Azure AD Tenant ID
   - `AZURE_SUBSCRIPTION_ID`: Azure Subscription ID
   - `AZURE_RESOURCE_GROUP`: Resource Group containing Sentinel workspace
   - `SENTINEL_WORKSPACE_NAME`: Name of the Sentinel workspace

## 🛠️ Setup Instructions

### Step 1: Configure Azure Service Principal

```bash
# Create a service principal with federated credentials for GitHub Actions
az ad sp create-for-rbac --name "github-sentinel-deployer" \
  --role "Microsoft Sentinel Contributor" \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}

# Note down the output: clientId, tenantId, subscriptionId
```

### Step 2: Configure Federated Credentials

1. Go to Azure Portal → Azure Active Directory → App Registrations
2. Select your app registration
3. Go to "Certificates & secrets" → "Federated credentials"
4. Add a new credential:
   - **Federated credential scenario**: GitHub Actions
   - **Organization**: Your GitHub username/org
   - **Repository**: Your repository name
   - **Entity type**: Branch
   - **GitHub branch name**: main

### Step 3: Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`
   - `AZURE_RESOURCE_GROUP`
   - `SENTINEL_WORKSPACE_NAME`

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
   - The GitHub Action will automatically trigger
   - Your content will be deployed to the Sentinel workspace
   - Check the Actions tab to see deployment status

### Directory Structure

```
MSFTSentinelContentDeploy/
├── .github/
│   └── workflows/
│       └── deploy-sentinel-content.yml    # GitHub Action workflow
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

1. **Use Federated Credentials**: Avoid storing long-lived secrets in GitHub
2. **Least Privilege**: Grant only necessary permissions to the service principal
3. **Review Changes**: Always review ARM templates before deployment
4. **Audit Logs**: Monitor Azure Activity Logs for deployment actions

## 🐛 Troubleshooting

### Deployment Fails with Authentication Error
- Verify GitHub secrets are correctly set
- Ensure service principal has proper permissions
- Check federated credential configuration

### Template Deployment Error
- Validate ARM template JSON syntax
- Ensure workspace parameter is correctly set
- Check that resource types match Sentinel API versions

### No Templates Found
- Verify templates are in the correct directories
- Ensure files have `.json` extension
- Check that templates follow the ARM template schema

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is provided as-is for use with Microsoft Sentinel deployments.

## 🔗 Useful Links

- [Microsoft Sentinel Documentation](https://docs.microsoft.com/azure/sentinel/)
- [ARM Template Reference](https://docs.microsoft.com/azure/templates/)
- [Azure Python SDK](https://docs.microsoft.com/python/api/overview/azure/)
- [GitHub Actions with Azure](https://docs.microsoft.com/azure/developer/github/connect-from-azure)
