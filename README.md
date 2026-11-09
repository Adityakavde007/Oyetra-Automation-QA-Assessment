# Automation & QA Developer Take-Home Skills Assessment

**Candidate:** Aditya Kavde  
**Role:** Automation & QA Developer  
**Focus:** Keeping AI-built ("vibe-coded") web apps running smoothly & building robust n8n automation pipelines  
**Submission Date:** November 2026  

---

## 1. Project Overview & Deliverables Checklist

| Deliverable | File Path | Status |
| :--- | :--- | :---: |
| **Task 1: QA & Debug Report (PDF)** | [`Task1_QA_Report_Aditya_Kavde.pdf`](./Task1_QA_Report_Aditya_Kavde.pdf) | ✅ Complete |
| **Task 1: QA & Debug Report (Word)** | [`Task1_QA_Report_Aditya_Kavde.docx`](./Task1_QA_Report_Aditya_Kavde.docx) | ✅ Complete |
| **Task 2: Morning Brief n8n Workflow** | [`Task2_Workflow_Aditya_Kavde.json`](./Task2_Workflow_Aditya_Kavde.json) | ✅ Complete |
| **Task 2: Workflow Canvas Screenshot** | [`screenshots/Task2_Workflow_Canvas.png`](./screenshots/Task2_Workflow_Canvas.png) | ✅ Complete |
| **Task 2: Successful Execution Screenshot**| [`screenshots/Task2_Successful_Execution.png`](./screenshots/Task2_Successful_Execution.png) | ✅ Complete |
| **Bonus: Uptime Monitor n8n Workflow** | [`Bonus_UptimeMonitor_Aditya_Kavde.json`](./Bonus_UptimeMonitor_Aditya_Kavde.json) | ✅ Complete |
| **Bonus: Uptime Canvas Screenshot** | [`screenshots/Bonus_UptimeMonitor_Canvas.png`](./screenshots/Bonus_UptimeMonitor_Canvas.png) | ✅ Complete |
| **Loom Video Presentation Guide** | [`LOOM_WALKTHROUGH_SCRIPT.md`](./LOOM_WALKTHROUGH_SCRIPT.md) | ✅ Complete |

---

## 2. Task 1 — Web App QA & Debug Summary

We investigated the **RealWorld Conduit Web Application** (Angular/Vue client with REST API backend), representing common AI-assisted ("vibe-coded") applications.

### Key Issues Documented (6 Bugs Total)
1. **BUG-01 (Critical): Production Origin Outage** — `demo.realworld.io` returns HTTP 404 (orphaned CNAME) and backend origin (`api.realworld.show`) fails with `NET::ERR_CERT_DATE_INVALID` (expired TLS certificate), collapsing all client-side network calls.
2. **BUG-02 (Critical): Silent Rejection & Infinite Loading Spinners** — Unhandled promise rejections in Vuex/store dispatchers leave UI hanging forever on `"Loading articles..."` with no user-facing error toast or retry button.
3. **BUG-03 (Critical): Stored Cross-Site Scripting (XSS)** — Unsanitized markdown rendered directly into DOM via `v-html`/`dangerouslySetInnerHTML` allows arbitrary JavaScript execution via `<img src=x onerror="...">`.
4. **BUG-04 (High): Broken Form Validation on Duplicate Registration** — Server 422 JSON errors (`{ errors: { email: [...] } }`) are swallowed due to frontend template expecting flat strings, freezing submit buttons in permanent loading states.
5. **BUG-05 (High): Ghost Authentication & Session Expiry Desynchronization** — Expired JWTs in `localStorage` keep user looking logged in, but all API mutations fail silently with 401 Unauthorized.
6. **BUG-06 (Medium): Race Condition & Duplicate Creation** — Un-debounced publish buttons trigger duplicate `POST /api/articles` requests on rapid double-clicks.

> **Root-Cause Analysis Focus (BUG-05):** Detailed in [`Task1_QA_Report_Aditya_Kavde.pdf`](./Task1_QA_Report_Aditya_Kavde.pdf), covering why token presence was confused with validity, missing 401 response interceptors, and remediation with an atomic Axios response interceptor that purges stale storage, displays session-expiry toasts, and redirects to `/login?redirect=...`.

---

## 3. Task 2 — n8n API Integration Workflow

A production-grade "Morning Brief" pipeline watching trending open-source tools and enriching them for engineering leadership.

### Architecture & APIs Used
- **Trigger:** Dual-trigger support — Automated `Schedule Trigger` (every 1 hour / 08:00 AM) + on-demand `Webhook Trigger` (`GET /morning-brief` with `responseMode: "lastNode"`).
- **First API Call (GitHub Search REST API):** Queries `https://api.github.com/search/repositories?q=topic:automation+stars:>1000&sort=stars&order=desc&per_page=10`. Free, highly reliable, and surfaces the top 10 automation projects (e.g. `n8n-io/n8n`).
- **Data Transformation (Code Node):** Reshapes raw payloads, normalizes metrics (stars, forks, open issues, language), sorts descending, isolates the **Top 5**, and extracts the **#1 Ranked Tool** (`n8n-io/n8n`) for deep enrichment.
- **Second API Call (GitHub Release Enrichment):** Enriches `#1` by querying `https://api.github.com/repos/{owner}/{name}/releases/latest`, fetching latest tag (`n8n@2.46.6`), release date, and changelog highlights.
- **Conditional Routing (IF Node):** Evaluates if `top_repo.stars >= 50,000`. If true, routes to a **High-Priority Channel** with crimson styling; otherwise routes to **Standard Brief**.
- **Output:** Posts formatted Discord Rich Embeds with clickable links, repository stats, release highlights, and ranked Top 5 summaries.
- **Error Handling:** Configured with `onError: continueRegularOutput` on API nodes plus a dedicated **Error Trigger (`n8n-nodes-base.errorTrigger`)** that catches unhandled failures, extracts failed node diagnostics, and alerts an emergency engineering channel.
- **Credentials:** No secrets are hardcoded; references `credentials.discordWebhookUrl` and standard n8n credential stores.

---

## 4. Bonus Task — Synthetic Uptime & Latency Monitor

A resilient uptime monitoring workflow combining QA auditing with automation.
- **5-Minute Synthetic Pings:** Continuously checks `https://demo.realworld.io` (or target API).
- **Latency Benchmarking:** Calculates high-precision response times in milliseconds (`Date.now() - startTime`). Warns on latency > 2000ms.
- **Exponential Retry Logic:** Retries failed requests up to 3 times with 2-second backoff before triggering alerts, eliminating false positives from transient network spikes.
- **Automated Discord Incident Alerts:** Dispatches rich alert cards featuring status code (e.g. 404/530/SSL expired), latency, error diagnostics, and incident timestamps.
- **Daily SLA Aggregator:** Scheduled midnight run compiling 24-hour availability percentages, average latency, and incident history.

---

## 5. How to Import & Run in n8n

1. Open your n8n instance (Self-hosted or n8n Cloud).
2. Go to **Workflows** → Click **`...`** (Top Right) → Select **Import from File**.
3. Select [`Task2_Workflow_Aditya_Kavde.json`](./Task2_Workflow_Aditya_Kavde.json) or [`Bonus_UptimeMonitor_Aditya_Kavde.json`](./Bonus_UptimeMonitor_Aditya_Kavde.json).
4. (Optional) Set your Discord/Slack Webhook URL in node parameters or environment credentials.
5. Click **"Test workflow"** or trigger via cURL:
   ```bash
   curl -X GET "http://localhost:5678/webhook/morning-brief"
   ```
