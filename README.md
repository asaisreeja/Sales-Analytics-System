# Sales Analytics System

## Description
A Python system that reads, cleans, validates, and analyzes sales transaction data. It also integrates with an external API to fetch product information.

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

# Sales Analytics System

## Module 3 – Python Programming Assignment

### 📌 Project Overview

The **Sales Analytics System** is a Python-based data preprocessing and validation application developed for an e-commerce use case.
It reads raw and messy sales transaction data, handles encoding issues, cleans malformed values, validates business rules, and produces a reliable dataset for further analysis and reporting.

This project demonstrates core Python skills including file handling, data cleaning, exception handling, and structured programming.

---

## 📂 Repository Structure

```
Sales-Analytics-System/
│
├── main.py                     # Application entry point
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies
│
├── utils/
│   └── file_handler.py         # File reading, parsing, validation logic
│
├── data/
│   └── sales_data.txt          # Provided sales dataset
│
└── output/                     # Generated outputs (future use)
```

---

## 🎯 Assignment Objectives

The system is designed to:

1. Read sales data files with potential encoding issues
2. Clean and preprocess raw transaction records
3. Validate data using predefined business rules
4. Filter invalid transactions
5. Prepare clean data for analytics and reporting

---

## ⚙️ Features Implemented (Question 2)

### 1. Robust File Handling

* Reads pipe (`|`) delimited sales data files
* Automatically handles non-UTF-8 encodings (`utf-8`, `latin-1`, `cp1252`)
* Skips header row and empty lines
* Gracefully handles file and encoding errors

---

### 2. Data Parsing & Cleaning

* Splits records using the pipe (`|`) delimiter
* Removes commas from product names (e.g., `Mouse,Wireless`)
* Cleans numeric fields by removing formatting commas (e.g., `1,500 → 1500`)
* Converts:

  * `Quantity` → integer
  * `UnitPrice` → float
* Skips malformed rows with incorrect field counts

---

### 3. Data Validation & Filtering

Transactions are validated using the following rules:

* Quantity must be greater than zero
* Unit price must be greater than zero
* TransactionID must start with `T`
* ProductID must start with `P`
* CustomerID must start with `C`
* CustomerID and Region must not be empty

The system also:

* Displays available regions before filtering
* Displays transaction amount range (min and max)
* Provides a detailed validation summary

---

## 📊 Sample Execution Output

```
Total raw records read: 80
Total parsed records: 80

Available Regions: {'North', 'South', 'East', 'West'}
Transaction Amount Range: -8982.0 - 818960.0

Validation Summary:
total_input: 80
invalid: 10
filtered_by_region: 0
filtered_by_amount: 0
final_count: 70
```

---

## ▶️ How to Run the Project

### Prerequisites

* Python 3.8 or higher

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/asaisreeja/Sales-Analytics-System.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Sales-Analytics-System
   ```

3. Run the application:

   ```bash
   python main.py
   ```

---

## 🧰 Technologies Used

* Python (Core Python)
* File I/O operations
* Data structures (lists, dictionaries)
* Exception handling

---

## 📝 Notes

* No external libraries are required for Question 2
* The project is structured for easy extension (API integration, analytics, reporting)
* Further modules will build upon the cleaned and validated dataset

---

## 👩‍💻 Author

**Asaisreeja**
GitHub: [https://github.com/asaisreeja](https://github.com/asaisreeja)

