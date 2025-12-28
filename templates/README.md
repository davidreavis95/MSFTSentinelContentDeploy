# Templates Directory

This directory contains ARM templates for Microsoft Sentinel content. The deployment script automatically discovers and deploys all `.json` files in these subdirectories.

## Directory Structure

- **analytics-rules/**: Analytics rules (scheduled queries, detection rules)
- **workbooks/**: Visualization workbooks for security data
- **watchlists/**: Custom watchlists for use in queries and rules

## How to Add New Content

1. **Export from Microsoft Sentinel**:
   - Navigate to your content in the Azure Portal
   - Click "Export" → "ARM Template"
   - Download the JSON file

2. **Add to Repository**:
   - Place the file in the appropriate subdirectory
   - Use a descriptive filename (e.g., `brute-force-detection.json`)
   - Commit and push to trigger deployment

3. **Automatic Deployment**:
   - Azure DevOps Pipeline will automatically deploy your content
   - Monitor the Pipelines tab for deployment status

## Example Templates

Each subdirectory contains example templates to demonstrate the expected format. You can:
- Use them as references for structure
- Delete them after adding your own content
- Keep them for testing purposes

## Template Format

All templates must be valid ARM templates with:
- `$schema` property
- `contentVersion` property
- `parameters` section (typically includes workspace name)
- `resources` section with Sentinel resource definitions

## Notes

- Templates are deployed incrementally (won't delete existing resources)
- Duplicate resource names will update the existing resource
- Ensure parameter names match what the script expects (especially `workspace` or `workspaceName`)
