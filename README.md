
# 📊 Event-Driven CSV File ETL
[Python](https://www.python.org/) | [PostgreSQL](https://www.postgresql.org/) | [Pandas](https://pandas.pydata.org/) | [SQLAlchemy](https://www.sqlalchemy.org/) | [Pydantic](https://docs.pydantic.dev/) | [Prefect](https://www.prefect.io/) | [GitHub Actions](https://github.com/features/actions)

---
## Project Overview

This project is an event-driven ETL pipeline designed to automatically process and clean incoming CSV files.

Whenever a new CSV file is added to the `storage/` directory, the pipeline is triggered to:
- Ingest the raw file
- Validate and enforce a predefined schema
- Clean and standardize the data (e.g., handle missing values, remove duplicates)
- Load the processed data into a structured output (CSV, Excel, or database)

## Problem It Solves

In many real-world scenarios, data teams receive multiple unclean or inconsistent files (e.g., `customers.csv`, Excel sheets) from different sources. Manually cleaning and standardizing these files is time-consuming and error-prone.

This pipeline automates that process by allowing users to simply drop raw files into a directory, after which the system handles validation, transformation, and storage. This ensures consistent, reliable, and analysis-ready data with minimal manual effort.


1. **Extracts** data using Python (`Pathlib`, `subprocess`)  
2. **Validates** data using **Pydantic** models  
3. **Transforms** data using **Pandas**  
4. **Saves raw JSON** files for auditing  
5. **Loads** transformed data into **Neon PostgreSQL** using **SQLAlchemy**  
6. Orchestrates the workflow automatically using **Prefect** and **GitHub Actions**  
7. sends slack notifications after failure or success

This pipeline is fully **serverless-ready** and suitable for modern **data engineering automation**.

---

## Project Structure
README.md
├── requirements.txt
| -- .github/workflows/flows.yml
├── src
│   ├── __init__.py
│   ├── extract_file.py
│   ├── load_save_data.py
│   ├── main.py
│   ├── models.py
│   ├── save_raw.py
│   ├── transform_data.py
│   └── validate_data.py
├── storage
│   ├── sample101.csv
│   └── sample_data.csv
├── tests
│   ├── __init__.py
│   ├── test_extract.py
│   ├── test_load_save.py
│   └── test_save_raw.py


---

## Features

- **Event-Driven**: Starts ETL automatically when CSV is committed  
- **Validation**: Pydantic models ensure schema consistency  
- **Transformation**: Pandas handles cleaning, type conversion, and calculations  
- **Raw Data Archiving**: Saves raw JSON for traceability  
- **Database Integration**: Uses SQLAlchemy to load data into PostgreSQL  
- **Orchestration**: Prefect flows handle ETL scheduling and retries  
- **CI/CD Ready**: GitHub Actions triggers ETL without manual intervention  

---

## Usage

1. Clone the repository:
2. Install dependencies:
3.Configure `.env` with your PostgreSQL credentials:
4. Commit any CSV file to `storage/` folder:
don't bother deleting the commited file make sure filename as a difference than the first example 
if first committed " sales.csv " then next file mmust be at leat "sales1.csv " otherwise etl will not run 

5. GitHub Actions will automatically trigger the ETL workflow:  
Extract → Validate → Transform → Save raw JSON → Load into PostgreSQL  

6. Check Prefect UI (if running locally or cloud) for flow monitoring:


---

## Workflow Diagram

Commit CSV to storage → Extract CSV → Validate with Pydantic → Transform with Pandas → Save raw JSON → Load to PostgreSQL → Orchestrate & Monitor with Prefect

---

## Tools & Libraries

| Tool        | Purpose                                   | Link |
|------------|-------------------------------------------|------|
| Python     | Core programming                           | https://www.python.org/ |
| Pandas     | Data transformation                        | https://pandas.pydata.org/ |
| Pydantic   | Data validation                            | https://docs.pydantic.dev/ |
| SQLAlchemy | Database ORM                               | https://www.sqlalchemy.org/ |
| Prefect    | Workflow orchestration                     | https://www.prefect.io/ |
| PostgreSQL | Data storage                               | https://www.postgresql.org/ |
| GitHub Actions | CI/CD & event-driven triggers          | https://github.com/features/actions |
| Pathlib    | File system path management                | https://docs.python.org/3/library/pathlib.html |
| Subprocess | Run external commands (optional)           | https://docs.python.org/3/library/subprocess.html |

---

## Testing

Run the tests using **pytest**:
---

## Notes

- Ensure `.env` is **never committed** to GitHub (add to `.gitignore`)  
- Raw JSON files are stored in `/storage/raw/`  
- The ETL pipeline is modular—easy to extend with new CSV sources or transformations