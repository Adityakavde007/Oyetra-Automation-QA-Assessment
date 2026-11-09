# Loom Video Presentation Guide & Talking Script

**Candidate:** Aditya Kavde  
**Role:** Automation & QA Developer  
**Assessment:** Oyetra Take-Home Skills Assessment  
**Target Video Duration:** 4–5 Minutes  

---

## 📹 Pre-Recording Setup Checklist
- [ ] Open the repository folder in VS Code or GitHub.
- [ ] Open [`Task1_QA_Report_Aditya_Kavde.pdf`](./Task1_QA_Report_Aditya_Kavde.pdf) in a PDF reader or browser.
- [ ] Open the screenshots in fullscreen or preview tabs:
  - [`screenshots/Task2_Workflow_Canvas.png`](./screenshots/Task2_Workflow_Canvas.png)
  - [`screenshots/Task2_Successful_Execution.png`](./screenshots/Task2_Successful_Execution.png)
  - [`screenshots/Bonus_UptimeMonitor_Canvas.png`](./screenshots/Bonus_UptimeMonitor_Canvas.png)
- [ ] Set your microphone and webcam (picture-in-picture in the corner).

---

## 🎙️ Step-by-Step Speaking Script

### ⏱️ Segment 1: Introduction (0:00 – 0:35)
> **What to show on screen:** Repository root or [`README.md`](./README.md)
>
> *"Hi everyone, my name is Aditya Kavde, and this is my walkthrough for the Automation & QA Developer Take-Home Skills Assessment.
>
> Today, I'll walk you through three core deliverables:
> 1. First, our **Task 1 Web App QA & Debug Report**, where we investigated a vibe-coded RealWorld web application, surfaced 6 production-blocking issues, and performed an in-depth root cause analysis on authentication session desynchronization.
> 2. Second, our **Task 2 n8n API Integration Workflow**, which runs a morning brief pipeline by consuming GitHub REST APIs, transforming and enriching data, routing via conditional logic, and dispatching rich embeds with enterprise error handling.
> 3. And third, our **Bonus Task Uptime Monitor**, which synthetically benchmarks web app availability, tracks response latency, applies retry backoff logic, and sends automated incident alerts."*

---

### ⏱️ Segment 2: Task 1 — Web App QA & Debug Report (0:35 – 2:00)
> **What to show on screen:** [`Task1_QA_Report_Aditya_Kavde.pdf`](./Task1_QA_Report_Aditya_Kavde.pdf) (Scroll to the Bug Report Table on Page 1 & 2)
>
> *"For Task 1, we audited the RealWorld Conduit single-page application across all core user flows: authentication, registration, feed browsing, article CRUD, markdown parsing, and session teardown.
>
> In typical vibe-coded applications, non-developers prompt an AI to generate features, but crucial defensive handling and edge cases are often missed. We documented **6 distinct issues**:
>
> - **BUG-01 (Critical Origin Outage):** The primary demo domain had an orphaned CNAME returning 404, while backend origins suffered from expired TLS certificates (`NET::ERR_CERT_DATE_INVALID`), blocking all HTTPS handshakes.
> - **BUG-02 (Critical Silent Rejection):** If an API call fails or the network drops, unhandled promise rejections leave the UI hanging permanently on 'Loading articles...' with zero user feedback or retry actions.
> - **BUG-03 (Critical Stored XSS):** Markdown bodies were injected directly into the DOM via unescaped `v-html`/`dangerouslySetInnerHTML`, allowing malicious script execution.
> - **BUG-04 (High Form Validation Break):** Duplicate user sign-up responses from the server returned a structured error object (`{ errors: { email: [...] } }`), but the frontend expected a flat string, causing form buttons to freeze indefinitely.
> - **BUG-05 (High Ghost Authentication):** This was our deep-dive focus. When a user's JWT expires on the server, the app naively checks `localStorage.getItem('token')` on reload and keeps rendering the user as logged in. Every time they try to post or like an article, requests fail with 401 Unauthorized, trapping the user in a broken session.
> - **BUG-06 (Medium Race Condition):** Rapid multi-clicking on 'Publish Article' lacked debouncing, creating duplicate articles in the database.
>
> In our Root-Cause Analysis, we outlined the production fix: implementing a centralized Axios response interceptor that intercepts 401 status codes, purges stale localStorage tokens, triggers a non-blocking session-expired toast, and automatically routes the user back to `/login` with the return URL preserved."*

---

### ⏱️ Segment 3: Task 2 — n8n API Integration Workflow (2:00 – 3:30)
> **What to show on screen:** Switch to [`screenshots/Task2_Workflow_Canvas.png`](./screenshots/Task2_Workflow_Canvas.png) and then [`screenshots/Task2_Successful_Execution.png`](./screenshots/Task2_Successful_Execution.png)
>
> *"Moving to Task 2, we built the daily 'Morning Brief' pipeline in n8n.
>
> Here is how the workflow is engineered:
> 1. **Triggering:** We support both a scheduled hourly trigger for automated runs and an on-demand webhook trigger for manual curl or CI/CD invocation.
> 2. **Primary API (GitHub Search):** We query `https://api.github.com/search/repositories` for trending repositories tagged with `topic:automation` having over 1,000 stars. We chose this API because it is free, robust, and directly relevant to automation engineering teams.
> 3. **Transformation (Code Node):** Our JavaScript code node reshapes the payload, strips unneeded attributes, sorts descending by stargazers, keeps the top 5 tools, and isolates the #1 ranked repository—which currently happens to be `n8n-io/n8n` with over 209,000 stars!
> 4. **Enrichment API:** We call GitHub's `/releases/latest` endpoint using the #1 repo's full name to fetch the latest version tag (`n8n@2.46.6`), release date, and changelog highlights.
> 5. **Conditional Branch (IF Node):** We set a threshold: `stars >= 50,000`. If true, the repo is classified as a 'Mega Trend' and routed to our High-Priority Alert branch with red highlight styling. Otherwise, it routes to the Standard Daily Brief.
> 6. **Notification Delivery:** It formats a rich Discord embed with clickable links, repository metrics, release details, and ranked summaries.
> 7. **Defensive Error Handling:** Notice on the canvas we implemented `continueRegularOutput` on the HTTP nodes and an explicit **Error Trigger node**. If GitHub rate limits or a network timeout occurs, the workflow doesn't crash silently—it captures the execution ID and failed node name, and alerts an emergency Slack/Discord channel."*

---

### ⏱️ Segment 4: Bonus Task — Synthetic Uptime Monitor (3:30 – 4:20)
> **What to show on screen:** Switch to [`screenshots/Bonus_UptimeMonitor_Canvas.png`](./screenshots/Bonus_UptimeMonitor_Canvas.png)
>
> *"Finally, in the Bonus Task, we bridged QA debugging and automation by building a continuous Synthetic Uptime & Latency Monitor:
> - Every 5 minutes, it pings the target web app and computes latency in milliseconds (`Date.now() - startTime`).
> - An IF condition checks whether the HTTP status is 200 and latency is under 2,000ms.
> - If an anomaly occurs (like the 404 or expired SSL cert we found in Task 1), our **Retry Logic** runs up to 3 times with exponential backoff before escalating. This prevents alerting engineers on transient 1-second network blips.
> - If down, a critical Discord alert is dispatched detailing status code, latency, and failure diagnostics.
> - At midnight, a secondary cron trigger aggregates 24-hour uptime SLA percentages and average latency for the team."*

---

### ⏱️ Segment 5: Conclusion & Next Steps (4:20 – 4:45)
> **What to show on screen:** Back to the GitHub repo [`README.md`](./README.md)
>
> *"All workflows have been exported to standard JSON files—[`Task2_Workflow_Aditya_Kavde.json`](./Task2_Workflow_Aditya_Kavde.json) and [`Bonus_UptimeMonitor_Aditya_Kavde.json`](./Bonus_UptimeMonitor_Aditya_Kavde.json)—and can be imported directly into any n8n instance in seconds.
>
> Thank you for reviewing my submission. I look forward to discussing the architecture, design choices, and QA methodologies in our follow-up technical conversation!"*

---

## 🎯 Interview Follow-Up Cheatsheet ("Defend Every Decision")

When asked in the 30-minute technical follow-up call:

1. **"Why the GitHub REST API for Task 2?"**  
   *Answer:* It requires no paid API keys, boasts 99.9% uptime, offers rich structured metadata (stars, forks, languages, releases), and produces a genuine, high-value morning brief that developers and automation engineers actually rely on.

2. **"Why set the threshold at 50,000 stars?"**  
   *Answer:* In GitHub's open-source ecosystem, 1,000+ stars represents established popularity, but 50,000+ stars is an elite tier reserved for transformational projects (e.g. `n8n`, `dify`, `langchain`). Using 50,000 allows us to cleanly bifurcate daily updates from major industry trends.

3. **"Why use both Continue On Fail and the Error Trigger?"**  
   *Answer:* Defensive depth. `Continue On Fail` (or `onError: continueRegularOutput`) on individual HTTP nodes allows partial degradation—for instance, if the top repo has no releases, the brief still compiles with the search data. The `Error Trigger` acts as a safety net for unexpected runtime crashes, ensuring engineering is alerted immediately.

4. **"How would you harden the n8n workflow for high-volume enterprise production?"**  
   *Answer:* In production, I would authenticate GitHub requests with a Personal Access Token stored in n8n Credentials to raise the rate limit from 60 to 5,000 requests/hour, persist historical uptime metrics in a PostgreSQL or InfluxDB time-series database rather than ephemeral memory, and use n8n's queue mode with Redis workers for horizontally scalable ping execution.
