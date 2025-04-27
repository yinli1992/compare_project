from configparser import ConfigParser
import cx_Oracle
import pymysql
import pandas as pd
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from Type_Compare.db_oracle_module_compare.Source_Function_Compare import *
from Type_Compare.db_mysql_module_compare.Target_Function_Compare import *
from Type_Compare.comm_py_module_compare.compare_data_types import *
from Type_Compare.comm_py_module_compare.Database_colse_compare import *

cf = ConfigParser()
exe_path = sys.path[0]
cf.read(os.path.join(exe_path, 'config.ini'))

# 入参设定
schema_name_source = sys.argv[1]
schema_name_target = sys.argv[2]

# 规则表source数据库参数
db_type_source = cf.get('source', 'db_type')
db_name_source = cf.get('source', 'db_name')
db_user_source = cf.get('source', 'db_user')
db_pwd_source = cf.get('source', 'db_pwd')
db_host_source = cf.get('source', 'db_host')
db_port_source = cf.get('source', 'db_port')
db_schame_source = cf.get('source', 'db_schame')


# 规则表target数据库参数
db_type_target = cf.get('target', 'db_type')
db_name_target = cf.get('target', 'db_name')
db_user_target = cf.get('target', 'db_user')
db_pwd_target = cf.get('target', 'db_pwd')
db_host_target = cf.get('target', 'db_host')
db_port_target = cf.get('target', 'db_port')
db_schame_target = cf.get('target', 'db_schame')
db_charset_target = cf.get('target', 'db_charset')

#连接源端数据源
back_source = Source_link_database( db_host_source, db_user_source,db_pwd_source)
source_conn = back_source[0]
source_cursor = back_source[1]
#获取源端表字段类型
source_table_columns_type = Source_coltype_sql_get(source_cursor,db_name_source)

# 获取目标端连接信息
back_target = Target_link_database(db_host_target, db_user_target,db_pwd_target,
                                            db_name_target,db_charset_target)
target_conn = back_target[0]
target_cursor = back_target[1]
#获取目端表字段类型
target_table_columns_type = Target_coltype_sql_get(target_cursor,db_name_source)

#比较源端和目标端字段类型
compare_result = compare_data_types(source_table_columns_type,target_table_columns_type,db_type_source,db_type_target)

#写入目标数据库
Oracle_insert_compare(source_cursor,compare_result,source_conn)

# 关闭源端数据库连接
Source_database_close(db_type_source, source_cursor, source_conn)
#关闭目标端数据库连接
Target_database_close(db_type_target,target_cursor,target_conn)
