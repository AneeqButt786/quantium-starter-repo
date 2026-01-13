# Quantium Starter Analytics Repository

Welcome to the Quantium Starter Repository — an end-to-end, professional data solution for analyzing and visualizing sales trends of the Pink Morsel product for Soul Foods. This project streamlines sales data preparation and delivers actionable insights through a high-quality analytical dashboard, leveraging robust Python technologies.

---

## Solution Architecture

This repository is engineered to provide:

- **Automated Data Consolidation:** Extraction, cleaning, and unification of all Pink Morsel transactions from disparate daily sales reports.
- **Interactive Data Exploration:** A responsive dashboard enabling granular region-based sales analysis and clear visualization of business-impacting events (such as price changes).

The workflow is organized into two core modules:

1. **Data Preparation Script** — Aggregates and standardizes product sales data.
2. **Sales Analysis Dashboard** — Presents user-friendly, dynamic sales insights.

---

## 1. Data Preparation with `combinig_dataset.py`

### Overview

The `combinig_dataset.py` script is designed to efficiently process all sales data files in the `data/` directory, focusing exclusively on the "pink morsel" product. It creates a unified dataset that is optimized for downstream analysis and visualization.

#### Key Attributes

- **Targeted Extraction:** Isolates sales entries for "pink morsel" only.
- **Data Consistency:** Converts and consolidates price and quantity data, ensuring numeric integrity.
- **Standard Output:** Produces a single `combined_sales_data.csv` file with columns:
  - `sales` – transaction value (numeric, calculated)
  - `date` – transaction date
  - `region` – transaction region (North, South, East, West)

#### How it Works

- Iterates over all `.csv` files in the `data/` directory.
- Selects records for the "pink morsel" product.
- Multiplies price (converted from string with `$`) and quantity to compute sales.
- Writes results to a clean, analysis-ready CSV.

#### Usage

To generate your analytics-ready dataset, run:

```bash
python combinig_dataset.py
```

Sample structure of the resulting file:

| sales  | date       | region |
|--------|------------|--------|
| 1638.0 | 2018-02-06 | north  |
| 1647.0 | 2018-02-06 | south  |
|   ...  |    ...     |  ...   |

#### Technical Specifications

- **Language/Dependencies:** Pure Python (standard library `csv`, `os` only).
- **Input Format:** Source files must include: `product`, `price`, `quantity`, `date`, `region`.
- **Output:** `combined_sales_data.csv` in the repository root.

---

## 2. Interactive Sales Dashboard (`app.py`)

### Business Context

Built with Dash, the analytics app empowers Quantium and Soul Foods teams to interactively explore Pink Morsel sales performance, with a special focus on the impact of pricing decisions.

#### Central Analysis Question

> **Did Pink Morsel sales increase or decrease after the price adjustment on January 15, 2021?**

### Dashboard Features

- **Time-Series Visualization:** Dynamic line chart showing daily sales.
- **Advanced Region Filtering:** Instantly segment data by region (All, North, South, East, West).
- **Event Highlighting:** Visually distinguishes sales before and after the price increase with shaded backgrounds.
- **Modern UI/UX:** Stylish, accessible interface with responsive layout and intuitive controls.
- **Insightful Hover Interactions:** Tooltips expose granular details for data-driven decision making.

#### How to Launch

1. Install necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure `combined_sales_data.csv` is present.
3. Start the app:
   ```bash
   python app.py
   ```
4. Open your browser to [http://127.0.0.1:8050](http://127.0.0.1:8050).

#### Requirements

- **Python 3.x**
- **Core packages:** 
  - `dash[testing]` — Web framework with testing utilities
  - `pandas` — Data processing and manipulation
  - `plotly` — Interactive charting library
  - `pytest` — Testing framework

#### Development Approach

- Cohesive, self-contained codebase for rapid onboarding and extension.
- Data is loaded once at startup; all real-time interactivity handled via Dash callbacks.

---

## 3. Test Suite (`test_app.py`)

### Overview

The repository includes a comprehensive test suite using `pytest` and Dash's testing framework to ensure the dashboard components are correctly implemented and functional.

### Test Coverage

The test suite verifies three critical UI components:

1. **Header/Title Presence** — Confirms the main title "Pink Morsel Sales Analysis" is rendered correctly.
2. **Line Chart Visualization** — Validates that the sales chart component is present and properly configured.
3. **Region Picker** — Ensures the radio button filter is functional with all expected options (All, North, East, South, West) and correct default selection.

### Running Tests

To execute the test suite:

```bash
pytest test_app.py -v
```

For more detailed output:

```bash
pytest test_app.py -v --tb=short
```

### Expected Results

All tests should pass, confirming:
- ✅ Header component is present with correct text
- ✅ Chart visualization is rendered
- ✅ Region filter is functional with all options

### Test Configuration

- `pytest.ini` — Configuration file that suppresses third-party deprecation warnings for cleaner test output.
- Tests use unit testing approach to verify component structure without requiring browser automation.

---

## Repository Contents

- `combinig_dataset.py`  
  Consolidates, filters, and standardizes source sales data. Outputs `combined_sales_data.csv`.

- `app.py`  
  Provides an interactive web dashboard for Pink Morsel sales trends and region-level analysis.

- `test_app.py`  
  Automated test suite verifying all dashboard UI components are correctly rendered.

- `pytest.ini`  
  Pytest configuration file for test execution settings.

- `requirements.txt`  
  Lists all required Python packages for local installation.

---

> **Quantium best practice:**  
> - Code, filenames, and outputs follow clear naming conventions.
> - All processing and visualization is focused on the Pink Morsel product for maximum business relevance.
> - The repository is structured for transparency, reliability, and ease of audit or further development.

For further queries or to contribute improvements, please contact the Quantium data science team.

