import pymysql
import pandas as pd
from Data_Validate.common_py_module.Common_Function import *

# --##连接mysql数据库
@logger.catch
def Target_link_database(db_host, db_user, db_password, db_name, db_charset):
    global conn, cursor,sql01
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name, charset=db_charset)
    cursor = conn.cursor()
    sql01 = "SHOW TABLES"
    return conn, cursor,sql01
    # cursor = conn.cursor()


def Target_coltype_sql_get(cursor,db_name):

    cursor.execute("""
               select table_name, column_name, replace(REGEXP_REPLACE(COLUMN_TYPE, '[^a-zA-Z()]', ''),'()','') as column_type
                 from information_schema.columns
                where table_schema = %s
            """, (db_name))

    columns = {}
    for table, col, dtype in cursor:
        if table not in columns:
            columns[table] = {}
        columns[table][col] = dtype
    return columns