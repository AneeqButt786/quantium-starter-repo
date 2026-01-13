# Quantium Starter Repository

This repository contains my solutions for Task 1, which focuses on data analysis using Python.
I created a virtual environment to ensure a secure and efficient workflow while completing the task professionally.

## Project Overview

This project involves combining multiple CSV files containing sales data into a single formatted output file for analysis.

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
