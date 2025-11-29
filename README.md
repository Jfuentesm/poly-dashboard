# Polycrisis Dashboard
A strategic intelligence tool for tracking the structural shifts in the global economic, monetary, and geopolitical order.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

---

## Overview

This project is not a standard financial dashboard. It is a strategic intelligence tool designed to track and interpret a fundamental paradigm shift in the global order. It is the technical implementation of the analysis presented in the foundational research report, **"A Strategic Analysis of the Global Polycrisis."**

The report concludes that we are not in a cyclical downturn but a structural **"polycrisis,"** driven by a confluence of three powerful and interconnected forces:

1.  **Unsustainable Debt Dynamics:** The fiscal trajectory of the United States, the issuer of the world's reserve currency, has become mathematically unsustainable, making debt monetization a structural necessity, not a policy choice.
2.  **Geopolitical Realignment:** The weaponization of the U.S. dollar and its associated financial infrastructure is forcing a global realignment, with nations actively seeking alternatives and moving toward a multipolar monetary system.
3.  **Physical vs. Financial Economy:** There is a dangerous and growing disconnect between the world of financial claims (money, debt) and the finite physical world of energy and commodities that underpins it. The report's core insight is that **"you can't print commodities,"** and this dashboard tracks the inevitable and often inflationary reconciliation between these two realms.

This dashboard's purpose is to provide a coherent, data-driven narrative of this unfolding polycrisis. Each indicator has been chosen to act as a real-time signal, tracking one of the core theses of the report to create a holistic view of the systemic stresses and transformations underway.

## Live Dashboard

**[Link to the live dashboard application]** `(placeholder)`

## Features

- **Narrative-Driven Modules:** The dashboard is organized into four distinct modules, each tracking a core thesis from the foundational report.
- **Strategic Indicators:** Each chart is chosen to be a signal, not noise, with a clear explanation of its strategic relevance.
- **Interactive Visualizations:** All charts are built with Plotly for interactivity (zoom, pan, hover-for-details) and time-range selection.
- **Automated Data Pipelines:** Scripts automatically fetch the latest data from open-source APIs to ensure indicators are as current as possible.
- **Transparent Sourcing:** All data sources are clearly cited, prioritizing free and official APIs like FRED, EIA, and the U.S. Treasury.

## Data Dictionary

For a comprehensive breakdown of every Key Performance Indicator (KPI), including the exact formula, strategic logic, and technical data source (URL/API), please refer to the **[DATA_DICTIONARY.md](DATA_DICTIONARY.md)**.

## Dashboard Modules

The dashboard is organized into four interconnected modules that guide the user through the report's core logic.

---

### Module 1: U.S. Fiscal & Monetary Health
This module is the epicenter of the crisis. The U.S. fiscal situation is the primary driver of instability, forcing the Federal Reserve into a position where it must ultimately monetize debt to prevent a systemic collapse.

| Indicator | Strategic Rationale | Data Source(s) |
| :--- | :--- | :--- |
| **Fiscal Unsustainability Ratio** | The cornerstone metric. Tracks the percentage of federal tax revenue consumed by mandatory spending and net interest, revealing the "debt spiral" in real time. | FRED |
| **Public Debt Burden** | Tracks the total federal debt relative to the economy's capacity to support it (Debt-to-GDP), a key measure of national solvency. | FRED |
| **Debt Monetization Proxy** | Tracks the growth of the Federal Reserve's balance sheet as a proxy for the central bank absorbing government debt to enable deficit spending. | FRED |
| **Cost of Debt (Treasury Yields)** | Tracks market interest rates (2-Year and 10-Year Treasuries), which are a leading indicator of future interest costs and fiscal pressure. | FRED |

---

### Module 2: De-Dollarization & The Multipolar Monetary System
This module tracks the erosion of the post-1971 petrodollar system. As confidence in U.S. debt as a "risk-free" asset wanes, we monitor the flight to neutral assets and the actions of foreign powers to divest from the dollar system.

| Indicator | Strategic Rationale | Data Source(s) |
| :--- | :--- | :--- |
| **U.S. Dollar Dominance** | Tracks the Trade-Weighted U.S. Dollar Index. A sustained decline signals a structural shift away from the dollar as the undisputed global reserve currency. | FRED |
| **Foreign Confidence in U.S. Debt** | Tracks the holdings of U.S. Treasuries by major foreign powers (e.g., China, Japan) as a primary signal of active de-dollarization. | U.S. Treasury TIC |
| **Central Bank Flight to Safety** | Tracks the verifiable surge in gold purchases by global central banks, a key indicator of the move toward neutral reserve assets. | World Gold Council |
| **Performance of Neutral Assets** | Tracks the price action of Gold and Bitcoin against fiat currencies as a barometer of distrust in the traditional debt-based system. | Yahoo Finance, CoinGecko |

---

### Module 3: The Physical vs. The Financial Economy
This module operationalizes the **"you can't print commodities"** thesis. It measures the value of financial assets against real-world physical goods to gauge the true health of the system and detect inflationary pressures at their source.

| Indicator | Strategic Rationale | Data Source(s) |
| :--- | :--- | :--- |
| **Key Commodity Prices** | Tracks foundational commodities (Oil, Copper, Food). Persistently rising prices signal the inflationary reconciliation of financial claims with physical reality. | EIA, Yahoo Finance, FAO |
| **Energy-Value of Money** | A crucial calculated metric measuring the purchasing power of financial assets (e.g., a Treasury bond) in real-world energy (e.g., barrels of oil). | Calculated |
| **U.S. Energy Independence** | Tracks domestic crude oil production. A decline in U.S. energy production removes a key subsidy for the petrodollar system and accelerates the crisis. | U.S. EIA |

---

### Module 4: Geopolitical Realignment & The New Mercantilism
This module tracks the strategic responses of major global powers to the crisis, focusing on the Sino-American competition and the broader shift away from globalization toward state-directed, protectionist industrial policy.

| Indicator | Strategic Rationale | Data Source(s) |
| :--- | :--- | :--- |
| **U.S. vs. China Economic Scale** | Tracks both Nominal and Purchasing Power Parity (PPP) GDP to understand the different dimensions of the Sino-American competition. | IMF, World Bank |
| **Trade Conflict Monitor** | Tracks the U.S. trade balance with China. A shrinking deficit signals intensifying economic conflict and a challenge to China's export-led model. | FRED, IMF |
| **Industrial Onshoring** | Tracks the U.S. Industrial Production Index and manufacturing's share of GDP as a signal of a successful re-industrialization policy. | FRED, World Bank |
| **"Prevailing Ism" News Tracker** | A qualitative indicator tracking the frequency of key terms (e.g., "tariffs," "national security" vs. "free trade," "globalization") in financial news. | NewsAPI, GDELT |

## Technical Stack

- **Backend & Data Manipulation:** Python, Pandas
- **Data Acquisition:** `requests`, `pandas-datareader`
- **Frontend & Visualization:** Plotly Dash / Streamlit
- **Web Scraping (where needed):** BeautifulSoup

## Getting Started

To run the dashboard on your local machine, follow these steps.

### Prerequisites

- Python 3.9 or higher
- Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/polycrisis-dashboard.git
    cd polycrisis-dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Usage

Run the dashboard application:
```sh
python app.py
```
Navigate to `http://127.0.0.1:8050` (or the address provided in your terminal) in your web browser.

## Contributing

Contributions are welcome! If you have suggestions for new indicators, improvements to the data pipelines, or frontend enhancements, please feel free to open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingIndicator`)
3.  Commit your Changes (`git commit -m 'Add some AmazingIndicator'`)
4.  Push to the Branch (`git push origin feature/AmazingIndicator`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
