"""
Data Combination Script
=======================
This script combines multiple CSV files containing sales data into a single
formatted output file with three fields: Sales, Date, and Region.

The script:
1. Reads three daily sales data CSV files
2. Calculates total sales (price × quantity) for each record
3. Extracts date and region information
4. Combines all records into a single output file
"""

import csv
import os
from pathlib import Path


def parse_price(price_string):
    """
    Parse price string (e.g., "$3.00") and convert to float.
    
    Args:
        price_string (str): Price string with dollar sign and decimal
        
    Returns:
        float: Numeric price value
    """
    # Remove dollar sign and convert to float
    return float(price_string.replace('$', ''))


def calculate_sales(price, quantity):
    """
    Calculate total sales by multiplying price and quantity.
    
    Args:
        price (str): Price string (e.g., "$3.00")
        quantity (str): Quantity as string
        
    Returns:
        float: Total sales amount
    """
    price_value = parse_price(price)
    quantity_value = int(quantity)
    return price_value * quantity_value


def combine_csv_files(input_files, output_file):
    """
    Combine multiple CSV files into a single formatted output file.
    
    This function reads each input CSV file, processes the data to calculate
    sales, and writes the combined results to an output file with columns:
    Sales, Date, Region.
    
    Args:
        input_files (list): List of input CSV file paths
        output_file (str): Path to the output CSV file
    """
    # Get the base directory (parent of script location)
    script_dir = Path(__file__).parent
    
    # List to store all processed records
    all_records = []
    
    # Process each input file
    for input_file in input_files:
        file_path = script_dir / input_file
        
        # Check if file exists
        if not file_path.exists():
            print(f"Warning: File {file_path} not found. Skipping...")
            continue
        
        print(f"Processing {input_file}...")
        
        # Read and process the CSV file
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Process each row in the file
            for row in csv_reader:
                # Calculate sales (price × quantity)
                sales = calculate_sales(row['price'], row['quantity'])
                
                # Extract date and region
                date = row['date']
                region = row['region']
                
                # Store the processed record
                all_records.append({
                    'Sales': sales,
                    'Date': date,
                    'Region': region
                })
    
    # Write the combined data to output file
    output_path = script_dir / output_file
    
    print(f"\nWriting combined data to {output_file}...")
    print(f"Total records: {len(all_records)}")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        # Define the field names for output
        fieldnames = ['Sales', 'Date', 'Region']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header row
        csv_writer.writeheader()
        
        # Write all records
        csv_writer.writerows(all_records)
    
    print(f"Successfully created {output_file} with {len(all_records)} records.")


def main():
    """
    Main function to execute the data combination process.
    
    Defines input files, output file, and calls the combination function.
    """
    # Define input CSV files (relative to script directory)
    input_files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv',
        'data/daily_sales_data_2.csv'
    ]
    
    # Define output file name
    output_file = 'combined_sales_data.csv'
    
    # Combine the CSV files
    combine_csv_files(input_files, output_file)
    
    print("\nData combination completed successfully!")


# Execute the main function when script is run
if __name__ == '__main__':
    main()
