# Sales Data Batch ETL Pipeline using Python & Pandas

## Project Overview

This project is an end-to-end Batch ETL (Extract, Transform, Load) pipeline built using Python and Pandas to process and analyze 382K+ synthetic sales records.

The pipeline:

* Extracts raw sales data from CSV
* Performs data cleaning and transformation
* Generates business insights
* Loads processed outputs into report files

---

## Tech Stack

* Python
* Pandas
* Pathlib
* Git
* GitHub
* PyCharm

---

## ETL Flow

Extract → Transform → Load

### Extract

* Loaded sales dataset from CSV

### Transform

Performed:

* Null checks
* Duplicate checks
* Business validation
* Age group segmentation
* Net revenue calculation

### Load

Generated output reports:

* age_summary.csv
* product_sales.csv
* product_net_revenue.csv

---

## Key Insights

* Age group **31–45** generated highest sales
* **Beauty** category had highest total sales
* **Beauty** category also generated highest net revenue

---

## Project Structure

batch_etl_project/

* data/
* output/
* src/
* README.md

---

## Future Improvements

* Add logging
* Add SQL database
* Add dashboard
* Automate pipeline scheduling
