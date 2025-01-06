# Learning DBT

Course: https://learn.getdbt.com/learn/course/dbt-fundamentals/welcome-to-dbt-fundamentals-5min/welcome

Documentation: https://docs.getdbt.com/

## ETL and ELT

Extract transform load -> get data, transform it and load it into a new database that can then be queried by Data Analyst.

Dataware house combines database and supercomputer, because data can be transformed directly in the DW.

Therefore Extract, Load, Transform has become a new standard.

## Analytics Engineer

Taking raw data, and transforming it to BI.

Gives Data Engineer the time to Extract and Load and Data Analyst to work with the data after the transform.

| Data Engineer                                 | Analytics Engineer                                                           | Data Analysts            |
|-----------------------------------------------|------------------------------------------------------------------------------|--------------------------|
| Build custom data ingestion integrations      | Provide clean, transformed data ready for analysis                           | Deep insights work       |
| Manage overall pipleine orchestration         | APply software engineering practices to analytics code                       | Work with business users |
| Develio and deploy machine learning endpoints | Maintain data docs and definitions                                           | Dashboards               |
| Build and maintain the data platform          | Train business users on how to use a data platform data visulatization tools | Forecasting              |
| DW performance optimization                   |                                                                              |                          |

## dbt in the modern data stack

dbt work directly on the data platform.

```bash
dbt run
```

```bash
dbt test
```

Build does both run and test.
```bash
dbt build
```


```bash
dbt docs generate
```


```bash
dbt docs generate
```
