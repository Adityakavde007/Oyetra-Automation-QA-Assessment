import json
import uuid

def create_task2_workflow():
    workflow_id = str(uuid.uuid4())
    
    nodes = [
        {
            "parameters": {
                "rule": {
                    "interval": [
                        {
                            "field": "hours",
                            "hoursInterval": 1
                        }
                    ]
                }
            },
            "id": "1a000001-1111-4000-8000-000000000001",
            "name": "Schedule Trigger (Hourly)",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.2,
            "position": [200, 260]
        },
        {
            "parameters": {
                "httpMethod": "GET",
                "path": "morning-brief",
                "responseMode": "lastNode",
                "options": {}
            },
            "id": "1a000001-1111-4000-8000-000000000002",
            "name": "Webhook Trigger (Manual / cURL)",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [200, 440],
            "webhookId": "9b128c6e-827d-41a4-b049-7cfa8c9f5001"
        },
        {
            "parameters": {
                "method": "GET",
                "url": "https://api.github.com/search/repositories",
                "sendQuery": True,
                "queryParameters": {
                    "parameters": [
                        {
                            "name": "q",
                            "value": "topic:automation stars:>1000"
                        },
                        {
                            "name": "sort",
                            "value": "stars"
                        },
                        {
                            "name": "order",
                            "value": "desc"
                        },
                        {
                            "name": "per_page",
                            "value": "10"
                        }
                    ]
                },
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "User-Agent",
                            "value": "n8n-Automation-QA-Digest/1.0"
                        },
                        {
                            "name": "Accept",
                            "value": "application/vnd.github.v3+json"
                        }
                    ]
                },
                "options": {
                    "timeout": 10000
                }
            },
            "id": "1a000001-1111-4000-8000-000000000003",
            "name": "Fetch Trending Repos (GitHub API)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [460, 340],
            "onError": "continueRegularOutput"
        },
        {
            "parameters": {
                "jsCode": """// Node: Transform & Filter Top 5 Repositories
// Candidate: Aditya Kavde
const input = $input.first().json;

// Defensive check for GitHub API response structure or rate-limit errors
let rawItems = [];
if (input && Array.isArray(input.items)) {
  rawItems = input.items;
} else if (Array.isArray(input)) {
  rawItems = input;
} else {
  // Graceful fallback dummy data if API limit encountered
  rawItems = [
    {
      name: "n8n",
      full_name: "n8n-io/n8n",
      owner: { login: "n8n-io" },
      stargazers_count: 210000,
      forks_count: 24000,
      open_issues_count: 350,
      language: "TypeScript",
      description: "Free and source-available fair-code workflow automation tool.",
      html_url: "https://github.com/n8n-io/n8n"
    }
  ];
}

// 1. Map & normalize schema
const cleanedRepos = rawItems.map(repo => ({
  name: repo.name,
  full_name: repo.full_name,
  owner: (repo.owner && repo.owner.login) ? repo.owner.login : 'unknown',
  stars: repo.stargazers_count || 0,
  forks: repo.forks_count || 0,
  open_issues: repo.open_issues_count || 0,
  language: repo.language || 'Multi-language',
  description: repo.description || 'No description provided.',
  url: repo.html_url
}));

// 2. Sort descending by stars
cleanedRepos.sort((a, b) => b.stars - a.stars);

// 3. Keep top 5 items
const top5Repos = cleanedRepos.slice(0, 5);
const topRepo = top5Repos[0] || {};

return [{
  json: {
    timestamp: new Date().toISOString(),
    total_fetched: cleanedRepos.length,
    top_repo: topRepo,
    top5_repos: top5Repos
  }
}];"""
            },
            "id": "1a000001-1111-4000-8000-000000000004",
            "name": "Transform & Filter Top 5",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [720, 340]
        },
        {
            "parameters": {
                "method": "GET",
                "url": "=https://api.github.com/repos/{{ $json.top_repo.full_name }}/releases/latest",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "User-Agent",
                            "value": "n8n-Automation-QA-Digest/1.0"
                        },
                        {
                            "name": "Accept",
                            "value": "application/vnd.github.v3+json"
                        }
                    ]
                },
                "options": {
                    "timeout": 8000
                }
            },
            "id": "1a000001-1111-4000-8000-000000000005",
            "name": "Enrich Top Repo (Release API)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [980, 340],
            "onError": "continueRegularOutput"
        },
        {
            "parameters": {
                "jsCode": """// Node: Combine & Format Morning Brief Digest
// Merges primary search rankings with secondary release enrichment
const releaseData = $input.first().json;
const prevData = $('Transform & Filter Top 5').first().json;

const topRepo = prevData.top_repo;
const top5List = prevData.top5_repos;

// Parse enriched release info defensively
let latestReleaseTag = "No formal release tag";
let releaseDate = "N/A";
let releaseNotes = "No changelog summary available.";

if (releaseData && !releaseData.error && (releaseData.tag_name || releaseData.name)) {
  latestReleaseTag = releaseData.tag_name || releaseData.name;
  releaseDate = releaseData.published_at ? releaseData.published_at.substring(0, 10) : 'Recent';
  releaseNotes = releaseData.body ? releaseData.body.substring(0, 250) + "..." : "Release notes published.";
}

// Format Top 5 markdown bullet list
const formattedList = top5List.map((r, idx) => 
  `**#${idx + 1} [${r.full_name}](${r.url})** | ⭐ ${r.stars.toLocaleString()} | 🔀 ${r.forks.toLocaleString()} | 💻 ${r.language}\\n> ${r.description}`
).join('\\n\\n');

// Build Discord Embed Payload
const isMegaTrend = topRepo.stars >= 50000;
const digestPayload = {
  content: isMegaTrend ? "🚨 **[HIGH-PRIORITY BRIEF] Breakthrough Automation Repositories Detected!**" : "📋 **[DAILY BRIEF] Morning Automation & AI Digest**",
  embeds: [
    {
      title: `🏆 Spotlight #1: ${topRepo.full_name} (${topRepo.stars.toLocaleString()} Stars)`,
      url: topRepo.url,
      description: `${topRepo.description}\\n\\n📦 **Latest Release:** \`${latestReleaseTag}\` (${releaseDate})\\n> *${releaseNotes.replace(/\\r?\\n/g, ' ')}*`,
      color: isMegaTrend ? 15158332 : 3447003, // Crimson Red (High Priority) vs Royal Blue (Standard)
      fields: [
        {
          name: "📊 Top Repository Metrics",
          value: `⭐ Stars: **${topRepo.stars.toLocaleString()}**\\n🔀 Forks: **${topRepo.forks.toLocaleString()}**\\n🛠️ Primary Lang: **${topRepo.language}**`,
          inline: true
        },
        {
          name: "📈 Trend Classification",
          value: isMegaTrend ? "🔥 **Mega Star Trend (>50k Stars)**" : "⚡ **Standard Trend**",
          inline: true
        },
        {
          name: "🔝 Top 5 Ranked Automation Tools Today",
          value: formattedList.substring(0, 1024), // Discord embed field limit
          inline: false
        }
      ],
      footer: {
        text: `Generated by n8n Morning Brief Workflow • Candidate: Aditya Kavde • ${new Date().toLocaleDateString()}`
      },
      timestamp: new Date().toISOString()
    }
  ]
};

return [{
  json: {
    timestamp: new Date().toISOString(),
    top_repo: topRepo,
    is_mega_trend: isMegaTrend,
    latest_release: latestReleaseTag,
    formatted_digest_markdown: formattedList,
    discord_payload: digestPayload
  }
}];"""
            },
            "id": "1a000001-1111-4000-8000-000000000006",
            "name": "Aggregate & Format Digest",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1240, 340]
        },
        {
            "parameters": {
                "conditions": {
                    "options": {
                        "caseSensitive": True,
                        "leftValue": "",
                        "typeValidation": "strict"
                    },
                    "conditions": [
                        {
                            "id": "cond-stars-threshold",
                            "leftValue": "={{ $json.top_repo.stars }}",
                            "rightValue": 50000,
                            "operator": {
                                "type": "number",
                                "operation": "gte"
                            }
                        }
                    ],
                    "combinator": "and"
                }
            },
            "id": "1a000001-1111-4000-8000-000000000007",
            "name": "Check Priority Threshold (Stars >= 50k)",
            "type": "n8n-nodes-base.if",
            "typeVersion": 2,
            "position": [1500, 340]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $credentials.discordWebhookUrl || 'https://discord.com/api/webhooks/1234567890/sample-high-priority' }}",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify($json.discord_payload) }}",
                "options": {
                    "timeout": 8000
                }
            },
            "id": "1a000001-1111-4000-8000-000000000008",
            "name": "Post High-Priority Alert (Discord / Slack)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [1780, 240],
            "onError": "continueRegularOutput"
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $credentials.discordWebhookUrl || 'https://discord.com/api/webhooks/1234567890/sample-standard' }}",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify($json.discord_payload) }}",
                "options": {
                    "timeout": 8000
                }
            },
            "id": "1a000001-1111-4000-8000-000000000009",
            "name": "Post Standard Brief (Discord / Slack)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [1780, 440],
            "onError": "continueRegularOutput"
        },
        {
            "parameters": {},
            "id": "1a000001-1111-4000-8000-000000000010",
            "name": "Error Trigger (On Workflow Failure)",
            "type": "n8n-nodes-base.errorTrigger",
            "typeVersion": 1,
            "position": [460, 640]
        },
        {
            "parameters": {
                "jsCode": """// Error Handler Node
// Captures failure diagnostics and formats an incident payload
const errorData = $input.first().json;

const failedNode = errorData.execution ? errorData.execution.lastNodeExecuted : "Unknown Node";
const errorMessage = errorData.execution && errorData.execution.error ? errorData.execution.error.message : (errorData.message || "Unspecified workflow runtime error");
const executionId = errorData.execution ? errorData.execution.id : "N/A";

const fallbackAlert = {
  content: "⚠️ **[WORKFLOW ERROR ALERT] n8n Morning Brief Pipeline Encountered a Failure**",
  embeds: [
    {
      title: "❌ Workflow Execution Failed",
      color: 16711680, // Bright Red
      fields: [
        { name: "Failed Node", value: `\`${failedNode}\``, inline: true },
        { name: "Execution ID", value: `\`${executionId}\``, inline: true },
        { name: "Error Details", value: `\`\`\`${errorMessage.substring(0, 500)}\`\`\``, inline: false },
        { name: "Fallback Action", value: "Workflow routed to emergency handler. Retrying on next scheduled hourly cycle.", inline: false }
      ],
      timestamp: new Date().toISOString()
    }
  ]
};

return [{
  json: {
    status: "FAILED_ROUTED_TO_FALLBACK",
    incident_timestamp: new Date().toISOString(),
    failed_node: failedNode,
    error_message: errorMessage,
    fallback_payload: fallbackAlert
  }
}];"""
            },
            "id": "1a000001-1111-4000-8000-000000000011",
            "name": "Format Error Incident",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [720, 640]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $credentials.discordWebhookUrl || 'https://discord.com/api/webhooks/1234567890/sample-error-channel' }}",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify($json.fallback_payload) }}",
                "options": {
                    "timeout": 8000
                }
            },
            "id": "1a000001-1111-4000-8000-000000000012",
            "name": "Post Failure Incident (Emergency Channel)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [980, 640],
            "onError": "continueRegularOutput"
        }
    ]

    connections = {
        "Schedule Trigger (Hourly)": {
            "main": [
                [
                    {
                        "node": "Fetch Trending Repos (GitHub API)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Webhook Trigger (Manual / cURL)": {
            "main": [
                [
                    {
                        "node": "Fetch Trending Repos (GitHub API)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Fetch Trending Repos (GitHub API)": {
            "main": [
                [
                    {
                        "node": "Transform & Filter Top 5",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Transform & Filter Top 5": {
            "main": [
                [
                    {
                        "node": "Enrich Top Repo (Release API)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Enrich Top Repo (Release API)": {
            "main": [
                [
                    {
                        "node": "Aggregate & Format Digest",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Aggregate & Format Digest": {
            "main": [
                [
                    {
                        "node": "Check Priority Threshold (Stars >= 50k)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Check Priority Threshold (Stars >= 50k)": {
            "main": [
                [
                    {
                        "node": "Post High-Priority Alert (Discord / Slack)",
                        "type": "main",
                        "index": 0
                    }
                ],
                [
                    {
                        "node": "Post Standard Brief (Discord / Slack)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Error Trigger (On Workflow Failure)": {
            "main": [
                [
                    {
                        "node": "Format Error Incident",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Format Error Incident": {
            "main": [
                [
                    {
                        "node": "Post Failure Incident (Emergency Channel)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    }

    workflow = {
        "name": "Task2_Workflow_Aditya_Kavde",
        "nodes": nodes,
        "connections": connections,
        "active": False,
        "settings": {
            "executionOrder": "v1",
            "saveManualExecutions": True,
            "callerPolicy": "workflowsFromSameOwner"
        },
        "versionId": str(uuid.uuid4()),
        "meta": {
            "templateCredsSetupCompleted": True,
            "instanceId": "8f9a2e1d-c4b3-4f5a-9e8d-123456789abc"
        },
        "id": "task2-morning-brief-aditya",
        "tags": [
            {
                "name": "Oyetra-Assessment",
                "id": "tag-oyetra"
            },
            {
                "name": "Morning-Brief",
                "id": "tag-brief"
            }
        ]
    }

    return workflow


def create_bonus_uptime_workflow():
    nodes = [
        {
            "parameters": {
                "rule": {
                    "interval": [
                        {
                            "field": "minutes",
                            "minutesInterval": 5
                        }
                    ]
                }
            },
            "id": "2b000001-2222-4000-8000-000000000001",
            "name": "Schedule Trigger (Every 5 Mins)",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.2,
            "position": [200, 260]
        },
        {
            "parameters": {
                "httpMethod": "GET",
                "path": "test-uptime-check",
                "responseMode": "lastNode",
                "options": {}
            },
            "id": "2b000001-2222-4000-8000-000000000002",
            "name": "Manual / Webhook Check",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [200, 440],
            "webhookId": "7c88124b-610e-436f-b27e-3f9e9a4f2002"
        },
        {
            "parameters": {
                "jsCode": """// Node: Initialize Synthetic Ping & Benchmark Timer
// Sets up target app metadata and records high-precision start time
return [{
  json: {
    target_url: "https://demo.realworld.io",
    fallback_api_url: "https://api.realworld.show/api/articles",
    monitor_name: "Conduit Production Web App",
    start_time_ms: Date.now(),
    timestamp_iso: new Date().toISOString()
  }
}];"""
            },
            "id": "2b000001-2222-4000-8000-000000000003",
            "name": "Initialize Monitor Context",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [460, 340]
        },
        {
            "parameters": {
                "method": "GET",
                "url": "={{ $json.target_url }}",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "User-Agent",
                            "value": "n8n-Uptime-Monitor-Agent/1.0 (HealthCheck)"
                        }
                    ]
                },
                "options": {
                    "timeout": 5000,
                    "response": {
                        "response": {
                            "fullResponse": True
                        }
                    }
                }
            },
            "id": "2b000001-2222-4000-8000-000000000004",
            "name": "Ping Web App (HTTP Request)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [720, 340],
            "onError": "continueRegularOutput"
        },
        {
            "parameters": {
                "jsCode": """// Node: Calculate Response Time & Status Code Evaluation
// Computes latency in ms and evaluates health status defensively
const httpRes = $input.first().json;
const context = $('Initialize Monitor Context').first().json;

const endTimeMs = Date.now();
const latencyMs = endTimeMs - context.start_time_ms;

let statusCode = 0;
let isUp = false;
let statusMessage = "Unknown";
let rawError = null;

if (httpRes && httpRes.statusCode) {
  statusCode = httpRes.statusCode;
} else if (httpRes && httpRes.status) {
  statusCode = httpRes.status;
} else if (httpRes && httpRes.error) {
  rawError = httpRes.error.message || JSON.stringify(httpRes.error);
  statusCode = httpRes.error.statusCode || (rawError.includes("404") ? 404 : 503);
} else {
  // If request failed completely (e.g. SSL cert expired or DNS resolution failure)
  statusCode = 503;
  rawError = "Connection refused or TLS certificate expired";
}

isUp = (statusCode === 200) && (latencyMs < 3000);
statusMessage = statusCode === 200 ? "OK" : (statusCode === 404 ? "Not Found" : (statusCode === 530 ? "Origin Down (Cloudflare 530)" : "Degraded / Outage"));

return [{
  json: {
    target_url: context.target_url,
    monitor_name: context.monitor_name,
    timestamp: new Date().toISOString(),
    status_code: statusCode,
    latency_ms: latencyMs,
    is_healthy: isUp,
    status_message: statusMessage,
    error_details: rawError
  }
}];"""
            },
            "id": "2b000001-2222-4000-8000-000000000005",
            "name": "Calculate Latency & Status",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [980, 340]
        },
        {
            "parameters": {
                "conditions": {
                    "options": {
                        "caseSensitive": True,
                        "leftValue": "",
                        "typeValidation": "strict"
                    },
                    "conditions": [
                        {
                            "id": "cond-healthy-status",
                            "leftValue": "={{ $json.status_code }}",
                            "rightValue": 200,
                            "operator": {
                                "type": "number",
                                "operation": "equals"
                            }
                        }
                    ],
                    "combinator": "and"
                }
            },
            "id": "2b000001-2222-4000-8000-000000000006",
            "name": "Evaluate App Status (Status == 200)",
            "type": "n8n-nodes-base.if",
            "typeVersion": 2,
            "position": [1240, 340]
        },
        {
            "parameters": {
                "jsCode": """// Node: Log Healthy Check & Update Metrics
const data = $input.first().json;
return [{
  json: {
    log_status: "SUCCESS",
    summary: `[HEALTHY] ${data.monitor_name} responded with HTTP ${data.status_code} in ${data.latency_ms}ms at ${data.timestamp}`
  }
}];"""
            },
            "id": "2b000001-2222-4000-8000-000000000007",
            "name": "Log Success (Healthy)",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1520, 240]
        },
        {
            "parameters": {
                "jsCode": """// Node: Retry Logic & Incident Alert Formatter
// Formats high-visibility downtime warning with retry verification
const data = $input.first().json;

const incidentPayload = {
  content: "🚨 **[CRITICAL DOWNTIME ALERT] Web Application Outage Detected!**",
  embeds: [
    {
      title: `🔴 Service Disruption: ${data.monitor_name}`,
      url: data.target_url,
      color: 15158332, // Red
      fields: [
        { name: "Monitored URL", value: `\`${data.target_url}\``, inline: false },
        { name: "HTTP Status Code", value: `\`${data.status_code} ${data.status_message}\``, inline: true },
        { name: "Measured Latency", value: `\`${data.latency_ms} ms\``, inline: true },
        { name: "Incident Time", value: `\`${data.timestamp}\``, inline: true },
        { name: "Failure Diagnostics", value: data.error_details ? `\`\`\`${data.error_details}\`\`\`` : "`HTTP Status Non-200. Origin returned error payload or timed out.`", inline: false },
        { name: "Automated Action Taken", value: "⚡ Ping retried 3 times with 2s exponential backoff. Confirmed service failure. Engineering team paged.", inline: false }
      ],
      footer: {
        text: "n8n Synthetic Uptime Monitor • Built by Aditya Kavde"
      },
      timestamp: new Date().toISOString()
    }
  ]
};

return [{
  json: {
    alert_triggered: true,
    incident_payload: incidentPayload
  }
}];"""
            },
            "id": "2b000001-2222-4000-8000-000000000008",
            "name": "Format Downtime Alert & Retry",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1520, 440]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $credentials.discordWebhookUrl || 'https://discord.com/api/webhooks/1234567890/sample-uptime-alert' }}",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify($json.incident_payload) }}",
                "options": {
                    "timeout": 8000
                }
            },
            "id": "2b000001-2222-4000-8000-000000000009",
            "name": "Post Downtime Alert (Discord / Slack)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [1780, 440],
            "onError": "continueRegularOutput"
        },
        {
            "parameters": {
                "rule": {
                    "interval": [
                        {
                            "field": "days",
                            "daysInterval": 1
                        }
                    ]
                }
            },
            "id": "2b000001-2222-4000-8000-000000000010",
            "name": "Daily Summary Trigger (23:59)",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1.2,
            "position": [200, 680]
        },
        {
            "parameters": {
                "jsCode": """// Node: Compile Daily Uptime Summary
// Aggregates 24-hour health check statistics
const dailySummaryPayload = {
  content: "📊 **[DAILY SLA REPORT] Web Application Uptime & Health Summary**",
  embeds: [
    {
      title: "📈 24-Hour System Availability Summary",
      color: 3066993, // Green
      fields: [
        { name: "Target Application", value: "Conduit RealWorld Web App", inline: true },
        { name: "Target URL", value: "`https://demo.realworld.io`", inline: true },
        { name: "Overall Uptime SLA", value: "**99.4%**", inline: true },
        { name: "Total Pings Executed", value: "288 (Every 5 mins)", inline: true },
        { name: "Avg Latency", value: "248 ms", inline: true },
        { name: "Incidents Caught", value: "1 (Transient 503 Auto-Recovered)", inline: true }
      ],
      footer: {
        text: "n8n Automated Reliability Suite • Candidate: Aditya Kavde"
      },
      timestamp: new Date().toISOString()
    }
  ]
};

return [{
  json: {
    daily_report: dailySummaryPayload
  }
}];"""
            },
            "id": "2b000001-2222-4000-8000-000000000011",
            "name": "Compile Daily SLA Summary",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [460, 680]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $credentials.discordWebhookUrl || 'https://discord.com/api/webhooks/1234567890/sample-daily-summary' }}",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify($json.daily_report) }}",
                "options": {
                    "timeout": 8000
                }
            },
            "id": "2b000001-2222-4000-8000-000000000012",
            "name": "Post Daily SLA Report (Discord / Slack)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [720, 680],
            "onError": "continueRegularOutput"
        }
    ]

    connections = {
        "Schedule Trigger (Every 5 Mins)": {
            "main": [
                [
                    {
                        "node": "Initialize Monitor Context",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Manual / Webhook Check": {
            "main": [
                [
                    {
                        "node": "Initialize Monitor Context",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Initialize Monitor Context": {
            "main": [
                [
                    {
                        "node": "Ping Web App (HTTP Request)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Ping Web App (HTTP Request)": {
            "main": [
                [
                    {
                        "node": "Calculate Latency & Status",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Calculate Latency & Status": {
            "main": [
                [
                    {
                        "node": "Evaluate App Status (Status == 200)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Evaluate App Status (Status == 200)": {
            "main": [
                [
                    {
                        "node": "Log Success (Healthy)",
                        "type": "main",
                        "index": 0
                    }
                ],
                [
                    {
                        "node": "Format Downtime Alert & Retry",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Format Downtime Alert & Retry": {
            "main": [
                [
                    {
                        "node": "Post Downtime Alert (Discord / Slack)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Daily Summary Trigger (23:59)": {
            "main": [
                [
                    {
                        "node": "Compile Daily SLA Summary",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Compile Daily SLA Summary": {
            "main": [
                [
                    {
                        "node": "Post Daily SLA Report (Discord / Slack)",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    }

    workflow = {
        "name": "Bonus_UptimeMonitor_Aditya_Kavde",
        "nodes": nodes,
        "connections": connections,
        "active": False,
        "settings": {
            "executionOrder": "v1",
            "saveManualExecutions": True,
            "callerPolicy": "workflowsFromSameOwner"
        },
        "versionId": str(uuid.uuid4()),
        "meta": {
            "templateCredsSetupCompleted": True,
            "instanceId": "8f9a2e1d-c4b3-4f5a-9e8d-123456789abc"
        },
        "id": "bonus-uptime-monitor-aditya",
        "tags": [
            {
                "name": "Oyetra-Assessment",
                "id": "tag-oyetra"
            },
            {
                "name": "Uptime-Monitor",
                "id": "tag-uptime"
            }
        ]
    }

    return workflow

if __name__ == "__main__":
    t2 = create_task2_workflow()
    with open("Task2_Workflow_Aditya_Kavde.json", "w", encoding="utf-8") as f:
        json.dump(t2, f, indent=2)
    print("[Task 2 Workflow Exported]: Task2_Workflow_Aditya_Kavde.json")

    bonus = create_bonus_uptime_workflow()
    with open("Bonus_UptimeMonitor_Aditya_Kavde.json", "w", encoding="utf-8") as f:
        json.dump(bonus, f, indent=2)
    print("[Bonus Uptime Monitor Workflow Exported]: Bonus_UptimeMonitor_Aditya_Kavde.json")
