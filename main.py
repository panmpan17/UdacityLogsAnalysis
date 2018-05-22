import psycopg2

def task1(c):
	print("Task 1\n")

	c.execute("""SELECT articles.title, count(log.id) FROM articles
		LEFT JOIN log
		ON log.path LIKE CONCAT('/article/', articles.slug)
		AND status='200 OK'
		GROUP BY articles.title
		ORDER BY count DESC
		LIMIT 3;""")

	for i in c.fetchall():
		print('"{}" - {} views'.format(i[0], i[1]))

def task2(c):
	print("\nTask 2\n")

	c.execute("""SELECT authors.name, sum(view_count) AS view_sum
		from authors, (SELECT articles.author AS author_id, count(log.id) AS view_count
		    FROM articles
		    LEFT JOIN log
		    ON log.path LIKE CONCAT('/article/', articles.slug)
		    AND status='200 OK'
		    GROUP BY articles.author) AS VC
		WHERE authors.id=author_id
		GROUP BY authors.name
		ORDER BY view_sum DESC;""")

	for i in c.fetchall():
		print('{} - {} views'.format(i[0], i[1]))

def task3(c):
	print("\nTask 3\n")

	c.execute("""SELECT success.date, (CAST(fail.count AS FLOAT)/CAST(success.count AS FLOAT))*100 AS fail_chance
		FROM (SELECT CAST(time AS DATE) AS date, count(*) FROM log
		WHERE status='200 OK'
		GROUP BY date) AS success, (SELECT CAST(time AS DATE) AS date, count(*) FROM log
		WHERE status='404 NOT FOUND'
		GROUP BY date) AS fail
		WHERE success.date=fail.date;""")

	for i in c.fetchall():
		print("{} - {}% errors".format(i[0].strftime("%b %d,%Y"), i[1]))

def main():
	DBNAME = "news"
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()

	task1(c)
	task2(c)
	task3(c)

	db.close()

if __name__ == "__main__":
	main()