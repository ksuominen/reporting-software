from config import config
import psycopg2
from psycopg2 import sql


def connect():
    con = None
    try:
        con = psycopg2.connect(**config())
        return con
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Add daily workhours for a consult
def db_get_workhours(consultname=None, customername=None):
    query = sql.SQL(
        """
        SELECT consultname, customername, DATE(starttime) as work_date, 
            SUM((EXTRACT(EPOCH FROM (endtime - starttime))/60) - lunchbreak) / 60 as total_hours
        FROM workhours
        WHERE consultname = %s OR customername = %s
        GROUP BY consultname, customername, work_date
        ORDER BY work_date ASC;
        """
    )
    con = connect()
    if con is not None:
        cursor = con.cursor()
        cursor.execute(query, (consultname, customername))
        rows = cursor.fetchall()
        cursor.close()
        con.close()
        return rows
