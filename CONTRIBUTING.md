# Contributing Guide

Thank you for using the Microsoft Sentinel Content Deployment solution! This guide will help you effectively use and contribute to this project.

## Quick Start for End Users

### Adding New Sentinel Content

1. **Export your content from Microsoft Sentinel**:
   ```
   Azure Portal → Sentinel Workspace → [Your Content Type] → Export → ARM Template
   ```

2. **Save the template file**:
   - Analytics Rules → `templates/analytics-rules/your-rule-name.json`
   - Workbooks → `templates/workbooks/your-workbook-name.json`
   - Watchlists → `templates/watchlists/your-watchlist-name.json`

3. **Commit and push**:
   ```bash
   git add templates/
   git commit -m "Add [description of content]"
   git push
   ```

4. **Monitor deployment**:
   - Go to the "Pipelines" tab in Azure DevOps
   - Watch your deployment progress
   - Check for any errors

### Best Practices

1. **Naming Convention**:
   - Use descriptive, lowercase filenames
   - Separate words with hyphens
   - Example: `failed-login-attempts-rule.json`

2. **One Resource Per File**:
   - Keep each template focused on a single resource
   - Makes troubleshooting easier
   - Enables selective deployments

3. **Test Before Committing**:
   - Validate JSON syntax
   - Ensure template has required parameters
   - Review the query/configuration

4. **Documentation**:
   - Add comments in commit messages
   - Describe what the rule/workbook does
   - Note any dependencies

## Advanced Usage

### Manual Deployment

Test ARM template deployments locally using Azure CLI:

```bash
# Set environment variables
export AZURE_RESOURCE_GROUP="xxx"
export SENTINEL_WORKSPACE_NAME="xxx"

# Authenticate
az login

# Deploy a single template
az deployment group create \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --name "test-deployment" \
  --template-file templates/analytics-rules/your-rule.json \
  --parameters workspace="$SENTINEL_WORKSPACE_NAME" \
  --mode Incremental
```

### Working with BICEP

While the solution uses ARM templates, you can also work with BICEP:

1. **Write in BICEP**:
   ```bicep
   // my-rule.bicep
   resource analyticsRule 'Microsoft.OperationalInsights/workspaces/providers/alertRules@2023-02-01-preview' = {
     name: '${workspace}/Microsoft.SecurityInsights/MyRule'
     kind: 'Scheduled'
     properties: {
       displayName: 'My Custom Rule'
       // ... other properties
     }
   }
   ```

2. **Convert to ARM**:
   ```bash
   az bicep build --file my-rule.bicep --outfile templates/analytics-rules/my-rule.json
   ```

3. **Commit the generated JSON**:
   ```bash
   git add templates/analytics-rules/my-rule.json
   git commit -m "Add my custom rule"
   git push
   ```

## Troubleshooting

### Deployment Fails

1. **Check Azure DevOps Pipeline logs**:
   - Pipelines tab → Select failed run
   - Review error messages

2. **Common issues**:
   - Invalid JSON syntax
   - Missing required parameters
   - Insufficient permissions
   - API version mismatch
   - Service connection not configured properly

3. **Validation**:
   ```bash
   # Validate JSON syntax using jq
   jq . templates/analytics-rules/your-file.json
   
   # Or using Python
   python -m json.tool templates/analytics-rules/your-file.json
   
   # Validate ARM template using Azure CLI
   az deployment group validate \
     --resource-group "$AZURE_RESOURCE_GROUP" \
     --template-file templates/analytics-rules/your-file.json \
     --parameters workspace="$SENTINEL_WORKSPACE_NAME"
   ```

### Authentication Issues

- Verify all pipeline variables are set correctly
- Check service connection is working (test in Azure DevOps settings)
- Ensure service principal has proper permissions on the resource group

## Contributing to the Project

### Reporting Issues

- Use the repository's issue tracking system to report bugs
- Include error messages and logs
- Describe steps to reproduce

### Suggesting Enhancements

- Open an issue describing the enhancement
- Explain the use case
- Provide examples if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with clear description

## Code Structure

The deployment logic is contained in the Azure DevOps pipeline (`azure-pipelines.yml`):

```
azure-pipelines.yml
└── Deploy Stage
    └── DeployContent Job
        └── AzureCLI@2 Task (PowerShell script)
            ├── Discover Analytics Rules templates
            ├── Deploy Analytics Rules using az deployment
            ├── Discover Workbooks templates
            ├── Deploy Workbooks using az deployment
            ├── Discover Watchlists templates
            └── Deploy Watchlists using az deployment
```

The pipeline uses Azure CLI's `az deployment group create` command to deploy each ARM template.

## Support

For questions and support:
- Review the main README.md
- Check existing GitHub Issues
- Consult Microsoft Sentinel documentation

## Additional Resources

- [ARM Template Best Practices](https://docs.microsoft.com/azure/azure-resource-manager/templates/best-practices)
- [Sentinel API Reference](https://docs.microsoft.com/rest/api/securityinsights/)
- [KQL Query Language](https://docs.microsoft.com/azure/data-explorer/kusto/query/)
