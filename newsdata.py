#!/usr/bin/env python

import psycopg2

db = psycopg2.connect("dbname=news")
c = db.cursor()


def view_articles_views(c):
    # Creates a view of total views of each article and the author
    view_query = '''
    CREATE VIEW articles_views AS
        SELECT articles.slug, articles.author, count(*) AS views FROM articles
        JOIN log ON (log.path = '/article/' || articles.slug)
        GROUP BY articles.slug, articles.author
        ORDER BY views desc;
    '''
    c.execute(view_query)
    db.commit()


def query_top_articles(c):
    # What are the most popular three articles of all time?
    query = '''
    SELECT * FROM articles_views
    limit 3;
    '''
    c.execute(query)
    rawData = c.fetchall()

    print('\nthe most popular three articles of all time are:')
    for i in range(3):
        print(str(i+1) + ': ' + rawData[i][0] + '---' +
              str(rawData[i][1]) + ' views')
    print('')


def query_top_authors(c):
    # Who are the most popular article authors of all time?

    query = '''
    SELECT authors.name, sum(articles_views.views) AS total_views
    FROM authors JOIN articles_views ON authors.id = articles_views.author
    GROUP BY articles_views.author, authors.name
    ORDER BY total_views desc;
    '''
    c.execute(query)
    rawData = c.fetchall()

    print('the most popular article authors of all time:')
    for i in range(len(rawData)):
        print(str(i+1) + ': ' + rawData[i][0] +
              '----' + str(rawData[i][1]) + ' views')
    print('')


def query_highErrorRate(c):
    # On which days did more than 1% of requests lead to errors?

    query = '''
    SELECT subq.*,
    round(1.0*subq.num_errors/subq.total_responses , 4) AS errors_percent
    FROM(
        SELECT date(l.time), COUNT(*) total_responses,
        SUM((status = '404 NOT FOUND')::int) num_errors
        FROM log l
        GROUP BY date(l.time)
    ) subq
    WHERE ((1.0 * num_errors / total_responses) > 0.01);
    '''
    c.execute(query)
    rawData = c.fetchall()

    print('more than 1% of requests lead to errors on: ')
    for i in range(len(rawData)):
        error_percent = 100.0 * float(rawData[i][3])
        print(str(i+1) + ': ' +
              str(rawData[i][0]) + '---' +
              str(error_percent) + '% errors')
    print('')

# Create view articles_views if not already existing.
try:
    view_articles_views(c)
except:
    db.close()
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

query_top_articles(c)
query_top_authors(c)
query_highErrorRate(c)
db.close()
