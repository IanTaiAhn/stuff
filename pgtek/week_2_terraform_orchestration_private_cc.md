### 🗓️ WEEK 2 — Terraform, Orchestration Platforms, and Private Cloud Concepts
You don’t need deep Terraform mastery — just enough to speak intelligently and connect infrastructure provisioning to real-world platforms and workflows.

---

## 🎯 Core Concepts

## Terraform Basics

### Providers
- Providers are plugins that allow Terraform to talk to external systems
- Examples:
  - AWS
  - Azure
  - GCP
  - VMware
- A provider defines:
  - What resources are available
  - How Terraform authenticates
- Terraform configs can use multiple providers at once

---

### Resources
- Resources describe **what Terraform creates or manages**
- Examples:
  - Virtual machines
  - Networks
  - Security groups
- Resources are declarative:
  - You describe the desired state
  - Terraform determines what to create, update, or destroy

---

### Variables
- Variables make configurations reusable and flexible
- Used to:
  - Avoid hardcoding values
  - Support multiple environments
- Can be defined:
  - In `variables.tf`
  - Via CLI
  - Via `.tfvars` files

---

### Outputs
- Outputs expose useful information after a run
- Common uses:
  - Displaying IP addresses
  - Passing values to other tools
  - Debugging and visibility
- Outputs do not create resources — they report state

---

### State
- State is how Terraform knows **what already exists**
- Stored in:
  - Local files
  - Remote backends (S3, Terraform Cloud, etc.)
- State tracks:
  - Resource IDs
  - Dependencies
  - Metadata

- Why state matters:
  - Enables idempotency
  - Prevents duplicate resources
  - Allows Terraform to plan safely

---

### Modules
- Modules are reusable Terraform components
- A module is:
  - A collection of resources
  - Parameterized with variables
- Benefits:
  - Reuse
  - Consistency
  - Cleaner configurations
- Root module calls child modules

---

## Cloud Management Platforms (CMPs)

### What a CMP Is
- A layer above raw cloud infrastructure
- Abstracts complexity for users
- Provides:
  - Governance
  - Automation
  - Standardization

- CMPs sit between:
  - Cloud providers
  - End users / developers / ops teams

---

## Morpheus — Conceptual Overview

### Service Catalogs
- A curated list of approved services
- Users choose *what* they want, not *how* it’s built
- Examples:
  - “Linux VM with monitoring”
  - “3-tier application stack”

- Benefits:
  - Consistency
  - Faster provisioning
  - Reduced risk

---

### Blueprints
- Templates that define full environments
- Can include:
  - Compute
  - Network
  - Storage
  - Configuration
- Often built on Terraform, Ansible, or cloud-native tools

---

### Provisioning Workflows
- Automated sequences of steps
- Example workflow:
  - User requests service
  - Policies are checked
  - Infrastructure is provisioned
  - Configuration is applied
  - Access is granted

- Workflows reduce manual intervention

---

### Policy Enforcement
- Rules that control usage and behavior
- Examples:
  - Instance size limits
  - Cost controls
  - Required tags
- Policies enforce guardrails, not blockers

---

### Private Cloud vs Public Cloud
- **Public cloud**
  - Shared infrastructure
  - Pay-as-you-go
  - Highly elastic

- **Private cloud**
  - Dedicated infrastructure
  - More control
  - Often on-prem or hosted

- CMPs often unify both into a **hybrid model**

---

### Tenants, Projects, Quotas, Identity
- **Tenants**
  - Isolated logical environments
  - Represent teams or business units

- **Projects**
  - Subdivisions within a tenant
  - Used for organization and cost tracking

- **Quotas**
  - Resource limits
  - Prevent overconsumption

- **Identity**
  - Authentication and authorization
  - Role-based access control (RBAC)

---

## 🛠️ Hands-On Tasks

### Write a Simple Terraform Configuration
Your config should:
- Create an AWS EC2 instance
- Add a security group
- Output the instance IP

Focus on:
- Clear variable usage
- Clean resource definitions
- Understanding the plan vs appl
