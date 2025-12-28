# Quick Start Guide

Get started with Microsoft Sentinel content deployment in 5 minutes!

## Prerequisites Checklist

- [ ] Azure Subscription with Microsoft Sentinel workspace
- [ ] Service Principal with Sentinel Contributor role
- [ ] GitHub repository forked or cloned

## Step 1: Create Service Principal (2 minutes)

```bash
# Login to Azure
az login

# Create service principal
az ad sp create-for-rbac \
  --name "sentinel-deployer" \
  --role "Microsoft Sentinel Contributor" \
  --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP

# Save the output - you'll need it for GitHub secrets!
```

## Step 2: Configure GitHub Secrets (1 minute)

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** for each:

| Secret Name | Value |
|-------------|-------|
| `AZURE_CLIENT_ID` | From service principal output |
| `AZURE_TENANT_ID` | From service principal output |
| `AZURE_SUBSCRIPTION_ID` | Your Azure subscription ID |
| `AZURE_RESOURCE_GROUP` | Resource group name |
| `SENTINEL_WORKSPACE_NAME` | Sentinel workspace name |

## Step 3: Configure Federated Credentials (1 minute)

1. Go to **Azure Portal** → **Azure Active Directory** → **App registrations**
2. Find your service principal → **Certificates & secrets** → **Federated credentials**
3. Add credential:
   - **Scenario**: GitHub Actions
   - **Organization**: Your GitHub username
   - **Repository**: Your repo name
   - **Entity**: Branch
   - **Branch name**: main

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
#    GitHub → Actions tab → See your deployment run!
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
- Check GitHub Actions logs for errors
- Verify all secrets are set correctly
- Ensure service principal has correct permissions

**Authentication error?**
- Confirm federated credentials are configured
- Check client ID, tenant ID match
- Verify repository name is exact

**Template error?**
- Validate JSON syntax
- Ensure exported from Sentinel correctly
- Check parameter names (should have `workspace`)
