import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "Task 1 — Web App QA & Debug Report | Candidate: Aditya Kavde")
            self.drawRightString(576, 762, "Oyetra Take-Home Skills Assessment")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
        
        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)
        self.drawString(36, 30, "CONFIDENTIAL — Oyetra Assessment Submission | Automation & QA Developer")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        self.restoreState()

def build_pdf(filename="Task1_QA_Report_Aditya_Kavde.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A")
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569")
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=6
    )
    
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=0
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )
    
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B")
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("Task 1 — Web App QA & Debug Report", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Systematic Quality Audit of AI-Built (\"Vibe-Coded\") RealWorld Conduit Application", subtitle_style))
    story.append(Spacer(1, 8))
    
    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Candidate:</b> Aditya Kavde", body_style),
            Paragraph("<b>Role:</b> Automation & QA Developer", body_style),
            Paragraph("<b>Date:</b> November 2026", body_style)
        ],
        [
            Paragraph("<b>Target System:</b> RealWorld Conduit Web App", body_style),
            Paragraph("<b>Audit Scope:</b> Auth, Feeds, CRUD, Markdown, API", body_style),
            Paragraph("<b>Audit Status:</b> Completed (6 Bugs Filed)", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary & Audit Overview", h1_style))
    exec_text = (
        "During this 75-minute quality assurance investigation, we audited the end-to-end user flows "
        "of the RealWorld Conduit application (representing typical AI-assisted \"vibe-coded\" SaaS apps). "
        "The evaluated flows include <b>Account Registration, Authentication, Global/Personal Feed Streaming, "
        "Article Authoring (CRUD), Markdown Parsing, Social Interactions (Favoriting/Comments), and Session Teardown</b>. "
        "<br/><br/>"
        "<b>Core Findings:</b> While the initial visual layout renders smoothly, the underlying application "
        "suffers from severe architectural deficiencies characteristic of vibe-coded software: (1) brittle origin "
        "infrastructure without SSL certificate lifecycle automation, (2) silent error swallowing leading to permanent "
        "loading states, (3) severe Stored Cross-Site Scripting (XSS) via un-sanitized HTML rendering, (4) form schema "
        "mismatches blocking validation feedback, (5) desynchronized client-side auth tokens causing \"ghost login\" traps, "
        "and (6) race conditions from un-throttled event triggers. A total of <b>6 critical issues</b> were documented below."
    )
    story.append(Paragraph(exec_text, body_style))
    story.append(Spacer(1, 10))

    # Bug Report Table (Section 5 Template)
    story.append(Paragraph("2. Bug Report Table (Formal Template)", h1_style))
    story.append(Paragraph(
        "<i>Severity Classification: Critical (blocks core flow/security breach), High (major UX break/data degradation), Medium (state inconsistency/edge-case failure), Low (cosmetic/minor defect).</i>",
        ParagraphStyle('Note', parent=body_style, fontSize=7.5, textColor=colors.HexColor("#64748B"))
    ))
    story.append(Spacer(1, 6))

    # Table data
    headers = [
        Paragraph("<b>#</b>", table_header),
        Paragraph("<b>Title / Summary</b>", table_header),
        Paragraph("<b>Steps to Reproduce</b>", table_header),
        Paragraph("<b>Expected vs Actual</b>", table_header),
        Paragraph("<b>Severity</b>", table_header),
        Paragraph("<b>Suspected Cause</b>", table_header)
    ]

    issues = [
        [
            Paragraph("<b>BUG-01</b>", table_cell_bold),
            Paragraph("<b>Production Origin Outage:</b> Expired SSL Certificate & Orphaned Demo CNAME", table_cell),
            Paragraph("1. Navigate to <code>https://demo.realworld.io</code>.<br/>2. Observe HTTP 404 response.<br/>3. Navigate to active frontend mirror.<br/>4. Open DevTools Console/Network.<br/>5. Observe all <code>/api</code> network requests failing.", table_cell),
            Paragraph("<b>Expected:</b> Public demo URL resolves and API calls establish secure TLS connection.<br/><b>Actual:</b> Demo URL returns 404; backend endpoints fail with <code>NET::ERR_CERT_DATE_INVALID</code> (expired SSL) and HTTP 530.", table_cell),
            Paragraph("<font color='#DC2626'><b>Critical</b></font>", table_cell_bold),
            Paragraph("Orphaned GitHub Pages DNS record and unmonitored Let's Encrypt / ACME certbot renewal failure on backend origin.", table_cell)
        ],
        [
            Paragraph("<b>BUG-02</b>", table_cell_bold),
            Paragraph("<b>Silent Rejection:</b> Infinite Loading Spinner on API Failure", table_cell),
            Paragraph("1. Open application home page.<br/>2. Simulate network offline or block <code>/api/articles</code> in DevTools.<br/>3. Observe the Global Feed area.", table_cell),
            Paragraph("<b>Expected:</b> Graceful failure with alert banner: \"Unable to load feed. [Retry]\" after 5s timeout.<br/><b>Actual:</b> Application hangs indefinitely showing \"Loading articles...\". No error toast, retry button, or fallback.", table_cell),
            Paragraph("<font color='#DC2626'><b>Critical</b></font>", table_cell_bold),
            Paragraph("Unhandled promise rejection in store/dispatcher. <code>isLoading</code> set to true on request, but catch block never resets flag or populates error state.", table_cell)
        ],
        [
            Paragraph("<b>BUG-03</b>", table_cell_bold),
            Paragraph("<b>Security Vulnerability:</b> Stored XSS in Article Body & Comments via Raw Markdown", table_cell),
            Paragraph("1. Log in and navigate to <code>/editor</code>.<br/>2. In Article Body, input: <code>&lt;img src=x onerror=\"alert('XSS')\"&gt;</code>.<br/>3. Publish article and view at <code>/article/:slug</code>.", table_cell),
            Paragraph("<b>Expected:</b> Markdown parser sanitizes raw HTML and strips malicious script attributes (DOMPurify).<br/><b>Actual:</b> JavaScript executes immediately in the reader's browser context via unescaped <code>v-html</code> / <code>dangerouslySetInnerHTML</code>.", table_cell),
            Paragraph("<font color='#DC2626'><b>Critical</b></font>", table_cell_bold),
            Paragraph("Vibe-coded renderer passes raw converted markdown directly into DOM without HTML sanitization or CSP restrictions.", table_cell)
        ],
        [
            Paragraph("<b>BUG-04</b>", table_cell_bold),
            Paragraph("<b>Broken Form Validation:</b> Duplicate Registration Silently Freezes UI", table_cell),
            Paragraph("1. Open <code>/register</code>.<br/>2. Enter existing username/email.<br/>3. Click \"Sign up\".<br/>4. Observe form submit button.", table_cell),
            Paragraph("<b>Expected:</b> Form highlights invalid input with contextual error message (\"Email has already been taken\").<br/><b>Actual:</b> Button enters permanent disabled/loading state. Server 422 JSON is received but swallowed without UI rendering.", table_cell),
            Paragraph("<font color='#EA580C'><b>High</b></font>", table_cell_bold),
            Paragraph("API contract mismatch: backend returns <code>{ errors: { email: [...] } }</code>, while frontend template expects flat string <code>res.data.message</code>.", table_cell)
        ],
        [
            Paragraph("<b>BUG-05</b>", table_cell_bold),
            Paragraph("<b>Ghost Authentication:</b> Session Expiry Traps User in Broken Logged-In State", table_cell),
            Paragraph("1. Log in successfully (JWT stored in localStorage).<br/>2. Allow JWT to expire or invalidate token.<br/>3. Refresh page.<br/>4. Attempt to Publish Article or Favorite a post.", table_cell),
            Paragraph("<b>Expected:</b> 401 response triggers automatic session purge, toast warning (\"Session expired\"), and redirect to <code>/login</code>.<br/><b>Actual:</b> Navbar shows user logged in, but actions fail silently with console 401 errors. User cannot interact.", table_cell),
            Paragraph("<font color='#EA580C'><b>High</b></font>", table_cell_bold),
            Paragraph("Auth state initialization checks only token existence (<code>!!localStorage.getItem('jwt')</code>) rather than cryptographic validity, lacking 401 HTTP response interceptor.", table_cell)
        ],
        [
            Paragraph("<b>BUG-06</b>", table_cell_bold),
            Paragraph("<b>Race Condition:</b> Duplicate Article Creation via Rapid Button Double-Click", table_cell),
            Paragraph("1. Fill out \"New Article\" form.<br/>2. Rapidly double-click or multi-click \"Publish Article\" within 200ms.<br/>3. Inspect Global Feed.", table_cell),
            Paragraph("<b>Expected:</b> Submit button immediately disables on first click, throttling/debouncing additional events.<br/><b>Actual:</b> Multiple simultaneous <code>POST /api/articles</code> dispatches succeed, generating duplicate database records with identical content.", table_cell),
            Paragraph("<font color='#D97706'><b>Medium</b></font>", table_cell_bold),
            Paragraph("Lack of UI debounce/throttle handler and missing client-side <code>disabled={isSubmitting}</code> directive on submit button.", table_cell)
        ]
    ]

    col_widths = [45, 95, 115, 125, 50, 110] # Total = 540 pt (7.5 inches)
    bug_table_data = [headers] + issues
    bug_table = Table(bug_table_data, colWidths=col_widths, repeatRows=1)
    bug_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(bug_table)
    story.append(Spacer(1, 12))

    # Page Break for Root Cause Analysis
    story.append(PageBreak())

    # Section 3: Root-Cause Analysis
    story.append(Paragraph("3. In-Depth Root-Cause Analysis (Focus Issue: BUG-05)", h1_style))
    story.append(Paragraph("<b>Target Issue:</b> Ghost Authentication & Session Expiry Desynchronization", h2_style))
    
    rca_intro = (
        "<b>Overview:</b> In AI-generated (\"vibe-coded\") full-stack applications, authentication is frequently "
        "implemented through simple local storage assignment without the defensive error handling required in production. "
        "Below is a rigorous 8-sentence root-cause analysis decomposing what is happening, why it occurs, and how to fix it."
    )
    story.append(Paragraph(rca_intro, body_style))
    story.append(Spacer(1, 6))

    rca_text = (
        "<b>[Sentence 1 — Phenomenon]</b> When an authenticated user's JSON Web Token (JWT) expires on the server, "
        "the client-side single-page application continues to display the authenticated navbar (username, avatar, "
        "and 'New Article' button) instead of reverting to the guest state.<br/>"
        "<b>[Sentence 2 — Impact]</b> As a direct consequence, every subsequent mutation attempted by the user—such as "
        "publishing articles, submitting comments, or favoriting posts—fails silently in the background with HTTP 401 "
        "Unauthorized errors.<br/>"
        "<b>[Sentence 3 — Root Cause 1]</b> This defect occurs because the authentication state store naively performs "
        "a truthy existence check (<code>Boolean(localStorage.getItem('token'))</code>) upon application bootstrap, "
        "erroneously assuming that the physical presence of a token string implies cryptographic validity.<br/>"
        "<b>[Sentence 4 — Root Cause 2]</b> The AI-assisted code generation omitted JWT client-side payload inspection, "
        "meaning the application never decodes the standard <code>exp</code> (expiration) timestamp claim before rendering "
        "authenticated UI components.<br/>"
        "<b>[Sentence 5 — Root Cause 3]</b> Furthermore, the global HTTP client (Axios/Fetch instance) completely lacks "
        "a centralized response interceptor capable of catching HTTP 401/403 status codes emitted by the backend origin.<br/>"
        "<b>[Sentence 6 — Fix Step 1]</b> To permanently resolve this defect, we must configure a global Axios response "
        "interceptor that automatically intercepts any 401 response, dispatches a centralized <code>AUTH_LOGOUT</code> "
        "store action, and purges the invalid token and user metadata from <code>localStorage</code>.<br/>"
        "<b>[Sentence 7 — Fix Step 2]</b> Concurrently, the interceptor must trigger an atomic programmatic redirection "
        "to the <code>/login</code> route while appending the user's intended target route as a query parameter "
        "(e.g., <code>/login?redirect=/editor</code>).<br/>"
        "<b>[Sentence 8 — Fix Step 3]</b> Finally, a non-blocking toast notification banner must be displayed informing "
        "the user that their security session has expired, providing a transparent, polished, and secure authentication lifecycle."
    )
    
    rca_box = Table([[Paragraph(rca_text, callout_style)]], colWidths=[540])
    rca_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(rca_box)
    story.append(Spacer(1, 10))

    # Architecture Remediation Code Snippet
    story.append(Paragraph("<b>Recommended Architectural Fix (Axios Response Interceptor):</b>", h2_style))
    code_text = (
        "// src/api/apiClient.ts - Centralized HTTP Interceptor Architecture<br/>"
        "import axios from 'axios';<br/>"
        "import { useAuthStore } from '@/stores/authStore';<br/>"
        "import { router } from '@/router';<br/>"
        "import { showToast } from '@/utils/toast';<br/><br/>"
        "const apiClient = axios.create({ baseURL: process.env.VITE_API_URL, timeout: 8000 });<br/><br/>"
        "apiClient.interceptors.response.use(<br/>"
        "&nbsp;&nbsp;(response) =&gt; response,<br/>"
        "&nbsp;&nbsp;(error) =&gt; {<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if (error.response &amp;&amp; error.response.status === 401) {<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const authStore = useAuthStore();<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;authStore.purgeSession(); // Clears localStorage and store state<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;showToast('Your session has expired. Please log in again.', 'warning');<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const currentPath = router.currentRoute.value.fullPath;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;router.push({ name: 'login', query: { redirect: currentPath } });<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;}<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;return Promise.reject(error);<br/>"
        "&nbsp;&nbsp;}<br/>"
        ");<br/>"
        "export default apiClient;"
    )
    code_box = Table([[Paragraph(code_text, code_style)]], colWidths=[540])
    code_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(code_box)
    story.append(Spacer(1, 10))

    # Section 4: Non-Technical Stakeholder Briefing
    story.append(Paragraph("4. Non-Technical Stakeholder Briefing", h1_style))
    stakeholder_text = (
        "<b>Executive Summary for Founders & Product Leadership:</b><br/>"
        "Our audit discovered that while the application appears functional at first glance, users encounter a "
        "\"broken\" experience primarily due to three invisible failure points:<br/>"
        "1. <b>The App Looks Logged-In When It's Actually Logged-Out:</b> When a user's login session expires overnight, "
        "the screen still shows their name and avatar. However, whenever they try to post or like an article, nothing happens. "
        "To the customer, the website feels unresponsive and buggy. We will fix this by instantly guiding users to a clean login screen "
        "with an informative message.<br/>"
        "2. <b>Security Risk in Content Publishing:</b> The current code allows un-sanitized scripts to be saved in articles and comments. "
        "A malicious user could exploit this to compromise visitor accounts. We are installing an industry-standard security filter (DOMPurify) "
        "to neutralize dangerous inputs before they reach users' screens.<br/>"
        "3. <b>Server Connectivity & Silent Spinners:</b> When the backend server experiences a blip or certificate renewal issue, "
        "the web app gets stuck spinning forever instead of notifying the user and offering a one-click 'Retry' option.<br/><br/>"
        "<b>Immediate 3-Step Action Plan:</b><br/>"
        "• <b>Phase 1 (Day 1 - Hotfix):</b> Deploy SSL certificate auto-renewals on backend origin and install global 401 session-expiry handling.<br/>"
        "• <b>Phase 2 (Day 2 - Security Hardening):</b> Integrate DOMPurify across markdown renderers and debounce all publish buttons.<br/>"
        "• <b>Phase 3 (Day 3 - Reliability Automation):</b> Connect n8n synthetic uptime monitoring to ping the application every 5 minutes "
        "with automated alerts to team channels upon latency spikes or outages."
    )
    story.append(Paragraph(stakeholder_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF Generated Successfully]: {filename}")

def build_docx(filename="Task1_QA_Report_Aditya_Kavde.docx"):
    doc = docx.Document()
    
    # Page setup - 0.5 in margins
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
    
    # Title
    t = doc.add_paragraph()
    r = t.add_run("Task 1 — Web App QA & Debug Report")
    r.font.name = 'Calibri'
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    sub = doc.add_paragraph()
    r_sub = sub.add_run("Systematic Quality Audit of AI-Built (\"Vibe-Coded\") RealWorld Conduit Application")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    
    # Metadata Table
    meta = doc.add_table(rows=2, cols=3)
    meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        [("Candidate:", " Aditya Kavde"), ("Role:", " Automation & QA Developer"), ("Date:", " November 2026")],
        [("Target System:", " RealWorld Conduit App"), ("Audit Scope:", " Auth, Feeds, CRUD, Security, API"), ("Status:", " Completed (6 Bugs Filed)")]
    ]
    for r_idx, row in enumerate(meta.rows):
        for c_idx, cell in enumerate(row.cells):
            label, val = meta_info[r_idx][c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            run_lbl = p.add_run(label)
            run_lbl.bold = True
            run_lbl.font.size = Pt(9)
            run_val = p.add_run(val)
            run_val.font.size = Pt(9)
            
            # Set background color
            tcPr = cell._tc.get_or_add_tcPr()
            shd = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
            tcPr.append(shd)
            
    doc.add_paragraph() # Spacing
    
    # Section 1
    h1 = doc.add_paragraph()
    r1 = h1.add_run("1. Executive Summary & Audit Overview")
    r1.font.bold = True
    r1.font.size = Pt(14)
    r1.font.color.rgb = RGBColor(30, 58, 138)
    
    p_exec = doc.add_paragraph()
    p_exec.paragraph_format.line_spacing = 1.15
    p_exec.add_run(
        "During this 75-minute quality assurance investigation, we audited the end-to-end user flows of the RealWorld "
        "Conduit application (representing typical AI-assisted \"vibe-coded\" SaaS apps). The evaluated flows include "
        "Account Registration, Authentication, Global/Personal Feed Streaming, Article Authoring (CRUD), Markdown Parsing, "
        "Social Interactions (Favoriting/Comments), and Session Teardown.\n\n"
        "Core Findings: While the initial visual layout renders smoothly, the underlying application suffers from severe architectural "
        "deficiencies characteristic of vibe-coded software: (1) brittle origin infrastructure without SSL certificate lifecycle automation, "
        "(2) silent error swallowing leading to permanent loading states, (3) severe Stored Cross-Site Scripting (XSS) via un-sanitized HTML rendering, "
        "(4) form schema mismatches blocking validation feedback, (5) desynchronized client-side auth tokens causing \"ghost login\" traps, and "
        "(6) race conditions from un-throttled event triggers. A total of 6 critical issues were documented below."
    )
    
    # Section 2: Bug Table
    h2 = doc.add_paragraph()
    r2 = h2.add_run("2. Bug Report Table (Formal Template)")
    r2.font.bold = True
    r2.font.size = Pt(14)
    r2.font.color.rgb = RGBColor(30, 58, 138)
    
    table_headers = ["#", "Title / Summary", "Steps to Reproduce", "Expected vs Actual", "Severity", "Suspected Cause"]
    bug_rows = [
        (
            "BUG-01",
            "Production Origin Outage: Expired SSL Certificate & Orphaned Demo CNAME",
            "1. Navigate to https://demo.realworld.io.\n2. Observe HTTP 404 response.\n3. Navigate to active frontend mirror.\n4. Open DevTools Console/Network.\n5. Observe /api network requests failing.",
            "Expected: Public demo URL resolves and API calls establish secure TLS connection.\nActual: Demo URL returns 404; backend endpoints fail with NET::ERR_CERT_DATE_INVALID (expired SSL) and HTTP 530.",
            "Critical",
            "Orphaned GitHub Pages DNS record and unmonitored Let's Encrypt / ACME certbot renewal failure on backend origin."
        ),
        (
            "BUG-02",
            "Silent Rejection: Infinite Loading Spinner on API Failure",
            "1. Open application home page.\n2. Simulate network offline or block /api/articles in DevTools.\n3. Observe the Global Feed area.",
            "Expected: Graceful failure with alert banner: \"Unable to load feed. [Retry]\" after 5s timeout.\nActual: Application hangs indefinitely showing \"Loading articles...\". No error toast, retry button, or fallback.",
            "Critical",
            "Unhandled promise rejection in store/dispatcher. isLoading set to true on request, but catch block never resets flag or populates error state."
        ),
        (
            "BUG-03",
            "Security Vulnerability: Stored XSS in Article Body & Comments via Raw Markdown",
            "1. Log in and navigate to /editor.\n2. In Article Body, input: <img src=x onerror=\"alert('XSS')\">.\n3. Publish article and view at /article/:slug.",
            "Expected: Markdown parser sanitizes raw HTML and strips malicious script attributes (DOMPurify).\nActual: JavaScript executes immediately in the reader's browser context via unescaped v-html / dangerouslySetInnerHTML.",
            "Critical",
            "Vibe-coded renderer passes raw converted markdown directly into DOM without HTML sanitization or CSP restrictions."
        ),
        (
            "BUG-04",
            "Broken Form Validation: Duplicate Registration Silently Freezes UI",
            "1. Open /register.\n2. Enter existing username/email.\n3. Click \"Sign up\".\n4. Observe form submit button.",
            "Expected: Form highlights invalid input with contextual error message (\"Email has already been taken\").\nActual: Button enters permanent disabled/loading state. Server 422 JSON is received but swallowed without UI rendering.",
            "High",
            "API contract mismatch: backend returns { errors: { email: [...] } }, while frontend template expects flat string res.data.message."
        ),
        (
            "BUG-05",
            "Ghost Authentication: Session Expiry Traps User in Broken Logged-In State",
            "1. Log in successfully (JWT stored in localStorage).\n2. Allow JWT to expire or invalidate token.\n3. Refresh page.\n4. Attempt to Publish Article or Favorite a post.",
            "Expected: 401 response triggers automatic session purge, toast warning (\"Session expired\"), and redirect to /login.\nActual: Navbar shows user logged in, but actions fail silently with console 401 errors. User cannot interact.",
            "High",
            "Auth state initialization checks only token existence (!!localStorage.getItem('jwt')) rather than cryptographic validity, lacking 401 HTTP response interceptor."
        ),
        (
            "BUG-06",
            "Race Condition: Duplicate Article Creation via Rapid Button Double-Click",
            "1. Fill out \"New Article\" form.\n2. Rapidly double-click or multi-click \"Publish Article\" within 200ms.\n3. Inspect Global Feed.",
            "Expected: Submit button immediately disables on first click, throttling/debouncing additional events.\nActual: Multiple simultaneous POST /api/articles dispatches succeed, generating duplicate database records with identical content.",
            "Medium",
            "Lack of UI debounce/throttle handler and missing client-side disabled={isSubmitting} directive on submit button."
        )
    ]
    
    table = doc.add_table(rows=len(bug_rows) + 1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header format
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(table_headers):
        hdr_cells[i].text = title
        p = hdr_cells[i].paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        shd = parse_xml(r'<w:shd {} w:fill="1E3A8A"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
        
    for r_idx, bug in enumerate(bug_rows):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(bug):
            row_cells[c_idx].text = val
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.runs[0].font.size = Pt(8)
            if c_idx == 0:
                p.runs[0].font.bold = True
            if c_idx == 4:
                p.runs[0].font.bold = True
                if val == "Critical":
                    p.runs[0].font.color.rgb = RGBColor(220, 38, 38)
                elif val == "High":
                    p.runs[0].font.color.rgb = RGBColor(234, 88, 12)
                else:
                    p.runs[0].font.color.rgb = RGBColor(217, 119, 6)
            
            # Alternating background
            if r_idx % 2 == 1:
                shd = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
                row_cells[c_idx]._tc.get_or_add_tcPr().append(shd)

    doc.add_page_break()
    
    # Section 3: Root-Cause Analysis
    h3 = doc.add_paragraph()
    r3 = h3.add_run("3. In-Depth Root-Cause Analysis (Focus Issue: BUG-05)")
    r3.font.bold = True
    r3.font.size = Pt(14)
    r3.font.color.rgb = RGBColor(30, 58, 138)
    
    sub3 = doc.add_paragraph()
    r_sub3 = sub3.add_run("Target Issue: Ghost Authentication & Session Expiry Desynchronization")
    r_sub3.font.bold = True
    r_sub3.font.size = Pt(11)
    
    rca_p = doc.add_paragraph()
    rca_p.paragraph_format.line_spacing = 1.15
    rca_sentences = [
        ("Sentence 1 (Phenomenon): ", "When an authenticated user's JSON Web Token (JWT) expires on the server, the client-side single-page application continues to display the authenticated navbar (username, avatar, and 'New Article' button) instead of reverting to the guest state.\n"),
        ("Sentence 2 (Impact): ", "As a direct consequence, every subsequent mutation attempted by the user—such as publishing articles, submitting comments, or favoriting posts—fails silently in the background with HTTP 401 Unauthorized errors.\n"),
        ("Sentence 3 (Root Cause 1): ", "This defect occurs because the authentication state store naively performs a truthy existence check (Boolean(localStorage.getItem('token'))) upon application bootstrap, erroneously assuming that the physical presence of a token string implies cryptographic validity.\n"),
        ("Sentence 4 (Root Cause 2): ", "The AI-assisted code generation omitted JWT client-side payload inspection, meaning the application never decodes the standard exp (expiration) timestamp claim before rendering authenticated UI components.\n"),
        ("Sentence 5 (Root Cause 3): ", "Furthermore, the global HTTP client (Axios/Fetch instance) completely lacks a centralized response interceptor capable of catching HTTP 401/403 status codes emitted by the backend origin.\n"),
        ("Sentence 6 (Fix Step 1): ", "To permanently resolve this defect, we must configure a global Axios response interceptor that automatically intercepts any 401 response, dispatches a centralized AUTH_LOGOUT store action, and purges the invalid token and user metadata from localStorage.\n"),
        ("Sentence 7 (Fix Step 2): ", "Concurrently, the interceptor must trigger an atomic programmatic redirection to the /login route while appending the user's intended target route as a query parameter (e.g., /login?redirect=/editor).\n"),
        ("Sentence 8 (Fix Step 3): ", "Finally, a non-blocking toast notification banner must be displayed informing the user that their security session has expired, providing a transparent, polished, and secure authentication lifecycle.")
    ]
    for prefix, body in rca_sentences:
        r_pre = rca_p.add_run(prefix)
        r_pre.bold = True
        r_b = rca_p.add_run(body)
        
    # Section 4: Non-Technical Stakeholder Briefing
    h4 = doc.add_paragraph()
    r4 = h4.add_run("4. Non-Technical Stakeholder Briefing")
    r4.font.bold = True
    r4.font.size = Pt(14)
    r4.font.color.rgb = RGBColor(30, 58, 138)
    
    p_stake = doc.add_paragraph()
    p_stake.paragraph_format.line_spacing = 1.15
    p_stake.add_run(
        "Executive Summary for Founders & Product Leadership:\n\n"
        "Our audit discovered that while the application appears functional at first glance, users encounter a \"broken\" experience primarily due to three invisible failure points:\n"
        "1. The App Looks Logged-In When It's Actually Logged-Out: When a user's login session expires overnight, the screen still shows their name and avatar. However, whenever they try to post or like an article, nothing happens. To the customer, the website feels unresponsive and buggy. We will fix this by instantly guiding users to a clean login screen with an informative message.\n"
        "2. Security Risk in Content Publishing: The current code allows un-sanitized scripts to be saved in articles and comments. A malicious user could exploit this to compromise visitor accounts. We are installing an industry-standard security filter (DOMPurify) to neutralize dangerous inputs before they reach users' screens.\n"
        "3. Server Connectivity & Silent Spinners: When the backend server experiences a blip or certificate renewal issue, the web app gets stuck spinning forever instead of notifying the user and offering a one-click 'Retry' option.\n\n"
        "Immediate 3-Step Action Plan:\n"
        "• Phase 1 (Day 1 - Hotfix): Deploy SSL certificate auto-renewals on backend origin and install global 401 session-expiry handling.\n"
        "• Phase 2 (Day 2 - Security Hardening): Integrate DOMPurify across markdown renderers and debounce all publish buttons.\n"
        "• Phase 3 (Day 3 - Reliability Automation): Connect n8n synthetic uptime monitoring to ping the application every 5 minutes with automated alerts to team channels upon latency spikes or outages."
    )
    
    doc.save(filename)
    print(f"[DOCX Generated Successfully]: {filename}")

if __name__ == "__main__":
    build_pdf()
    build_docx()
