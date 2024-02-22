from src.config import config
import psycopg2
from psycopg2 import sql
from datetime import datetime


def connect():
    con = None
    try:
        con = psycopg2.connect(**config())
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Add daily workhours for a consult
def db_get_workhours(date=datetime.now()):
    date_ob = datetime.date(date)
    query = sql.SQL(
            '''
            SELECT consultname, customername, DATE(starttime) as work_date,
            ROUND ( 
            SUM((EXTRACT(EPOCH FROM (endtime - starttime))/60) - lunchbreak) / 60
            , 2) AS total_hours 
            FROM workhours 
            WHERE CAST(starttime AS DATE) = %(date_ob)s 
            GROUP BY consultname, customername, work_date ORDER BY consultname, work_date ASC;
            '''
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(
            query,
            {
                "date_ob": date_ob,
            },
        )
        rows = cursor.fetchall()
        cursor.close()
        con.close()
        return rows


def db_cumulative_hours_by_customers(date=datetime.now()):
    date_ob = datetime.date(date)
    query = sql.SQL(
        '''
        SELECT consultname, customername, 
        ROUND (
            SUM((EXTRACT(EPOCH FROM (endtime - starttime)/60) - lunchbreak) / 60) OVER (
        PARTITION BY customername ORDER BY starttime
        ), 2) AS cumulative_hours
        FROM workhours
        WHERE CAST(starttime AS DATE) = %(date_ob)s
        ORDER BY customername, consultname;
        '''
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(
            query,
            {
                "date_ob": date_ob,
            },
        )
        rows = cursor.fetchall()
        cursor.close()
        con.close()
        return rows