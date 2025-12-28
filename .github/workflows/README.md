# GitHub Actions to Azure DevOps Migration

> **⚠️ DEPRECATED**: This GitHub Actions workflow has been replaced with an Azure DevOps Pipeline.
>
> See `azure-pipelines.yml` in the root directory for the new Azure DevOps pipeline configuration.

## Migration Notice

This repository has been migrated from GitHub Actions to Azure DevOps Pipelines. The GitHub Actions workflow in this directory is kept for reference only and is no longer maintained.

## What Changed

- **Old**: GitHub Actions workflow in `.github/workflows/deploy-sentinel-content.yml`
- **New**: Azure DevOps pipeline in `azure-pipelines.yml`

## Setup Instructions

For setting up the new Azure DevOps pipeline, please refer to:
- [Quick Start Guide](../../QUICKSTART.md)
- [Azure DevOps Setup Guide](../../AZURE_DEVOPS_SETUP.md)
- [Main README](../../README.md)

## Why the Change?

The project has been converted to use Azure DevOps Pipelines instead of GitHub Actions to:
- Better integrate with Azure DevOps workflows
- Use Azure DevOps service connections for authentication
- Leverage Azure DevOps variable groups and environments
- Align with organizational standards

## For GitHub Users

If you prefer to continue using GitHub Actions, you can:
1. Keep the workflow file in this directory
2. Configure the required GitHub secrets (see the workflow file for details)
3. Enable GitHub Actions in your repository settings

Note that the GitHub Actions workflow will not receive updates or support going forward.
