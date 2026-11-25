import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Page Margins Setup (1 inch all around for standard academic & industry specifications)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper Functions
def add_custom_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    for run in h.runs:
        run.font.color.rgb = RGBColor(16, 44, 87)
    return h

def set_cell_border_and_shading(cell, color="1F4E79", sz="12", val="single", bg_color="F2F4F7"):
    """Applies clean vector borders and background shading tint to a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
    tcPr.append(shd)

    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def add_diagram_box(doc, title, subtitle="", bg_color="F4F6F9", border_color="1F4E79"):
    """Creates a standalone bordered architecture box for workflow visualization."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)

    set_cell_border_and_shading(cell, color=border_color, sz="12", bg_color=bg_color)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(3)

    run_title = p.add_run(title)
    run_title.bold = True
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor(16, 44, 87)

    if subtitle:
        p2 = cell.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(5)
        run_sub = p2.add_run(subtitle)
        run_sub.font.size = Pt(8.5)
        run_sub.font.color.rgb = RGBColor(80, 80, 80)

def add_arrow(doc, label=""):
    """Creates a styled downward connector arrow with pipeline context."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)

    if label:
        r_label = p.add_run(f"[{label}]\n")
        r_label.font.size = Pt(8)
        r_label.font.color.rgb = RGBColor(100, 100, 100)

    r_arrow = p.add_run("↓")
    r_arrow.bold = True
    r_arrow.font.size = Pt(12)
    r_arrow.font.color.rgb = RGBColor(31, 78, 121)

def add_bullet_item(doc, text, bold_prefix=""):
    """Adds a bullet point with justified alignment."""
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.25
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.bold = True
        r_bold.font.color.rgb = RGBColor(16, 44, 87)
    p.add_run(text)
    return p

# ==============================================================================
# PAGE 1: COVER & TITLE
# ==============================================================================
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = title.add_run("PROJECT SYNOPSIS\n\nCloud DevOps & SRE Lifecycle Implementation Plan for AI Investment Research Suite\n")
run_title.bold = True
run_title.font.size = Pt(20)
run_title.font.color.rgb = RGBColor(16, 44, 87)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = sub.add_run("An End-to-End Infrastructure, Automation, Security, and Observability Blueprint\nSpanning AWS, Docker, Terraform, CloudFormation, Jenkins DevSecOps, Prometheus, and Grafana\n\n\n")
run_sub.font.size = Pt(12)
run_sub.italic = True

meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.add_run("Submitted in partial fulfillment of the requirements for the degree of\nBachelor of Technology / Master of Technology in Computer Science & Engineering\n\n")
meta.add_run("Academic Session: 2026–2027\n\n")
meta.paragraph_format.line_spacing = 1.3

# Textbooks & References Summary Box on Cover Page
add_diagram_box(
    doc,
    title="PRESCRIBED TEXTBOOKS & REFERENCE MANUALS",
    subtitle=(
        "• Cloud Computing: Concepts, Technology, Security & Architecture by Thomas Erl (Pearson)\n"
        "• Continuous Delivery and DevOps: A Quickstart Guide by Paul Swartout (Shroff)\n"
        "• Cloud Security Handbook by Eyal Estrin (Packt Publishing)"
    ),
    bg_color="F9FAFC",
    border_color="1F4E79"
)

doc.add_page_break()

# ==============================================================================
# PAGE 2: ABSTRACT & INTRODUCTION
# ==============================================================================
add_custom_heading("1. Abstract", 1)
p_abs = doc.add_paragraph(
    "Modern financial platforms demand high operational availability, rapid deployment cycles, zero-downtime releases, "
    "and real-time system monitoring. The AI Investment Research Suite is an enterprise multi-agent market intelligence application "
    "that ingests financial data, headlines, and metrics to execute multi-agent investment evaluation graphs. "
    "This synopsis presents a comprehensive operational blueprint to transition the suite from a local container environment to a fully "
    "automated, cloud-native DevOps lifecycle. The proposed architecture incorporates AWS cloud infrastructure (VPC, EC2, IAM, Lambda), "
    "Infrastructure as Code (IaC using Terraform and AWS CloudFormation), containerization and registry workflows (Docker & Docker Hub), "
    "automated CI/CD with integrated security scanning (Jenkins DevSecOps & Trivy), full-stack infrastructure telemetry (Prometheus & Node Exporter), "
    "operational dashboards (Grafana), and cloud financial governance (AWS Cost Explorer & AWS Budgets)."
)
p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_abs.paragraph_format.line_spacing = 1.3

add_custom_heading("2. Introduction & Operational Context", 1)
p_intro = doc.add_paragraph(
    "In financial intelligence systems, operational downtime or insecure deployments can cause critical data gaps and revenue loss. "
    "While modern applications run seamlessly in local Docker environments, enterprise production demands automated provisioning, "
    "role-based access control, security vulnerability checks, and real-time observability. "
    "Applying structured DevOps practices bridges the gap between software development and cloud operations. "
    "Grounded in core cloud architecture principles (Erl, 2013), continuous delivery pipelines (Swartout, 2014), and cloud security controls (Estrin, 2022), "
    "this project outlines the step-by-step roadmap to deploy, manage, monitor, and optimize the AI Investment Research application across AWS and cloud-native toolchains."
)
p_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_intro.paragraph_format.line_spacing = 1.3

doc.add_page_break()

# ==============================================================================
# PAGE 3: PROBLEM STATEMENT & DEVOPS EXPERIMENTS MAP
# ==============================================================================
add_custom_heading("3. Problem Statement", 1)
p_prob = doc.add_paragraph(
    "Deploying complex multi-service applications without a formal DevOps pipeline introduces significant operational bottlenecks:"
)
p_prob.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_prob.paragraph_format.line_spacing = 1.3

add_bullet_item(doc, "Provisioning cloud servers manually leads to unpinned dependencies, security misconfigurations, and environment mismatch.", "Configuration Drift & Manual Setup: ")
add_bullet_item(doc, "Pushing application updates without automated SAST audits or container vulnerability scans increases threat exposure.", "Lack of Automated Quality & Security Gates: ")
add_bullet_item(doc, "Running microservices without active metric collection prevents proactive detection of CPU, memory, or network bottlenecks.", "Unmonitored Infrastructure: ")
add_bullet_item(doc, "Deploying cloud workloads without resource tagging, budgeting alerts, or rightsizing strategies leads to cost overruns.", "Uncontrolled Cloud Expenditure: ")

p_prob_obj = doc.add_paragraph(
    "Core Objective: To design and codify a complete, automated DevOps pipeline covering infrastructure provisioning, security hardening, CI/CD, monitoring, and cost management for the AI Investment Research application."
)
p_prob_obj.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_prob_obj.paragraph_format.space_before = Pt(6)
p_prob_obj.paragraph_format.line_spacing = 1.3

add_custom_heading("4. Comprehensive List of DevOps Practicals & Implementation Scope", 1)
p_prac_intro = doc.add_paragraph(
    "The operational plan is structured into 11 core practical modules directly aligned with the DevOps curriculum:"
)
p_prac_intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_prac_intro.paragraph_format.line_spacing = 1.3

add_bullet_item(doc, "Provision custom VPC, public/private subnets, Security Groups, connect remotely via SSH/RDP, install Apache/Nginx web servers, deploy application, and verify public IP accessibility.", "AWS EC2 & VPC Networking Setup: ")
add_bullet_item(doc, "Create IAM users, groups, roles, and custom JSON policies. Configure Multi-Factor Authentication (MFA), enforce least-privilege permissions, test role assumption (STS AssumeRole), and verify RBAC.", "AWS IAM Governance & RBAC: ")
add_bullet_item(doc, "Design and deploy CloudFormation templates to provision cloud stacks, update stack configurations, validate template changes, perform automated rollbacks on failure, and benchmark against Terraform.", "Infrastructure as Code via AWS CloudFormation: ")
add_bullet_item(doc, "Build multi-stage Docker images for the web application, execute containers, expose required ports, push images to Docker Hub, pull onto target host environments, and manage container lifecycles.", "Docker Containerization & Registry Lifecycle: ")
add_bullet_item(doc, "Install Terraform, write modular .tf configuration files to provision EC2 instances and S3 storage, execute init/validate/plan/apply lifecycle, manage terraform.tfstate, and execute clean infrastructure destruction.", "Declarative IaC with Terraform: ")
add_bullet_item(doc, "Deploy Jenkins server, integrate GitHub webhooks for push triggers, configure automated build and test pipelines, and execute automatic deployments upon successful stage completion.", "Automated CI/CD Pipeline with Jenkins & GitHub: ")
add_bullet_item(doc, "Integrate static code analysis, vulnerability scanning of Docker images using Trivy, secure secret management (Jenkins Credentials & AWS Secrets Manager), and generate security assessment reports.", "DevSecOps Integration in Jenkins: ")
add_bullet_item(doc, "Deploy Prometheus, install Node Exporter on host instances, collect CPU, memory, disk, and network metrics, define alert rules (alert.rules.yml), and validate alert triggers.", "Infrastructure Monitoring with Prometheus: ")
add_bullet_item(doc, "Deploy Grafana, integrate Prometheus as a data source, design operational monitoring dashboards, visualize system utilization, and analyze trend metrics under load.", "Visual Analytics & Dashboards with Grafana: ")
add_bullet_item(doc, "Develop serverless functions using AWS Lambda, integrate with API Gateway endpoints, execute event tests, inspect execution logs in CloudWatch, and evaluate latency/cost metrics.", "Serverless Architecture with AWS Lambda & CloudWatch: ")
add_bullet_item(doc, "Analyze AWS Cost Explorer and billing reports, implement resource tagging and rightsizing strategies, configure AWS Budgets with automated alert notifications, and identify idle cloud assets.", "Cloud Cost Governance & Optimization: ")

doc.add_page_break()

# ==============================================================================
# PAGE 4: PARADIGM SHIFT & TECH STACK MAPPING
# ==============================================================================
add_custom_heading("5. Paradigm Comparison: Manual vs. Automated DevOps Lifecycle", 1)

# Table Caption ABOVE the table
p_tbl1_cap = doc.add_paragraph()
p_tbl1_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_tbl1_cap.paragraph_format.space_before = Pt(4)
p_tbl1_cap.paragraph_format.space_after = Pt(4)
r_t1 = p_tbl1_cap.add_run("Table 1: Paradigm Comparison: Manual vs. Automated DevOps Implementation")
r_t1.bold = True
r_t1.font.size = Pt(10)
r_t1.font.color.rgb = RGBColor(16, 44, 87)

table_comp = doc.add_table(rows=1, cols=3)
table_comp.style = 'Table Grid'
hdr = table_comp.rows[0].cells
hdr[0].text = "Lifecycle Phase"
hdr[1].text = "Traditional / Manual Approach"
hdr[2].text = "Proposed DevOps Implementation"
for cell in hdr:
    cell.paragraphs[0].runs[0].bold = True

rows_data = [
    ("Infrastructure Provisioning", "Manual ClickOps console setup", "Terraform & CloudFormation declarative templates"),
    ("Access Governance", "Shared root credentials, plain keys", "IAM RBAC, MFA enforcement, STS Role Assumption"),
    ("Application Packaging", "Unpinned host-level runtime dependencies", "Docker containerization & Docker Hub registry delivery"),
    ("Deployment & Delivery", "Manual SSH git pull & manual restart", "Jenkins CI/CD automated pipeline via GitHub Webhooks"),
    ("Security Auditing", "Post-incident manual code reviews", "DevSecOps stage: Trivy container scanning & secret scans"),
    ("System Telemetry", "Flat-file log inspecting after failure", "Prometheus metric scraping & Grafana visualization dashboards"),
    ("Serverless Extension", "Dedicated idle server background jobs", "Event-driven AWS Lambda functions & CloudWatch logs"),
    ("Cost Optimization", "Unchecked monthly cloud bill invoices", "AWS Cost Explorer analysis & AWS Budgets threshold alerts")
]
for phase, manual, devops in rows_data:
    row = table_comp.add_row().cells
    row[0].text = phase
    row[1].text = manual
    row[2].text = devops
    for c in row:
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

doc.add_paragraph().paragraph_format.space_after = Pt(8)

add_custom_heading("6. Technology Stack & Toolchain Alignment", 1)

add_bullet_item(doc, "AWS EC2, Custom VPC, Security Groups, Internet Gateways, Route Tables", "Cloud Compute & Networking: ")
add_bullet_item(doc, "AWS IAM (Users, Groups, Roles, Custom Policies, MFA, RBAC)", "Security & Identity: ")
add_bullet_item(doc, "Terraform (0.15+), AWS CloudFormation (YAML/JSON templates)", "Infrastructure as Code: ")
add_bullet_item(doc, "Docker Engine, Dockerfiles, Docker Compose, Docker Hub Registry", "Containerization: ")
add_bullet_item(doc, "Jenkins, GitHub Webhooks, Trivy Vulnerability Scanner, SAST toolchains", "CI/CD & DevSecOps: ")
add_bullet_item(doc, "Prometheus, Node Exporter, Grafana, Alertmanager", "Telemetry & Monitoring: ")
add_bullet_item(doc, "AWS Lambda, Amazon API Gateway, AWS CloudWatch", "Serverless & Logs: ")
add_bullet_item(doc, "AWS Cost Explorer, AWS Budgets, AWS Resource Tags", "Financial & Cost Governance: ")

doc.add_page_break()

# ==============================================================================
# PAGE 5: ARCHITECTURE DIAGRAM (MATCHING DRAW.IO FLOWCHART)
# ==============================================================================
add_custom_heading("7. End-to-End DevOps Architecture Flowchart", 1)
p_arch_desc = doc.add_paragraph(
    "The flowchart below outlines the integration of all 11 practical modules across source control, CI/CD pipelines, "
    "cloud infrastructure provisioning, serverless components, telemetry collectors, and cost governance."
)
p_arch_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_arch_desc.paragraph_format.line_spacing = 1.3

# Node 1
add_diagram_box(
    doc,
    title="1. Source Control & Git Workflow",
    subtitle="GitHub Repository, Automated Webhooks, Commit Event Triggers",
    bg_color="EBF1F5",
    border_color="2F5597"
)

add_arrow(doc)

# Node 2
add_diagram_box(
    doc,
    title="2. Jenkins CI/CD & DevSecOps Pipeline",
    subtitle="Automated Build -> Docker Hub Push",
    bg_color="F2F4F7",
    border_color="1F4E79"
)

add_arrow(doc)

# Node 3
add_diagram_box(
    doc,
    title="3. Infrastructure As Code (Terraform & CloudFormation)",
    subtitle="VPC Network Provisioning, EC2 Instance, S3 Buckets, etc",
    bg_color="EAECEF",
    border_color="1F4E79"
)

add_arrow(doc)

# Node 4
add_diagram_box(
    doc,
    title="4. Cloud Runtime & Serverless Layer (AWS)",
    subtitle="EC2 Containers (Docker), NGINX Web Server, API Gateway",
    bg_color="F7F9FB",
    border_color="2E75B6"
)

add_arrow(doc)

# Node 5
add_diagram_box(
    doc,
    title="5. Telemetry & Cost Governance Layer",
    subtitle="Prometheus, Grafana, AWS Cost Explorer",
    bg_color="EBF1F5",
    border_color="1F4E79"
)

# Flowchart Name / Caption BELOW the flowchart
p_fig_cap = doc.add_paragraph()
p_fig_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fig_cap.paragraph_format.space_before = Pt(8)
p_fig_cap.paragraph_format.space_after = Pt(12)
r_fig = p_fig_cap.add_run("Figure 1: End-to-End DevOps Architecture Flowchart")
r_fig.bold = True
r_fig.italic = True
r_fig.font.size = Pt(9.5)
r_fig.font.color.rgb = RGBColor(16, 44, 87)

doc.add_page_break()

# ==============================================================================
# PAGE 6: PHASED IMPLEMENTATION ROADMAP & REFERENCES
# ==============================================================================
add_custom_heading("8. Phased Execution Roadmap", 1)

# Table Caption ABOVE the table
p_tbl2_cap = doc.add_paragraph()
p_tbl2_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_tbl2_cap.paragraph_format.space_before = Pt(4)
p_tbl2_cap.paragraph_format.space_after = Pt(4)
r_t2 = p_tbl2_cap.add_run("Table 2: Phased Execution Roadmap & Deliverables")
r_t2.bold = True
r_t2.font.size = Pt(10)
r_t2.font.color.rgb = RGBColor(16, 44, 87)

table_plan = doc.add_table(rows=1, cols=3)
table_plan.style = 'Table Grid'
h_plan = table_plan.rows[0].cells
h_plan[0].text = "Phase"
h_plan[1].text = "DevOps Practical Domain"
h_plan[2].text = "Planned Milestone & Deliverables"
for c in h_plan:
    c.paragraphs[0].runs[0].bold = True

phases = [
    ("Phase 1", "AWS Core & Networking", "Deploy VPC, Subnets, Security Groups, EC2 instance with Nginx/Apache."),
    ("Phase 2", "Identity & Access Control", "Configure IAM Users, Roles, Custom Policies, MFA, and test RBAC authorization."),
    ("Phase 3", "Containerization & Registry", "Build Docker images, test local execution, push to Docker Hub & test remote pull."),
    ("Phase 4", "Infrastructure as Code", "Develop CloudFormation and Terraform templates for EC2 & S3; test state & destroy."),
    ("Phase 5", "CI/CD & DevSecOps", "Deploy Jenkins, configure GitHub webhooks, integrate Trivy scanning & auto-deploy."),
    ("Phase 6", "Telemetry & Analytics", "Deploy Prometheus & Node Exporter; design custom Grafana monitoring dashboards."),
    ("Phase 7", "Serverless & Governance", "Implement AWS Lambda & API Gateway; configure AWS Budgets alerts & Cost Explorer.")
]
for p_id, p_dom, p_del in phases:
    r = table_plan.add_row().cells
    r[0].text = p_id
    r[1].text = p_dom
    r[2].text = p_del
    for c in r:
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

doc.add_paragraph().paragraph_format.space_after = Pt(8)

add_custom_heading("9. Expected Educational & Technical Outcomes", 1)

add_bullet_item(doc, "Complete codification of cloud assets using Terraform and CloudFormation.", "Automated Infrastructure Provisioning: ")
add_bullet_item(doc, "Continuous delivery with security audits (SAST & container image scans) integrated seamlessly.", "Secure CI/CD Pipeline: ")
add_bullet_item(doc, "Active monitoring of infrastructure health, CPU/memory metrics, and system alert generation.", "Full-Stack Telemetry: ")
add_bullet_item(doc, "Governance frameworks using AWS Budgets and Cost Explorer to maintain low operational expenses.", "Cloud Cost Efficiency: ")

add_custom_heading("10. Textbooks & Reference Literature", 1)

add_bullet_item(doc, "Erl, T. (2013). Cloud Computing: Concepts, Technology, Security & Architecture. Pearson Education India.")
add_bullet_item(doc, "Swartout, P. (2014). Continuous Delivery and DevOps: A Quickstart Guide. Shroff Publishers & Distributors Pvt. Ltd.")
add_bullet_item(doc, "Estrin, E. (2022). Cloud Security Handbook. Packt Publishing.")
add_bullet_item(doc, "HashiCorp Terraform Documentation (2026). Infrastructure as Code Best Practices. https://developer.hashicorp.com/terraform")
add_bullet_item(doc, "AWS Documentation (2026). AWS CloudFormation, IAM, EC2, Lambda, and Cost Explorer User Guides. https://docs.aws.amazon.com/")
add_bullet_item(doc, "Prometheus & Grafana Documentation (2026). Monitoring & Dashboarding Guide. https://prometheus.io/docs/")

# Save document
output_path = "C:\\Users\\prabh\\.gemini\\antigravity\\scratch\\investment-research-agent-docker\\AI_Investment_Research_Agent_DevOps_Synopsis.docx"
doc.save(output_path)
print(f"Generated {output_path} successfully!")
