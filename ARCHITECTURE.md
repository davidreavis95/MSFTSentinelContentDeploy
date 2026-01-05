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
Step 3: CI PIPELINE TRIGGERED
┌─────────────────────────────────┐
│   GitHub Actions / Azure Pipelines│
│                                 │
│  ┌───────────────────────────┐  │
│  │ 1. Checkout code          │  │
│  │ 2. Setup Python 3.11      │  │
│  │ 3. Install dependencies   │  │
│  │ 4. Azure Login (OIDC or   │  │
│  │    Service Connection)    │  │
│  │ 5. Run deploy script      │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
           │
           │ Execute deployment
           ▼
Step 4: PYTHON SCRIPT DEPLOYS
┌─────────────────────────────────┐
│   deploy_sentinel_content.py    │
│                                 │
│  ┌───────────────────────────┐  │
│  │ • Discover templates      │  │
│  │ • Load ARM templates      │  │
│  │ • Prepare parameters      │  │
│  │ • Deploy to Azure         │  │
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
├── scripts/
│   └── deploy_sentinel_content.py         ◄─── Deployment logic
│
└── requirements.txt                       ◄─── Python dependencies

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
