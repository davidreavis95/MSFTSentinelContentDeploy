# Quick Start Guide

Get started with Microsoft Sentinel content deployment in 5 minutes!

## Prerequisites Checklist

- [ ] Azure Subscription with Microsoft Sentinel workspace
- [ ] Azure DevOps organization and project
- [ ] Appropriate permissions to create service connections

## Step 1: Create Azure DevOps Service Connection (2 minutes)

```
1. Go to your Azure DevOps project
2. Navigate to Project Settings → Service connections
3. Click "New service connection" → "Azure Resource Manager"
4. Select "Service principal (automatic)"
5. Configure:
   - Scope: Subscription (or Resource Group)
   - Select your subscription and resource group
   - Connection name: "sentinel-deployer"
6. Grant access to all pipelines
7. Save

# The service principal is automatically created with appropriate permissions
```

## Step 2: Configure Pipeline Variables (1 minute)

In your Azure DevOps project:

1. Go to **Pipelines** → **Library**
2. Create a variable group: **sentinel-deployment-vars**
3. Add these variables:

| Variable Name | Value |
|---------------|-------|
| `AZURE_SERVICE_CONNECTION` | Name of service connection (e.g., "sentinel-deployer") |
| `AZURE_RESOURCE_GROUP` | Resource group name |
| `SENTINEL_WORKSPACE_NAME` | Sentinel workspace name |

Alternatively, you can add these directly to your pipeline as variables.

## Step 3: Create Pipeline (1 minute)

1. In Azure DevOps, go to **Pipelines** → **Create Pipeline**
2. Select your repository source (Azure Repos Git, GitHub, etc.)
3. Choose **Existing Azure Pipelines YAML file**
4. Select `/azure-pipelines.yml`
5. Click **Run** to validate the setup

If using a variable group, link it in the pipeline settings or add to the YAML:
```yaml
variables:
  - group: sentinel-deployment-vars
```

## Step 4: Deploy Your First Content (1 minute)

```bash
# 1. Export ARM template from Sentinel
#    Azure Portal → Sentinel → Analytics → [Your Rule] → Export

# 2. Add to repository
cp ~/Downloads/exported-rule.json templates/analytics-rules/my-rule.json

# 3. Commit and push
git add templates/analytics-rules/my-rule.json
git commit -m "Add my detection rule"
git push

# 4. Watch deployment
#    Azure DevOps → Pipelines → See your deployment run!
```

## That's It! 🎉

Your content is now automatically deployed to Sentinel. Add more templates anytime by repeating Step 4.

## Common Content Types

| Content Type | Export From | Save To |
|--------------|-------------|---------|
| Analytics Rule | Sentinel → Analytics | `templates/analytics-rules/` |
| Workbook | Sentinel → Workbooks | `templates/workbooks/` |
| Watchlist | Sentinel → Watchlists | `templates/watchlists/` |

## Need Help?

- Review [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for advanced usage
- See [templates/README.md](templates/README.md) for template format

## Troubleshooting

**Deployment failed?**
- Check Azure DevOps pipeline logs for errors
- Verify all variables are set correctly
- Ensure service connection has correct permissions

**Authentication error?**
- Confirm service connection is working (test connection in settings)
- Check resource group exists and is accessible
- Verify service principal has access to Sentinel workspace

**Template error?**
- Validate JSON syntax
- Ensure exported from Sentinel correctly
- Check parameter names (should have `workspace`)
