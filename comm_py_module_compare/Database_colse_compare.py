# 关闭数据库连接
def Source_database_close(type, cursor, conn):
    if type == 'json':
        pass
    else:
        cursor.close()
        conn.close()


def Target_database_close(type, cursor, conn):
    if type == 'json':
        pass
    else:
        cursor.close()
        conn.close()