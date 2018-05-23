#!/usr/bin/env python
import psycopg2


def print_popular_articles(c):
    print("1. What are the most popular three articles of all time?\n")

    c.execute("""SELECT articles.title, count(log.id) FROM articles
        LEFT JOIN log
        ON log.path=CONCAT('/article/', articles.slug)
        AND status='200 OK'
        GROUP BY articles.title
        ORDER BY count DESC
        LIMIT 3;""")

    for i in c.fetchall():
        print('"{}" - {} views'.format(i[0], i[1]))


def print_author_ranking(c):
    print("\n2. Who are the most popular article authors of all time?\n")

    c.execute("""SELECT authors.name, sum(view_count) AS view_sum
        from authors,
        (SELECT articles.author AS author_id, count(log.id) AS view_count
            FROM articles
            LEFT JOIN log
            ON log.path=CONCAT('/article/', articles.slug)
            AND status='200 OK'
            GROUP BY articles.author) AS VC
        WHERE authors.id=author_id
        GROUP BY authors.name
        ORDER BY view_sum DESC;""")

    for i in c.fetchall():
        print('{} - {} views'.format(i[0], i[1]))


def print_error_percentage(c):
    print("\n3. On which days did more than 1% of requests lead to errors?\n")

    c.execute("""SELECT success.date,
            (error.count/(CAST(success.count AS FLOAT)+error.count)*100)
        FROM (SELECT CAST(time AS DATE) AS date, count(*) FROM log
            WHERE status='200 OK'
            GROUP BY date) AS success,
        (SELECT CAST(time AS DATE) AS date, count(*) FROM log
            WHERE status='404 NOT FOUND'
            GROUP BY date) AS error
        WHERE success.date=error.date
        AND (error.count/(CAST(success.count AS FLOAT)+error.count)*100)>1;""")

    for i in c.fetchall():
        print("{0:%B %d, %Y} - {1:.2f}% errors".format(i[0], i[1]))


def main():
    DBNAME = "news"
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    print_popular_articles(c)
    print_author_ranking(c)
    print_error_percentage(c)

    db.close()


if __name__ == "__main__":
    main()
