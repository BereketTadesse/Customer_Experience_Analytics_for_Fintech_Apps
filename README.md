# Customer Experience Analytics for Ethiopian Fintech Apps

This repository contains the complete data engineering and analysis project for evaluating customer satisfaction with mobile banking apps from three major Ethiopian banks: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank. The project simulates the role of a Data Analyst at Omega Consultancy, a firm advising these banks on how to improve their digital offerings.

## Business Objective

Omega Consultancy aims to help its banking clients enhance customer retention and satisfaction by improving their mobile applications. This project provides a data-driven foundation for strategic recommendations by:

1.  **Scraping** thousands of user reviews from the Google Play Store.
2.  **Analyzing** review sentiment and extracting key themes (e.g., "bugs", "UI", "performance").
3.  **Identifying** key satisfaction drivers and critical pain points for each bank.
4.  **Storing** the cleaned data in a robust, enterprise-grade Oracle database.
5.  **Delivering** a final report with compelling visualizations and actionable insights.
## Project Tasks Breakdown

This project was executed in four distinct tasks, from data collection to final analysis.

### Task 1: Data Collection & Preprocessing

**Goal:** To gather raw user feedback from the Google Play Store and prepare it for analysis.

*   **Activities:**
    *   Used the `google-play-scraper` library to collect over 3,000 reviews, ratings, and dates for the apps of CBE, BOA, and Dashen Bank.
    *   Performed data cleaning by removing duplicate reviews and handling missing values.
    *   Standardized date formats to `YYYY-MM-DD`.
*   **Deliverable:** A clean CSV file (`data/raw_reviews.csv`) containing the initial dataset.
*   **Script:** `scripts/scrape_reviews.py`

### Task 2: Sentiment and Thematic Analysis

**Goal:** To enrich the raw text data with quantitative sentiment and qualitative themes.

*   **Activities:**
    *   Applied a pre-trained NLP model (`distilbert-base-uncased-finetuned-sst-2-english`) to classify each review as `Positive`, `Negative`, or `Neutral`.
    *   Used keyword extraction and rule-based clustering to identify and assign recurring themes to each review (e.g., 'Transaction Performance', 'User Interface & Experience', 'Customer Support').
*   **Deliverable:** An enriched CSV file (`data/task2_sentiment_themes.csv`) with new columns for sentiment and themes.
*   **Script:** `scripts/sentiment_theming.py`

### Task 3: Data Persistence in Oracle Database

**Goal:** To design and implement a relational database schema to store the cleaned data, simulating an enterprise data engineering workflow.

*   **Activities:**
    *   Connected to an Oracle XE database instance.
    *   Designed a relational schema with two tables: `TBL_BANKS` (to store bank information) and `TBL_REVIEWS` (to store review data with a foreign key relationship to `TBL_BANKS`).
    *   Wrote a Python script using `cx_Oracle` to automatically create the tables and efficiently load the 1,200+ records from the enriched CSV.
*   **Deliverable:** A fully populated Oracle database schema.
*   **Script:** `scripts/db_loader.py`

### Task 4: Insights, Visualization, and Recommendations

**Goal:** To analyze the final, structured dataset to derive actionable business insights and create compelling visualizations.

*   **Activities:**
    *   Performed deep-dive analysis on key business questions regarding app stability, competitive advantages, and critical failure points.
    *   Generated a series of plots using Matplotlib and Seaborn, including:
        *   **Rating Polarization Box Plots:** To measure the consistency of user experience.
        *   **Proportional Bar Charts:** To identify unique strengths and weaknesses.
        *   **Theme Count Plots:** To diagnose the most frequent causes of 1-star reviews.
    *   Synthesized all findings into a final report.
*   **Deliverable:** A collection of charts in the `visuals/` directory and a final analytical report (this README and/or a Jupyter Notebook).
*   **Script:** `scripts/visualization.ipynb`
## How to Run This Project

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Set Up Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**
    -   Ensure you have a running instance of Oracle XE Database.
    -   Install the Oracle Instant Client and ensure its path is correctly configured.

5.  **Execute Scripts in Order:**
    -   Run `scrape_reviews.py` to generate the raw data (if not already present).
    -   Run `sentiment_theming.py` to process the raw data and generate the enriched CSV.
    -   Run `db_loader.py` to populate the Oracle database.
    -   Run `visualization.ipynb` or the corresponding Jupyter Notebook to generate all analytical charts.

## Summary of Key Insights

1.  **App Experience is Highly Inconsistent:** The analysis revealed a dramatic difference in user experience consistency. **Dashen Bank** offers a highly reliable and positive experience, while **BOA's** app is extremely polarized (a "love it or hate it" gamble), and **CBE** has a strong core experience but suffers from significant "edge case" issues.

2.  **A Shared, Critical Weakness:** The single most dominant and identifiable reason for negative reviews across **all three banks** is poor **'Transaction Performance'**. Fixing the reliability and speed of transactions is the most critical challenge for the entire sector.

3.  **UI is the Key Strength:** Among the identifiable positive themes, a high-quality **'User Interface & Experience'** was the most common driver of satisfaction for all banks.