
# UdacityLogsAnalysis
## Purpose
Analyze date from Postgres database which from a fictional website.

To find out the questions beblows:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Database Structure

#### authors
- id
- name
- bio

#### articles
- id
- title
- slug
- lead
- body
- author
- time

#### log
- id
- ip
- method
- path
- status
- time

## Requirement
- Python2
- psycopg2 (Python Library)
- Postgres server & blank database named **"news"**
- [Fictional data provided by Udacity](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

## Execute
execute `$ psql -d news -f newsdata.sql`

execute `$ python main.py`