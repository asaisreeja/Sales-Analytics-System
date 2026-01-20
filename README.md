# Sales Analytics System

## Description
A Python system that reads, cleans, validates, and analyzes sales transaction data. It also integrates with an external API to fetch product information.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

# Sales Analytics System

## Module 3 – Python Programming Assignment

Project Overview

The Sales Analytics System is a comprehensive Python application developed for an e-commerce scenario. It manages the full data lifecycle: from reading "messy" raw files and cleaning malformed records to enriching data via external APIs and generating professional business intelligence reports.

This project demonstrates proficiency in:

File handling and data cleaning

API integration and data enrichment

Business logic implementation and analytics

Automated report generation

Repository Structure
Sales-Analytics-System/
├── main.py                     # Application entry point & controller
├── README.md                   # Project documentation
├── requirements.txt            # Project dependencies (requests)
│
├── data/
│   ├── sales_data.txt          # Raw pipe-delimited dataset
│   └── enriched_sales_data.txt # Output: Data enriched with API details
│
├── utils/
│   ├── file_handler.py         # Q1 & Q2: File I/O and Data Cleaning
│   ├── data_processor.py       # Q3 & Q5: Analytics logic & Report generation
│   └── api_handler.py          # Q4: DummyJSON API integration
│
└── output/
    └── sales_report.txt        # Final Business Intelligence Report

 Features Implemented
1. Robust File Handling & Cleaning (Q1 & Q2)

Supports multiple encodings: UTF-8, Latin-1, CP1252.

Cleans numeric formatting (removes commas from prices and product names).

Filters invalid records based on business rules (e.g., negative prices, non-standard IDs).

2. Advanced Sales Analytics (Q3)

Financial Metrics: Automated calculation of Total Revenue and Average Order Value.

Regional Analysis: Percentage contribution and transaction counts per region.

Product Insights: Identifies Top 5 selling products and low-performing inventory.

Customer Behavior: Tracks top spenders and unique product purchase history.

3. API Integration & Data Enrichment (Q4)

External Connectivity: Integrates with DummyJSON API to fetch global product data.

Data Mapping: Extracts numeric IDs (e.g., P101 → 101) to link local sales to API categories.

Enrichment: Adds Category, Brand, and Rating metadata to sales records.

Fault Tolerance: Graceful handling of connection timeouts or API errors.

4. Professional Report Generation (Q5)

Automated Export: Generates structured text reports in the output/ folder.

Trend Visualization: Includes daily revenue trends and API enrichment success rates.

 Sample Execution Output
Reading sales data file...
Total raw records read: 80
Parsing and cleaning data...
Validation Summary:
total_input: 80 | invalid: 10 | final_count: 70

Connecting to DummyJSON API...
Successfully fetched products from API.
Enriched data saved to data/enriched_sales_data.txt

Finalizing system and generating report...
Comprehensive report generated: output/sales_report.txt

 How to Run the Project
Prerequisites

Python 3.8 or higher

Steps

Clone the repository:

git clone https://github.com/asaisreeja/Sales-Analytics-System.git
cd Sales-Analytics-System


Install dependencies:

pip install -r requirements.txt


Run the application:

python main.py

Technologies Used

Python (Core): File I/O, Lists/Dictionaries, List Comprehensions

Requests: For external API communication

OS & Datetime: Directory management and report timestamping

Author

Asaisreeja
GitHub: https://github.com/asaisreeja



