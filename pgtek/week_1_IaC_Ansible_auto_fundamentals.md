### 🗓️ WEEK 1 — IaC, Ansible, and Automation Fundamentals
This week builds the foundation for everything else. The goal is to understand *why* automation works the way it does, not just *how* to run commands.

---

## 🎯 Core Concepts

### Declarative vs Imperative Automation
- **Imperative automation**
  - You describe *how* to do something step by step
  - Example: “Install package X, then edit file Y, then restart service Z”
  - Common in shell scripts and ad-hoc commands
  - Fragile if steps fail or are run multiple times

- **Declarative automation**
  - You describe the *desired end state*
  - Example: “Package X should be installed and service Z should be running”
  - The tool figures out how to reach that state
  - Ansible is primarily declarative

- **Why this matters**
  - Declarative systems are easier to reason about
  - They scale better and reduce human error
  - They naturally support idempotency

---

### Idempotency
- **Definition**
  - An operation is idempotent if running it multiple times produces the same result
  - Example: Installing a package that’s already installed does nothing

- **In Ansible**
  - Most modules are idempotent by design
  - Tasks check the current state before making changes
  - Ansible reports `changed` vs `ok`

- **Why it matters**
  - Safe re-runs
  - Enables continuous configuration enforcement
  - Reduces outages caused by repeated automation

---

### Configuration Drift
- **What it is**
  - When a system’s actual state diverges from its intended configuration
  - Caused by manual changes, hotfixes, or emergency edits

- **Why it’s dangerous**
  - Makes environments inconsistent
  - Bugs become hard to reproduce
  - Breaks trust in automation

- **How IaC helps**
  - Infrastructure and configuration are defined in code
  - Re-running automation restores the desired state
  - Drift becomes detectable and reversible

---

### Infrastructure-as-Code (IaC) Principles
- Infrastructure is:
  - **Version controlled**
  - **Repeatable**
  - **Reviewable**
  - **Testable**

- Treat infrastructure like application code
- Enables:
  - Peer review
  - Rollbacks
  - CI/CD pipelines
  - Auditing and compliance

---

## 🧱 Ansible Architecture

### Playbooks
- YAML files that define:
  - Hosts to target
  - Tasks to run
  - Variables and roles to apply
- Top-level orchestration layer

---

### Tasks
- The smallest unit of work in Ansible
- Each task:
  - Uses a module
  - Describes a desired state
- Example actions:
  - Install a package
  - Create a file
  - Start a service

---

### Roles
- A standardized way to organize Ansible content
- Improve reusability and readability
- Typical structure:
  - `tasks/`
  - `handlers/`
  - `templates/`
  - `files/`
  - `vars/`
  - `defaults/`
  - `meta/`

- Roles allow:
  - Separation of concerns
  - Easier sharing across projects
  - Cleaner playbooks

---

### Handlers
- Special tasks triggered by changes
- Only run when notified
- Common use cases:
  - Restarting services
  - Reloading configurations

- Example logic:
  - Update config file → notify handler → restart service

---

### Inventories
- Define *which* systems Ansible manages
- Can be:
  - Static (INI or YAML)
  - Dynamic (cloud providers, scripts, APIs)

- Group hosts logically:
  - By environment
  - By role
  - By region

---

### Jinja2 Templates
- Used to generate dynamic configuration files
- Allow:
  - Variables
  - Conditionals
  - Loops

- Templates end in `.j2`
- Rendered on the target system
- Essential for managing environment-specific configs

---

### Ansible Vault
- Encrypts sensitive data:
  - Passwords
  - API keys
  - Secrets

- Allows secrets to live safely in version control
- Can encrypt:
  - Entire files
  - Individual variables

- Best practice:
  - Separate secrets from logic
  - Never hardcode credentials

---

## 🛠️ Hands-On Tasks

### Write a Simple Ansible Playbook
Your playbook should:
- Install a package
- Configure a service
- Use a handler
- Use a Jinja2 template

Focus on:
- Clean task naming
- Idempotent behavior
- Clear structure

---

### Create a Role and Refactor
- Convert your playbook into a role
- Move:
  - Tasks into `tasks/main.yml`
  - Templates into `templates/`
  - Handlers into `handlers/main.yml`
- Keep the playbook minimal by calling the role

---

### Use Ansible Vault
- Encrypt at least one variable
- Practice:
  - Creating a vault file
  - Editing encrypted content
  - Running playbooks with vault passwords

---

### Run Ansible Locally
- Target:
  - A local VM, container, or localhost
- Use this to:
  - Iterate quickly
  - Break things safely
  - Learn by experimentation

---

## 🗣️ Interview Prep

### Be Able to Explain:

#### “What is idempotency and why does it matter?”
- Emphasize safety, repeatability, and consistency
- Connect it to production reliability

---

#### “How do you structure an Ansible role?”
- Explain the standard directory layout
- Highlight separation of concerns
- Mention reuse and scalability

---

#### “How do you test IaC before deploying it?”
- Syntax checks
- Dry runs
- Local testing
- CI pipelines
- Incremental rollouts

---

### 🎯 Outcome
- You understand *why* automation works
- You can reason about system state
- You sound polished and professional when discussing Ansible and IaC
- This foundation will support all future DevOps and platform work
