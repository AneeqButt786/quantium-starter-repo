# Quantium Starter Repository

This repository contains my solutions for Task 1, which focuses on data analysis using Python.
I created a virtual environment to ensure a secure and efficient workflow while completing the task professionally.

## Project Overview

This project involves combining multiple CSV files containing sales data into a single formatted output file for analysis, and then visualizing the data using a Dash web application to answer business questions about sales trends.

## Data Combination Script

### Description

The `combinig_dataset.py` script processes three daily sales data CSV files and combines them into a single output file with three fields:
- **Sales**: Calculated as price × quantity for each record
- **Date**: The transaction date
- **Region**: The sales region (north, south, east, west)

### Features

- Reads and processes multiple CSV files automatically
- Calculates total sales by multiplying price and quantity
- Handles price strings with dollar signs (e.g., "$3.00")
- Combines all records into a single output file
- Includes error handling for missing files
- Provides progress feedback during execution

### Usage

1. Ensure you have Python 3.x installed
2. Navigate to the repository directory
3. Run the script:

```bash
python combinig_dataset.py
```

### Input Files

The script processes the following input files located in the `data/` directory:
- `daily_sales_data_0.csv`
- `daily_sales_data_1.csv`
- `daily_sales_data_2.csv`

### Output

The script generates `combined_sales_data.csv` in the root directory with the following structure:

| Sales | Date | Region |
|-------|------|--------|
| 1638.0 | 2018-02-06 | north |
| 1647.0 | 2018-02-06 | south |
| ... | ... | ... |

### Code Structure

The script is organized into modular functions:
- `parse_price()`: Converts price strings to numeric values
- `calculate_sales()`: Computes total sales (price × quantity)
- `combine_csv_files()`: Main function that processes and combines all CSV files
- `main()`: Entry point that defines input/output files and executes the combination

### Requirements

- Python 3.x
- Standard library modules: `csv`, `os`, `pathlib`

No external dependencies are required - the script uses only Python's built-in libraries.

## Sales Data Visualizer (Dash App)

### Description

The `app.py` script creates an interactive web application using Dash to visualize sales data over time. The app helps answer the business question: **"Were sales higher before or after the Pink Morsel price increase on January 15th, 2021?"**

### Features

- Interactive line chart showing total sales over time
- Data aggregated by date (sums all sales for each day)
- Visual marker indicating the price increase date (January 15, 2021)
- Clean, professional interface with appropriate axis labels
- Responsive design with hover tooltips

### Usage

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure the `combined_sales_data.csv` file exists (run `combinig_dataset.py` first if needed)

3. Run the Dash application:

```bash
python app.py
```

4. Open your web browser and navigate to the URL shown in the terminal (typically `http://127.0.0.1:8050`)

### Code Structure

The app is organized into simple, modular functions:
- `load_sales_data()`: Reads and processes the CSV file, groups sales by date
- `create_line_chart()`: Creates the Plotly line chart with price increase marker
- `create_app()`: Configures the Dash app layout and components
- `main()`: Entry point that runs the application

### Requirements

- Python 3.x
- External packages (install via `requirements.txt`):
  - `dash`: Web framework for building the application
  - `pandas`: Data processing and manipulation
  - `plotly`: Interactive charting library
