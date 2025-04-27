import cx_Oracle
import pandas as pd

def Source_link_database(db_host, db_user, db_password):
    global conn, cursor
    try:
        conn = cx_Oracle.connect(db_user, db_password, db_host)
    except  cx_Oracle.DatabaseError as msg:
        print(msg)
    cursor = conn.cursor()
    return conn, cursor


def Source_coltype_sql_get(cursor2,db_name):
    db_name = db_name.upper()
    sql = """
        select table_name,column_name,data_type
          from all_tab_columns
         where owner = :db_name
    """
    params = {'db_name': db_name}
    cursor2.execute(sql, params)
    columns = {}
    for table, col, dtype in cursor2:
        if table not in columns:
            columns[table] = {}
        columns[table][col] = dtype
    return columns


def Oracle_insert_compare(cursor,result,conn):
    # 3. 执行批量插入
    try:
        sql = """insert into  YZZT_DI.SCHEMA_DIFF_REPORT (table_name,field_name,diff_type,source_db,target_db,description)
        values (:1, :2, :3, :4, :5, :6) """
        cursor.executemany(sql, result)
        conn.commit()
        print("成功插入差异记录")
    except cx_Oracle.DatabaseError as e:
        print(f"数据库错误: {e}")