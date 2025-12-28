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

Run the deployment script locally for testing:

```bash
# Set environment variables
export AZURE_SUBSCRIPTION_ID="xxx"
export AZURE_RESOURCE_GROUP="xxx"
export SENTINEL_WORKSPACE_NAME="xxx"

# Authenticate
az login

# Run deployment
python scripts/deploy_sentinel_content.py
```

### Custom Template Directory

Use a different templates directory:

```bash
export TEMPLATES_DIR="custom-templates"
python scripts/deploy_sentinel_content.py
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
   # Validate JSON syntax
   python -m json.tool templates/analytics-rules/your-file.json
   
   # Or use jq
   jq . templates/analytics-rules/your-file.json
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

```
scripts/deploy_sentinel_content.py
├── SentinelContentDeployer class
│   ├── discover_templates()    # Find all ARM templates
│   ├── load_template()         # Parse JSON files
│   ├── prepare_parameters()    # Set up deployment parameters
│   ├── deploy_template()       # Deploy single template
│   └── deploy_all()            # Deploy all discovered templates
└── main()                      # Entry point
```

## Support

For questions and support:
- Review the main README.md
- Check existing GitHub Issues
- Consult Microsoft Sentinel documentation

## Additional Resources

- [ARM Template Best Practices](https://docs.microsoft.com/azure/azure-resource-manager/templates/best-practices)
- [Sentinel API Reference](https://docs.microsoft.com/rest/api/securityinsights/)
- [KQL Query Language](https://docs.microsoft.com/azure/data-explorer/kusto/query/)
