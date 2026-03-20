# Reseller Profit Tracker — MVP Spec

A solo-dev SaaS for vintage and secondhand resellers selling across eBay, Poshmark, Depop, and Facebook Marketplace. The core value proposition: know your **real profit per item**, not just your sale price.

---

## Problem Statement

Resellers across eBay, Poshmark, Depop, and Facebook Marketplace have no simple way to track true per-item profit. They guess. They accept bad offers. They source items with thin margins without realizing it. Spreadsheets break down fast, and existing tools (My Reseller Genie, Flipwise) require heavy manual entry and lack real-time fee math.

---

## Target User

- Part-time to full-time resellers
- Selling on 2–4 platforms simultaneously
- Managing 50–500 active SKUs
- Currently using spreadsheets or nothing
- Willing to pay $10–15/month for something that saves hours and surfaces real numbers

---

## MVP Goals

1. Log inventory purchases with cost
2. Log sales and auto-calculate platform fees
3. Show true per-item profit (revenue − fees − COGS − shipping)
4. Evaluate offers before accepting them
5. Export a basic P&L for tax prep

---

## Platform Fee Structures (Built-in)

These are hardcoded at launch and updated manually when platforms change.

| Platform | Fee Structure |
|---|---|
| eBay | 13.25% final value fee + 2.9% + $0.30 payment processing |
| Poshmark | $2.95 flat (sales under $15) or 20% (sales $15+) |
| Depop | 10% + 3.3% + $0.45 payment processing |
| Facebook Marketplace | 0% (local) or 5% (shipped, min $0.40) |
| Mercari | 10% + 2.9% + $0.30 payment processing |

---

## Core Features (v1)

### 1. Inventory Log

Add an item when you purchase it.

**Fields:**
- Item name / description
- Purchase price (COGS)
- Purchase date
- Source (thrift store, estate sale, bin store, etc.) — free text
- Category (clothing, electronics, shoes, home goods, etc.)
- SKU / label — auto-generated or custom
- Notes (optional)
- Photo (optional, single image)

---

### 2. Sale Logger

Record a sale manually or via CSV import.

**Fields:**
- Link to inventory item
- Platform sold on (eBay, Poshmark, Depop, FBMP, Mercari, Other)
- Sale price
- Shipping charged to buyer
- Shipping cost paid by seller
- Date sold

**Auto-calculated on save:**
- Platform fee (based on platform + sale price)
- Net payout = sale price − platform fee − seller shipping cost
- Profit = net payout − COGS
- ROI = (profit ÷ COGS) × 100%
- Days to sell = sale date − purchase date

---

### 3. Offer Evaluator

A quick calculator available before accepting an offer.

**Inputs:**
- Offer price
- Platform
- Seller shipping cost (or use saved default)
- Item COGS (pulled from inventory if linked)

**Output (instant, no save required):**
- Platform fee
- Net payout
- Profit
- ROI %
- A clear signal: `✓ Good deal` / `⚠ Thin margin` / `✗ Losing money`

Thresholds are user-configurable (default: good = ROI > 50%, thin = 20–50%, losing = under 20%).

---

### 4. Dashboard

A single-screen overview of the business.

**Metrics shown:**
- Total profit (this month / all time)
- Total revenue (this month / all time)
- Number of items sold
- Average profit per sale
- Average ROI %
- Best performing platform (by avg profit)
- Best performing category (by avg profit)
- Items currently listed (active inventory count)
- Items sold in last 30 days

**Charts:**
- Profit by month (bar chart, last 6 months)
- Sales by platform (donut chart)

---

### 5. Inventory List

A table of all active (unsold) inventory.

**Columns:** SKU, Name, Category, COGS, Date Purchased, Days Listed, Source

**Filters:** Category, Source, Days Listed (30 / 60 / 90+ days)

**Aging highlight:** Items listed 90+ days are flagged in amber. Items 180+ days flagged in red.

---

### 6. Sales History

A table of all completed sales.

**Columns:** Date, Item, Platform, Sale Price, Fees, Shipping Cost, Net Payout, Profit, ROI %

**Sortable by:** Date, Profit, ROI, Platform

**Filters:** Platform, Date range, Category

---

### 7. P&L Export

A downloadable CSV covering a selected date range.

**Includes:**
- All sales with: sale price, platform fee, shipping cost, COGS, profit
- Summary row: total revenue, total fees, total shipping, total COGS, total profit
- Suitable for handing to an accountant or importing into a spreadsheet

---

### 8. CSV Import (eBay)

eBay allows sellers to export sold order history. Support importing this CSV to auto-populate sales without manual entry.

**Mapped fields:** Order date, item title, sale price, shipping charged, eBay fees (if present in export)

**User action:** Match imported rows to existing inventory items, or create new inventory entries on import.

---

## Out of Scope for v1

These are intentionally deferred to avoid scope creep:

- Automatic marketplace API sync (eBay, Poshmark, etc.)
- Crosslisting / listing creation
- Mileage tracking
- Multi-user / team accounts
- Mobile app (web only, mobile-responsive)
- Inventory aging price suggestions (v2)
- Sourcing ROI intelligence (v2)
- AI-powered features (v2)

---

## Data Model

### `items` table

| Field | Type | Notes |
|---|---|---|
| id | uuid | Primary key |
| user_id | uuid | Foreign key → users |
| name | text | Item description |
| sku | text | Auto-generated or custom |
| cogs | decimal | Purchase price |
| source | text | Free text |
| category | text | Enum or free text |
| purchased_at | date | |
| status | enum | `active`, `sold` |
| notes | text | Optional |
| photo_url | text | Optional |
| created_at | timestamp | |

### `sales` table

| Field | Type | Notes |
|---|---|---|
| id | uuid | Primary key |
| user_id | uuid | Foreign key → users |
| item_id | uuid | Foreign key → items |
| platform | enum | `ebay`, `poshmark`, `depop`, `fbmp`, `mercari`, `other` |
| sale_price | decimal | |
| shipping_charged | decimal | What buyer paid |
| shipping_cost | decimal | What seller paid |
| platform_fee | decimal | Auto-calculated |
| net_payout | decimal | Auto-calculated |
| profit | decimal | Auto-calculated |
| roi_pct | decimal | Auto-calculated |
| days_to_sell | integer | Auto-calculated |
| sold_at | date | |
| created_at | timestamp | |

### `users` table

| Field | Type | Notes |
|---|---|---|
| id | uuid | Primary key |
| email | text | |
| plan | enum | `free`, `pro` |
| created_at | timestamp | |
| settings | jsonb | Thresholds, defaults |

---

## Tech Stack (Recommended)

| Layer | Choice | Rationale |
|---|---|---|
| Frontend | Next.js (React) | Fast to build, easy deployment |
| Styling | Tailwind CSS | Utility-first, minimal setup |
| Backend | Next.js API routes | No separate backend needed for MVP |
| Database | Supabase (Postgres) | Free tier, auth included, real-time |
| Auth | Supabase Auth | Email/password to start |
| Payments | Stripe | Industry standard, easy integration |
| Hosting | Vercel | Free tier, zero-config Next.js deploy |
| Charts | Recharts | Lightweight, React-native |

**Total infra cost at launch: ~$0/month** until meaningful scale.

---

## Pricing Model

| Plan | Price | Limits |
|---|---|---|
| Free | $0 | Up to 50 items, 30-day history, no export |
| Pro | $12/month | Unlimited items, full history, CSV export, offer evaluator |

The free tier is generous enough to onboard real sellers and demonstrate value before asking for payment.

---

## MVP Build Phases

### Phase 1 — Core loop (weeks 1–3)
- Auth (sign up / sign in)
- Add inventory item
- Log a sale (manual)
- Per-item profit calculation
- Basic inventory list and sales history table

### Phase 2 — Value add (weeks 4–5)
- Dashboard with key metrics and charts
- Offer evaluator calculator
- Inventory aging highlights (90 / 180 day flags)
- Platform fee engine (all 5 platforms)

### Phase 3 — Retention and monetization (weeks 6–7)
- P&L CSV export
- eBay CSV import
- Stripe integration (free vs pro)
- User settings (profit thresholds, default shipping cost)

### Phase 4 — Polish and launch (week 8)
- Mobile-responsive layout
- Empty states and onboarding flow
- Basic landing page
- Soft launch to reseller communities (Reddit: r/Flipping, r/Poshmark; Facebook reseller groups)

---

## Key Metrics to Track Post-Launch

- Signups per week
- Free → Pro conversion rate (target: 8–12%)
- Monthly churn rate (target: < 5%)
- Average items logged per active user
- MRR growth

---

## Competitive Positioning

| | My Reseller Genie | Flipwise | **This app** |
|---|---|---|---|
| Free tier | No | No | Yes |
| Per-item profit | Yes | Yes | Yes |
| Real-time fee calc | Partial | Partial | Yes |
| Offer evaluator | No | No | Yes |
| Vintage reseller focus | No | No | Yes |
| Simple onboarding | Moderate | Moderate | Priority |
| Price | $10–20/mo | Variable | $12/mo |

---

## Success Criteria for MVP

- 100 active users within 60 days of launch
- 10% free-to-pro conversion within 90 days
- At least 3 unprompted user testimonials ("this saved me time / money")
- MRR of $500+ within 90 days
