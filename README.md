# Automated Job Scraper and Analyzer for Halifax
This project is an automated pipeline designed to collect and analyze job postings in Halifax, Canada. The pipeline categorizes job opportunities by sector, salary range, and growing demand, with the goal of helping users find and apply for relevant job openings.

Currently, the focus is on scraping job postings for "Data Engineer" roles, but the system is designed to be scalable and adaptable to other job titles and categories in the future.

## Key Features
 - Web Scraping: Uses BeautifulSoup to collect job postings from various job boards.
 - Data Cleaning and Standardization: Leverages Python and pandas to clean, transform, and standardize the collected data.
 - Scheduling: Utilizes Apache Airflow to automate and schedule the scraping and analysis tasks.
 - Database Storage: Stores processed data in a PostgreSQL database for easy querying and analysis.
 - Future Enhancements: Potential integration of machine learning or OpenAI for advanced job description analysis.

## Goals
 - Help users identify and apply for job opportunities efficiently.
 - Provide insights into job market trends, such as high-demand sectors and salary ranges.
 - Serve as a foundation for future enhancements, including advanced NLP-based job description analysis.

## Technologies Used
 - Web Scraping: BeautifulSoup
 - Data Processing: Python, pandas
 - Workflow Automation: Apache Airflow
 - Database: PostgreSQL

## Future Plans
 - Expand job categories beyond "Data Engineer."
 - Implement machine learning or OpenAI-based analysis for job descriptions.
 - Add features for automated job application submissions.

 ---

## 💡 Author
- Carlos Hayashi - [@9caca](https://github.com/9caca)
- Distributed under the [MIT License](https://github.com/9caca/datajobs_pipeline/blob/master/LICENSE)