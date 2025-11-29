# Polycrisis Dashboard: Data Dictionary

This document serves as the single source of truth for the data indicators used in the Polycrisis Dashboard. It defines the strategic logic, operational formula, and technical retrieval method for each Key Performance Indicator (KPI).

---

## Module 1: U.S. Fiscal & Monetary Health

### 1. Fiscal Unsustainability Ratio
*   **Strategic Definition:** Measures the extent to which non-discretionary obligations (Mandatory Spending + Interest) consume federal revenue. A ratio above 100% indicates the government must borrow to fund even its basic operations (defense, infrastructure, etc.).
*   **Operational Formula:** `(Mandatory Spending + Net Interest) / Total Federal Receipts`
    *   *Mandatory Spending Proxy:* Sum of Social Security (`W823RC1`) + Medicare (`W824RC1`) + Medicaid (`W825RC1`).
*   **Data Source:** Federal Reserve Economic Data (FRED).
*   **Method:** API / CSV Fetch.
*   **Series IDs:**
    *   Total Receipts: `W006RC1Q027SBEA` (Quarterly)
    *   Net Interest: `A091RC1Q027SBEA` (Quarterly)
    *   Social Security: `W823RC1` (Quarterly)
    *   Medicare: `W824RC1` (Quarterly)
    *   Medicaid: `W825RC1` (Quarterly)

### 2. Interest Burden
*   **Strategic Definition:** The share of tax revenue consumed solely by servicing the debt.
*   **Operational Formula:** `Net Interest / Total Federal Receipts`
*   **Data Source:** FRED.
*   **Series IDs:** `A091RC1Q027SBEA` (Interest), `W006RC1Q027SBEA` (Receipts).

---

## Module 2: De-Dollarization & Monetary System

### 3. Foreign Confidence (U.S. Debt Holdings)
*   **Strategic Definition:** Tracks the willingness of rival powers (China) and allies (Japan) to hold U.S. government debt.
*   **Operational Formula:** Raw holding amount in Billions USD.
*   **Data Source:** U.S. Treasury International Capital (TIC) System.
*   **Method:**
    *   *Primary:* Web scraping the TIC "Major Foreign Holders" text file.
    *   *Proxy:* FRED Series `FDHBFIN` (Total Foreign Holdings) if granular data fails.
*   **URL:** `https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/mfh.txt`

### 4. Central Bank Gold Reserves
*   **Strategic Definition:** A proxy for "flight to safety" and moving away from fiat currencies.
*   **Operational Formula:** Metric Tons of Gold held by Central Banks (or monetary value).
*   **Data Source:** IMF International Financial Statistics (IFS) or World Bank.
*   **Method:** API (IMF) or Third-party Aggregator.

---

## Module 3: The Physical Economy

### 5. Energy-Value of Money (Treasury-to-Oil Ratio)
*   **Strategic Definition:** The purchasing power of the premier financial asset (10Y US Treasury) measured in the premier physical asset (Crude Oil).
*   **Operational Formula:** `(Price of Theoretical 10Y Zero-Coupon Bond) / (Price of WTI Crude Oil)`
    *   *Bond Price Calculation:* `100 / (1 + 10Y_Yield)^10`
*   **Data Source:** Yahoo Finance (`yfinance`).
*   **Tickers:**
    *   Oil: `CL=F` (WTI Crude Futures)
    *   10Y Yield: `^TNX` (CBOE 10 Year Treasury Note Yield Index)

---

## Module 4: Geopolitical Realignment

### 6. The "Prevailing Ism" News Tracker
*   **Strategic Definition:** Quantifies the shift in public discourse from "Globalization" to "Protectionism".
*   **Operational Formula:** Count of news articles mentioning "Tariffs" vs. "Free Trade".
*   **Data Source:** GDELT Project (Global Database of Events, Language, and Tone).
*   **Method:** GDELT 2.0 Doc API (JSON).
*   **Query:** `(tariffs OR protectionism)` vs `("free trade" OR globalization)`
