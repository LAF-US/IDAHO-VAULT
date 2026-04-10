---
authority: LOGAN
related:
- Idaho
- Idaho Legislature
- format
- web
- website
---

# Plan

1.  **Initial Normalization:** Create a Python script to transform the `minidata.csv` into a new `normalized_budget_data.csv` file. This script will map the existing fields to the new schema and leave the missing fields empty. This step is complete.

2.  **Schema Enrichment:** The next step is to populate the missing fields in the `normalized_budget_data.csv` file. This will likely require modifying the scraper to extract more data from the Idaho Legislature website. The fields that need to be populated are: `budget_type`, `sector`, `agency`, `program`, `status`, and `event_date`.

3.  **Publication:** Once the `normalized_budget_data.csv` file is complete, it can be used for publication.

# Remaining Schema and Publication Risks

1.  **Missing Data:** The current `minidata.csv` file is missing several key fields required for the final normalized dataset. Populating these fields will require enhancing the web scraper to extract this information from the Idaho Legislature website. This might be a complex task, as the data may not be available in a structured format.

2.  **Data Ambiguity:** The `last_action` field is being used for `event_summary`, and `title` is being used for `description`. These mappings are not perfect and might not accurately represent the data. The `last_action` field might not always be a summary of the event, and the `title` might not be a good description.

3.  **Status and Event Date:** The `status` and `event_date` fields are critical for tracking the progress of the bills. Without this information, the dataset is of limited use. The scraper needs to be updated to extract this information.

4.  **Categorization:** The `budget_type`, `sector`, `agency`, and `program` fields require categorization of the bills. This information may not be explicitly available on the website and might require some manual categorization or the use of keywords to infer the categories. This could be a time-consuming and error-prone process.
