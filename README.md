# Basically a place where I can access my stuff from anywhere since that's what I need.

Very solid url with career advice and such.

https://github.com/fractal-bootcamp/bootcamp-monorepo/tree/main/advice/career

Well I'm in a pickle with what I want to do and say about my rag pipeline...

Should I just make a post about the "live website"?
Even though it's just a static website and it makes calls to a backend fast api that does the rag stuff there.

I had fun with playing around with a local rag pipeline I thought maybe it'd also be fun to try to host it completely for free.

While I did find a "working" solution there were a couple of cavets to my completely "Free" and hosted rag pipeline.

Hugging Face deprecated their embedding/reranker api endpoints in Sept. 2025 so I had to pivot to another free option, Jina API.
This became the biggest limitation since my Jina Api key would only last for one session of frequent use, and then once my free tier of Render powered down Jina API would throttle the key.

I was working with 512MB and 0.1 CPU of processing power on Render (free tier limitations) and I thought maybe I could get away with using sentence_transformers for embeddings/rernaking, but unfortuneatyl, torch is quite large(version I used was 350mb).

The LLM (text generator) was easy since Groq api endpoints are free as long as you don't spam their endpoints.

In the end the hosted Rag pipeline worked faster than my locally hosted rag pipeline, and competely for free, albeit that one slight caveat of it only working once before Jina API key would be throttled and I would need to regenerate a new Jina API key to add into my Render's environment variables.

This prototype showed me how expensive live production is and made me appreciate my covered access to Gemeni Enterprise a little more.
Overall, this was a fun learnign experience and the constraints put on this live rag pipeline prototype made me think outside the box than if I had all the required resources needed right off the bat. 
I really trimmed the fat off of my requirements.txt to have it fit on Render's free tier, and leveraged "free" api endpoints so that my rag pipeline would run.

Refined version:

I was playing around with a local RAG pipeline and thought
"What if I tried to host it completely for free?"

TL;DR: it worked albeit with some caveats.

Since Hugging Face deprecated their embedding/reranking APIs in Sept 2025, I had to pivot to Jina. At first it was my key to hosting this for free, but then it became the biggest bottleneck. My Jina API key only survived a single session of heavy use, and once Render’s free tier powered down, the key would get throttled.

I was also limited to 512MB RAM and 0.1 CPU on Render. I considered running sentence-transformers locally, but Torch alone (~350MB) made that unrealistic.

The LLM side was easy and Groq’s free API worked great as long as I didn’t spam it.

In the end:

The hosted RAG pipeline was faster than my local one
It cost $0
But it only worked once before I had to regenerate a Jina API key and redeploy the backend on Render

This little experiment made me:

Appreciate how expensive “real” production actually is
Value enterprise tools (like Gemini Enterprise) a lot more
Think more creatively under constraints

I trimmed the fat off my requirements.txt and stitched together only "free" APIs to make it work.
Fun project overall and you can check out the static frontend website here and the source code here. (backend will definitely be broken unless you personally message me so that I can regenerate a Jina API key for you XD)

1/14/2026:

Companies Workflows:

🏥 Healthcare
Clinics
Specialty practices
Billing companies
Insurance brokers
Home health agencies

💰 Finance
Accounting firms
Wealth management offices
Credit unions
Fintech startups
Insurance underwriting teams

💻 Tech
SaaS companies
DevOps teams
Customer support teams
HR/IT internal ops
Cybersecurity firms

🏢 Professional Services
Law firms
Real estate brokerages
Logistics companies
Manufacturing
Construction

Companies with 50–500 employees

* Manual
* Repetitive
* Document-heavy
* Error-prone
* Compliance-sensitive
* Time-consuming

### Examples:

#### Healthcare:
* Prior auth
* Claims appeals
* Chart summarization
* Patient intake
* Policy lookup

#### Finance:
* KYC document extraction
* Compliance updates
* Fraud review
* Report generation
* Audit prep

#### Tech:
* Internal knowledge search
* Onboarding
* Incident response
* Ticket triage
* Log summarization

Okay.
So healthcare sounds like it would be my best bet tbh. Doctors make their own practices and do all of that stuff. It sounds so tedious how they handle it.
Maybe I do need to learn the jargon to communicate effectively with people like that, and then solve workflow problems within mid-large healthcare companies.

#### Specialty Clinics (50–300 employees):
* The Urology Group
* Midwest Orthopaedics
* Retina Consultants of America (regional offices)
* HeartPlace Cardiology
* OrthoCarolina
* Digestive Health Associates
* Women’s Health USA
* Dermatology Associates of Wisconsin
* ENT & Allergy Associates
* Arthritis & Rheumatism Associates

#### Medical Billing & RCM Companies:
* R1 RCM (regional divisions)
* Medusind
* Coronis Health
* AdvantEdge Healthcare Solutions
* CareCloud RCM division

#### Home Health & Hospice:
* Amedisys regional offices
* LHC Group regional offices
* AccentCare
* Enhabit Home Health

These companies are drowning in:
PDFs
faxed forms
insurance rules
compliance documents
manual data entry

#### Cold call people like this:
* Prior auth specialist
* Claims processor
* Compliance analyst
* Customer support lead

* Clinical Operations Manager

Hi [Name], I’m doing a small research project on how teams in [industry] handle [specific workflow]. 
I’m not selling anything — just trying to understand what’s tedious or time‑consuming in the process.

Would you be open to 2–3 quick questions about how your team handles this today?

### 🏥 1. The Core Healthcare Domains You’ll Encounter
* If you’re building automation or RAG tools, you’ll mostly interact with:
* Revenue Cycle Management (RCM)
* Prior Authorization (PA)
* Claims & Denials
* Clinical Documentation
* Patient Intake & Scheduling
* Compliance & Policy Management

Each of these has its own vocabulary. You don’t need to memorize everything — just enough to ask smart questions.

### 📘 2. The Essential Jargon (Grouped by Workflow)
🔵 A. Prior Authorization (PA)
This is one of the messiest workflows in healthcare.

#### Key terms:
* PA / Prior Auth – insurer approval before a procedure
* Medical Necessity – justification for why the patient needs it
* Clinical Notes – doctor’s documentation supporting the request
* LOMN – Letter of Medical Necessity
* CPT Code – procedure code
* ICD‑10 Code – diagnosis code
* Payer – insurance company
* UM Nurse – Utilization Management nurse (reviews PAs)
* Peer‑to‑Peer – doctor-to-doctor call to justify a procedure

If you know these terms, PA specialists will immediately trust you.

### 🔵 B. Claims & Denials
This is where clinics lose money — and where automation is gold.

#### Key terms:
Claim – request for payment sent to insurer
EDI 837 – electronic claim format
ERA / EOB – Explanation of Benefits (payment or denial info)
Denial Code – reason the claim was denied
Appeal – request to reconsider a denial
Timely Filing – deadline for submitting claims
Clearinghouse – middleman that sends claims to payers
RCM – Revenue Cycle Management

If you can talk about “denial codes” or “timely filing,” you sound like an insider.

🔵 C. Clinical Documentation
This is where doctors spend hours charting.

#### Key terms:
* EHR / EMR – electronic health record
* SOAP Note – Subjective, Objective, Assessment, Plan
* HPI – History of Present Illness
* ROS – Review of Systems
* Assessment & Plan – doctor’s diagnosis and next steps
* ICD‑10 – diagnosis codes
* CPT / HCPCS – billing codes

If you’re building summarization or extraction tools, these matter.

### 🔵 D. Patient Intake & Scheduling
This is where clinics lose time and accuracy.

#### Key terms:
Demographics – patient info (name, DOB, address)
Insurance Verification – checking coverage
Eligibility Check – confirming benefits
Copay / Coinsurance / Deductible – patient responsibility
Referral – doctor sends patient to a specialist

These workflows are perfect for automation.

#### 🔵 E. Compliance & Policy
Healthcare is regulated to the extreme.

### Key terms:
* HIPAA – privacy rules
* PHI – protected health information
* Audit Trail – record of who accessed what
* Policy & Procedure (P&P) – internal rules
* CMS – Centers for Medicare & Medicaid Services
* OIG – Office of Inspector General

If you’re building RAG over policies, these matter.

#### 🧠 3. How to Get Versed in Healthcare Workflows (Fast)
Here’s the roadmap solo devs use to get fluent without going to med school.

#### ⭐ Step 1: Talk to the people doing the work
This is the fastest way to learn.

### Target roles:
* Prior Authorization Specialist
* Medical Biller
* Claims Analyst
* RCM Manager
* Clinical Documentation Specialist
* Front Desk Coordinator
* Practice Manager

### Ask:
* “Walk me through your day.”
* “What slows you down?”
* “What do you copy/paste the most?”
* “What documents do you use?”
* “What do you wish software did for you?”

You’ll learn more in 30 minutes than in 30 hours of reading.

#### ⭐ Step 2: Read job postings
This is a cheat code.

### Search for:
* “Prior Authorization Specialist”
* “Medical Biller”
* “RCM Analyst”
* “Clinical Documentation Specialist”

Job descriptions reveal:
* tools they use
* workflows
* pain points
* jargon
* responsibilities

This is how you learn the language of the domain.

### ⭐ Step 3: Watch YouTube videos of real workflows
Search:
* “prior authorization workflow”
* “medical billing process”
* “claims denial management”
* “EHR training”
* “RCM overview”

These videos show the actual screens and steps.

### ⭐ Step 4: Read payer (insurance) policy PDFs
These are the documents your RAG pipeline will ingest.

Look up:
* “UnitedHealthcare prior authorization policy”
* “Aetna clinical policy bulletin”
* “Blue Cross medical necessity guidelines”

You’ll see:
* CPT codes
* ICD‑10 codes
* criteria
* documentation requirements

This is the raw material of healthcare automation.

### ⭐ Step 5: Learn the tools they use
Common systems:
* Epic
* Cerner
* Athenahealth
* eClinicalWorks
* NextGen
* Kareo
* DrChrono

You don’t need access — just knowing the names helps you sound credible.

#### 🧩 4. The Good News
You don’t need to become a clinician.
You need to become fluent in operational workflows, not medicine.

#### Healthcare ops is basically:
* documents
* rules
* codes
* forms
* approvals
* denials
* checklists
* compliance
* manual steps

This is exactly the kind of environment where your RAG + automation skills shine.

#### Vendors tend to solve:
* tracking
* routing
* form submission
* basic extraction
* simple automation

#### They do not solve:
* unstructured data interpretation
* payer-policy reasoning
* assembling documentation
* workflow-specific summarization
* edge cases
* small clinic needs

This is exactly where AI shines — and where a solo developer can win.

Okay. I think it would be a good idea to start synthetic, build a prototype, and then find a small clinic, or reach out to the correct people and see if I can provide value.
Models are good enough that a 6gb executable is solid.

1. Prior Auth Packet Builder
Input: fake chart + fake policy
Output: structured PA packet + missing info checklist

2. Denial Appeal Assistant
Input: fake denial code + fake chart
Output: appeal letter + required documents list

3. Policy-Aware Chart Summarizer
Input: fake chart + real payer policy PDF
Output: summary aligned to policy criteria

4. Intake Data Validator
Input: fake intake form + fake insurance card
Output: structured data + inconsistency flags

5. Payer Policy Search Engine
Input: “Does Aetna require PA for CPT 72148?”
Output: extracted answer from policy PDFs

None of these require real PHI.

Why Prior Auth + Chart Summarization is the perfect wedge

#### The Outline:
#### 🧩 Core User Flow (Simple, Fast, No Integration)
#### Step 1 — Upload
User uploads:
* a chart note (PDF or text)
* or pasting text into a box

#### Step 2 — Select
User selects:
* payer (dropdown)
* CPT code (dropdown or free text)

#### Step 3 — AI Processing
Your backend:
* extracts key clinical facts
* matches them to payer policy criteria
* identifies missing elements
* generates a justification paragraph
* produces a clean summary

#### Step 4 — Output
User sees:
* Summary: “Patient has chronic knee pain for 6 months, failed NSAIDs, completed PT…”
* Checklist: “Missing: recent imaging, conservative therapy duration”
* Justification: A payer‑friendly paragraph
* Packet: A formatted output they can copy/paste into a portal
* This is enough to make a clinic say “wow.”

### 🛠️ What You Need to Build (Technically)
#### 1. Frontend (simple)
* File upload
* Text box
* Dropdowns for payer + CPT
* Results panel
* React, Svelte, or even plain HTML works.

#### 2. Backend
Your RAG pipeline
* A small policy database (PDFs → embeddings)
* A summarization + extraction prompt
* A justification generator prompt
* A missing‑info detector

#### 3. Synthetic Data
You generate:
* fake chart notes
* fake clinical histories
* fake PA requests
* fake denial examples
* This avoids HIPAA and lets you iterate fast.

#### 4. Policy Data
* Use real payer PDFs (publicly available).
* You don’t need to store PHI — just the rules.

#### 🎯 Scope Control (What NOT to Build Yet)
Do not build:
* EHR integration
* Portal submission
* Real‑time status tracking
* Multi‑user accounts
* Billing
* Role‑based access
* Audit logs

These are enterprise features.
Your MVP is a workflow assistant, not a platform.

#### The safest framing for your MVP
* You’re not building:
* a clinical decision tool
* a diagnostic tool
* an autonomous system

#### You’re building:
* a documentation assistant
* a summarization helper
* a policy‑aware checklist generator
* This keeps you in a safe, responsible zone.

#### Your tool becomes:
* a second set of eyes
* a fast reader
* a policy interpreter
* a packet organizer

#### “PA readiness checking”
#### How I’d tighten the positioning (this is key)

Your conclusion is good. I’d make it even sharper and safer with one reframing:

####Don’t sell “PA chart summarization”

Sell “PA readiness checking”

That subtle shift:
* Moves you away from document AI comparisons
* Anchors you in outcomes, not artifacts
* Makes the value immediately obvious

#### Example positioning:
“Before you submit a prior authorization, we tell you:
* whether it meets payer criteria
* what’s missing
* and generate the justification text for you”

Now Attinio isn’t even in the same mental category.

#### A more precise bottom line (my version)

I’d slightly revise your final takeaway to this:
* Attinio is a document intelligence platform.
* Your idea is a prior-authorization readiness and validation tool.

The overlap is implementation detail, not product intent.

#### Small clinics don’t need better document extraction —
* they need fewer denials and fewer resubmissions.
* That problem is still very much unsolved for them.
* That framing is defensible, accurate, and compelling.