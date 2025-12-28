# Deployment Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MICROSOFT SENTINEL DEPLOYMENT FLOW                   │
└─────────────────────────────────────────────────────────────────────────┘

Step 1: USER EXPORTS CONTENT
┌─────────────────────────────────┐
│   Microsoft Sentinel Portal    │
│                                 │
│  ┌───────────────────────────┐  │
│  │  Analytics Rule           │  │
│  │  Workbook                 │  │──────► Export as ARM Template
│  │  Watchlist                │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
           │
           │ Download JSON
           ▼
Step 2: USER UPLOADS TO REPOSITORY
┌─────────────────────────────────┐
│    Code Repository              │
│    (Azure Repos/GitHub)         │
│                                 │
│  templates/                     │
│  ├─ analytics-rules/            │
│  │  └─ my-rule.json     ◄──────┼─── User adds file here
│  ├─ workbooks/                  │
│  └─ watchlists/                 │
└─────────────────────────────────┘
           │
           │ git push
           ▼
Step 3: AZURE DEVOPS PIPELINE TRIGGERED
┌─────────────────────────────────┐
│   Azure DevOps Pipeline         │
│                                 │
│  ┌───────────────────────────┐  │
│  │ 1. Checkout code          │  │
│  │ 2. Authenticate to Azure  │  │
│  │    (Service Connection)   │  │
│  │ 3. Discover templates     │  │
│  │ 4. Deploy using Azure CLI │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
           │
           │ Execute deployment
           ▼
Step 4: AZURE CLI DEPLOYS
┌─────────────────────────────────┐
│   Azure CLI (via AzureCLI@2)    │
│                                 │
│  ┌───────────────────────────┐  │
│  │ • Discover templates      │  │
│  │ • Loop through each file  │  │
│  │ • Deploy ARM template     │  │
│  │ • Validate deployment     │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
           │
           │ Azure SDK API calls
           ▼
Step 5: CONTENT DEPLOYED TO AZURE
┌─────────────────────────────────┐
│   Microsoft Sentinel            │
│                                 │
│  ┌───────────────────────────┐  │
│  │  ✓ Analytics Rule Active  │  │
│  │  ✓ Workbook Available     │  │
│  │  ✓ Watchlist Populated    │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════

AUTHENTICATION FLOW:
────────────────────

Azure DevOps Pipeline ──► Azure Service Connection
                          │
                          ▼
                      Service Principal
                          │
                          ▼
                  Microsoft Sentinel Workspace

═══════════════════════════════════════════════════════════════════════════

FILE ORGANIZATION:
──────────────────

MSFTSentinelContentDeploy/
├── azure-pipelines.yml                   ◄─── Azure DevOps Pipeline definition
│
├── templates/
│   ├── analytics-rules/                   ◄─── Add rule templates here
│   ├── workbooks/                         ◄─── Add workbook templates here
│   └── watchlists/                        ◄─── Add watchlist templates here
│
└── README.md

═══════════════════════════════════════════════════════════════════════════

SUPPORTED CONTENT TYPES:
─────────────────────────

┌──────────────────┬─────────────────────┬──────────────────────────────┐
│  Content Type    │  Directory          │  Resource Type               │
├──────────────────┼─────────────────────┼──────────────────────────────┤
│ Analytics Rules  │ analytics-rules/    │ alertRules (Scheduled)       │
│ Workbooks        │ workbooks/          │ Microsoft.Insights/workbooks │
│ Watchlists       │ watchlists/         │ Watchlists                   │
└──────────────────┴─────────────────────┴──────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
```
