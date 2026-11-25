# Enterprise DevOps & SRE Suite: AI Investment Research Agent

This directory contains the end-to-end production **Infrastructure as Code (IaC)**, **DevSecOps automation**, **AWS IAM RBAC governance**, **Serverless compute**, and **Cloud Cost Governance** toolchains for the AI Investment Research Suite.

---

## Directory Structure

```text
devops/
├── cloudformation/
│   └── infrastructure-stack.yml      # CloudFormation YAML stack (VPC, EC2, S3, IAM, Security Groups)
├── cost-governance/
│   ├── aws-budget.json               # AWS Budgets monthly threshold ($25 cap + 80%/100% email alerts)
│   ├── cleanup-idle-resources.py     # FinOps script auditing orphaned EBS volumes and stopped VMs
│   └── tagging-policy.json           # AWS Organizations mandatory resource tagging policy
├── iam/
│   ├── developer-policy.json         # Least-privilege IAM JSON policy for CI/CD and Developers
│   ├── ec2-s3-access-role.json       # IAM trust relationship for EC2 instance profile
│   ├── sts-assume-role-test.ps1      # PowerShell verification of STS temporary credentials
│   └── sts-assume-role-test.sh       # Bash verification of STS temporary credentials & RBAC
├── jenkins/
│   └── Jenkinsfile.devsecops         # Multi-stage CI/CD pipeline with Trivy & Gitleaks gates
├── scripts/
│   ├── deploy-ec2.sh                 # Zero-downtime SSH remote pull and restart trigger
│   ├── ec2-bootstrap.sh              # Ubuntu 24.04 LTS UserData script (Docker + Compose + Firewall)
│   ├── verify-health.bat             # Windows smoke test for all 5 microservices
│   └── verify-health.sh              # Linux smoke test verifying ports 80, 5005, 9090, 3002
├── security/
│   ├── gitleaks-config.toml          # Secret detection rules for Finnhub, Gemini & AWS keys
│   └── trivy-scan.sh                 # Container image CVE scanner for HIGH/CRITICAL alerts
├── serverless/
│   ├── api-gateway-swagger.yml       # OpenAPI 3.0 specification for API Gateway Lambda proxy
│   ├── cloudwatch-alarms.json        # CloudWatch alarm definitions for Lambda errors & latency
│   └── lambda_function.py            # Python serverless microservice for fast DCF valuation
└── terraform/
    ├── ec2.tf                        # EC2 Ubuntu host with gp3 encrypted storage & UserData
    ├── iam.tf                        # EC2 IAM Role, Instance Profile, and S3 access policy
    ├── outputs.tf                    # Public IP, DNS, URLs, and SSH connection string
    ├── s3.tf                         # S3 bucket for research reports with Glacier lifecycle
    ├── security_groups.tf            # Hardened Security Group rules (22, 80, 443, 5005, 3002, 9090)
    ├── terraform.tfvars.example      # Example variable values
    ├── variables.tf                  # Input parameters (region, CIDR, instance type, key name)
    ├── versions.tf                   # Terraform >= 1.5.0 & AWS Provider ~> 5.0 specifications
    └── vpc.tf                        # Custom VPC, Public Subnet, Internet Gateway & Route Tables
```

---

## 11 DevOps Practical Modules Matrix

| Module | Practical Domain | Primary Implementation File(s) |
| :---: | :--- | :--- |
| **1** | **AWS EC2 & VPC Networking** | [`devops/terraform/vpc.tf`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/terraform/vpc.tf), [`devops/terraform/ec2.tf`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/terraform/ec2.tf), [`devops/scripts/ec2-bootstrap.sh`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/scripts/ec2-bootstrap.sh) |
| **2** | **AWS IAM Governance & RBAC** | [`devops/iam/developer-policy.json`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/iam/developer-policy.json), [`devops/iam/sts-assume-role-test.sh`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/iam/sts-assume-role-test.sh) |
| **3** | **AWS CloudFormation (IaC)** | [`devops/cloudformation/infrastructure-stack.yml`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/cloudformation/infrastructure-stack.yml) |
| **4** | **Docker & Registry Lifecycle** | [`backend/Dockerfile`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/backend/Dockerfile), [`frontend/Dockerfile`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/frontend/Dockerfile), [`docker-compose.prod.yml`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/docker-compose.prod.yml) |
| **5** | **Declarative IaC with Terraform** | Full module in [`devops/terraform/`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/terraform/) |
| **6** | **Automated CI/CD with Jenkins** | [`Jenkinsfile`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/Jenkinsfile) & [`devops/scripts/deploy-ec2.sh`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/scripts/deploy-ec2.sh) |
| **7** | **DevSecOps Integration** | [`devops/jenkins/Jenkinsfile.devsecops`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/jenkins/Jenkinsfile.devsecops), [`devops/security/trivy-scan.sh`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/security/trivy-scan.sh) |
| **8** | **Telemetry via Prometheus** | [`monitoring/prometheus/prometheus.yml`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/monitoring/prometheus/prometheus.yml), [`monitoring/prometheus/alert_rules.yml`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/monitoring/prometheus/alert_rules.yml) |
| **9** | **Visual Dashboards with Grafana** | [`monitoring/grafana/provisioning/`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/monitoring/grafana/provisioning/) |
| **10** | **Serverless Compute with AWS Lambda**| [`devops/serverless/lambda_function.py`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/serverless/lambda_function.py), [`devops/serverless/cloudwatch-alarms.json`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/serverless/cloudwatch-alarms.json) |
| **11** | **Cloud Cost Governance & FinOps** | [`devops/cost-governance/aws-budget.json`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/cost-governance/aws-budget.json), [`devops/cost-governance/cleanup-idle-resources.py`](file:///C:/Users/prabh/.gemini/antigravity/scratch/investment-research-agent-docker/devops/cost-governance/cleanup-idle-resources.py) |

---

## Quickstart Execution Commands

### 1. Provision Infrastructure with Terraform
```bash
cd devops/terraform
cp terraform.tfvars.example terraform.tfvars
# Update ssh_key_name and allowed_ssh_cidr in terraform.tfvars
terraform init
terraform plan
terraform apply -auto-approve
```

### 2. Deploy CloudFormation Stack
```bash
aws cloudformation create-stack \
  --stack-name ai-investment-production-stack \
  --template-body file://devops/cloudformation/infrastructure-stack.yml \
  --parameters ParameterKey=KeyName,ParameterValue=ai-investment-key \
  --capabilities CAPABILITY_IAM
```

### 3. Verify Least-Privilege STS AssumeRole
```bash
# Linux / macOS
bash devops/iam/sts-assume-role-test.sh "arn:aws:iam::<ACCOUNT_ID>:role/ai-investment-ec2-role-prod"

# Windows PowerShell
.\devops\iam\sts-assume-role-test.ps1 -RoleArn "arn:aws:iam::<ACCOUNT_ID>:role/ai-investment-ec2-role-prod"
```

### 4. Execute DevSecOps Container Security Scan
```bash
bash devops/security/trivy-scan.sh prabhatrai05/ai-investment-backend:latest prabhatrai05/ai-investment-frontend:latest
```

### 5. Run Serverless DCF Valuation Microservice Locally
```bash
python devops/serverless/lambda_function.py
```

### 6. Audit Cloud Costs and Orphaned Assets
```bash
python devops/cost-governance/cleanup-idle-resources.py
```

### 7. Run Health Smoke Test
```bash
# Linux
bash devops/scripts/verify-health.sh <EC2_PUBLIC_IP>

# Windows
.\devops\scripts\verify-health.bat <EC2_PUBLIC_IP>
```
