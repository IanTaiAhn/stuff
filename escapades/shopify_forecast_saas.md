# Shopify Inventory Forecasting SaaS — Project Outline & Python Template

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Target Customer](#2-target-customer)
3. [Architecture Overview](#3-architecture-overview)
4. [Data Layer — Shopify API Integration](#4-data-layer--shopify-api-integration)
5. [Feature Engineering Pipeline](#5-feature-engineering-pipeline)
6. [Forecasting Model — SARIMA/SARIMAX](#6-forecasting-model--sarimasarimax)
7. [Reorder Logic Engine](#7-reorder-logic-engine)
8. [Output Layer — Plain English Recommendations](#8-output-layer--plain-english-recommendations)
9. [Deployment Considerations](#9-deployment-considerations)
10. [Tech Stack Summary](#10-tech-stack-summary)

---

## 1. Project Overview

**Product Name (placeholder):** StockSense / RestockIQ / [Your Name Here]

**The Gap Being Filled:**
- Existing tools (Prediko $119/mo, Cogsy $199/mo) are priced out of range for small stores
- Sensible Forecasting charges $29/mo but uses a simple moving average — no seasonality
- Target: Shopify stores doing **$10k–$100k/month revenue** who need *seasonal-aware* forecasting
  at an affordable price point ($29–$49/month)

**Core Value Proposition:**
> "Know exactly what to reorder, how much, and when — automatically accounting for seasons,
> promotions, and your supplier lead times. Never stockout again."

**What Makes This Technically Differentiated:**
- SARIMA model per SKU (handles seasonality that moving-average tools miss)
- SARIMAX exogenous variables (promotions, holidays, day-of-week effects)
- Log transformation on demand data (handles right-skewed sales distributions)
- Automatic stationarity testing and differencing
- Per-SKU model selection via AIC/BIC (not one global model)

---

## 2. Target Customer

| Attribute         | Profile                                              |
|-------------------|------------------------------------------------------|
| Platform          | Shopify (Basic, Shopify, Advanced, or Plus)          |
| Monthly Revenue   | $10,000 – $100,000                                   |
| SKU Count         | 30 – 500 active products                             |
| Business Type     | Physical products, holds own inventory (not dropship)|
| Reorder Cycle     | Regular purchase orders to 1–3 suppliers             |
| Current Solution  | Excel spreadsheets or nothing                        |
| Pain Point        | Stockouts on bestsellers, overstock on slow movers   |

**Best Niches to Start With (pronounced seasonality = model advantage):**
- Apparel / seasonal fashion
- Supplements / health products
- Outdoor / sporting goods
- Holiday / gift products
- Pet supplies

---

## 3. Architecture Overview

```
Shopify Store
     │
     │  OAuth + API Token
     ▼
[Data Ingestion Layer]         ← Pull orders, inventory, products via Shopify API
     │
     ▼
[Preprocessing Pipeline]       ← Clean, aggregate, log-transform, stationarity check
     │
     ▼
[Feature Engineering]          ← Lag features, rolling averages, seasonality flags,
     │                            promo flags, lead time, day-of-week encoding
     ▼
[SARIMA / SARIMAX Model]       ← Per-SKU model, auto parameter selection (pmdarima)
     │
     ▼
[Reorder Logic Engine]         ← Apply safety stock, lead time, reorder point calc
     │
     ▼
[Output / Recommendation Layer] ← Plain English alerts, weekly email digest,
                                   CSV export for purchase orders
```

---

## 4. Data Layer — Shopify API Integration

```python
# ============================================================
# shopify_client.py
# Handles OAuth token storage and all Shopify API calls
# ============================================================

import requests
import pandas as pd
from datetime import datetime, timedelta


SHOPIFY_API_VERSION = "2024-10"  # Update quarterly


class ShopifyClient:
    """
    Wrapper for Shopify Admin GraphQL API.
    Requires: store domain + OAuth access token (obtained during app install).
    """

    def __init__(self, shop_domain: str, access_token: str):
        self.shop_domain = shop_domain  # e.g. "mystore.myshopify.com"
        self.access_token = access_token
        self.base_url = f"https://{shop_domain}/admin/api/{SHOPIFY_API_VERSION}"
        self.headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json",
        }

    # ----------------------------------------------------------
    # Pull full order history (requires read_all_orders scope)
    # Returns a flat DataFrame: order_date, product_id, variant_id,
    #                           sku, quantity, price
    # ----------------------------------------------------------
    def get_orders(self, days_back: int = 365) -> pd.DataFrame:
        since = (datetime.utcnow() - timedelta(days=days_back)).isoformat()
        orders = []
        url = f"{self.base_url}/orders.json"
        params = {
            "status": "any",
            "created_at_min": since,
            "limit": 250,
            "fields": "id,created_at,line_items",
        }

        while url:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            for order in data.get("orders", []):
                for item in order.get("line_items", []):
                    orders.append({
                        "order_date": pd.to_datetime(order["created_at"]).date(),
                        "product_id": item.get("product_id"),
                        "variant_id": item.get("variant_id"),
                        "sku": item.get("sku"),
                        "quantity": item.get("quantity", 0),
                        "price": float(item.get("price", 0)),
                    })

            # Handle pagination via Link header
            link_header = response.headers.get("Link", "")
            url = self._parse_next_link(link_header)
            params = {}  # Clear params after first page (URL already has them)

        return pd.DataFrame(orders)

    # ----------------------------------------------------------
    # Pull current inventory levels for all active products
    # Returns DataFrame: variant_id, sku, product_title,
    #                    inventory_quantity, lead_time_days (manual input)
    # ----------------------------------------------------------
    def get_inventory(self) -> pd.DataFrame:
        url = f"{self.base_url}/variants.json"
        params = {"limit": 250, "fields": "id,sku,product_id,inventory_quantity,title"}
        variants = []

        while url:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            variants.extend(data.get("variants", []))
            link_header = response.headers.get("Link", "")
            url = self._parse_next_link(link_header)
            params = {}

        return pd.DataFrame(variants)

    @staticmethod
    def _parse_next_link(link_header: str) -> str | None:
        """Extract next page URL from Shopify pagination Link header."""
        if 'rel="next"' not in link_header:
            return None
        for part in link_header.split(","):
            if 'rel="next"' in part:
                return part.split(";")[0].strip().strip("<>")
        return None
```

---

## 5. Feature Engineering Pipeline

```python
# ============================================================
# feature_engineering.py
# Transforms raw order data into model-ready time series
# ============================================================

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def build_daily_demand(orders_df: pd.DataFrame, sku: str) -> pd.Series:
    """
    Aggregate raw order rows into a daily demand time series for one SKU.
    Fills missing days with 0 (no sales = 0 demand, not NaN).
    """
    sku_orders = orders_df[orders_df["sku"] == sku].copy()
    daily = (
        sku_orders
        .groupby("order_date")["quantity"]
        .sum()
        .asfreq("D")          # Set daily frequency
        .fillna(0)            # Fill gaps with zero demand
        .sort_index()
    )
    return daily


def apply_log_transform(series: pd.Series, offset: float = 1.0) -> pd.Series:
    """
    Log-transform demand data to stabilize variance.
    Offset of 1 handles zero-demand days: log(0 + 1) = 0
    """
    return np.log(series + offset)


def inverse_log_transform(series: pd.Series, offset: float = 1.0) -> pd.Series:
    """Reverse the log transform to get back to units."""
    return np.exp(series) - offset


def check_stationarity(series: pd.Series, significance: float = 0.05) -> dict:
    """
    Augmented Dickey-Fuller test for stationarity.
    Returns dict with result and recommended differencing order.
    """
    result = adfuller(series.dropna(), autolag="AIC")
    is_stationary = result[1] < significance  # p-value check
    return {
        "is_stationary": is_stationary,
        "p_value": result[1],
        "adf_statistic": result[0],
        "recommended_d": 0 if is_stationary else 1,
    }


def add_exogenous_features(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add exogenous variables (X in SARIMAX) to the time series DataFrame.
    These become the 'exog' parameter passed to the SARIMAX model.

    Add your own columns here — promotions, ad spend, holidays, etc.
    """
    df = daily_df.copy()
    df.index = pd.to_datetime(df.index)

    # Day of week (0=Monday, 6=Sunday) — captures weekend sales spikes
    df["day_of_week"] = df.index.dayofweek

    # Week of year — captures annual seasonal position
    df["week_of_year"] = df.index.isocalendar().week.astype(int)

    # Month — for monthly seasonality
    df["month"] = df.index.month

    # Is weekend flag (binary)
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # TODO: Add promotion flag (0/1) — pull from Shopify price rule API
    # df["is_promo"] = ...

    # TODO: Add holiday flag — use a holidays library or manual calendar
    # from holidays import US
    # us_holidays = US()
    # df["is_holiday"] = df.index.map(lambda d: 1 if d in us_holidays else 0)

    return df


def aggregate_to_weekly(daily_series: pd.Series) -> pd.Series:
    """
    For stores with sparse daily sales (< 30 orders/week),
    aggregate to weekly demand before modeling.
    Weekly data is often more stable for SARIMA.
    """
    return daily_series.resample("W").sum()
```

---

## 6. Forecasting Model — SARIMA/SARIMAX

```python
# ============================================================
# forecasting_model.py
# Per-SKU SARIMA/SARIMAX model with automatic parameter selection
# ============================================================

import warnings
import numpy as np
import pandas as pd
import pmdarima as pmd
import statsmodels.api as sm
from feature_engineering import (
    build_daily_demand,
    apply_log_transform,
    inverse_log_transform,
    check_stationarity,
    aggregate_to_weekly,
)

warnings.filterwarnings("ignore")  # Suppress convergence warnings in production


class SKUForecaster:
    """
    Trains and stores a SARIMA/SARIMAX model for a single SKU.

    Workflow:
        1. Build daily time series from order history
        2. Optionally aggregate to weekly (for sparse SKUs)
        3. Log-transform to stabilize variance
        4. Check stationarity → set d parameter
        5. Auto-select SARIMA order via pmdarima (equivalent to R's auto.arima)
        6. Refit with statsmodels SARIMAX if exogenous variables are present
        7. Forecast N periods ahead
        8. Inverse-transform back to units
    """

    def __init__(self, sku: str, seasonality_period: int = 52):
        """
        Args:
            sku: Product SKU identifier
            seasonality_period: Seasonal period.
                52 = weekly data with annual seasonality (recommended)
                 7 = daily data with weekly seasonality
                12 = monthly data with annual seasonality
        """
        self.sku = sku
        self.seasonality_period = seasonality_period
        self.model_ = None
        self.model_fit_ = None
        self.order_ = None
        self.seasonal_order_ = None
        self.use_log_ = True
        self.use_weekly_ = True

    def fit(self, orders_df: pd.DataFrame, exog_df: pd.DataFrame = None):
        """
        Fit the SARIMA model for this SKU.

        Args:
            orders_df: Raw orders DataFrame from ShopifyClient.get_orders()
            exog_df: Optional DataFrame of exogenous features aligned to time index
        """
        # Step 1: Build and optionally aggregate demand series
        daily = build_daily_demand(orders_df, self.sku)

        if self.use_weekly_:
            series = aggregate_to_weekly(daily)
        else:
            series = daily

        # Step 2: Log transform
        if self.use_log_:
            series_transformed = apply_log_transform(series)
        else:
            series_transformed = series

        # Step 3: Check stationarity
        stationarity = check_stationarity(series_transformed)
        d = stationarity["recommended_d"]

        # Step 4: Auto-select ARIMA order (pmdarima = R's auto.arima)
        # This searches over p, q combinations and picks lowest AIC
        auto_model = pmd.auto_arima(
            series_transformed,
            d=d,
            seasonal=True,
            m=self.seasonality_period,
            start_p=0, max_p=3,
            start_q=0, max_q=3,
            start_P=0, max_P=2,
            start_Q=0, max_Q=2,
            D=1,               # Always seasonally difference once
            information_criterion="aic",
            stepwise=True,     # Faster than full grid search
            error_action="ignore",
            suppress_warnings=True,
            trace=False,
        )

        self.order_ = auto_model.order
        self.seasonal_order_ = auto_model.seasonal_order

        # Step 5: Refit with statsmodels SARIMAX
        # Use this path for production — gives access to forecast intervals,
        # better diagnostics, and exogenous variable support
        if exog_df is not None:
            exog_aligned = exog_df.reindex(series_transformed.index).fillna(0)
        else:
            exog_aligned = None

        self.model_ = sm.tsa.statespace.SARIMAX(
            series_transformed,
            exog=exog_aligned,
            order=self.order_,
            seasonal_order=self.seasonal_order_,
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        self.model_fit_ = self.model_.fit(disp=False)
        self.last_index_ = series_transformed.index
        self.series_ = series_transformed

        return self

    def predict(self, n_periods: int = 12, exog_future: pd.DataFrame = None) -> dict:
        """
        Forecast n_periods ahead.

        Args:
            n_periods: Number of periods to forecast (weeks if use_weekly_=True)
            exog_future: Future exogenous variables aligned to forecast dates

        Returns:
            dict with keys:
                'forecast': pd.Series of predicted demand (in original units)
                'lower_ci': lower 95% confidence interval
                'upper_ci': upper 95% confidence interval
                'dates': forecast date index
        """
        if self.model_fit_ is None:
            raise RuntimeError("Model not fitted. Call .fit() first.")

        forecast_result = self.model_fit_.get_forecast(
            steps=n_periods,
            exog=exog_future,
        )

        forecast_mean = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int()

        # Inverse transform from log scale back to units
        if self.use_log_:
            forecast_units = inverse_log_transform(forecast_mean)
            lower_units = inverse_log_transform(conf_int.iloc[:, 0])
            upper_units = inverse_log_transform(conf_int.iloc[:, 1])
        else:
            forecast_units = forecast_mean
            lower_units = conf_int.iloc[:, 0]
            upper_units = conf_int.iloc[:, 1]

        # Clip to non-negative (demand can't be negative)
        forecast_units = forecast_units.clip(lower=0)
        lower_units = lower_units.clip(lower=0)
        upper_units = upper_units.clip(lower=0)

        return {
            "sku": self.sku,
            "forecast": forecast_units,
            "lower_ci": lower_units,
            "upper_ci": upper_units,
            "model_order": self.order_,
            "seasonal_order": self.seasonal_order_,
        }

    def get_model_summary(self) -> str:
        """Return statsmodels summary for diagnostics/logging."""
        if self.model_fit_ is None:
            return "Model not fitted."
        return str(self.model_fit_.summary())
```

---

## 7. Reorder Logic Engine

```python
# ============================================================
# reorder_engine.py
# Converts demand forecasts into actionable reorder recommendations
# ============================================================

import pandas as pd
import numpy as np


class ReorderEngine:
    """
    Takes a demand forecast and current inventory state,
    and outputs a reorder recommendation.

    Key Inputs Per SKU:
        - forecast_units: pd.Series of predicted weekly demand
        - current_stock: int, units currently on hand
        - lead_time_weeks: int, supplier lead time in weeks
        - safety_stock_weeks: float, weeks of buffer stock to maintain
        - on_order_units: int, units already on order (in transit)
    """

    def __init__(
        self,
        current_stock: int,
        lead_time_weeks: int,
        safety_stock_weeks: float = 1.5,
        on_order_units: int = 0,
    ):
        self.current_stock = current_stock
        self.lead_time_weeks = lead_time_weeks
        self.safety_stock_weeks = safety_stock_weeks
        self.on_order_units = on_order_units

    def calculate_reorder(self, forecast: dict) -> dict:
        """
        Core reorder calculation.

        Returns a recommendation dict with:
            - should_reorder: bool
            - reorder_quantity: int
            - order_by_date: str (ISO date)
            - stockout_risk_date: str or None
            - days_of_stock_remaining: float
            - recommendation_text: str (plain English for UI)
        """
        forecast_series = forecast["forecast"]
        weekly_demand = forecast_series.values

        # --- Days of stock remaining ---
        avg_weekly_demand = weekly_demand[:4].mean()  # Use next 4-week avg
        avg_daily_demand = avg_weekly_demand / 7

        if avg_daily_demand > 0:
            days_of_stock = (self.current_stock + self.on_order_units) / avg_daily_demand
        else:
            days_of_stock = 999  # Effectively infinite if no demand

        # --- Reorder point ---
        # Stock needed to cover lead time + safety buffer
        demand_during_lead_time = avg_weekly_demand * self.lead_time_weeks
        safety_stock_units = avg_weekly_demand * self.safety_stock_weeks
        reorder_point = demand_during_lead_time + safety_stock_units

        # --- Should reorder? ---
        available_stock = self.current_stock + self.on_order_units
        should_reorder = available_stock <= reorder_point

        # --- Reorder quantity (Economic Order Quantity simplified) ---
        # Cover lead time + safety stock + next cycle demand (8 weeks default)
        target_stock = demand_during_lead_time + safety_stock_units + (avg_weekly_demand * 8)
        reorder_quantity = max(0, int(np.ceil(target_stock - available_stock)))

        # --- Stockout risk date ---
        stockout_date = None
        if avg_daily_demand > 0:
            stockout_days = available_stock / avg_daily_demand
            stockout_date = (
                pd.Timestamp.today() + pd.Timedelta(days=stockout_days)
            ).strftime("%Y-%m-%d")

        # --- Order by date (must order before stock runs below reorder point) ---
        order_by_days = max(0, int(days_of_stock - (self.lead_time_weeks * 7)))
        order_by_date = (
            pd.Timestamp.today() + pd.Timedelta(days=order_by_days)
        ).strftime("%Y-%m-%d")

        return {
            "sku": forecast["sku"],
            "should_reorder": should_reorder,
            "reorder_quantity": reorder_quantity,
            "order_by_date": order_by_date,
            "stockout_risk_date": stockout_date,
            "days_of_stock_remaining": round(days_of_stock, 1),
            "avg_weekly_demand": round(avg_weekly_demand, 1),
            "reorder_point_units": round(reorder_point, 0),
        }
```

---

## 8. Output Layer — Plain English Recommendations

```python
# ============================================================
# recommendations.py
# Converts reorder engine output into human-readable text
# for UI display, email digests, and CSV exports
# ============================================================

import pandas as pd
from dataclasses import dataclass


@dataclass
class ReorderRecommendation:
    sku: str
    product_title: str
    should_reorder: bool
    reorder_quantity: int
    order_by_date: str
    days_of_stock_remaining: float
    avg_weekly_demand: float
    stockout_risk_date: str


def build_recommendation_text(rec: ReorderRecommendation) -> str:
    """
    Generate plain English recommendation for a single SKU.
    This is what shows up in the merchant's dashboard and email digest.
    """
    if not rec.should_reorder:
        return (
            f"✅ {rec.product_title} — You have ~{rec.days_of_stock_remaining:.0f} days "
            f"of stock remaining. No action needed yet."
        )

    urgency = "🚨 URGENT:" if rec.days_of_stock_remaining < 14 else "⚠️"

    return (
        f"{urgency} {rec.product_title} — Only ~{rec.days_of_stock_remaining:.0f} days "
        f"of stock remaining (selling ~{rec.avg_weekly_demand:.0f} units/week). "
        f"Order {rec.reorder_quantity} units by {rec.order_by_date} to avoid a stockout."
    )


def build_weekly_digest(recommendations: list[ReorderRecommendation]) -> str:
    """
    Format a full weekly email digest.
    Sections: urgent reorders → upcoming reorders → healthy stock.
    """
    urgent = [r for r in recommendations if r.should_reorder and r.days_of_stock_remaining < 14]
    upcoming = [r for r in recommendations if r.should_reorder and r.days_of_stock_remaining >= 14]
    healthy = [r for r in recommendations if not r.should_reorder]

    lines = ["# Weekly Inventory Digest\n"]

    if urgent:
        lines.append("## 🚨 Urgent — Order Now\n")
        for r in urgent:
            lines.append(f"- {build_recommendation_text(r)}")
        lines.append("")

    if upcoming:
        lines.append("## ⚠️ Reorder Soon\n")
        for r in upcoming:
            lines.append(f"- {build_recommendation_text(r)}")
        lines.append("")

    if healthy:
        lines.append(f"## ✅ Healthy Stock ({len(healthy)} products)\n")
        lines.append("All other products are stocked for 14+ days. No action needed.")

    return "\n".join(lines)


def export_to_csv(recommendations: list[ReorderRecommendation]) -> pd.DataFrame:
    """
    Export reorder recommendations as a DataFrame (for CSV download
    or direct supplier email attachment).
    """
    rows = []
    for r in recommendations:
        if r.should_reorder:
            rows.append({
                "SKU": r.sku,
                "Product": r.product_title,
                "Order Qty": r.reorder_quantity,
                "Order By": r.order_by_date,
                "Days of Stock Left": r.days_of_stock_remaining,
                "Avg Weekly Demand": r.avg_weekly_demand,
            })
    return pd.DataFrame(rows).sort_values("Days of Stock Left")
```

---

## 9. Deployment Considerations

### Minimum Viable Infrastructure (< $50/month to start)

| Component | Tool | Cost |
|---|---|---|
| Web framework | FastAPI or Flask | Free |
| Database | PostgreSQL on Railway or Supabase | Free–$5/mo |
| Background jobs (model retraining) | Celery + Redis or APScheduler | Free |
| Hosting | Railway, Render, or Fly.io | $5–$20/mo |
| Email digests | Resend or SendGrid free tier | Free |
| Shopify app listing | Shopify Partner account | Free |

### Model Retraining Schedule
```python
# Retrain each SKU model weekly (Sunday night, before Monday digest)
# Use APScheduler or a cron job on your server

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("cron", day_of_week="sun", hour=2)
def retrain_all_models():
    """
    For each installed store:
        1. Pull last 365 days of orders from Shopify API
        2. Retrain SKUForecaster for each active SKU
        3. Store model artifacts (pickle or joblib)
        4. Run ReorderEngine
        5. Send weekly email digest
    """
    pass  # TODO: implement

scheduler.start()
```

### Data Storage Per Merchant
```
merchants/
├── {shop_domain}/
│   ├── access_token          ← Encrypted OAuth token
│   ├── settings.json         ← Lead times, safety stock per SKU
│   ├── models/
│   │   ├── {sku_1}.pkl       ← Serialized SKUForecaster
│   │   ├── {sku_2}.pkl
│   │   └── ...
│   └── last_sync.json        ← Timestamp of last Shopify data pull
```

### Key API Scopes to Request at Install
```python
REQUIRED_SCOPES = [
    "read_orders",          # Order history
    "read_all_orders",      # Full order history (> 60 days) — requires Shopify approval
    "read_inventory",       # Current stock levels
    "read_products",        # Product/variant metadata
    "write_draft_orders",   # Optional: create draft purchase orders in Shopify
]
```

---

## 10. Tech Stack Summary

```
Backend:        Python 3.11+
Web Framework:  FastAPI
Forecasting:    statsmodels (SARIMAX), pmdarima (auto_arima)
Data:           pandas, numpy
ML Pipeline:    scikit-learn (preprocessing), joblib (model serialization)
Shopify:        Shopify Admin REST/GraphQL API + OAuth
Database:       PostgreSQL (SQLAlchemy ORM)
Job Queue:      APScheduler (simple) or Celery + Redis (scalable)
Email:          Resend API or SendGrid
Hosting:        Railway or Render
Testing:        pytest
```

### Install Dependencies
```bash
pip install fastapi uvicorn statsmodels pmdarima pandas numpy scikit-learn \
            sqlalchemy psycopg2-binary requests apscheduler joblib python-dotenv
```

---

## Next Steps / Build Order

1. **[ ] OAuth flow** — Get Shopify app credentials, implement install/callback routes
2. **[ ] Data ingestion** — `ShopifyClient.get_orders()` working end-to-end for one test store
3. **[ ] Single SKU forecast** — Run `SKUForecaster.fit()` + `.predict()` on real data, validate output
4. **[ ] Reorder logic** — Wire `ReorderEngine` to forecast output, check recommendations make sense
5. **[ ] Plain English output** — Build `build_weekly_digest()`, send test email
6. **[ ] CSV export** — Let user download reorder list, test with a real merchant
7. **[ ] Multi-SKU loop** — Run the full pipeline across all active SKUs for one store
8. **[ ] Weekly cron job** — Automate the retrain → recommend → email cycle
9. **[ ] Shopify App Store listing** — Submit for review (takes 1–2 weeks)
10. **[ ] Pricing + billing** — Implement Shopify Billing API for $29–$49/mo subscription

---

*This document is a working technical blueprint. Each section maps directly to a Python module
in the final codebase. Start with steps 1–3 to validate the core loop before building the full product.*
