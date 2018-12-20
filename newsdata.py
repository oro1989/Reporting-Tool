#!/usr/bin/python

import psycopg2

db = psycopg2.connect("dbname=news")
c = db.cursor()


def report1(c):
    # What are the most popular three articles of all time?
    query = '''
    select path, count(*) as views from log
    where status = '200 OK' and path != '/'
    group by path
    order by views desc
    limit 3;
    '''
    c.execute(query)
    rawData = c.fetchall()

    print('\nthe most popular three articles of all time are:')
    for i in range(3):
        print(str(i+1) + ': ' + rawData[i][0][9:] + '---' +
              str(rawData[i][1]) + ' views')
    print('')


def report2(c):
    # Who are the most popular article authors of all time?
    view_query = '''
    create view articles_views as
        select path, count(*) as views from log
        where status = '200 OK' and path != '/'
        group by path;
    '''
    c.execute(view_query)

    view_query = '''
    create view top_rank_ids as
        select sum(articles_views.views) total_views, articles.author
        from articles_views
        join articles on (articles_views.path = '/article/' || articles.slug)
        group by articles.author
        order by total_views desc;
    '''
    c.execute(view_query)

    query = '''
    select authors.name, top_rank_ids.total_views
    from authors join top_rank_ids on authors.id = top_rank_ids.author;
    '''
    c.execute(query)
    rawData = c.fetchall()

    print('the most popular article authors of all time:')
    for i in range(len(rawData)):
        print(str(i+1) + ': ' + rawData[i][0] +
              '----' + str(rawData[i][1]) + ' views')
    print('')


def report3(c):
    # On which days did more than 1% of requests lead to errors?

    view_query = '''
    create view days_total as
        select time::date, status, count(*)
        from log
        group by time::date, status;
    '''
    c.execute(view_query)

    view_query = '''
    create view ok_response as
        select t.time, t.count ok
        from days_total t
        where t.status = '200 OK';
    '''
    c.execute(view_query)

    view_query = '''
    create view error_response as
        select t.time, t.count error
        from days_total t
        where t.status = '404 NOT FOUND';
    '''
    c.execute(view_query)

    query = '''
    select t1.time, t1.ok, t2.error
    from ok_response as t1
    join error_response as t2
    on t1.time = t2.time
    where (t1.ok / t2.error < 99);
    '''
    c.execute(query)
    rawData = c.fetchall()

    print('more than 1% of requests lead to errors on: ')
    for i in range(len(rawData)):
        error_percent = 100.0 * rawData[i][2] / (rawData[i][2] + rawData[i][1])
        print(str(i+1) + ': ' +
              str(rawData[i][0]) + '---' +
              str(round(error_percent, 2)) + ' % errors')
    print('')

report1(c)
report2(c)
report3(c)
db.close()
