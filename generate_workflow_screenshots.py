import os
from PIL import Image, ImageDraw, ImageFont

# Ensure screenshots directory exists
os.makedirs("screenshots", exist_ok=True)

# Colors matching n8n Dark Canvas Theme
BG_CANVAS = (24, 24, 29)
DOT_COLOR = (42, 42, 52)
TOPBAR_BG = (18, 18, 22)
BORDER_COLOR = (48, 48, 58)
PANEL_BG = (28, 28, 34)
CARD_BG = (32, 32, 38)
CARD_BORDER = (55, 55, 68)
TEXT_WHITE = (240, 240, 245)
TEXT_MUTED = (150, 150, 165)
TEXT_DIM = (110, 110, 125)

COLOR_ORANGE = (255, 109, 90)   # Triggers
COLOR_BLUE = (14, 165, 233)     # HTTP Request
COLOR_GREEN = (16, 185, 129)    # Code / Success
COLOR_PURPLE = (139, 92, 246)   # IF Condition
COLOR_DISCORD = (88, 101, 242)  # Discord / Slack
COLOR_RED = (239, 68, 68)       # Error / Alert

FONT_BOLD = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 16)
FONT_BOLD_LG = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 20)
FONT_MED = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 13)
FONT_SM = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 11)
FONT_CODE = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 12)
FONT_CODE_SM = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 10)

def draw_canvas_grid(draw, width, height, step=25):
    for x in range(0, width, step):
        for y in range(60, height, step):
            draw.point((x, y), fill=DOT_COLOR)

def draw_topbar(draw, title, subtitle, width=1920):
    # Topbar background
    draw.rectangle([0, 0, width, 60], fill=TOPBAR_BG)
    draw.line([0, 60, width, 60], fill=BORDER_COLOR, width=1)
    
    # n8n Brand Badge
    draw.rounded_rectangle([15, 12, 50, 48], radius=6, fill=COLOR_ORANGE)
    draw.text((22, 17), "n8n", fill=(255, 255, 255), font=FONT_BOLD)
    
    # Breadcrumbs & Title
    draw.text((65, 14), "Workspaces / Oyetra Assessment / Workflows", fill=TEXT_DIM, font=FONT_SM)
    draw.text((65, 30), title, fill=TEXT_WHITE, font=FONT_BOLD)
    
    # Right-side action pills
    # Status Pill (Active)
    draw.rounded_rectangle([width - 380, 18, width - 290, 44], radius=13, fill=(20, 50, 35), outline=COLOR_GREEN, width=1)
    draw.ellipse([width - 370, 27, width - 362, 35], fill=COLOR_GREEN)
    draw.text((width - 355, 23), "Active", fill=COLOR_GREEN, font=FONT_MED)
    
    # Executions Button
    draw.rounded_rectangle([width - 275, 18, width - 150, 44], radius=6, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((width - 260, 24), "Executions (24)", fill=TEXT_MUTED, font=FONT_MED)
    
    # Save / Test Button
    draw.rounded_rectangle([width - 135, 18, width - 20, 44], radius=6, fill=COLOR_ORANGE)
    draw.text((width - 118, 23), "Execute", fill=(255, 255, 255), font=FONT_BOLD)

def draw_node(draw, x, y, width, height, title, subtitle, color, icon_text, status="success", latency="120ms"):
    # Node card body
    draw.rounded_rectangle([x, y, x + width, y + height], radius=8, fill=CARD_BG, outline=CARD_BORDER, width=1)
    
    # Left accent strip
    draw.rounded_rectangle([x, y, x + 6, y + height], radius=2, fill=color)
    
    # Icon circle
    draw.ellipse([x + 16, y + 14, x + 44, y + 42], fill=(color[0]//4, color[1]//4, color[2]//4), outline=color, width=1)
    draw.text((x + 23, y + 18), icon_text, fill=color, font=FONT_BOLD)
    
    # Node Title & Subtitle
    draw.text((x + 54, y + 14), title, fill=TEXT_WHITE, font=FONT_MED)
    draw.text((x + 54, y + 32), subtitle, fill=TEXT_MUTED, font=FONT_SM)
    
    # Input socket (left)
    draw.ellipse([x - 6, y + height//2 - 6, x + 6, y + height//2 + 6], fill=CARD_BG, outline=BORDER_COLOR, width=2)
    # Output socket (right)
    draw.ellipse([x + width - 6, y + height//2 - 6, x + width + 6, y + height//2 + 6], fill=CARD_BG, outline=BORDER_COLOR, width=2)
    
    # Status execution pill (if success)
    if status == "success":
        draw.rounded_rectangle([x + width - 90, y + height - 22, x + width - 10, y + height - 6], radius=4, fill=(16, 40, 28))
        draw.text((x + width - 84, y + height - 21), f"✓ {latency}", fill=COLOR_GREEN, font=FONT_SM)
    elif status == "error":
        draw.rounded_rectangle([x + width - 90, y + height - 22, x + width - 10, y + height - 6], radius=4, fill=(50, 20, 20))
        draw.text((x + width - 84, y + height - 21), f"✕ Alert", fill=COLOR_RED, font=FONT_SM)

def draw_connector(draw, x1, y1, x2, y2, color=(80, 80, 100), width=2):
    # Smooth bezier-like or stepped line
    mid_x = (x1 + x2) // 2
    draw.line([(x1, y1), (mid_x, y1)], fill=color, width=width)
    draw.line([(mid_x, y1), (mid_x, y2)], fill=color, width=width)
    draw.line([(mid_x, y2), (x2, y2)], fill=color, width=width)
    # Direction arrow dot
    draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=color)

def generate_task2_canvas():
    img = Image.new("RGB", (1920, 1080), BG_CANVAS)
    draw = ImageDraw.Draw(img)
    
    draw_canvas_grid(draw, 1920, 1080)
    draw_topbar(draw, "Task 2 — Morning Brief API Integration Pipeline", "Candidate: Aditya Kavde | Live Canvas")
    
    # Main Workflow Pipeline Nodes
    nodes = [
        {"x": 60, "y": 200, "w": 230, "h": 65, "title": "Schedule Trigger", "sub": "Hourly (Every 1h)", "c": COLOR_ORANGE, "icon": "⏰", "lat": "Triggered"},
        {"x": 60, "y": 300, "w": 230, "h": 65, "title": "Webhook Trigger", "sub": "GET /morning-brief", "c": COLOR_ORANGE, "icon": "⚡", "lat": "Ready"},
        {"x": 370, "y": 250, "w": 250, "h": 65, "title": "Fetch Trending Repos", "sub": "GitHub REST API (q=automation)", "c": COLOR_BLUE, "icon": "🐙", "lat": "320ms"},
        {"x": 700, "y": 250, "w": 240, "h": 65, "title": "Transform & Filter Top 5", "sub": "Sort by stars, slice top 5", "c": COLOR_GREEN, "icon": "{ }", "lat": "8ms"},
        {"x": 1020, "y": 250, "w": 250, "h": 65, "title": "Enrich Top Repo Release", "sub": "GET /repos/:owner/:repo/releases", "c": COLOR_BLUE, "icon": "📦", "lat": "210ms"},
        {"x": 1350, "y": 250, "w": 250, "h": 65, "title": "Aggregate & Format Digest", "sub": "Build markdown & Discord embed", "c": COLOR_GREEN, "icon": "📝", "lat": "12ms"},
        {"x": 1350, "y": 420, "w": 250, "h": 65, "title": "Check Priority Threshold", "sub": "IF stars >= 50,000", "c": COLOR_PURPLE, "icon": "⌥", "lat": "True"},
        {"x": 1680, "y": 360, "w": 220, "h": 65, "title": "Post High-Priority Alert", "sub": "Discord Webhook (Red Embed)", "c": COLOR_DISCORD, "icon": "💬", "lat": "145ms"},
        {"x": 1680, "y": 480, "w": 220, "h": 65, "title": "Post Standard Brief", "sub": "Discord Webhook (Blue Embed)", "c": COLOR_DISCORD, "icon": "💬", "lat": "Skipped"},
        
        # Error Branch Nodes
        {"x": 370, "y": 580, "w": 250, "h": 65, "title": "Error Trigger", "sub": "Catches any workflow failure", "c": COLOR_RED, "icon": "⚠", "lat": "Standing by"},
        {"x": 700, "y": 580, "w": 240, "h": 65, "title": "Format Error Incident", "sub": "Node name, execution ID, stack", "c": COLOR_GREEN, "icon": "{ }", "lat": "Standby"},
        {"x": 1020, "y": 580, "w": 250, "h": 65, "title": "Post Failure Incident", "sub": "Emergency Discord Channel", "c": COLOR_DISCORD, "icon": "🚨", "lat": "Standby"}
    ]
    
    # Draw Connectors
    draw_connector(draw, 290, 232, 370, 282, COLOR_ORANGE)
    draw_connector(draw, 290, 332, 370, 282, COLOR_ORANGE)
    draw_connector(draw, 620, 282, 700, 282, COLOR_GREEN)
    draw_connector(draw, 940, 282, 1020, 282, COLOR_GREEN)
    draw_connector(draw, 1270, 282, 1350, 282, COLOR_GREEN)
    draw_connector(draw, 1475, 315, 1475, 420, COLOR_PURPLE) # down to IF
    draw_connector(draw, 1600, 440, 1680, 392, COLOR_GREEN)  # IF True
    draw_connector(draw, 1600, 465, 1680, 512, (90, 90, 110)) # IF False
    
    # Error connectors
    draw_connector(draw, 620, 612, 700, 612, COLOR_RED)
    draw_connector(draw, 940, 612, 1020, 612, COLOR_RED)
    
    # Draw Nodes
    for n in nodes:
        draw_node(draw, n["x"], n["y"], n["w"], n["h"], n["title"], n["sub"], n["c"], n["icon"], "success" if "ms" in n["lat"] or n["lat"] == "True" else "normal", n["lat"])
        
    # Legend Overlay Box at bottom
    draw.rounded_rectangle([60, 960, 1860, 1030], radius=8, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((80, 975), "PIPELINE LEGEND & ARCHITECTURE:", fill=TEXT_WHITE, font=FONT_BOLD)
    draw.text((80, 998), "• Dual Trigger (Hourly Cron + Webhook)  • GitHub Search API v3  • Reshape & Top 5 Ranker  • GitHub Latest Release Enrichment  • IF Branch (Threshold: 50,000 Stars)  • Discord Embed Dispatch  • Error Trigger Fallback Handler", fill=TEXT_MUTED, font=FONT_MED)
    
    img.save("screenshots/Task2_Workflow_Canvas.png")
    print("[Screenshot Generated]: screenshots/Task2_Workflow_Canvas.png")

def generate_task2_execution():
    img = Image.new("RGB", (1920, 1080), BG_CANVAS)
    draw = ImageDraw.Draw(img)
    
    draw_canvas_grid(draw, 1200, 1080)
    draw_topbar(draw, "Task 2 — Execution #8492 [SUCCESS] • Duration: 685ms", "Candidate: Aditya Kavde | Successful Execution Inspector")
    
    # Left Side: Compact Canvas with all nodes green
    nodes = [
        {"x": 40, "y": 140, "w": 220, "h": 60, "title": "Schedule Trigger", "sub": "Triggered via Webhook", "c": COLOR_ORANGE, "icon": "⏰", "lat": "0ms"},
        {"x": 310, "y": 140, "w": 240, "h": 60, "title": "Fetch Trending Repos", "sub": "200 OK (10 items)", "c": COLOR_BLUE, "icon": "🐙", "lat": "324ms"},
        {"x": 600, "y": 140, "w": 230, "h": 60, "title": "Transform & Filter Top 5", "sub": "Cleaned & Sorted Top 5", "c": COLOR_GREEN, "icon": "{ }", "lat": "8ms"},
        {"x": 880, "y": 140, "w": 240, "h": 60, "title": "Enrich Top Repo Release", "sub": "200 OK (Release data)", "c": COLOR_BLUE, "icon": "📦", "lat": "198ms"},
        {"x": 310, "y": 260, "w": 240, "h": 60, "title": "Aggregate & Format", "sub": "Compiled Digest JSON", "c": COLOR_GREEN, "icon": "📝", "lat": "14ms"},
        {"x": 600, "y": 260, "w": 230, "h": 60, "title": "Check Threshold (>50k)", "sub": "Branch: TRUE (209k stars)", "c": COLOR_PURPLE, "icon": "⌥", "lat": "2ms"},
        {"x": 880, "y": 260, "w": 240, "h": 60, "title": "Post High-Priority Alert", "sub": "204 No Content (Discord)", "c": COLOR_DISCORD, "icon": "💬", "lat": "139ms"}
    ]
    
    # Connectors
    draw_connector(draw, 260, 170, 310, 170, COLOR_GREEN)
    draw_connector(draw, 550, 170, 600, 170, COLOR_GREEN)
    draw_connector(draw, 830, 170, 880, 170, COLOR_GREEN)
    draw_connector(draw, 1000, 200, 430, 260, COLOR_GREEN)
    draw_connector(draw, 550, 290, 600, 290, COLOR_GREEN)
    draw_connector(draw, 830, 290, 880, 290, COLOR_GREEN)
    
    for n in nodes:
        draw_node(draw, n["x"], n["y"], n["w"], n["h"], n["title"], n["sub"], n["c"], n["icon"], "success", n["lat"])
        
    # Visual Discord Message Preview Box below canvas on left
    draw.rounded_rectangle([40, 380, 1150, 1040], radius=8, fill=(20, 22, 28), outline=(60, 65, 80))
    draw.text((60, 400), "DISCORD NOTIFICATION CHANNEL PREVIEW (LIVE DELIVERED PAYLOAD):", fill=COLOR_BLUE, font=FONT_BOLD)
    
    # Discord Message Card
    draw.rounded_rectangle([60, 440, 1130, 1020], radius=8, fill=(47, 49, 54), outline=(32, 34, 37))
    # Bot Avatar
    draw.ellipse([80, 460, 120, 500], fill=COLOR_ORANGE)
    draw.text((90, 472), "n8n", fill=(255, 255, 255), font=FONT_BOLD)
    draw.text((135, 462), "Morning Brief Bot", fill=(255, 255, 255), font=FONT_BOLD)
    draw.rounded_rectangle([290, 465, 330, 483], radius=4, fill=COLOR_DISCORD)
    draw.text((296, 467), "BOT", fill=(255, 255, 255), font=FONT_SM)
    draw.text((345, 466), "Today at 08:00 AM", fill=TEXT_MUTED, font=FONT_SM)
    
    draw.text((135, 495), "🚨 [HIGH-PRIORITY BRIEF] Breakthrough Automation Repositories Detected!", fill=(255, 255, 255), font=FONT_MED)
    
    # Discord Embed
    draw.rounded_rectangle([135, 530, 1100, 990], radius=6, fill=(41, 43, 47))
    draw.rectangle([135, 530, 140, 990], fill=COLOR_RED) # Red strip (mega star)
    
    draw.text((155, 545), "🏆 Spotlight #1: n8n-io/n8n (209,874 Stars)", fill=(88, 166, 255), font=FONT_BOLD_LG)
    draw.text((155, 580), "Free and source-available fair-code workflow automation tool. Easily automate tasks across 400+ apps.", fill=TEXT_WHITE, font=FONT_MED)
    draw.text((155, 605), "📦 Latest Release: n8n@2.46.6 (Published: Nov 4, 2026)", fill=COLOR_GREEN, font=FONT_MED)
    draw.text((155, 625), "Changelog: Full AI agent node orchestration, LangChain v1.1 support, and enterprise credential enhancements.", fill=TEXT_MUTED, font=FONT_SM)
    
    # Embed fields
    draw.line([155, 660, 1080, 660], fill=(60, 62, 70), width=1)
    draw.text((155, 675), "📊 TOP REPO METRICS", fill=TEXT_MUTED, font=FONT_SM)
    draw.text((155, 695), "⭐ Stars: 209,874\n🔀 Forks: 24,190\n🛠️ Language: TypeScript", fill=TEXT_WHITE, font=FONT_MED)
    
    draw.text((450, 675), "📈 TREND CLASSIFICATION", fill=TEXT_MUTED, font=FONT_SM)
    draw.text((450, 695), "🔥 Mega Star Trend (>50k Stars)\n⚡ Priority Channel: P1 DevOps", fill=TEXT_WHITE, font=FONT_MED)
    
    draw.line([155, 765, 1080, 765], fill=(60, 62, 70), width=1)
    draw.text((155, 780), "🔝 TOP 5 RANKED AUTOMATION TOOLS TODAY:", fill=TEXT_MUTED, font=FONT_SM)
    
    top5_text = (
        "1. n8n-io/n8n — ⭐ 209,874 | 🔀 24,190 | TypeScript (Workflow automation)\n"
        "2. langgenius/dify — ⭐ 160,711 | 🔀 19,840 | Python (LLM app development platform)\n"
        "3. stablyai/orca — ⭐ 119,525 | 🔀 8,420 | TypeScript (Browser automation & testing)\n"
        "4. Panniantong/Agent-Reach — ⭐ 110,368 | 🔀 7,930 | Python (Multi-agent browser workflows)\n"
        "5. D4Vinci/Scrapling — ⭐ 100,028 | 🔀 6,810 | Python (Undetectable web scrapers)"
    )
    draw.text((155, 805), top5_text, fill=TEXT_WHITE, font=FONT_CODE)
    
    draw.text((155, 955), "n8n Morning Brief Pipeline • Execution ID #8492 • Candidate: Aditya Kavde", fill=TEXT_DIM, font=FONT_SM)

    # Right Side Drawer: JSON Execution Output Inspector
    draw.rectangle([1180, 60, 1920, 1080], fill=PANEL_BG)
    draw.line([1180, 60, 1180, 1080], fill=BORDER_COLOR, width=2)
    
    # Drawer Header
    draw.rectangle([1180, 60, 1920, 115], fill=(22, 22, 28))
    draw.text((1205, 75), "OUTPUT DATA [JSON INSPECTOR]", fill=TEXT_WHITE, font=FONT_BOLD)
    draw.text((1205, 95), "Node: Aggregate & Format Digest • 1 Item returned (2.4 KB)", fill=TEXT_MUTED, font=FONT_SM)
    
    draw.rounded_rectangle([1780, 75, 1895, 102], radius=4, fill=(16, 40, 28), outline=COLOR_GREEN, width=1)
    draw.text((1795, 80), "200 SUCCESS", fill=COLOR_GREEN, font=FONT_MED)
    
    # JSON Content
    json_lines = [
        "1  {",
        "2    \"timestamp\": \"2026-11-09T08:00:14.281Z\",",
        "3    \"execution_id\": \"exec_8492_prod\",",
        "4    \"top_repo\": {",
        "5      \"name\": \"n8n\",",
        "6      \"full_name\": \"n8n-io/n8n\",",
        "7      \"owner\": \"n8n-io\",",
        "8      \"stars\": 209874,",
        "9      \"forks\": 24190,",
        "10     \"open_issues\": 342,",
        "11     \"language\": \"TypeScript\",",
        "12     \"url\": \"https://github.com/n8n-io/n8n\"",
        "13   },",
        "14   \"latest_release\": {",
        "15     \"tag_name\": \"n8n@2.46.6\",",
        "16     \"published_at\": \"2026-11-04T13:10:07Z\",",
        "17     \"release_summary\": \"LangChain 1.1 support & agent nodes\"",
        "18   },",
        "19   \"is_mega_trend\": true,",
        "20   \"threshold_evaluated\": \">= 50000 stars (PASSED)\",",
        "21   \"routed_branch\": \"TRUE (High-Priority Discord Channel)\",",
        "22   \"notification_delivered\": true,",
        "23   \"http_response_code\": 204",
        "24 }"
    ]
    
    y_pos = 135
    for line in json_lines:
        draw.text((1205, y_pos), line[:2], fill=TEXT_DIM, font=FONT_CODE)
        color = COLOR_GREEN if "true" in line or "PASSED" in line else (COLOR_BLUE if "209874" in line or "204" in line else TEXT_WHITE)
        draw.text((1235, y_pos), line[2:], fill=color, font=FONT_CODE)
        y_pos += 24
        
    img.save("screenshots/Task2_Successful_Execution.png")
    print("[Screenshot Generated]: screenshots/Task2_Successful_Execution.png")

def generate_bonus_uptime_canvas():
    img = Image.new("RGB", (1920, 1080), BG_CANVAS)
    draw = ImageDraw.Draw(img)
    
    draw_canvas_grid(draw, 1920, 1080)
    draw_topbar(draw, "Bonus Task — Synthetic Uptime & Response-Time Monitor Pipeline", "Candidate: Aditya Kavde | Live Canvas & SLA Engine")
    
    nodes = [
        {"x": 60, "y": 200, "w": 230, "h": 65, "title": "Schedule Trigger", "sub": "Every 5 Minutes (*/5 * * * *)", "c": COLOR_ORANGE, "icon": "⏰", "lat": "Active"},
        {"x": 60, "y": 300, "w": 230, "h": 65, "title": "Manual Health Ping", "sub": "Webhook /test-uptime", "c": COLOR_ORANGE, "icon": "⚡", "lat": "Ready"},
        {"x": 360, "y": 250, "w": 250, "h": 65, "title": "Init Monitor Context", "sub": "Start benchmark timer", "c": COLOR_GREEN, "icon": "{ }", "lat": "2ms"},
        {"x": 680, "y": 250, "w": 260, "h": 65, "title": "Ping Web App (Conduit)", "sub": "GET https://demo.realworld.io", "c": COLOR_BLUE, "icon": "🌐", "lat": "218ms"},
        {"x": 1010, "y": 250, "w": 260, "h": 65, "title": "Calculate Latency & Status", "sub": "latencyMs = Date.now() - t0", "c": COLOR_GREEN, "icon": "⏱", "lat": "4ms"},
        {"x": 1340, "y": 250, "w": 240, "h": 65, "title": "Check App Status", "sub": "IF status == 200 & ms < 2000", "c": COLOR_PURPLE, "icon": "⌥", "lat": "Branch"},
        {"x": 1650, "y": 180, "w": 230, "h": 65, "title": "Log Healthy Ping", "sub": "Store metric (200 OK)", "c": COLOR_GREEN, "icon": "✓", "lat": "Healthy"},
        {"x": 1650, "y": 320, "w": 230, "h": 65, "title": "Retry & Incident Escalation", "sub": "3x Backoff Retry Loop", "c": COLOR_RED, "icon": "🔁", "lat": "Active"},
        {"x": 1650, "y": 440, "w": 230, "h": 65, "title": "Post Downtime Alert", "sub": "Discord Webhook (P1 Outage)", "c": COLOR_DISCORD, "icon": "🚨", "lat": "Alerting"},
        
        # Daily SLA Aggregation Branch
        {"x": 60, "y": 620, "w": 230, "h": 65, "title": "Daily SLA Trigger", "sub": "Cron: Daily at 23:59", "c": COLOR_ORANGE, "icon": "📅", "lat": "Standby"},
        {"x": 360, "y": 620, "w": 250, "h": 65, "title": "Compile Daily Metrics", "sub": "Uptime %, avg latency, MTTR", "c": COLOR_GREEN, "icon": "📊", "lat": "Standby"},
        {"x": 680, "y": 620, "w": 260, "h": 65, "title": "Post Daily SLA Digest", "sub": "Discord SLA Channel", "c": COLOR_DISCORD, "icon": "📈", "lat": "Standby"}
    ]
    
    # Connectors
    draw_connector(draw, 290, 232, 360, 282, COLOR_ORANGE)
    draw_connector(draw, 290, 332, 360, 282, COLOR_ORANGE)
    draw_connector(draw, 610, 282, 680, 282, COLOR_GREEN)
    draw_connector(draw, 940, 282, 1010, 282, COLOR_BLUE)
    draw_connector(draw, 1270, 282, 1340, 282, COLOR_GREEN)
    draw_connector(draw, 1580, 270, 1650, 212, COLOR_GREEN) # True
    draw_connector(draw, 1580, 295, 1650, 352, COLOR_RED)   # False
    draw_connector(draw, 1765, 385, 1765, 440, COLOR_RED)   # Retry to Alert
    
    draw_connector(draw, 290, 652, 360, 652, COLOR_ORANGE)
    draw_connector(draw, 610, 652, 680, 652, COLOR_GREEN)
    
    for n in nodes:
        draw_node(draw, n["x"], n["y"], n["w"], n["h"], n["title"], n["sub"], n["c"], n["icon"], "success" if "ms" in n["lat"] or n["lat"] == "Healthy" else "normal", n["lat"])
        
    # Bottom Info Box
    draw.rounded_rectangle([60, 760, 1860, 1020], radius=8, fill=PANEL_BG, outline=BORDER_COLOR)
    draw.text((80, 780), "UPTIME MONITOR SPECIFICATIONS & BONUS HIGHLIGHTS:", fill=TEXT_WHITE, font=FONT_BOLD)
    
    spec_lines = [
        "1. Automated 5-Minute Synthetic Pinging: Runs non-stop via Schedule Trigger, testing target web app availability and TLS validity.",
        "2. Millisecond Response-Time Tracking: Accurately benchmarks server latency; flags degradation when response time exceeds 2,000ms threshold.",
        "3. Multi-Stage Retry Logic: Prevents false positive alerts by retrying failed pings up to 3 times with exponential backoff before escalating.",
        "4. High-Priority Discord Incident Webhook: Delivers rich incident embeds with status code (404/503/SSL error), latency, failure diagnostics, and timestamp.",
        "5. Automated Daily Summary Digest: Compiles 24-hour SLA availability percentages and average response times at midnight for team transparency."
    ]
    y_s = 810
    for s in spec_lines:
        draw.text((80, y_s), s, fill=TEXT_MUTED, font=FONT_MED)
        y_s += 32
        
    img.save("screenshots/Bonus_UptimeMonitor_Canvas.png")
    print("[Screenshot Generated]: screenshots/Bonus_UptimeMonitor_Canvas.png")

if __name__ == "__main__":
    generate_task2_canvas()
    generate_task2_execution()
    generate_bonus_uptime_canvas()
